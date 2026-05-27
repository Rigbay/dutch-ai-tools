# Dutch AI Tools Comparison Site — Codex Build Spec

**Mission slug:** dutch-ai-tools-comparison
**Date:** 2026-05-16
**Owner:** Hermes (research + spec), Codex (implementation)
**Status:** ready-to-build, zero anonymous-operator input required until monetization signups

## Goal
Build and deploy a static Astro-based Dutch-language AI/SaaS tools comparison & review site at GitHub Pages (rigbay.github.io/dutch-ai-tools or similar). 15-20 seed articles covering "beste AI tools voor [doelgroep] 2026". Monetization via recurring SaaS affiliate programs with placeholder links ready for swap-in. Same architecture as dutch-appliances site for reuse.

## Success Criteria
- Astro site compiles cleanly, deploys to GitHub Pages via `gh pages` or Astro config.
- 15-20 articles generated with:
  - Dutch titles (e.g. "Beste AI Tools voor Kleine Ondernemers 2026")
  - Comparison tables (pricing, features, pros/cons)
  - Affiliate link placeholders for active programs only
  - Schema.org Article + FAQ + BreadcrumbList
  - Internal linking between articles
- SEO foundation: sitemap, robots.txt, llms.txt, IndexNow ready
- Zero runtime cost, <1hr/wk maintenance post-launch
- Ready for anonymous-operator's one-time affiliate signup bundle for active programs

## Tech Stack (reuse from appliances)
- Astro 4.x + Tailwind + MDX
- Content Collections for articles
- GitHub Pages deployment (free)
- Gemini 2.5 Flash-Lite for article generation (raw markdown → frontmatter injection)

## Files Codex Must Create / Modify
1. `/workspace/agent-workspace/scripts/missions/passive-income/dutch-ai-tools-comparison/` (this dir)
   - astro.config.mjs (GitHub Pages base path)
   - package.json (Astro deps)
   - src/content/config.ts (Article schema enforcing date, products min 5? no — for tools: features min 4)
   - src/content/articles/ (15-20 .md files with frontmatter + body)
   - src/pages/index.astro + article pages
   - public/robots.txt, sitemap, llms.txt
2. Generate script: `generate-articles.py` (Gemini calls for Dutch content, raw-text mode to avoid JSON issues)
3. Affiliate placeholder map in `affiliates.ts` or config
4. Deploy script or instructions for `gh repo create` + Pages enable if needed

## Article Topics (seed 15-20, prioritize high-intent Dutch searches)
- Beste AI Tools voor Kleine Ondernemers 2026
- Beste AI Schrijftools voor Content Creators
- Beste AI Tools voor Developers / Programmeurs
- Beste AI Marketing Tools 2026
- Beste AI Tools voor Solopreneurs
- Beste Notion Alternatieven + AI Integraties
- Beste Email Marketing Tools met AI (beehiiv focus)
- Beste AI Productivity Tools 2026
- Beste AI Research Tools voor Kenniswerkers
- Beste AI Image/Video Tools 2026
- Beste AI Customer Support Tools
- Beste AI Data Analysis Tools voor Non-Tech
- Beste AI Automation Tools (Zapier + Make + n8n)
- Beste AI Chatbots voor Bedrijven
- Beste AI SEO Tools 2026
- Beste AI Tools voor Freelancers
- Beste AI Tools voor Marketing Agencies
- Beste AI Tools voor E-commerce (Dutch context)
- Beste AI Tools voor Onderwijs / Leraren
- Beste AI Tools voor Gezondheidszorg / Therapeuten (tie to CU audience later)

Each article: 1200-1800 words Dutch, table of 5-8 tools, pros/cons lists, pricing tiers, affiliate placeholders, FAQ.

## Environment / Credentials Needed
- GEMINI_API_KEY (already in `~/.hermes/private/gemini-api-key`)
- GitHub CLI `gh` authenticated (Rigbay)
- No other secrets until affiliate links

## Execution Order for Codex
1. Scaffold Astro project with Tailwind + MDX + content collections
2. Define article schema (title, slug, date, tools: array, pros/cons, affiliateLinks, related)
3. Write generate-articles.py using Gemini raw-markdown output + frontmatter injection
4. Generate all 20 articles in batch (handle 400s by skipping/retrying)
5. Build static site, verify links + schema
6. Init git repo, push to GitHub (new repo or fork pattern), enable Pages
7. Output RESULT.md with deploy URL, article count, next steps for anonymous-operator (affiliate signups)

## Constraints
- No active time for anonymous-operator
- Dutch language primary
- Recurring affiliate focus (placeholders only)
- Reuse appliance site patterns where possible (schema, deployment)
- One pilot at a time — appliance monetization still gated

## Verification
Codex must produce RESULT.md or STATUS.md at end of run. Hermes will read it and update opportunities.md status.

**Ready for delegation.**
