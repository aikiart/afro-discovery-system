# Afro Discovery System Architecture

## Goal

Discover Afro-centric websites, apps, organizations, media, educational resources, and businesses worldwide.

## Required Data

- URL
- Site Name
- Description
- Contact Email
- Phone Number
- Social Media Links
- Category
- Tags
- Date Discovered

## Agents

### Discovery Agent

Input:
- Search query

Output:
- URL
- Title
- Search Snippet

### Scraper Agent

Input:
- URL

Output:
- Site Metadata
- About Text
- Contact Information
- Social Links

### Categorizer Agent

Input:
- Scraped Content

Output:
- Category
- Tags

### Database Agent

Input:
- Categorized Data

Output:
- Firebase Record

### Update Agent

Runs Weekly

Tasks:
- Re-run discovery
- Check existing URLs
- Detect new resources
- Update records

## Future Search Providers

- Bing
- Brave
- SearchAPI.io
- Custom crawler

# Afro Discovery System - Architecture & Pipeline

## High-Level Architecture
1. **Discovery & Scraping Pipeline:**
   `DiscoveryAgent` (loads queries) ➔ `ScraperAgent` (queries Exa & deep scrapes websites) ➔ `data/export.json`
2. **Database Ingestion Pipeline:**
   `data/export.json` ➔ `main.py` / `DatabaseAgent` ➔ Firebase Firestore (`afro_centric_apps`)
3. **Frontend Application:**
   Firestore Database ➔ React (`src/App.jsx`) ➔ Firebase Hosting

## Key Module Responsibilities
- `agents/discovery_agent.py`: Loads search topics and queries for Exa Search API.
- `agents/scraper_agent.py`: Executes web queries, deep scrapes target sites for title/description/emails/socials/location, and filters out broken links (404/500/SSL errors).
- `agents/database_agent.py`: Handles connection, upserting, deduplication, and record deletions in Firestore.
- `main.py`: Local orchestrator that reads `data/export.json` and pushes valid records to Firestore.
- `src/App.jsx`: Main UI component displaying platform cards, counts, filter badges, and links.