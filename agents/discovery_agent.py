import json

class DiscoveryAgent:

    def search(self, query):

        print(f"Searching for: {query}")

        return {
            "query": query,
            "results": [
                {
                    "name": "African Leadership Academy",
                    "url": "https://www.africanleadershipacademy.org"
                },
                {
                    "name": "Black Founders",
                    "url": "https://blackfounders.com"
                }
            ]
        }

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