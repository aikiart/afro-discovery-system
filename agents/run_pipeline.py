from agents.scraper_agent import scrape_site
from agents.categorizer_agent import categorize
from agents.database_agent import save_organization

def run_pipeline(url: str, query: str):
    # Step 1: Scrape site data
    scraped_data = scrape_site(url)

    # Step 2: Categorize the scraped data (one argument only)
    result = categorize(scraped_data)
    category = result["category"]
    tags = result["tags"]

    # Step 3: Build organization record
    org_record = {
        "url": url,
        "query": query,
        "site_name": scraped_data.get("site_name", ""),
        "description": scraped_data.get("description", ""),
        "emails": scraped_data.get("emails", []),
        "phones": scraped_data.get("phones", []),
        "social_links": scraped_data.get("social_links", []),
        "contact_pages": scraped_data.get("contact_pages", []),
        "category": category,
        "tags": tags
    }

    # Step 4: Save to Firestore
    status = save_organization(org_record)
    return status

if __name__ == "__main__":
    result = run_pipeline("https://flutterwave.com", "African fintech companies")
    print("Pipeline result:", result)
