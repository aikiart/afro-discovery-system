import json
import os
import sys
import warnings
from dotenv import load_dotenv
from agents.scraper_agent import ScraperAgent
from agents.categorizer_agent import CategorizerAgent
from agents.database_agent import DatabaseAgent

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()


def load_queries(config_path: str = "data/discovery_queries.json") -> list:
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"⚠️ Query file '{config_path}' not found. Falling back to default queries.")
    return [
        "Afrocentric mobile applications and digital platforms",
        "Black literature author discovery and web apps",
        "African cultural preservation digital projects archives"
    ]


def main(results_per_query: int = 10):
    print("🚀 Starting automated Afro-Centric discovery & ingestion pipeline...")

    # Initialize Agents
    scraper = ScraperAgent()
    categorizer = CategorizerAgent()
    db_agent = DatabaseAgent()

    # Step 1: Query Firebase to get list of existing URLs
    print("📦 Fetching existing records from Firestore to prevent duplicate processing...")
    existing_urls = db_agent.get_existing_urls(collection_name="afro_centric_apps")
    print(f"🔑 Found {len(existing_urls)} existing URLs in Firebase.")

    # Step 2: Search via Exa, Skip Existing URLs, & Delete Broken Links
    queries = load_queries()
    print(f"🔎 Running discovery search across {len(queries)} topics...")
    new_sites = scraper.search_and_enrich(
        queries=queries,
        existing_urls=existing_urls,
        db_agent=db_agent,
        num_results_per_query=results_per_query
    )

    print(f"📊 Discovered {len(new_sites)} net-new candidate platforms.")

    if not new_sites:
        print("🎉 No new platforms to process. Firebase database is up-to-date!")
        return

    # Step 3: Categorize only net-new entries
    processed_sites = categorizer.process_batch(new_sites)

    # Step 4: Write only new records to Firestore
    db_agent.save_records(
        records=processed_sites,
        collection_name="afro_centric_apps"
    )

    print("🎉 Pipeline execution completed successfully!")


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    main(results_per_query=limit)