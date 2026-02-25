# Changelog

All notable changes to the databricks-eda framework will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) — SemVer.

---

## [1.1.0] - 2026-02-25

### Added
- `databricks_eda/` installable Python package replacing the old `utils/` folder
- `databricks-eda-setup` CLI entry point for token refresh and connection testing
- `CLAUDE.md` as the primary Claude Code instructions file (replaces `AGENTS.md`)
- Sample query patterns in `CLAUDE.md`: single query, multi-query client reuse, error handling
- New project setup section in `CLAUDE.md` with full bootstrap commands
- `pyproject.toml` build system (hatchling) with proper entry points
- `personal` git remote pointing to local personal repo for offline sync
- `carteakey` git remote pointing to personal GitHub for cloud sync

### Changed
- Import style: `from databricks_eda import query_databricks` — no `sys.path` manipulation needed
- Token setup: `databricks-eda-setup --refresh-token` replaces `python3 utils/token_auth_setup.py`
- `databricks-cli` dependency replaced with `databricks-sdk`
- README rewritten to document library-based new project workflow

### Removed
- `utils/` folder (functionality moved into `databricks_eda` package)
- `AGENTS.md` (replaced by `CLAUDE.md`)

---

## [1.0.0] - 2026-01-02

### Added
- Initial release: volleying workflow with Claude Code for Databricks EDA
- `utils/` folder with REST-based Databricks SQL client
- OAuth token management via `token_auth_setup.py`
- Jupytext QA step for notebook validation
- Sample airline dataset EDA analysis
