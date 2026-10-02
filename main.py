import os
import time
from dotenv import load_dotenv
from agents.discovery_agent import DiscoveryAgent
from agents.scraper_agent import ScraperAgent
from agents.categorizer_agent import CategorizerAgent
from agents.database_agent import DatabaseAgent

load_dotenv()


def run_pipeline():
    print("🚀 Initializing Afro-Discovery Scraping Pipeline...\n")

    discovery = DiscoveryAgent()
    scraper = ScraperAgent()
    categorizer = CategorizerAgent()
    db_agent = DatabaseAgent()

    # Step 1: Discover
    discovered_items = discovery.discover_urls(num_results_per_query=2)
    print(f"\n📍 Total candidate URLs discovered from Exa: {len(discovered_items)}\n")

    # Step 2: Iterate
    for idx, item in enumerate(discovered_items, 1):
        url = item["url"]
        print(f"[{idx}/{len(discovered_items)}] Processing: {url}")

        # Check DB
        print("  🔎 Checking Firestore for duplicate...")
        if db_agent.exists(url):
            print(f"  ⏩ Skipping existing URL: {url}\n")
            continue

        # Scrape
        scraped_data = scraper.scrape(url)
        if not scraped_data.get("url"):
            print("  ⚠️ Skipping invalid page data.\n")
            continue

        # Title Fallback
        if not scraped_data.get("title"):
            scraped_data["title"] = item.get("title", "")

        # Categorize
        category_data = categorizer.categorize(scraped_data)
        scraped_data["category"] = category_data.get("category", "Business")
        scraped_data["tags"] = [f"#{t.replace('#', '')}" for t in category_data.get("tags", ["africa"])]

        # Save
        db_agent.save(scraped_data)
        print()

    print("✨ Pipeline execution finished!")


if __name__ == "__main__":
    run_pipeline()