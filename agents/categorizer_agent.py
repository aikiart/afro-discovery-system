# agents/categorizer_agent.py

class CategorizerAgent:

    def categorize(self, data):

        text = (
            data.get("title", "") +
            " " +
            data.get("description", "")
        ).lower()

        if "education" in text:
            return "Education"

        if "health" in text:
            return "Health"

        if "finance" in text:
            return "Fintech"

        if "community" in text:
            return "Community"

        if "technology" in text:
            return "Technology"

        return "Other"