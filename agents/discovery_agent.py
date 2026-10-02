import os
import json
from exa_py import Exa


class DiscoveryAgent:

    def __init__(self):
        api_key = os.getenv("EXA_API_KEY")
        if not api_key:
            raise ValueError("EXA_API_KEY is missing from environment variables.")
        self.exa = Exa(api_key=api_key)

    def load_queries(self, sources_file="data/discovery_sources.json"):
        with open(sources_file, "r", encoding="utf-8") as file:
            sources = json.load(file)
        return list(sources.keys())

    def discover_urls(self, num_results_per_query=3):
        queries = self.load_queries()
        discovered_records = []

        for query_text in queries:
            print(f"🔍 [DiscoveryAgent] Exa Searching: '{query_text}'")
            try:
                # Removed the invalid 'use_autoprompt' parameter
                response = self.exa.search(
                    query=query_text,
                    num_results=num_results_per_query
                )
                for result in response.results:
                    discovered_records.append({
                        "query": query_text,
                        "url": result.url,
                        "title": getattr(result, "title", "")
                    })
            except Exception as e:
                print(f"❌ Exa search error for '{query_text}': {e}")

        return discovered_records