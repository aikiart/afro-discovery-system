class CategorizerAgent:

    def categorize(self, scraped):

        text = (
            scraped.get(
                "title",
                ""
            )
            + " "
            + scraped.get(
                "description",
                ""
            )
        ).lower()

        if any(
            word in text
            for word in [
                "fintech",
                "finance",
                "bank",
                "payment"
            ]
        ):
            return {
                "category": "Fintech",
                "tags": [
                    "finance",
                    "africa"
                ]
            }

        if any(
            word in text
            for word in [
                "education",
                "learning",
                "school",
                "training"
            ]
        ):
            return {
                "category": "Education",
                "tags": [
                    "education",
                    "africa"
                ]
            }

        if any(
            word in text
            for word in [
                "health",
                "medical",
                "healthcare"
            ]
        ):
            return {
                "category": "Health",
                "tags": [
                    "health",
                    "africa"
                ]
            }

        if any(
            word in text
            for word in [
                "community",
                "nonprofit",
                "organization"
            ]
        ):
            return {
                "category": "Community",
                "tags": [
                    "community",
                    "africa"
                ]
            }

        return {
            "category": "Business",
            "tags": [
                "business",
                "africa"
            ]
        }