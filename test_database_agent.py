from agents.database_agent import DatabaseAgent

database = DatabaseAgent()

resource = {
    "site_name": "African Fintech Example",
    "url": "https://example.com",
    "description": "Example African fintech company",
    "contact_email": "",
    "phone": "",
    "social_links": [],
    "category": "Fintech",
    "tags": [
        "africa",
        "fintech"
    ],
    "date_discovered": "2026-09-19"
}

database.save(resource)