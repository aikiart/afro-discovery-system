from agents.scraper_agent import ScraperAgent
from agents.database_agent import DatabaseAgent

scraper = ScraperAgent()
database = DatabaseAgent()

result = scraper.scrape(
    "https://african.business"
)

resource = {
    "site_name": result["title"],
    "url": result["url"],
    "description": result["description"],
    "contact_email": (
        result["emails"][0]
        if result["emails"]
        else ""
    ),
    "phone": "",
    "social_links": result["social_links"],
    "category": "Business",
    "tags": [
        "africa",
        "business"
    ],
    "date_discovered": "2026-09-19"
}

database.save(resource)

print("Pipeline completed.")