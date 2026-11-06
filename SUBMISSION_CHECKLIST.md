# 🔒 Public Repository Submission Checklist

**[← README](README.md)**

## Audit of the uploaded ZIP (performed)

- [x] Inspected archive structure: **113,706 entries**; includes a virtual environment, Git metadata, backup folders, `.env`, and local database files.
- [x] Inspected the archived Git index: **618 tracked files**; `.env` is **not currently tracked**, but approximately **364 backup files** and **2 database/backup files** are tracked. These must be reviewed and removed from version control before publication.
- [x] Confirmed `.env.example` is tracked.
- [x] Prepared the README, demo guide, and avatar reference image.
- [ ] **BLOCKER:** Remove tracked backup files and database snapshots from Git and verify they contain no private student information.
- [ ] **BLOCKER:** Inspect Git history for credentials and sensitive data. Current index checks cannot establish historical safety.
- [ ] **BLOCKER:** Review and rotate any real API keys in `.env` that have been shared or committed. I did not display or validate their values.
- [ ] Run a clean installation and full demo locally; I cannot certify these without executing the app with your credentials.
- [ ] Confirm licensing/attribution and record the final demo video.

**Status: NOT YET SAFE TO MAKE PUBLIC.** The archived Git index contains tracked backups and database files, and history/credential checks remain outstanding.

## Final publication checklist

The uploaded development ZIP includes `.env`, `.git/`, `.venv/`, local `.db` files, frontend backups, and logs. The existence of a `.gitignore` does **not** remove already tracked files or erase Git history.

- [ ] Inspect `.env` **locally** for real credentials. Rotate any API key that was ever committed or shared.
- [ ] Run `git ls-files` and confirm no `.env`, `*.db`, logs, `.venv`, backups, or generated student data are tracked.
- [ ] Inspect Git history for previously committed secrets; rewrite/sanitize history if necessary before making public.
- [ ] Do not publish development backups or the 402 MB source ZIP as-is.
- [ ] Add `README.md`, `DEMO_GUIDE.md`, `SUBMISSION_CHECKLIST.md`, `backend/requirements.txt`, and `docs/images/avatar-design-exploration.png` from this package.
- [ ] Keep the repository's existing `ATTRIBUTION.md`, `docs/AI_USAGE_LOG.md`, `.env.example`, and `.gitignore` (review them for accuracy).
- [ ] Verify fresh backend/frontend installs and test the full demo with the final API configuration.
- [ ] Confirm frontend `localhost:8000` assumptions; these are suitable for the documented local demo but not a hosted deployment.
- [ ] Check license choice, attribution, and any permissions needed to publish avatar images, logos, and team research.
- [ ] Record the demo with fictional student information and without exposing secrets.

Suggested ignore additions (merge into existing `.gitignore`, don't replace it blindly):

```gitignore
.env
.env.*
!.env.example
.venv/
node_modules/
frontend/dist/
*.db
*.db-*
*.bak
logs/
frontend.backup.*/
backup_lesson_files/
__pycache__/
.pytest_cache/
.DS_Store
```

**Caution:** The requirements file is import-based, not a tested lockfile; validate it in a clean environment before public release.
