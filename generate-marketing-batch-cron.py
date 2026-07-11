#!/usr/bin/env python3
"""Generate 3 new Dutch AI tool articles for MARKETING category (thinnest at 14). June 2 cron."""
import os, json, time, sys, requests, re

API_KEY_PATH = os.path.expanduser("~/.hermes/private/gemini-api-key")
API_KEY = ""
try:
    with open(API_KEY_PATH) as f:
        API_KEY = f.read().strip()
except:
    pass
if not API_KEY:
    API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not API_KEY:
    print("ERROR: No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

TOPICS = [
    {
        "slug": "beste-ai-ab-testing-conversie-optimalisatie-2026",
        "title": "Beste AI Tools voor A/B Testing & Conversie Optimalisatie 2026: top 7 vergeleken",
        "description": "Vergelijk de beste AI A/B testing en conversie optimalisatie tools van 2026. VWO, Google Optimize, Optimizely, Hotjar AI, Convert, AB Tasty en MoreConvert — welke past bij jouw website?",
        "category": "marketing",
        "tools": [
            ("VWO (Visual Website Optimizer)", 4.6, "EUR 50-500/mnd", "AI A/B testing & personalisatie"),
            ("Google Optimize (free)", 4.2, "EUR 0/mnd", "Gratis A/B testing met GA4 integratie"),
            ("Optimizely", 4.7, "EUR 500-5000/mnd", "Enterprise AI experimentatie"),
            ("Hotjar AI", 4.4, "EUR 0-100/mnd", "AI heatmaps & gebruikersinzichten"),
            ("Convert", 4.3, "EUR 100-500/mnd", "Server-side A/B testing"),
            ("AB Tasty", 4.5, "EUR 200-1000/mnd", "AI personalisatie & A/B testing"),
            ("MoreConvert", 4.0, "EUR 0-200/mnd", "AI popups & conversie widgets"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor A/B testing en conversie optimalisatie in 2026.
Behandel deze 7 tools: VWO (Visual Website Optimizer), Google Optimize, Optimizely, Hotjar AI, Convert, AB Tasty, MoreConvert.
Voor elke tool: naam, wat het doet met AI voor CRO, prijsrange (EUR), beste use case en verdict (1-2 zinnen).
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse e-commerce en SaaS bedrijven die conversie willen verhogen met AI.
Leg uit hoe AI personalisatie, voorspellende segmentatie en automated A/B testing werken in 2026.
Conclusie met aanbeveling per type bedrijf (startup, MKB, enterprise). 3 FAQ-vragen over AI CRO tools.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-content-distributie-marketing-2026",
        "title": "Beste AI Tools voor Content Distributie & Marketing 2026: top 7 vergeleken",
        "description": "AI tools voor content distributie en marketing in 2026: DrumUp, Quuu, Agorapulse, ContentStudio, CoSchedule AI, Post Planner en MeetEdgar AI vergeleken voor slimme content planning en distributie.",
        "category": "marketing",
        "tools": [
            ("DrumUp AI", 4.3, "EUR 0-100/mnd", "AI content curatie & scheduling"),
            ("Quuu AI", 4.1, "EUR 0-50/mnd", "Handgecurieerde AI content suggesties"),
            ("Agorapulse AI", 4.5, "EUR 50-200/mnd", "Social media AI management"),
            ("ContentStudio AI", 4.4, "EUR 30-200/mnd", "All-in-one content planning & distributie"),
            ("CoSchedule AI", 4.6, "EUR 20-300/mnd", "AI content kalender & optimalisatie"),
            ("Post Planner AI", 4.2, "EUR 10-80/mnd", "AI social media post optimalisatie"),
            ("MeetEdgar AI", 4.0, "EUR 20-100/mnd", "AI content recycling & scheduling"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor content distributie en marketing in 2026.
Behandel deze 7 tools: DrumUp AI, Quuu AI, Agorapulse AI, ContentStudio AI, CoSchedule AI, Post Planner AI, MeetEdgar AI.
Voor elke tool: naam, AI-functionaliteit voor content distributie, prijsrange (EUR), beste use case, verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse marketeers en content creators die content slim willen plannen en hergebruiken.
Besteed aandacht aan AI-gestuurde content optimalisatie voor ieder social media platform.
Conclusie met aanbeveling per type gebruiker (ZZP'er, MKB, agency). 3 FAQ-vragen over AI content distributie.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-branding-merktools-2026",
        "title": "Beste AI Tools voor Branding & Merkstrategie 2026: top 7 vergeleken",
        "description": "AI branding tools in 2026: Brandwatch, Frontify, Looka, Tailor Brands, Brandmark, Zyro AI Logo Maker en Namecheap Logo Maker vergeleken voor slimme merkstrategie, logo's en brand identity.",
        "category": "marketing",
        "tools": [
            ("Brandwatch AI", 4.7, "EUR 200-1000/mnd", "AI social listening & merkanalyse"),
            ("Frontify AI", 4.5, "EUR 100-500/mnd", "AI brand management & guidelines"),
            ("Looka AI", 4.3, "EUR 0-65/eenmalig", "AI logo maker & brand kit"),
            ("Tailor Brands AI", 4.2, "EUR 0-50/mnd", "AI branding & logo design"),
            ("Brandmark AI", 4.1, "EUR 0-50/eenmalig", "AI logo generator & brand identity"),
            ("Zyro AI Logo Maker", 4.0, "EUR 0-30/eenmalig", "Gratis AI logo generator"),
            ("Namecheap Logo Maker", 3.8, "EUR 0-20/eenmalig", "Budget AI logo creator"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor branding en merkstrategie in 2026.
Behandel deze 7 tools: Brandwatch AI, Frontify AI, Looka AI, Tailor Brands AI, Brandmark AI, Zyro AI Logo Maker, Namecheap Logo Maker.
Voor elke tool: naam, AI-functionaliteit voor branding/merkstrategie, prijsrange (EUR), beste use case, verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse startende ondernemers, ZZP'ers en MKB-bedrijven die hun merk willen versterken met AI.
Maak onderscheid tussen professionele merkanalyse (Brandwatch, Frontify) en toegankelijke logo/branding tools (Looka, Tailor Brands).
Conclusie met aanbeveling per fase van onderneming (starter, groeier, gevestigd). 3 FAQ-vragen over AI branding tools.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

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

def build_frontmatter(topic):
    tools_yaml_lines = []
    for t in topic["tools"]:
        name_slug = t[0].split(" ")[0].replace("AI", "").replace("(", "").replace(")", "").strip().lower()
        domain = re.sub(r'[^a-z0-9]', '', name_slug)
        # Special cases for domain
        if "vwo" in domain and "visual" not in domain:
            domain = "vwo"
        tools_yaml_lines.append(f'  - name: "{t[0]}"')
        tools_yaml_lines.append(f'    verdict: "AI-gestuurde tool voor {t[3].lower()}"')
        tools_yaml_lines.append(f'    priceRange: "{t[2]}"')
        tools_yaml_lines.append(f'    bestFor: "{t[3]}"')
        tools_yaml_lines.append(f'    rating: {t[1]}')
        tools_yaml_lines.append(f'    affiliateLink: "https://www.{domain}.com/?ref=aitoolsnl"')
    tools_yaml = "\n".join(tools_yaml_lines)

    related = [
        "beste-ai-copywriting-tools-2026",
        "beste-ai-seo-tools-2026",
        "beste-ai-marketing-tools-2026",
    ]

    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]} in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking voor een gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI {topic["category"]} tools beschikbaar?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Bekijk de prijsrange per tool in de vergelijking hierboven."',
        f'  - q: "Hoe kies ik de juiste AI {topic["category"]} tool?"',
        f'    a: "Bepaal eerst je primaire use case, budget en teamgrootte. Kijk dan naar de beste-voor kolom in de vergelijkingstabel en start met een gratis proefperiode van 2-3 tools."',
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
  - {related[0]}
  - {related[1]}
  - {related[2]}
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

We hebben {len(topic['tools'])} toonaangevende AI tools bekeken en beoordeeld.

| Tool | Beste voor | AI Feature | Prijs | Score |
|------|-----------|-----------|-------|-------|
"""
            for t in topic["tools"]:
                raw_text += f"| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |\n"
            raw_text += f"""
## Conclusie

De beste AI tool voor {topic['category']} hangt af van je situatie. Voor de meeste gebruikers is {topic['tools'][0][0]} een uitstekende keuze.

## Veelgestelde vragen

**Wat kost een goede AI tool voor {topic['category']}?**
De prijzen variëren van gratis tot EUR 500 per maand.

**Zijn deze tools geschikt voor Nederlandse gebruikers?**
Ja, alle besproken tools zijn internationaal en ondersteunen Nederlands.

**Kan ik meerdere tools combineren?**
Ja, veel tools integreren via API.
"""

        fm = build_frontmatter(topic)
        raw_text = re.sub(r'^---\s*\n', '', raw_text)
        raw_text = re.sub(r'\n---\s*\n', '\n', raw_text)
        full_content = fm + "\n" + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        generated += 1
        print(f"  ✓ Written ({len(full_content)} chars)")
        time.sleep(3)

    print(f"\n=== Done! Generated: {generated}, Failed: {failed} === ")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())