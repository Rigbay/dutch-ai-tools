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


## LLM Preamble Leak Validation (added 2026-07-10 by Fable)

Before committing ANY generated article (kieskeuken or dutch-ai-tools), scan body AND frontmatter description for model-wrapper preamble that leaked into content:

```bash
grep -rn -iE 'geschreven vanuit het perspectief|Door uw consumentenjournalist|^(Oke|Oké|Absoluut|Zeker|Natuurlijk)., (hier|Hier) is' src/content/
```

Any hit = the generation script pasted the model's framing sentence ("Oké, hier is de koopgids...") into the article. Strip it: the article body must START at its first real heading; the description must be a real meta description, never the model's reply preamble. Root cause: generation scripts writing the raw model response without trimming the conversational wrapper — add a trim step to every new gen-*.py.

Receipt: 2026-07-10 Fable found 14 PUBLISHED articles with this leak (13 kieskeuken + 1 dutch-ai-tools, 2 leaked into SEO meta descriptions), stripped them (commits ab3a6ec / 09f8d276).


## Frontmatter Validation — deploy is a SILENT failure point (added 2026-07-11 by Fable)

ONE schema-invalid or YAML-broken article kills the ENTIRE GitHub Pages deploy — and every deploy after it — while `git push` keeps succeeding. Between Jul 9 17:43 and Jul 11 02:36 dutchaitools.nl was frozen on a stale build: 13 new articles, the preamble-leak fixes, and the merchants.json scrub were all pushed but never reached readers.

Before committing ANY generated or edited article:

1. Run `python3 ~/clawd/scripts/fable-guardian/lint-money-repos.py` — validates YAML parseability (both repos) plus the dutch-ai-tools collection schema (description 80-180 chars, faq >= 3, related 1-3, tools >= 3, pros/cons >= 2, category enum). Zero output between the headers = clean.
2. The #1 generator bug: Dutch plural apostrophes (`BBQ's`, `accu's`, `deelauto's`, `TV's`) inside single-quoted YAML values. Generators must emit DOUBLE-quoted YAML strings, never single-quoted.
3. Colons inside unquoted values (`verdict: Meest veelzijdig: een...`) also break parsing — quote them.
4. After every push, verify the deploy actually succeeded: `gh run list -R Rigbay/dutch-ai-tools -L 1` must show `success`. **"Pushed" is not "live."**

Receipt: 2026-07-11 Fable found 9 broken articles blocking all deploys since Jul 9 (fixed in ca21cf85; kieskeuken had 1 more, fixed in 189bf93 — a Coolblue link inserted at column 0 under affiliateLinks).
