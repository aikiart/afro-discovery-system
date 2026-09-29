# Afro Discovery System - Project Status

## Environment & Architecture
- Root Directory: `I:\afro-discovery-system\`
- Python Agents: Located in `agents/` (`discovery_agent.py`, `database_agent.py`, `scraper_agent.py`, `categorizer_agent.py`, `update_agent.py`)
- Frontend: React application in `src/App.jsx` deployed via Firebase Hosting (`afro-discovery-system.web.app`)
- Firestore Collection: `afro_centric_apps`
- Service Account Key: `config/serviceAccountKey.json`

## Active Pipeline Configuration
- Data Ingestion: `main.py` loads records from `data/export.json` and upserts records to Firestore via `DatabaseAgent.save_records()`.
- Data Handling: UTF-8 encoding is enforced across file reads/writes, and URL sanitization (`sanitize_doc_id`) prevents key formatting issues in Firestore.
- Frontend Design: Forest green header (`#0d5c46`), light gray background (`#f8f9fa`), white card surfaces, exact sub-header text, and live counter logic (`Showing X platforms`).

---

## Command Reference & Scripts

### 1. Run Data Scraper & Sync to Firestore (with Limit Flag)
To execute the discovery pipeline, scrape target sources with the 25-record limit flag, and push updated records directly to your Firestore database:

```powershell
python main.py 25

I am resuming work on the `afro-discovery-system` project. Here is my project documentation and file mapping:

---

### PROJECT DOCUMENTATION (`project_status.md`)
[PASTE THE CONTENTS OF YOUR project_status.md FILE HERE]

---

### CURRENT FILE DIRECTORY & ACTIVE CODE LOCATIONS

1. **Root Directory:** `I:\afro-discovery-system\`
2. **Primary Python Pipeline File:** `main.py` (Ingestion, scraping, and Firestore sync caller)
3. **Python Agents (`agents/` directory):**
   - `agents/discovery_agent.py` — Web discovery and URL processing logic
   - `agents/database_agent.py` — Firestore connection, document ID sanitization, and upsert logic
   - `agents/scraper_agent.py` — Content scraping and web parsing
   - `agents/categorizer_agent.py` — Data categorization and tagging
   - `agents/update_agent.py` — Database update utilities
4. **Frontend Files (`src/` directory):**
   - `src/App.jsx` — Primary React UI component (Forest green `#0d5c46` header, platform cards grid, live counter)
   - `src/index.js` or `src/main.jsx` — Entry point
5. **Data Files (`data/` directory):**
   - `data/export.json` / `data/categorized_results.json` — Target JSON data datasets for ingestion
6. **Config & Environment:**
   - `.gitignore` — Protecting `config/serviceAccountKey.json` and `serviceAccount*.json`
   - `firebase.json` — Firebase Hosting deployment configuration
7. **Active Git Branch:** `clean-backup` (Bypasses GitHub secret scanning and branch protection rules)

---

### PROMPT INSTRUCTION
Please review this state and confirm you understand the architecture, scripts, and active branch configuration before we proceed with the next task.
Locally update: python main.py 25 "run those 2 commands"
npm run dev

## Live Web Discovery, Scraping & Firebase Deployment Workflow

To perform a fresh live web search across Afro-centric queries, enrich platform metadata, update Firestore, and deploy the updated application:

### Step 1: Run Live Web Scraper & Save Results
Executes Exa search queries, deep-scrapes new sites, filters broken links, and saves enriched records directly to `data/export.json`:

```powershell
python -c "import json; from agents.discovery_agent import DiscoveryAgent; from agents.scraper_agent import ScraperAgent; da = DiscoveryAgent(); sa = ScraperAgent(); queries = da.load_queries(); results = sa.search_and_enrich(queries, set()); json.dump(results, open('data/export.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False); print(f'Successfully saved {len(results)} records to data/export.json')"