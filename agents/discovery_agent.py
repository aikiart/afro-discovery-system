import json
import os
from typing import List, Dict, Any


class DiscoveryAgent:
    """Agent responsible for managing discovery queries and handling raw platform data."""

    def __init__(self, queries_file: str = None):
        if queries_file is None:
            queries_file = os.path.join("config", "queries.json")
        self.queries_file = queries_file

    def load_queries(self) -> List[str]:
        """Loads search queries from the config JSON file or provides default search terms."""
        if os.path.exists(self.queries_file):
            try:
                with open(self.queries_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and "queries" in data:
                        return data["queries"]
            except Exception as e:
                print(f"⚠️ Error reading '{self.queries_file}': {e}. Using fallback queries.")

        # Default Afro-Centric Discovery Queries
        return [
            "Afro-centric tech platforms and applications",
            "African literature and publishing digital platforms",
            "Black-owned technology networks and directory apps",
            "Afro-descendant cultural archives and web projects"
        ]