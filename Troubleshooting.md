# Troubleshooting & Restoration Status

## Resolved Issues
1. **Dev Mode 404 Error:**
   - *Cause:* `index.html` was referencing pre-built production asset `/assets/index-D3PKHqgr.js` instead of source code.
   - *Fix:* `index.html` updated to load `<script type="module" src="/src/App.jsx"></script>`.

2. **Source Code Safety:**
   - Preserved `src/App.jsx` without unwanted file modifications or overwrites. Backup of original `index.html` saved as `index.html.bak`.

## Active Next Step (To resume next session)
- **Issue:** Blank page on `http://localhost:5173` with console error:
  `Uncaught SyntaxError: The requested module '/website/lib/firebase.ts' does not provide an export named 'db'`
- **Diagnosis:** `website/lib/firebase.ts` is currently empty (0 bytes).
- **First Command for Next Time:**
  ```powershell
  git checkout HEAD -- website/lib/firebase.ts