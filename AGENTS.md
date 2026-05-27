# Dutch AI Tools — AGENTS.md for autonomous agents

## Repository: Rigbay/dutch-ai-tools

Astro 5 + Tailwind CSS static site. 126 AI tool comparison articles in `src/content/tools/` and `src/content/articles/`.

## Rules

1. **No remote git push** — local-only
2. **No builds** — don't run `npm run build` or `astro build`
3. **`git diff --check` clean** before committing
4. **Affiliate registry** lives at `~/.hermes/affiliates/merchants.json` — never hardcode affiliate status text in components
5. **Do not edit `~/.openclaw/` or `~/.hermes/` config files** — those are separate agent profiles
6. **Generator scripts** in repo root must reference `merchants.json` for affiliate URLs, not hardcoded links
