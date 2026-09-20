import json


class DiscoveryAgent:

    def discover(self):

        with open(
            "data/discovery_sources.json",
            "r",
            encoding="utf-8"
        ) as file:

            sources = json.load(file)

        results = []

        for query, urls in sources.items():

            print(
                f"Processing query: {query}"
            )

            for url in urls:

                results.append(
                    {
                        "query": query,
                        "url": url
                    }
                )

        return results