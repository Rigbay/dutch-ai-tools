#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool comparison articles targeting content gaps."""
import os, json, time, sys, requests, re

API_KEY = os.environ.get("GEMINI_API_KEY", "") or open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

TOPICS = [
    # 1. Web Analytics — Plausible vs Google Analytics vs Matomo (privacy angle, strong NL relevance)
    {
        "slug": "plausible-vs-google-analytics-vs-matomo-2026",
        "title": "Plausible vs Google Analytics vs Matomo 2026: beste privacy-vriendelijke web analytics voor Nederlandse sites",
        "description": "Vergelijk Plausible, Google Analytics 4, Matomo, Fathom en Simple Analytics in 2026: privacyvriendelijkheid, AVG-compliance, dashboards, prijzen en welke het beste past bij jouw Nederlandse website of webshop.",
        "category": "marketing",
        "tools": [
            ("Plausible Analytics", 4.7, "EUR 9-150/mnd", "Privacy-first web analytics"),
            ("Google Analytics 4", 4.3, "Gratis (premium EUR 50K+/jr)", "Enterprise analytics"),
            ("Matomo Cloud", 4.5, "EUR 20-500/mnd", "Open-source analytics"),
            ("Fathom Analytics", 4.6, "EUR 14-54/mnd", "Simpele privacy analytics"),
            ("Simple Analytics", 4.2, "EUR 9-35/mnd", "Zero-tracking analytics"),
            ("Pirsch Analytics", 4.1, "EUR 6-30/mnd", "Duitse privacy analytics"),
            ("Umami", 4.4, "Gratis (self-host)", "Open-source self-hosted"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1400-1800 woorden over de beste web analytics tools in 2026. Focus: privacy-vriendelijke alternatieven voor Google Analytics, vanuit Nederlands/EU perspectief.

Behandel deze 7 tools: Plausible Analytics, Google Analytics 4, Matomo Cloud, Fathom Analytics, Simple Analytics, Pirsch Analytics, Umami.

Voor elke tool:
- Naam en belangrijkste onderscheidende feature
- Privacy en AVG/GDPR-compliance status
- Dashboard kwaliteit en gebruiksgemak
- Prijsmodel (aantal pageviews per tier)
- Beste use case (blog, webshop, corporate, agency)
- Verdict

Inclusief:
- Markdown vergelijkingstabel met: Tool, Privacy-score, AVG-vriendelijk, Dashboard, Prijs, Beste voor, Rating
- Sectie over 'Waarom Google Analytics 4 niet altijd de beste keuze is' (privacy, cookiewet, datadoorgifte VS)
- Nederlandse context: Autoriteit Persoonsgegevens, cookiewet, AVG-boetes
- 3 FAQ-vragen over analytics in Nederland

Gebruik ## koppen. Schrijf in helder Nederlands. Geen YAML frontmatter."""
    },
    # 2. API Testing — Postman vs Insomnia vs Bruno (dev audience)
    {
        "slug": "postman-vs-insomnia-vs-bruno-vs-hoppscotch-2026",
        "title": "Postman vs Insomnia vs Bruno vs Hoppscotch 2026: beste API testing tool voor developers",
        "description": "Vergelijk Postman, Insomnia, Bruno en Hoppscotch in 2026: REST en GraphQL testing, collections, environment management, CI/CD integratie en prijs voor Nederlandse developers en teams.",
        "category": "development",
        "tools": [
            ("Postman", 4.6, "Gratis - EUR 49/dev/mnd", "Volledige API platform"),
            ("Insomnia", 4.4, "Gratis - EUR 12/dev/mnd", "Simpele REST/GraphQL client"),
            ("Bruno", 4.5, "Gratis (open-source)", "Git-native API client"),
            ("Hoppscotch", 4.3, "Gratis - EUR 10/mnd", "Browser-based API client"),
            ("Thunder Client", 4.2, "Gratis - EUR 6/mnd", "VS Code API client"),
            ("Apidog", 4.3, "Gratis - EUR 35/mnd", "API design + testing"),
            ("HTTPie", 4.1, "Gratis - EUR 15/mnd", "CLI-first API testing"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1400-1800 woorden over de beste API testing tools in 2026 voor developers.

Behandel deze 7 tools: Postman, Insomnia, Bruno, Hoppscotch, Thunder Client, Apidog, HTTPie.

Voor elke tool:
- Naam en type (desktop app, browser, VS Code extensie, CLI)
- REST, GraphQL, WebSocket ondersteuning
- Environment management en variabelen
- CI/CD integratie (Newman, GitHub Actions pipeline)
- Prijs per developer
- Beste use case (solo dev, klein team, enterprise)
- Verdict

Inclusief:
- Markdown vergelijkingstabel met: Tool, Type, Protocol support, CI/CD, Prijs, Beste voor, Rating
- Sectie: 'Bruno vs Postman — waarom git-native API testing aan populariteit wint'
- Sectie over offline/air-gapped werken en data-soevereiniteit
- 3 FAQ-vragen

Gebruik ## koppen. Schrijf in helder Nederlands. Geen YAML frontmatter."""
    },
    # 3. Headless CMS — Strapi vs Contentful vs Sanity (enterprise)
    {
        "slug": "strapi-vs-contentful-vs-sanity-vs-payload-2026",
        "title": "Strapi vs Contentful vs Sanity vs Payload 2026: beste headless CMS voor Nederlandse websites",
        "description": "Vergelijk de beste headless CMS in 2026: Strapi, Contentful, Sanity, Payload CMS, Storyblok en Hygraph. Voor Nederlandse developers, agencies en marketing teams die op zoek zijn naar flexibel contentbeheer.",
        "category": "development",
        "tools": [
            ("Strapi", 4.6, "Gratis open-source - EUR 99+/mnd cloud", "Open-source headless CMS"),
            ("Contentful", 4.5, "EUR 300-2500/mnd", "Enterprise content platform"),
            ("Sanity", 4.6, "EUR 99-999/mnd", "Real-time structured content"),
            ("Payload CMS", 4.4, "Gratis open-source - EUR 35+/mnd cloud", "TypeScript-native CMS"),
            ("Storyblok", 4.5, "EUR 90-800/mnd", "Visual editor headless CMS"),
            ("Hygraph", 4.2, "EUR 0-799/mnd", "GraphQL-native CMS"),
            ("Directus", 4.3, "Gratis open-source - EUR 25+/mnd cloud", "Database-wrapper CMS"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1400-1800 woorden over de beste headless CMS platforms in 2026 voor Nederlandse developers en agencies.

Behandel deze 7 tools: Strapi, Contentful, Sanity, Payload CMS, Storyblok, Hygraph, Directus.

Voor elke tool:
- Naam en type (open-source, SaaS, hybride)
- API type (REST, GraphQL) en developer experience
- Visual editing en content preview
- Hosting opties (self-hosted, cloud, on-premise)
- Prijsmodel
- Beste use case
- Verdict

Inclusief:
- Markdown vergelijkingstabel met: CMS, Type, API, Visual Editor, Self-host?, Prijs, Beste voor, Rating
- Sectie: 'Open-source vs SaaS headless CMS — wat past bij jouw project?'
- Sectie over welke CMS het beste werkt met Astro, Next.js, Nuxt (NL agency stack)
- 3 FAQ-vragen over headless CMS keuze

Gebruik ## koppen. Schrijf in helder Nederlands. Geen YAML frontmatter."""
    },
    # 4. Transactional Email — SendGrid vs Mailgun vs Postmark (overlaps email marketing coverage)
    {
        "slug": "sendgrid-vs-mailgun-vs-postmark-vs-ses-2026",
        "title": "SendGrid vs Mailgun vs Postmark vs Amazon SES 2026: beste transactional email service voor Nederlandse apps",
        "description": "Vergelijk transactional email services in 2026: SendGrid, Mailgun, Postmark, Amazon SES, Resend en Brevo voor delivery rate, prijs, API en betrouwbaarheid vanuit Nederlandse/Europese servers.",
        "category": "development",
        "tools": [
            ("SendGrid", 4.5, "Gratis (100/dag) - EUR 20-250/mnd", "Grootste email API"),
            ("Mailgun", 4.4, "Gratis trial - EUR 35-150/mnd", "Developer-friendly email"),
            ("Postmark", 4.7, "EUR 15-245/mnd", "Snelste delivery"),
            ("Amazon SES", 4.3, "EUR 0,10/1000 emails", "Goedkoopste bulk email"),
            ("Resend", 4.5, "Gratis (100/dag) - EUR 20/mnd", "Moderne email API voor React"),
            ("Brevo (Sendinblue)", 4.2, "Gratis (300/dag) - EUR 25-65/mnd", "Transactioneel + marketing"),
            ("Mailtrap", 4.1, "Gratis - EUR 15-50/mnd", "Email testing sandbox"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1400-1800 woorden over de beste transactional email services in 2026 voor Nederlandse developers.

Behandel deze 7 tools: SendGrid, Mailgun, Postmark, Amazon SES, Resend, Brevo (Sendinblue), Mailtrap.

Voor elke tool:
- Naam en type (API-first, SMTP, testing)
- Delivery rate (percentage) en snelheid
- API kwaliteit en SDK talen
- Europese/EU datacenters (relevant voor AVG)
- Prijs per 10.000 emails
- Beste use case
- Verdict

Inclusief:
- Markdown vergelijkingstabel: Service, Delivery Rate, EU Servers, API Score, Prijs/10K, Beste voor, Rating
- Sectie: 'Amazon SES — goedkoopste maar complexste: wanneer wel/niet gebruiken'
- Sectie: 'Resend — waarom de nieuwe generatie email API aantrekkelijk is voor React/Next.js devs'
- AVG/data sovereignty: waarom EU-servers belangrijk zijn
- 3 FAQ-vragen

Gebruik ## koppen. Schrijf in helder Nederlands. Geen YAML frontmatter."""
    },
    # 5. Code hosting — GitHub vs GitLab vs Bitbucket (strong developer search volume)
    {
        "slug": "github-vs-gitlab-vs-bitbucket-vs-gitea-2026",
        "title": "GitHub vs GitLab vs Bitbucket vs Gitea 2026: beste code hosting platform voor Nederlandse developers",
        "description": "Vergelijk code hosting platforms in 2026: GitHub, GitLab, Bitbucket en Gitea op prijs, CI/CD, AI features (Copilot), security en self-hosting opties voor Nederlandse developers, startups en enterprises.",
        "category": "development",
        "tools": [
            ("GitHub", 4.8, "Gratis - EUR 8-25/dev/mnd", "Grootste developer platform"),
            ("GitLab", 4.6, "Gratis - EUR 29-179/dev/mnd", "All-in-one DevOps platform"),
            ("Bitbucket", 4.3, "Gratis - EUR 3-6/dev/mnd", "Atlassian-integratie"),
            ("Gitea", 4.4, "Gratis (self-host)", "Lichtgewicht self-hosted Git"),
            ("Azure DevOps", 4.2, "Gratis (5 devs) - EUR 6-52/dev/mnd", "Enterprise Git + CI/CD"),
            ("Codeberg", 4.1, "Gratis", "Privacy-first EU hosting"),
            ("SourceHut", 4.0, "EUR 2-10/mnd", "Minimalistische workflow"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1400-1800 woorden over de beste code hosting platforms in 2026 voor Nederlandse developers.

Behandel deze 7 tools: GitHub, GitLab, Bitbucket, Gitea, Azure DevOps, Codeberg, SourceHut.

Voor elke tool:
- Naam en type (cloud SaaS, self-hosted, EU-based)
- CI/CD mogelijkheden (GitHub Actions, GitLab CI, Bitbucket Pipelines)
- AI features (GitHub Copilot, GitLab Duo, CodeWhisperer)
- Security en compliance (SOC2, ISO27001, SBOM)
- Prijs per developer
- Beste use case
- Verdict

Inclusief:
- Markdown vergelijkingstabel: Platform, Type, CI/CD, AI Features, Self-host?, Prijs/dev/mnd, Beste voor, Rating
- Sectie: 'GitHub Copilot vs GitLab Duo — AI-coding assistenten vergeleken'
- Sectie: 'Gitea en Codeberg — Europese alternatieven voor soevereine code hosting'
- Sectie: 'Wanneer kies je self-hosted boven cloud?'
- 3 FAQ-vragen

Gebruik ## koppen. Schrijf in helder Nederlands. Geen YAML frontmatter."""
    },
]

AFFILIATE_TEMPLATES = {
    "amazon": "https://www.amazon.nl/dp/{asin}?tag=kieskeukennl-21",
    "beehiiv": "https://www.beehiiv.com/?via=anonymous-operator",
    "generic": "https://www.{domain}.com/?ref=aitoolsnl",
}

def call_gemini(prompt, max_retries=5):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=180)
            if resp.status_code == 429:
                wait = 20 * (attempt + 1)
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                return None
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
    return None

def slugify(domain):
    return domain.lower().replace(" ", "").replace(".", "").replace("(", "").replace(")", "").replace("+", "").replace("/", "")

def build_frontmatter(topic, body_text=""):
    tools_yaml = "\n".join([
        f'  - name: "{t[0]}"\n'
        f'    verdict: "AI-gedreven {t[3].lower()}"\n'
        f'    priceRange: "{t[2]}"\n'
        f'    bestFor: "{t[3]}"\n'
        f'    rating: {t[1]}\n'
        f'    affiliateLink: "https://www.{slugify(t[0].split(" ")[0].replace("AI","").strip())}.com/?ref=aitoolsnl"'
        for t in topic["tools"]
    ])
    all_articles = [f.replace(".md", "") for f in os.listdir(OUT_DIR) if f.endswith(".md") and f != "index.md" and f != "404.md"]
    # Pick 3 related articles in same category or random
    cat_articles = [a for a in all_articles if topic["category"] in a and topic["slug"] not in a]
    if len(cat_articles) < 3:
        cat_articles = [a for a in all_articles if topic["slug"] not in a][:3]
    import random; random.shuffle(cat_articles)
    related = cat_articles[:3]

    faqs = [
        f'  - q: "Wat is de beste tool in deze categorie voor Nederlandse gebruikers in 2026?"',
        f'    a: "Voor de meeste gebruikers is {topic["tools"][0][0]} de beste keuze vanwege de balans tussen functionaliteit, prijs en gebruiksgemak. Lees de volledige vergelijking voor een gedetailleerd advies per use case."',
        f'  - q: "Zijn er gratis alternatieven beschikbaar?"',
        f'    a: "Ja, veel tools bieden een gratis tier of open-source versie. {topic["tools"][0][0]} biedt bijvoorbeeld een gratis startoptie. Bekijk de prijsrange per tool in de vergelijkingstabel hierboven."',
        f'  - q: "Hoe kies ik de juiste tool voor mijn behoeften?"',
        f'    a: "Bepaal eerst je budget, teamgrootte en belangrijkste vereisten. Kijk dan naar de Beste voor-kolom in de vergelijkingstabel. Probeer 2-3 tools met een gratis trial voordat je een definitieve keuze maakt."',
    ]
    return f"""---
title: '{topic["title"]}'
slug: {topic["slug"]}
description: {topic["description"]}
category: {topic["category"]}
rating: 4.4
priceRange: EUR 0-2500/mnd
pros:
  - Eerlijke en uitgebreide AI-tool vergelijking
  - Concrete prijzen en use cases per tool
  - Nederlandstalig met EU/AVG-context
cons:
  - Prijzen kunnen wijzigen — check altijd de aanbieder
  - Niet elke tool is uitgebreid praktisch getest
  - Sommige features nog in beta of rolling release
affiliateLinks:
  - https://www.beehiiv.com/?via=anonymous-operator
date: 2026-06-06
modelYear: 2026
featuredTool: "{topic['tools'][0][0]}"
readingTime: 8 min
tools:
{tools_yaml}
related:
  - {related[0] if len(related) > 0 else topic["slug"]}
  - {related[1] if len(related) > 1 else topic["slug"]}
  - {related[2] if len(related) > 2 else topic["slug"]}
draft: false
faq:
{chr(10).join(faqs)}
---

"""

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    generated = 0
    failed = 0
    skipped = 0

    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(TOPICS)}] {topic['slug']} — EXISTS, skipping")
            skipped += 1
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['slug']} ({topic['category']})")
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None:
            print(f"  FAILED — using fallback content")
            failed += 1
            raw_text = f"""## Introductie

AI en digitale tools veranderen hoe we werken met {topic["category"]}. Dit artikel vergelijkt de beste tools in deze categorie voor 2026. Hieronder vind je een overzicht van de belangrijkste opties, hun prijzen en onze beoordeling.

## De tools vergeleken

We hebben {len(topic["tools"])} toonaangevende tools bekeken en beoordeeld op functionaliteit, prijs en gebruiksgemak.

| Tool | Beste voor | Prijs | Score |
|------|-----------|-------|-------|
"""
            for t in topic["tools"]:
                raw_text += f"| {t[0]} | {t[3]} | {t[2]} | {t[1]}/5 |\n"
            raw_text += f"""
## Conclusie

De beste tool in deze categorie hangt af van je specifieke situatie. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende keuze.

## Veelgestelde vragen

**Wat kost een goede tool in deze categorie?**
De prijzen variëren van gratis tot EUR 500 per maand, afhankelijk van schaal en functionaliteit.

**Zijn deze tools geschikt voor Nederlandse gebruikers?**
Ja, alle besproken tools zijn internationaal en ondersteunen de Nederlandse markt.

**Kan ik meerdere tools combineren?**
Ja, veel tools integreren via API. Een combinatie dekt vaak meer use cases.
"""
        else:
            generated += 1

        fm = build_frontmatter(topic, raw_text)
        full_content = fm + "\n" + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"  ✓ Written ({len(full_content)} chars)")
        time.sleep(3)  # rate limiting

    print(f"\n=== Done! Generated: {generated}, Failed: {failed}, Skipped: {skipped} ===")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
