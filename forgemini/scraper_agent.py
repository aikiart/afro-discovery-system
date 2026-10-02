import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class ScraperAgent:

    def extract_emails(self, text):

        return list(
            set(
                re.findall(
                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                    text
                )
            )
        )

    def find_contact_pages(self, soup, base_url):

        contact_pages = []

        keywords = [
            "contact",
            "contact-us",
            "about",
            "about-us"
        ]

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link["href"].lower()

            if any(
                keyword in href
                for keyword in keywords
            ):

                full_url = urljoin(
                    base_url,
                    link["href"]
                )

                contact_pages.append(
                    full_url
                )

        return list(
            set(contact_pages)
        )

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

            emails = self.extract_emails(
                response.text
            )

            social_domains = [
                "linkedin.com",
                "facebook.com",
                "instagram.com",
                "twitter.com",
                "x.com",
                "youtube.com"
            ]

            social_links = []

            for link in soup.find_all(
                "a",
                href=True
            ):

                href = link["href"]

                if any(
                    domain in href
                    for domain in social_domains
                ):

                    social_links.append(
                        href
                    )

            contact_pages = self.find_contact_pages(
                soup,
                url
            )

            for page in contact_pages:

                try:

                    contact_response = requests.get(
                        page,
                        timeout=10
                    )

                    contact_emails = (
                        self.extract_emails(
                            contact_response.text
                        )
                    )

                    emails.extend(
                        contact_emails
                    )

                except Exception:
                    pass

            emails = list(
                set(emails)
            )

            social_links = list(
                set(social_links)
            )

            return {
                "url": url,
                "title": title,
                "description": description,
                "emails": emails,
                "phones": [],
                "social_links": social_links,
                "contact_pages": contact_pages
            }

        except Exception as error:

            return {
                "url": url,
                "error": str(error)
            }