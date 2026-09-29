# Architectural Decisions Log

## 1. Local Command Trigger vs. Python Entry Points
- **Decision:** Execute discovery/scraping via explicitly constructed inline Python scripts in terminal commands rather than relying on class entry points like `UpdateAgent.run()`.
- **Reason:** Bypasses silent execution failures and thread/async logging suppression, providing a live real-time console stream of scraped sites.

## 2. In-Memory Search & Explicit JSON Export
- **Decision:** Always dump scraped results explicitly to `data/export.json` using `json.dump()` before executing `main.py`.
- **Reason:** `main.py` reads exclusively from `data/export.json`. In-memory scraping without a JSON save step resulted in stale data being written to Firestore.

## 3. Dynamic Location Inference
- **Decision:** Infer country/location during deep scraping using TLD mappings (e.g., `.ng`, `.ke`, `.br`) and keyword matching in raw HTML text.
- **Reason:** Provides geographic provenance on platform cards without requiring rigid predefined database schemas.
