# Handoff

_Last updated: 2026-10-29 — Updated repo URLs to renamed GitHub repo `saishayy/asset-optimizations`_

## Current State
- Skill lives at `skills/assets-optimizations/` (`SKILL.md` name: `assets-optimizations`).
- Plugin + marketplace manifests use name `assets-optimizations`; install via `/plugin install assets-optimizations@assets-optimizations`.
- Cursor rule renamed to `.cursor/rules/assets-optimizations.mdc`.
- All script paths in AGENTS.md, GEMINI.md, .windsurfrules, copilot-instructions, README updated.
- GitHub repo is `saishayy/asset-optimizations` (singular "asset"); README + plugin.json URLs point there. Skill/plugin name is `assets-optimizations` (plural).

## Next Steps
- Confirm whether repo should be `asset-optimizations` or `assets-optimizations`; if renamed again, update README + plugin.json URLs and `git remote set-url`.
- Commit the rename.
- If the plugin was already installed anywhere, reinstall under the new name.

## Changelog
### 2026-10-29 — Repo URL update
- Repo renamed on GitHub; updated README (marketplace add, clone, cp, tree root) and plugin.json `repository` to `saishayy/asset-optimizations` (verified via `gh repo view`; `assets-optimizations` does not exist).
- Fixed README agent table alignment.

### 2026-10-29 — Skill rename
- `git mv` skill folder and Cursor rule to `assets-optimizations`.
- Replaced `asset-optimization` → `assets-optimizations` in SKILL.md frontmatter, plugin.json, marketplace.json, and all docs/agent instruction files.
