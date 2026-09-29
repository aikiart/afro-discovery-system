# Project TODO List

- [ ] Add domain-fallback logic in `scraper_agent.py` to eliminate "Untitled Platform" records automatically.
- [ ] Implement `extract_location()` function in `scraper_agent.py` to detect platform countries/states.
- [ ] Add location pill badges (📍 Country) to card views in `src/App.jsx`.
- [ ] Create `admin_cleanup.py` script to bulk-purge incomplete or unwanted Firestore records.
- [ ] Implement optional `is_visible` flag on database records to allow soft deletion/hiding from the UI.