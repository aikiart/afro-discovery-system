import json


class DiscoveryAgent:

    def load_queries(self):

        with open(
            "data/discovery_queries.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def discover(self):

        queries = self.load_queries()

        discovered_urls = []

        for query in queries:

            print(
                f"Processing query: {query}"
            )

            # Placeholder until we plug in
            # a search provider

            discovered_urls.append(
                {
                    "query": query,
                    "url": "https://african.business"
                }
            )

        return discovered_urls