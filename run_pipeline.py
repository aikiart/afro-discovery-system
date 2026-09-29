from agents.discovery_agent import DiscoveryAgent
from agents.scraper_agent import ScraperAgent
from agents.database_agent import DatabaseAgent
from agents.categorizer_agent import CategorizerAgent

discovery = DiscoveryAgent()
scraper = ScraperAgent()
database = DatabaseAgent()
categorizer = CategorizerAgent()

print("\nStarting Discovery Pipeline...\n")

results = discovery.discover()

for item in results:

    print(
        f"Processing: {item['query']}"
    )

    scraped = scraper.scrape(
        item["url"]
    )

    category_data = (
        categorizer.categorize(
            scraped
        )
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
        "emails": scraped.get(
            "emails",
            []
        ),
        "phones": scraped.get(
            "phones",
            []
        ),
        "social_links": scraped.get(
            "social_links",
            []
        ),
        "contact_pages": scraped.get(
            "contact_pages",
            []
        ),
        "category": category_data[
            "category"
        ],
        "tags": category_data[
            "tags"
        ],
        "query": item["query"]
    }

    database.save(
        resource
    )

print(
    "\nPipeline Complete.\n"
)