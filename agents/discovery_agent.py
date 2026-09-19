import json
from duckduckgo_search import DDGS


class DiscoveryAgent:

    def search(self, query):

        print(f"Searching: {query}")

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=10
            )

            for item in search_results:

                results.append(
                    {
                        "query": query,
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "description": item.get("body", "")
                    }
                )

        return results

    def save_results(self, data):

        with open(
            "data/raw_results.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print("Results saved.")