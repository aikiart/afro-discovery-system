from agents.discovery_agent import DiscoveryAgent
from agents.run_pipeline import run_pipeline

def bulk_run():
    agent = DiscoveryAgent()

    # Define the queries you want to discover dynamically
    queries = [
        "African fintech companies",
        "Black owned software companies",
        "African educational platforms",
        "African health technology startups",
        "Afrocentric community organizations",
        "African ecommerce platforms",
        "Black owned mobile apps",
        "African media companies",
        "African cultural organizations",
        "African nonprofit organizations"
    ]

    sources = agent.discover(queries)  # pass queries here

    saved_count = 0
    duplicate_count = 0

    for entry in sources:
        url = entry["url"]
        query = entry["query"]

        status = run_pipeline(url, query)
        if status == "saved":
            saved_count += 1
        elif status == "duplicate":
            duplicate_count += 1

    print("=== Summary ===")
    print("New records saved:", saved_count)
    print("Duplicates skipped:", duplicate_count)

if __name__ == "__main__":
    bulk_run()
