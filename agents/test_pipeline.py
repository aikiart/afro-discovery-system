from database_agent import save_organization

def main():
    # Simulated scraped + categorized data
    org_record = {
        "site_name": "Flutterwave",
        "url": "https://flutterwave.com",
        "description": "Payments technology company connecting Africa to the global economy.",
        "emails": ["hi@flutterwavego.com", "serviceclient@flutterwavego.com"],
        "phones": ["+234-1-888-1234"],
        "social_links": [
            "https://twitter.com/flutterwave",
            "https://linkedin.com/company/flutterwave"
        ],
        "contact_pages": ["/contact", "/about"],
        "category": "Fintech",
        "tags": ["payments", "africa", "financial-services"],
        "query": "African fintech companies"
    }

    save_organization(org_record)

if __name__ == "__main__":
    main()
