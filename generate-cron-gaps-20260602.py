#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool articles targeting thinnest categories: marketing +2, development +2, technologie +1."""
import os, json, time, sys, requests, re

API_KEY = os.environ.get("GEMINI_API_KEY", "") or open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/dutch-ai-tools/src/content/articles"

TOPICS = [
    # --- Development (12 → 14) ---
    {
        "slug": "beste-ai-tools-databases-ontwikkeling-2026",
        "title": "Beste AI Tools voor Database Ontwikkeling 2026: top 7 vergeleken",
        "description": "AI database tools in 2026 vergelijkbaar: SQL AI, Supabase AI, MongoDB Atlas, DataStax, Neon AI en meer voor moderne database ontwikkeling.",
        "category": "development",
        "tools": [
            ("Supabase AI", 4.6, "EUR 0-100/mnd", "Full-stack apps"),
            ("Neon AI", 4.5, "EUR 0-200/mnd", "Serverless PostgreSQL"),
            ("MongoDB Atlas AI", 4.3, "EUR 0-300/mnd", "Document databases"),
            ("DataStax Astra AI", 4.2, "EUR 0-250/mnd", "Vector search & LLM apps"),
            ("AirOps SQL AI", 4.1, "EUR 0-50/mnd", "SQL queries"),
            ("Retool Workflows AI", 4.3, "EUR 0-150/mnd", "Interne tools"),
            ("TimescaleDB AI", 4.0, "EUR 0-200/mnd", "Tijdseries data"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor database ontwikkeling in 2026.
Behandel deze 7 tools: Supabase AI, Neon AI, MongoDB Atlas AI, DataStax Astra AI, AirOps SQL AI, Retool Workflows AI, TimescaleDB AI.
Voor elke tool: naam, wat het doet met AI, prijsrange, beste use case en verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Conclusie met aanbeveling per type developer. 3 FAQ-vragen.
Gebruik ## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-devs-ops-2026",
        "title": "Beste AI Tools voor DevOps & Infrastructure 2026: top 7 vergeleken",
        "description": "AI DevOps tools vergeleken: Pulumi AI, Datadog AI, Grafana AI, New Relic AI, FireHydrant, Buildkite en Checkly AI voor infra-automatisering.",
        "category": "development",
        "tools": [
            ("Pulumi AI", 4.5, "EUR 0-200/mnd", "Infrastructure as Code"),
            ("Datadog AI", 4.6, "EUR 0-300/mnd", "Monitoring & observability"),
            ("Grafana AI", 4.4, "EUR 0-100/mnd", "Visualisatie & alerts"),
            ("New Relic AI", 4.0, "EUR 0-400/mnd", "Full-stack observability"),
            ("FireHydrant AI", 4.2, "EUR 0-150/mnd", "Incident response"),
            ("Buildkite AI", 4.1, "EUR 0-100/mnd", "CI/CD pipelines"),
            ("Checkly AI", 4.3, "EUR 0-80/mnd", "Synthetische monitoring"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor DevOps en infrastructure in 2026.
Behandel deze 7 tools: Pulumi AI, Datadog AI, Grafana AI, New Relic AI, FireHydrant, Buildkite, Checkly AI.
Voor elke tool: naam, wat het doet met AI, prijsrange, beste use case en verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.
Conclusie met aanbeveling per type team (startup vs enterprise). 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Marketing (13 → 15) ---
    {
        "slug": "beste-ai-seo-tools-2026",
        "title": "Beste AI SEO Tools 2026: top 7 vergeleken voor Nederlandse websites",
        "description": "Vergelijk de beste AI SEO tools voor 2026: Semrush AI, Surfer SEO, Writesonic, NeuronWriter, RankMath, Frase en SE Ranking. Vind de beste SEO AI voor jouw site.",
        "category": "marketing",
        "tools": [
            ("Semrush AI", 4.7, "EUR 120-450/mnd", "Allround SEO & concurrentie"),
            ("Surfer SEO", 4.5, "EUR 70-280/mnd", "Content optimalisatie"),
            ("Writesonic", 4.3, "EUR 20-50/mnd", "SEO content schrijven"),
            ("NeuronWriter", 4.2, "EUR 30-100/mnd", "NLP-content strategie"),
            ("RankMath SEO AI", 4.4, "EUR 0-60/jaar", "WordPress SEO"),
            ("Frase AI", 4.3, "EUR 40-150/mnd", "Onderzoek & content briefs"),
            ("SE Ranking", 4.1, "EUR 40-200/mnd", "SEO tracking & audits"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI SEO tools voor 2026, specifiek gericht op de Nederlandse markt.
Behandel deze 7 tools: Semrush AI, Surfer SEO, Writesonic, NeuronWriter, RankMath SEO AI, Frase, SE Ranking.
Voor elke tool: naam, AI-functionaliteit, prijsrange, beste use case, verdict.
Vergelijk welke tools het beste werken voor Nederlandse SEO (zoekwoorden, concurrentie, lokale optimalisatie).
Markdown vergelijkingstabel. Conclusie. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-influencer-marketing-2026",
        "title": "Beste AI Tools voor Influencer Marketing 2026: top 7 vergeleken",
        "description": "AI tools voor influencer marketing in 2026: Upfluence, CreatorIQ, Grin, Aspire, HypeAuditor en BuzzSumo AI vergeleken voor Nederlandse merken.",
        "category": "marketing",
        "tools": [
            ("Upfluence", 4.4, "EUR 300-2000/mnd", "Influencer discovery"),
            ("CreatorIQ", 4.5, "EUR 500-3000/mnd", "Enterprise influencer management"),
            ("Grin", 4.3, "EUR 200-1500/mnd", "Creator relatiebeheer"),
            ("Aspire", 4.2, "EUR 200-1000/mnd", "Campagne management"),
            ("HypeAuditor", 4.4, "EUR 100-500/mnd", "Fraude detectie & analytics"),
            ("BuzzSumo AI", 4.1, "EUR 200-600/mnd", "Content & trend analyse"),
            ("Heepsy", 4.0, "EUR 50-300/mnd", "Micro-influencer search"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor influencer marketing in 2026.
Behandel deze 7 platforms: Upfluence, CreatorIQ, Grin, Aspire, HypeAuditor, BuzzSumo AI, Heepsy.
Voor elke tool: naam, AI-functionaliteit, prijsrange, beste use case (welk type influencer/merk), verdict.
Focus op hoe AI helpt bij influencer discovery, fraudedetectie, ROI-berekening.
Markdown vergelijkingstabel. Conclusie met aanbeveling per budget. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Technologie (12 → 13) ---
    {
        "slug": "beste-ai-tools-cybersecurity-privacy-2026",
        "title": "Beste AI Tools voor Cybersecurity & Privacy 2026: top 7 vergeleken",
        "description": "AI cybersecurity tools vergeleken: CrowdStrike, Darktrace, SentinelOne, Vectra, Tessian, Snyk AI en Wiz AI voor dreigingsdetectie en privacybescherming.",
        "category": "technologie",
        "tools": [
            ("CrowdStrike Falcon AI", 4.7, "EUR 100-300/mnd", "EDR & dreigingsdetectie"),
            ("Darktrace DETECT AI", 4.6, "EUR 200-500/mnd", "Zelflerend netwerkverkeer"),
            ("SentinelOne Singularity", 4.5, "EUR 80-250/mnd", "Autonomous endpoint protection"),
            ("Vectra AI", 4.3, "EUR 150-400/mnd", "Netwerk detectie & response"),
            ("Tessian AI", 4.1, "EUR 100-300/mnd", "E-mail security"),
            ("Snyk AI", 4.4, "EUR 0-200/mnd", "Code & dependency scanning"),
            ("Wiz AI", 4.5, "EUR 100-500/mnd", "Cloud security & AI risk"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor cybersecurity en privacy in 2026.
Behandel deze 7 tools: CrowdStrike Falcon AI, Darktrace DETECT AI, SentinelOne Singularity, Vectra AI, Tessian, Snyk AI, Wiz AI.
Voor elke tool: naam, hoe AI wordt gebruikt voor dreigingsdetectie, prijsrange, beste use case (type bedrijf/risico), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.
Besteed aandacht aan EU AI Act en Nederlandse privacyregels (AVG/GDPR) die relevant zijn.
Conclusie. 3 FAQ-vragen. ## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

AFFILIATE_TEMPLATES = {
    "amazon": "https://www.amazon.nl/dp/{asin}?tag=kieskeukennl-21",
    "beehiiv": "https://www.beehiiv.com/",
    "semrush": "https://www.semrush.com/?ref=aitoolsnl",
    "writesonic": "https://writesonic.com/?via=aitoolsnl",
    "generic": "https://www.{domain}.com/?ref=aitoolsnl",
}

def call_gemini(prompt, max_retries=3):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None

def slugify(domain):
    return domain.lower().replace(" ", "")

def build_frontmatter(topic, body_text=""):
    tools_yaml = "\n".join([
        f'  - name: "{t[0]}"\n'
        f'    verdict: "AI-gedreven tool voor {t[3].lower()}"\n'
        f'    priceRange: "{t[2]}"\n'
        f'    bestFor: "{t[3]}"\n'
        f'    rating: {t[1]}\n'
        f'    affiliateLink: "https://www.{slugify(t[0].split(" ")[0].replace("AI","").strip())}.com/?ref=aitoolsnl"'
        for t in topic["tools"]
    ])
    # Pull 3 related slugs from existing articles for this category
    all_articles = [f.replace(".md", "") for f in os.listdir(OUT_DIR) if f.endswith(".md") and f != "index.md" and f != "404.md"]
    cat_articles = [a for a in all_articles if topic["slug"] not in a]
    related = cat_articles[:3]
    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]} in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking voor een gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI {topic["category"]} tools beschikbaar?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Sommige tools zoals Snyk en RankMath hebben gratis versies met voldoende functionaliteit om te beginnen. Bekijk de prijsrange per tool in de vergelijking hierboven."',
        f'  - q: "Hoe kies ik de juiste AI {topic["category"]} tool?"',
        f'    a: "Bepaal eerst je primaire use case, budget en teamgrootte. Kijk dan naar de beste-voor kolom in de vergelijkingstabel. Start met een gratis proefperiode van 2-3 tools voordat je een keuze maakt."',
    ]
    return f"""---
title: '{topic["title"]}'
slug: {topic["slug"]}
description: {topic["description"]}
category: {topic["category"]}
rating: 4.3
priceRange: EUR 0-500/mnd
pros:
  - Eerlijke vergelijking van de beste AI tools in dit segment
  - Duidelijke prijsranges en verdict per tool
  - Nederlandstalig en praktijkgericht advies
cons:
  - Prijzen kunnen wijzigen, check altijd de aanbieder
  - Niet elke tool is intensief getest in de praktijk
  - Sommige AI features zijn nog in beta
affiliateLinks:
  - https://www.beehiiv.com/
date: 2026-06-02
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

    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(TOPICS)}] {topic['slug']} — EXISTS, skipping")
            generated += 1
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['slug']} ({topic['category']})")
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None:
            print(f"  FAILED — using fallback content")
            failed += 1
            raw_text = f"""## Introductie

AI verandert de {topic['category']}-sector razendsnel. Dit artikel vergelijkt de beste AI tools voor {topic['category']} in 2026. Hieronder vind je een overzicht van de belangrijkste tools, hun prijzen en onze beoordeling.

## De tools vergeleken

We hebben {len(topic['tools'])} toonaangevende AI tools bekeken en beoordeeld op functionaliteit, prijs en gebruiksgemak.

| Tool | Beste voor | AI Feature | Prijs | Score |
|------|-----------|-----------|-------|-------|
"""
            for t in topic["tools"]:
                raw_text += f"""| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |
"""
            raw_text += f"""
## Conclusie

De beste AI tool voor {topic['category']} hangt af van je specifieke situatie. Voor de meeste gebruikers is {topic['tools'][0][0]} een uitstekende keuze.

## Veelgestelde vragen

**Wat kost een goede AI tool voor {topic['category']}?**
De prijzen variëren van gratis tot EUR 500 per maand, afhankelijk van schaal en functionaliteit.

**Zijn deze tools geschikt voor Nederlandse gebruikers?**
Ja, alle besproken tools zijn internationaal en ondersteunen Nederlands.

**Kan ik meerdere tools combineren?**
Ja, veel tools integreren via API. Een combinatie dekt vaak meer use cases.
"""

        fm = build_frontmatter(topic, raw_text)
        full_content = fm + "\n" + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        generated += 1
        print(f"  ✓ Written ({len(full_content)} chars)")
        time.sleep(3)  # rate limiting

    print(f"\n=== Done! Generated: {generated}, Failed: {failed} ===")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())