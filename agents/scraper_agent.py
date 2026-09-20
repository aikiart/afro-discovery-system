import requests
import re

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

            if soup.title:
                title = soup.title.text.strip()

            description = ""

            meta = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            if meta:
                description = meta.get(
                    "content",
                    ""
                )

            emails = list(
                set(
                    re.findall(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                        response.text
                    )
                )
            )

            # Temporarily disabled because the regex
            # was collecting dates and image sizes
            phones = []

            social_links = []

            social_domains = [
                "linkedin.com",
                "facebook.com",
                "instagram.com",
                "twitter.com",
                "x.com",
                "youtube.com"
            ]

            for link in soup.find_all("a", href=True):

                href = link["href"]

                if any(
                    domain in href
                    for domain in social_domains
                ):
                    social_links.append(href)

            social_links = list(
                set(social_links)
            )

            return {
                "url": url,
                "title": title,
                "description": description,
                "emails": emails,
                "phones": phones,
                "social_links": social_links
            }

        except Exception as error:

            return {
                "url": url,
                "error": str(error)
            }