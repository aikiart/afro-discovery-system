# agents/database_agent.py

import json

class DatabaseAgent:

    def save(self, data):

        with open(
            "data/categorized_results.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print("Results saved.")