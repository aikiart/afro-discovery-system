# agents/scraper_agent.py

import requests
from bs4 import BeautifulSoup

class ScraperAgent:

    def scrape(self, url):

        try:

            response = requests.get(
                url,
                timeout=10
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = ""
            description = ""

            if soup.title:
                title = soup.title.text.strip()

            meta = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            if meta:
                description = meta.get(
                    "content",
                    ""
                )

            return {
                "url": url,
                "title": title,
                "description": description
            }

        except Exception as error:

            return {
                "url": url,
                "error": str(error)
            }