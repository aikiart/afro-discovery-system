from agents.discovery_agent import DiscoveryAgent
from agents.scraper_agent import ScraperAgent
from agents.database_agent import DatabaseAgent

discovery = DiscoveryAgent()
scraper = ScraperAgent()
database = DatabaseAgent()

print("\nStarting Discovery Pipeline...\n")

results = discovery.discover()

for item in results:

    print(
        f"Processing: {item['query']}"
    )

    scraped = scraper.scrape(
        item["url"]
    )

    resource = {
        "site_name": scraped.get(
            "title",
            ""
        ),
        "url": scraped.get(
            "url",
            ""
        ),
        "description": scraped.get(
            "description",
            ""
        ),
        "contact_email": (
            scraped["emails"][0]
            if scraped.get("emails")
            else ""
        ),
        "phone": "",
        "social_links": scraped.get(
            "social_links",
            []
        ),
        "category": "Uncategorized",
        "tags": [],
        "query": item["query"]
    }

    database.save(resource)

print("\nPipeline Complete.\n")