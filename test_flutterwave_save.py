from agents.scraper_agent import ScraperAgent
from agents.database_agent import DatabaseAgent

scraper = ScraperAgent()
database = DatabaseAgent()

result = scraper.scrape(
    "https://flutterwave.com"
)

resource = {
    "site_name": result["title"],
    "url": result["url"] + "?test=v2",
    "description": result["description"],
    "emails": result["emails"],
    "phones": result["phones"],
    "social_links": result["social_links"],
    "contact_pages": result["contact_pages"],
    "category": "Fintech",
    "tags": ["africa", "fintech"]
}

database.save(resource)

print("Test record saved.")