import json


class DiscoveryAgent:

    def load_queries(self):

        with open(
            "data/discovery_queries.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)