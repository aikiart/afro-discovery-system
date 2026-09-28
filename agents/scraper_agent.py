import os
import re
from typing import Any, Dict, List, Set
from dotenv import load_dotenv
from exa_py import Exa
import requests
from bs4 import BeautifulSoup

load_dotenv()


def scrape_site(url: str) -> dict:
    """Scrape basic metadata from a site with strict error handling for broken links."""
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Unreachable site ({url}): {e}")
        return {
            "url": url,
            "title": "",
            "description": "",
            "emails": [],
            "phones": [],
            "social_links": [],
            "contact_pages": [],
            "error": str(e)
        }

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and "content" in meta_desc.attrs:
        description = meta_desc["content"].strip()

    emails = list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text)))
    social_domains = ["twitter.com", "x.com", "facebook.com", "instagram.com", "linkedin.com", "youtube.com"]
    social_links = []
    contact_pages = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if any(domain in href.lower() for domain in social_domains):
            social_links.append(href)
        if "contact" in href.lower() or "about" in href.lower():
            contact_pages.append(href)

    return {
        "url": url,
        "title": title,
        "description": description,
        "emails": emails,
        "phones": [],
        "social_links": list(set(social_links)),
        "contact_pages": list(set(contact_pages)),
        "error": None
    }


class ScraperAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY is missing from .env file.")
        self.exa = Exa(api_key=self.api_key)

    def search_and_enrich(
        self,
        queries: List[str],
        existing_urls: Set[str],
        db_agent=None,
        num_results_per_query: int = 10
    ) -> List[Dict[str, Any]]:
        """Searches via Exa, skips existing URLs, and removes broken links from DB."""
        new_results = []

        for query in queries:
            print(f"🔍 Searching Exa for: '{query}'...")
            try:
                response = self.exa.search(
                    query=query,
                    type="neural",
                    num_results=num_results_per_query,
                    contents={"highlights": True},
                )

                for item in response.results:
                    clean_url = item.url.rstrip("/")

                    # SKIP: URL already exists in Firebase Database
                    if clean_url in existing_urls:
                        print(f"⏩ Skipping existing database entry: {item.url}")
                        continue

                    print(f"🌐 Deep scraping new site: {item.url}")
                    deep_scraped = scrape_site(item.url)

                    # REMOVE: If link is invalid or returned HTTP error, purge from DB if present
                    if deep_scraped.get("error"):
                        if db_agent:
                            db_agent.delete_record_by_url(item.url)
                        continue

                    merged_record = {
                        "title": deep_scraped["title"] or getattr(item, "title", "Untitled"),
                        "url": item.url,
                        "description": deep_scraped["description"],
                        "published_date": getattr(item, "published_date", None),
                        "highlights": getattr(item, "highlights", []),
                        "emails": deep_scraped["emails"],
                        "social_links": deep_scraped["social_links"],
                        "contact_pages": deep_scraped["contact_pages"],
                        "search_query": query,
                        "categorized": False,
                    }
                    new_results.append(merged_record)
                    existing_urls.add(clean_url)  # Prevent duplicates within current execution batch

            except Exception as e:
                print(f"⚠️ Error executing search for query '{query}': {e}")

        return new_results