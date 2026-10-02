import re
import requests
from bs4 import BeautifulSoup


class ScraperAgent:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
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
            # timeout=(connect_timeout, read_timeout) to prevent SSL/TCP connection hangs
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=(3.0, 5.0), 
                stream=True
            )
            
            if response.status_code != 200:
                print(f"  ⚠️ Non-200 status ({response.status_code}) for {url}")
                return {"url": url, "title": "", "description": "", "emails": [], "contactEmail": None}

            # Limit download content size to avoid hanging on large media files
            content = response.raw.read(500000).decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, "html.parser")

            # Extract Title
            og_title = soup.find("meta", property="og:title")
            title = ""
            if og_title and og_title.get("content"):
                title = og_title["content"].strip()
            elif soup.title and soup.title.text:
                title = soup.title.text.strip()

            # Extract Description
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

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            print(f"  ⏱️ Connection timed out / unreachable: {url}")
            return {"url": url, "title": "", "description": "", "emails": [], "contactEmail": None}
        except Exception as error:
            print(f"  ❌ Error scraping {url}: {error}")
            return {"url": url, "title": "", "description": "", "emails": [], "contactEmail": None}