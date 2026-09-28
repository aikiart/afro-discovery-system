import sys
import os
import json

from agents.discovery_agent import DiscoveryAgent
from agents.database_agent import DatabaseAgent


def main():
    print("🚀 Starting Afro Discovery Pipeline...")

    # Initialize Agents
    discovery = DiscoveryAgent()
    db_agent = DatabaseAgent()

    # 1. Load Discovery Queries
    queries = discovery.load_queries()
    print(f"📋 Loaded {len(queries)} discovery queries.")

    # 2. Search for scraped datasets in data/
    possible_paths = [
        os.path.join("data", "export.json"),
        os.path.join("data", "categorized_results.json"),
        os.path.join("data", "raw_results.json"),
        os.path.join("data", "scraped_records.json"),
    ]

    records_to_save = []
    loaded_from_path = None

    for path in possible_paths:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        records_to_save = data
                        loaded_from_path = path
                        break
                    elif isinstance(data, dict):
                        for key in ["records", "data", "results", "platforms"]:
                            if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                                records_to_save = data[key]
                                loaded_from_path = path
                                break
                        if records_to_save:
                            break
            except json.JSONDecodeError:
                continue

    if loaded_from_path and records_to_save:
        print(f"📦 Loaded {len(records_to_save)} records from '{loaded_from_path}'.")

        # 3. Upsert records into Firestore collection 'afro_centric_apps'
        count = db_agent.save_records(records_to_save, collection_name="afro_centric_apps")
        print(f"🎉 Success! {count} total records updated in Firestore collection 'afro_centric_apps'.")
    else:
        print("⚠️ No valid JSON data found in 'data/'.")


if __name__ == "__main__":
    main()