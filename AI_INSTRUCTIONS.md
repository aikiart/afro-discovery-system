# AI Collaborator Instructions

Before modifying code or answering questions, read:
1. `PROJECT_STATUS.md`
2. `ARCHITECTURE.md`
3. `DECISIONS.md`
4. `TODO.md`

## Guidelines for AI Assistants:
- **Do not alter core execution workflow:** Always preserve the verified one-line PowerShell execution command for scraping and deployment.
- **Firestore Schema:** Remember Firestore is schemaless. New fields like `location` or `is_visible` can be added without altering table definitions.
- **Deployment Safety:** Always remind the user to check updates in an Incognito / Private window to avoid browser caching issues.
