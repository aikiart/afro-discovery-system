Set-Content -Path "I:\afro-discovery-system\PROJECT_CONTEXT.md" -Value @"
# Project Context: Afro-Discovery System

## 1. Project Overview & Architecture
- **Web App Domain:** \`https://afro-discovery-system.web.app\`
- **Repository:** \`https://github.com/aikiart/afro-discovery-system\`
- **Purpose:** Discovery platform indexing Afrocentric digital archives, literature, tech initiatives, and platforms.
- **Frontend Stack:** React, Vite, Tailwind CSS, Firebase Client SDK (\`onSnapshot\` for live Firestore streaming).
- **Backend/Scraper:** Autonomous Python pipeline using Exa AI (\`exa-py\`), BeautifulSoup4, and Google Auth REST APIs.
- **Database:** Google Firebase Cloud Firestore (\`afro_centric_apps\` collection).

---

## 2. Key Components & Implementation Details
- **Autonomous Scraper:** Located at \`agents/scraper_agent.py\`.
- **Search Engine:** Integrates Exa AI (\`EXA_API_KEY\`) with neural queries for platform discovery.
- **REST Transport Fix:** Uses standard HTTP REST (\`requests.patch\`) with Google OAuth2 tokens to bypass gRPC transport socket hangs on Windows.
- **Deduplication:** Uses deterministic URL-encoded hashes (\`make_doc_id\`) as Firestore document IDs.
- **Scraping Agent:** Extracts metadata (\`og:title\`, \`og:description\`) and email contacts while filtering non-HTML assets.

---

## 3. Environment & Local Setup
- **Directory:** \`I:\afro-discovery-system\`
- **Python Virtual Env:** \`venv/\`
- **Secrets Management:** 
  - Service account keys (\`serviceAccountKey.json\`, \`serviceAccount.json\`) reside locally in root or \`agents/\` and are strictly ignored in \`.gitignore\`.
  - Exa API Key loaded via environment variable: \`\$env:EXA_API_KEY="..."\`
- **Git Rules:** Push protection enabled on GitHub; service keys are untracked.

---

## 4. How to Run the Pipeline
\`\`\`powershell
# Navigate to project root
cd I:\afro-discovery-system

# Activate virtual environment (if applicable)
.\venv\Scripts\Activate.ps1

# Set Exa API Key and execute discovery agent
\$env:EXA_API_KEY="<YOUR_EXA_API_KEY>"
python agents/scraper_agent.py
\`\`\`

---

## 5. Future Roadmap & Expansion Ideas
- Add new topic queries to \`discovery_jobs\` inside \`scraper_agent.py\`.
- Expand frontend filtering by category, country, or tags in \`App.jsx\`.
- Add automated scheduled runs via GitHub Actions or cloud cron jobs.
"@ -Encoding UTF8


10/5/2026
# Project Context: Afro-Discovery System

## 1. Project Overview & Architecture
- **Web App Domain:** `https://afro-discovery-system.web.app`
- **Repository:** `https://github.com/aikiart/afro-discovery-system`
- **Purpose:** Discovery platform indexing Afrocentric digital archives, literature, tech initiatives, and platforms.
- **Frontend Stack:** React, Vite, Tailwind CSS, Firebase Client SDK (`onSnapshot` for live Firestore streaming).
- **Backend/Scraper:** Autonomous Python pipeline using Exa AI (`exa-py`), BeautifulSoup4, and Google Auth REST APIs.
- **Database:** Google Firebase Cloud Firestore (`afro_centric_apps` collection).

---

## 2. Key Components & Implementation Details
- **Autonomous Scraper:** Located at `agents/scraper_agent.py`.
- **Search Engine:** Integrates Exa AI (`EXA_API_KEY`) with targeted neural queries across 5 distinct categories.
- **REST Transport Fix:** Uses standard HTTP REST (`requests.patch`) with Google OAuth2 tokens to bypass gRPC transport socket hangs on Windows.
- **Deduplication:** Uses deterministic URL-encoded hashes (`make_doc_id`) as Firestore document IDs.
- **Filtering & Reliability:** Pre-filters non-HTTPS sites, sets extended read timeouts (10s), and extracts OpenGraph metadata and contact emails.

---

## 3. Environment & Local Setup
- **Directory:** `I:\afro-discovery-system`
- **Python Virtual Env:** `venv/`
- **Secrets Management:** 
  - Service account keys (`serviceAccountKey.json`, `serviceAccount.json`) reside locally in root or `agents/` and are strictly ignored in `.gitignore`.
  - Exa API Key loaded via environment variable: `$env:EXA_API_KEY="..."`
- **Git Rules:** Push protection enabled on GitHub; service keys are untracked.

---

## 4. How to Run the Pipeline
```powershell
# Navigate to project root
cd I:\afro-discovery-system

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Set Exa API Key and execute discovery agent
$env:EXA_API_KEY="<YOUR_EXA_API_KEY>"
python agents/scraper_agent.py