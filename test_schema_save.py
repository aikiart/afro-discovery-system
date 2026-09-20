from agents.scraper_agent import ScraperAgent
from services.firebase_service import FirebaseService

scraper = ScraperAgent()
firebase = FirebaseService()

result = scraper.scrape(
    "https://flutterwave.com"
)

resource = {
    "site_name": "SCHEMA TEST",
    "url": "https://schema-test-001.com",
    "description": result["description"],
    "emails": result["emails"],
    "phones": result["phones"],
    "social_links": result["social_links"],
    "contact_pages": result["contact_pages"],
    "category": "Test",
    "tags": ["test"]
}

doc_ref = firebase.db.collection(
    "resources"
).add(resource)

print("\nDOCUMENT REFERENCE:")
print(doc_ref)

print("\nDOCUMENT ID:")
print(doc_ref[1].id)

print("\nDONE")