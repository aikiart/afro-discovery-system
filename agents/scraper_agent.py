import os
import re
import requests
import json
import warnings
import urllib.parse
from bs4 import BeautifulSoup
from exa_py import Exa
from google.oauth2 import service_account
import google.auth.transport.requests

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

project_root = r"I:\afro-discovery-system"

possible_paths = [
    os.path.join(project_root, "serviceAccountKey.json"),
    os.path.join(project_root, "serviceAccount.json"),
    os.path.join(project_root, "agents", "serviceAccountKey.json"),
    os.path.join(project_root, "agents", "serviceAccount.json"),
]

KEY_PATH = None
for p in possible_paths:
    if os.path.exists(p):
        KEY_PATH = p
        break

if KEY_PATH:
    print(f"🔑 Loaded Credentials from: {KEY_PATH}")
    with open(KEY_PATH) as f:
        key_data = json.load(f)
    PROJECT_ID = key_data.get("project_id", "afro-discovery-system")
    CREDS = service_account.Credentials.from_service_account_file(
        KEY_PATH, 
        scopes=["https://www.googleapis.com/auth/datastore"]
    )
else:
    print("⚠️ Warning: Service Account key file not found in root or agents directory.")
    PROJECT_ID = "afro-discovery-system"
    CREDS = None

TARGET_COLLECTION = "afro_centric_apps"


class ScraperAgent:

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def extract_emails(self, text):
        raw_emails = set(
            re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                text
            )
        )
        valid_emails = [
            e for e in raw_emails
            if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg', '.js', '.css'))
        ]
        return valid_emails

    def scrape(self, url):
        print(f"  🌐 [ScraperAgent] Fetching {url}...")
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=(4.0, 5.0), 
                verify=False
            )
            
            if response.status_code != 200:
                print(f"  ⚠️ Non-200 status ({response.status_code}) for {url}")
                return {"url": url, "title": "", "description": "", "emails": [], "contactEmail": None}

            content = response.text[:500000]
            soup = BeautifulSoup(content, "html.parser")

            og_title = soup.find("meta", property="og:title")
            title = ""
            if og_title and og_title.get("content"):
                title = og_title["content"].strip()
            elif soup.title and soup.title.text:
                title = soup.title.text.strip()

            og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
            description = ""
            if og_desc and og_desc.get("content"):
                description = og_desc["content"].strip()

            emails = self.extract_emails(content)
            primary_contact_email = emails[0] if emails else None

            return {
                "url": url,
                "title": title,
                "description": description,
                "emails": emails,
                "contactEmail": primary_contact_email
            }

        except Exception as error:
            print(f"  ⏱️ Fetching timed out / skipped: {url}")
            return {"url": url, "title": "", "description": "", "emails": [], "contactEmail": None}


def make_doc_id(url):
    clean_url = url.strip().rstrip('/').lower()
    return urllib.parse.quote_plus(clean_url).replace('%', '_')[:100]


def push_to_firestore_rest(record, category="Literature and Publishing"):
    if not CREDS:
        print("  ⚠️ Skipped Firestore write: No credentials loaded.")
        return

    try:
        # Obtain Google OAuth2 access token for standard REST request
        auth_req = google.auth.transport.requests.Request()
        CREDS.refresh(auth_req)
        access_token = CREDS.token

        doc_id = make_doc_id(record["url"])
        endpoint = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{TARGET_COLLECTION}/{doc_id}"

        # Construct Firestore REST Payload
        payload = {
            "fields": {
                "url": {"stringValue": record["url"]},
                "title": {"stringValue": record["title"] if record["title"] else "Untitled Platform"},
                "summary": {"stringValue": record["description"] if record["description"] else "No description provided."},
                "contactEmail": {"stringValue": record["contactEmail"] if record["contactEmail"] else ""},
                "category": {"stringValue": category},
                "country": {"stringValue": "International"},
                "tags": {
                    "arrayValue": {
                        "values": [
                            {"stringValue": "#technology"},
                            {"stringValue": "#digital-platform"},
                            {"stringValue": "#afro-centric"}
                        ]
                    }
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        res = requests.patch(endpoint, headers=headers, json=payload, timeout=5.0)
        
        if res.status_code in (200, 201):
            print(f"  ✅ Saved to Firestore via REST: {record['url']}")
        else:
            print(f"  ⚠️ Firestore REST Write Error ({res.status_code}): {res.text}")

    except Exception as e:
        print(f"  ⚠️ Firestore write error: {e}")


def run_exa_discovery(query_prompt, num_results=5, category="Literature and Publishing"):
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        print("❌ Error: EXA_API_KEY environment variable is not set.")
        return

    print(f"\n🔍 Querying Exa AI for: '{query_prompt}'...")
    exa = Exa(api_key=api_key)
    
    try:
        results = exa.search(
            query_prompt,
            num_results=num_results,
            type="neural"
        )
        
        discovered_urls = [item.url for item in results.results]
        print(f"✨ Exa discovered {len(discovered_urls)} candidate URLs.")

        agent = ScraperAgent()
        for url in discovered_urls:
            scraped_data = agent.scrape(url)
            print(f"   Fetched: {scraped_data['title']} | Contact Email: {scraped_data['contactEmail']}")
            push_to_firestore_rest(scraped_data, category=category)
            print("-" * 55)

    except Exception as e:
        print(f"❌ Exa API search failed: {e}")


if __name__ == "__main__":
    print("\n🚀 Initializing Autonomous Exa-Powered Discovery Engine...\n")
    
    discovery_jobs = [
        {
            "query": "Afrocentric digital archives literature publishing platforms", 
            "category": "Literature and Publishing"
        },
        {
            "query": "Black tech organizations, directories, and innovation platforms", 
            "category": "Technology and Innovation"
        }
    ]
    
    for job in discovery_jobs:
        run_exa_discovery(job["query"], num_results=3, category=job["category"])
        
    print("\n✨ Autonomous discovery process finished.")
