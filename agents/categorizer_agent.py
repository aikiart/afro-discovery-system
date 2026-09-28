from datetime import datetime, timezone
import json
import os
import time
from typing import Any, Dict, List
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types
from google.genai.errors import APIError


def seconds_until_midnight_pacific() -> int:
    """Calculates the exact time in seconds until Midnight Pacific Time (00:00 US/Pacific)."""
    pacific_tz = ZoneInfo("America/Los_Angeles")
    now_pacific = datetime.now(pacific_tz)

    # Next midnight in Pacific Time
    tomorrow_pacific = datetime(
        year=now_pacific.year,
        month=now_pacific.month,
        day=now_pacific.day + 1,
        hour=0,
        minute=0,
        second=5,  # 5-second buffer to guarantee reset
        tzinfo=pacific_tz,
    )

    seconds_to_wait = int((tomorrow_pacific - now_pacific).total_seconds())
    return max(seconds_to_wait, 60)


def categorize(scraped_data: dict) -> dict:
    """Assigns category and tags using Gemini AI with automatic rate-limit wait handling."""
    url = scraped_data.get("url", "").lower()
    title = scraped_data.get("title", "")
    description = scraped_data.get("description", "")
    highlights = scraped_data.get("highlights", [])

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        while True:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                Analyze the following website/platform metadata and categorize it for an Afro-Centric platforms directory:
                URL: {url}
                Title: {title}
                Description: {description}
                Highlights: {' '.join(highlights)}

                Return ONLY a valid JSON object with the following schema:
                {{
                    "category": "<Single Main Category e.g. Literature & Publishing, Mobile & Web Apps, Culture & Heritage, Education & EdTech, Community & Social, Fintech & E-Commerce>",
                    "tags": ["tag1", "tag2", "tag3"]
                }}
                """

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                )

                result = json.loads(response.text)
                return {
                    "category": result.get(
                        "category", "General Afro-Centric Resource"
                    ),
                    "tags": result.get("tags", ["africa", "platform"]),
                }

            except APIError as e:
                # Catch 429 Resource Exhausted / Quota Errors
                if getattr(e, "code", None) == 429 or "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = seconds_until_midnight_pacific()
                    hours = round(wait_time / 3600, 2)
                    print(
                        f"\n🛑 Daily Gemini Quota Exhausted (429). Sleeping for {hours} hours (until Midnight Pacific)..."
                    )
                    time.sleep(wait_time)
                    print(
                        "🌅 Quota reset period reached! Resuming AI categorization loop..."
                    )
                    continue  # Retry categorization for current item
                else:
                    print(
                        f"⚠️ AI Categorization failed with APIError ({e}). Falling back to rule-based logic."
                    )
                    break
            except Exception as e:
                print(
                    f"⚠️ Unexpected error ({e}). Falling back to rule-based logic."
                )
                break

    # Rule-Based Categorization Fallback
    text_content = f"{url} {title} {description} {' '.join(highlights)}".lower()

    if any(
        k in text_content
        for k in ["book", "author", "literature", "reading", "novel", "writer"]
    ):
        category = "Literature & Publishing"
        tags = ["literature", "authors", "books", "reading"]
    elif any(
        k in text_content
        for k in ["app", "ios", "android", "software", "platform"]
    ):
        category = "Mobile & Web Apps"
        tags = ["technology", "mobile-app", "digital-platform"]
    elif any(
        k in text_content
        for k in ["history", "archive", "culture", "heritage", "museum"]
    ):
        category = "Culture & Heritage"
        tags = ["culture", "history", "preservation", "heritage"]
    elif any(
        k in text_content for k in ["fintech", "payment", "finance", "bank"]
    ):
        category = "Fintech & E-Commerce"
        tags = ["fintech", "payments", "financial-services"]
    elif any(
        k in text_content
        for k in ["school", "university", "learn", "education", "course"]
    ):
        category = "Education & EdTech"
        tags = ["education", "learning", "students"]
    else:
        category = "Community & Social"
        tags = ["community", "organization", "network"]

    return {"category": category, "tags": tags}


class CategorizerAgent:

    def categorize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        result = categorize(record)
        updated_record = dict(record)
        updated_record["category"] = result["category"]
        updated_record["tags"] = result["tags"]
        updated_record["categorized"] = True
        return updated_record

    def process_batch(
        self, records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        if not records:
            return []
        print(f"🏷️ Categorizing {len(records)} new discovered records...")
        categorized_records = []
        for index, record in enumerate(records, start=1):
            categorized_records.append(self.categorize_record(record))
            if os.getenv("GEMINI_API_KEY") and index < len(records):
                time.sleep(13)
        print("✅ Categorization complete.")
        return categorized_records