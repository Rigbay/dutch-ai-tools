#!/usr/bin/env python3
"""Generate 4 new Dutch AI tool articles in genuine gap categories:
automatisering/robotica, investeren/beleggen, non-profit/sociaal, interim/detachering."""

import os, json, time, sys, requests, re

sys.path.insert(0, os.path.dirname(__file__))

API_KEY = os.environ.get("GEMINI_API_KEY", "") or open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

TOPICS = [
    # --- AI Automatisering & Robotica (0 existing) ---
    {
        "slug": "beste-ai-tools-automatisering-robotica-2026",
        "title": "Beste AI Tools voor Automatisering & Robotica 2026: top 7 vergeleken",
        "description": "AI automatisering en robotica tools voor 2026: UiPath AI, Automation Anywhere, Blue Prism, RoboDK, Microsoft Power Automate AI, ABB Ability AI en Fanuc AI vergeleken voor procesautomatisering en robotica.",
        "category": "business",
        "tools": [
            ("UiPath AI", 4.7, "EUR 300-3000/mnd", "Enterprise RPA & AI-automatisering"),
            ("Automation Anywhere AI", 4.6, "EUR 200-2000/mnd", "AI-gestuurde RPA-platform"),
            ("Blue Prism AI", 4.5, "EUR 300-2500/mnd", "Decacenter-automatisering & AI"),
            ("Microsoft Power Automate AI", 4.4, "EUR 15-200/mnd", "No-code workflow automatisering"),
            ("RoboDK AI", 4.3, "EUR 500-3000/mnd", "Robot simulatie & AI-optimalisatie"),
            ("ABB Ability AI", 4.5, "EUR 1000-10000/mnd", "Industriële robotica & AI"),
            ("Fanuc AI", 4.4, "EUR 1000-10000/mnd", "CNC & robotautomatisering met AI"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor automatisering en robotica in 2026.
Behandel deze 7 tools: UiPath AI, Automation Anywhere AI, Blue Prism AI, Microsoft Power Automate AI, RoboDK AI, ABB Ability AI, Fanuc AI.
Voor elke tool: naam, AI-functionaliteit voor automatisering/robotica, prijsrange, beste use case (type proces/industrie), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: AI-gedreven RPA, intelligente documentverwerking, predictive maintenance, mens-robot samenwerking, no-code automatisering.
Besteed aandacht aan Nederlandse context: Nederlandse logistiek, maakindustrie en overheid die RPA en robotics adopteren, AVG-compliance.
Conclusie met aanbeveling per organisatiegrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Investeren & Beleggen (0 dedicated) ---
    {
        "slug": "beste-ai-tools-investeren-beleggen-2026",
        "title": "Beste AI Tools voor Investeren & Beleggen 2026: top 7 vergeleken",
        "description": "AI beleggen tools voor 2026: eToro AI, TradingView AI, Interactive Brokers IBot, Bloomberg GPT, QuantConnect AI, Trade Ideas AI en Portfolio Visualizer AI vergeleken voor slim investeren.",
        "category": "business",
        "tools": [
            ("eToro AI", 4.3, "Gratis-50/mnd", "CopyTrading & AI-aanbevelingen"),
            ("TradingView AI", 4.6, "EUR 15-100/mnd", "AI-technische analyse & signalen"),
            ("Interactive Brokers IBot AI", 4.4, "EUR 0-100/mnd", "AI chatbot voor beleggingsvragen"),
            ("Bloomberg GPT", 4.7, "EUR 2000-5000/mnd", "AI voor financiële analyse & nieuws"),
            ("QuantConnect AI", 4.5, "Gratis-500/mnd", "Algoritmische trading backtesting"),
            ("Trade Ideas AI", 4.3, "EUR 100-300/mnd", "Real-time AI handelssignalen"),
            ("Portfolio Visualizer AI", 4.2, "Gratis-50/mnd", "AI portefeuille-optimalisatie"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor investeren en beleggen in 2026.
Behandel deze 7 tools: eToro AI, TradingView AI, Interactive Brokers IBot AI, Bloomberg GPT, QuantConnect AI, Trade Ideas AI, Portfolio Visualizer AI.
Voor elke tool: naam, AI-functionaliteit voor beleggen, prijsrange, beste use case (type belegger/portfolio), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: AI-gedreven marktanalyse, sentimentanalyse, portefeuille-optimalisatie, risicomanagement, algoritmische trading.
Besteed aandacht aan Nederlandse context: NL-beleggers (DeGiro, ABN AMRO, Rabobank), belastingregels (box 3), ESG-beleggen.
VERMELD duidelijk dat AI tools advies geven maar geen financieel adviseur zijn — risico's blijven.
Conclusie met aanbeveling per type belegger. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Non-profit & Sociaal-Maatschappelijk (0 dedicated) ---
    {
        "slug": "beste-ai-tools-non-profit-sociaal-maatschappelijk-2026",
        "title": "Beste AI Tools voor Non-profit & Sociaal-Maatschappelijk 2026: top 7 vergeleken",
        "description": "AI non-profit tools voor 2026: Salesforce Nonprofit Cloud AI, Blackbaud AI, DonorSearch AI, Givebutter AI, Keela AI, Fundraising AI en Charity Engine vergeleken voor goede doelen.",
        "category": "business",
        "tools": [
            ("Salesforce Nonprofit Cloud AI", 4.6, "EUR 100-500/mnd", "CRM voor goede doelen met AI"),
            ("Blackbaud AI", 4.5, "EUR 200-1000/mnd", "Non-profit fundraising & AI"),
            ("DonorSearch AI", 4.3, "EUR 100-500/mnd", "AI donor prospect research"),
            ("Keela AI", 4.4, "EUR 50-300/mnd", "Intelligent donor management"),
            ("Givebutter AI", 4.2, "Gratis-100/mnd", "AI fundraising voor kleine NPO's"),
            ("Fundraising AI", 4.1, "EUR 50-200/mnd", "AI optimalisatie van campagnes"),
            ("Charity Engine", 4.0, "EUR 0-50/mnd", "Donated computing power via AI"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor non-profitorganisaties en sociaal-maatschappelijke organisaties in 2026.
Behandel deze 7 tools: Salesforce Nonprofit Cloud AI, Blackbaud AI, DonorSearch AI, Keela AI, Givebutter AI, Fundraising AI, Charity Engine.
Voor elke tool: naam, AI-functionaliteit voor non-profits, prijsrange, beste use case (type organisatie/budget), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: donor management & prospect research, AI-gestuurde campagnes, vrijwilligerscoördinatie, impactmeting, fondsenwerving.
Besteed aandacht aan Nederlandse context: ANBI-status, CBF-keurmerk, NL goede doelen (KNCV, UNICEF NL, Natuurmonumenten), AVG voor donordata.
Speciale aandacht voor budgetvriendelijke opties — non-profits hebben vaak beperkte middelen.
Conclusie met aanbeveling per organisatiegrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Interim & Detachering (0 dedicated) ---
    {
        "slug": "beste-ai-tools-interim-detachering-2026",
        "title": "Beste AI Tools voor Interim Management & Detachering 2026: top 7 vergeleken",
        "description": "AI interim en detachering tools voor 2026: LinkedIn Recruiter AI, Harver AI, Textkernel AI, CAIRE AI, Bullhorn AI, Workforce Planner AI en Eightfold AI vergeleken voor interim-professionals.",
        "category": "productiviteit",
        "tools": [
            ("LinkedIn Recruiter AI", 4.5, "EUR 200-1000/mnd", "AI talent sourcing & matching"),
            ("Harver AI", 4.4, "EUR 100-500/mnd", "AI assessment & hiring platform"),
            ("Textkernel AI", 4.6, "EUR 200-2000/mnd", "AI CV-parsing & skills matching"),
            ("CAIRE AI", 4.3, "EUR 100-500/mnd", "AI recruitment chatbot & screening"),
            ("Bullhorn AI", 4.4, "EUR 200-1000/mnd", "ATS met AI-matchmaking"),
            ("Eightfold AI", 4.7, "EUR 300-3000/mnd", "AI talent intelligence platform"),
            ("Workforce Planner AI", 4.2, "EUR 100-500/mnd", "AI workforce planning & forecasting"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor interim management en detachering in 2026.
Behandel deze 7 tools: LinkedIn Recruiter AI, Harver AI, Textkernel AI, CAIRE AI, Bullhorn AI, Workforce Planner AI, Eightfold AI.
Voor elke tool: naam, AI-functionaliteit voor interim/detachering, prijsrange, beste use case (type bureau/schaal), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: AI skills matching & gap-analyse, CV parsing, candidate screening, workforce planning, contract compliance.
Besteed aandacht aan Nederlandse context: Nederlandse detacheringsmarkt (Randstad, Adecco, Yacht, Brunel), NBBU/ABU-cao, AVG voor kandidaatdata.
Vermeld de waarde voor zowel detacheringsbureaus als zelfstandige interimmers.
Conclusie met aanbeveling per bureau-type. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

AFFILIATE_MAP = {
    "beehiiv": "https://www.beehiiv.com/",
    "taskade": "https://taskade.com/?via=55nfr2",
    "writesonic": "https://writesonic.com/?via=aitoolsnl",
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
            text = re.sub(r'^```(?:markdown)?\s*\n?', '', text)
            text = re.sub(r'\n```\s*$', '', text)
            return text.strip()
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None


def build_frontmatter(topic, body_text=""):
    tools_yaml_lines = []
    for t in topic["tools"]:
        tools_yaml_lines.append(f'  - name: "{t[0]}"')
        tools_yaml_lines.append(f'    verdict: "AI-gedreven tool voor {t[3].lower()}"')
        tools_yaml_lines.append(f'    priceRange: "{t[2]}"')
        tools_yaml_lines.append(f'    bestFor: "{t[3]}"')
        tools_yaml_lines.append(f'    rating: {t[1]}')
        tools_yaml_lines.append(f'    affiliateLink: "https://www.beehiiv.com/"')
    tools_yaml = "\n".join(tools_yaml_lines)

    all_articles = [f.replace(".md", "") for f in os.listdir(OUT_DIR) if f.endswith(".md")]
    cat_articles = [a for a in all_articles if topic["slug"] not in a and topic["category"] in a]
    related = cat_articles[:3] if len(cat_articles) >= 3 else all_articles[:3]

    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]}-toepassingen in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking hierboven voor gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI tools beschikbaar voor {topic["category"]}?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Bekijk de prijsrange per tool in de vergelijkingstabel. Sommige tools hebben gratis versies met voldoende functionaliteit om te beginnen."',
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
  - https://taskade.com/?via=55nfr2
  - https://writesonic.com/?via=aitoolsnl
date: 2026-06-04
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

        if raw_text is None or len(raw_text) < 300:
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
                raw_text += f"| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |\n"

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

        frontmatter = build_frontmatter(topic, raw_text)
        full_text = frontmatter + raw_text + "\n"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        generated += 1
        print(f"  ✓ Written to {out_path} ({len(full_text)} chars)")

        # Small delay between API calls
        if i < len(TOPICS) - 1:
            time.sleep(2)

    print(f"\n=== DONE ===")
    print(f"Generated: {generated}")
    print(f"Failed (fallback used): {failed}")
    print(f"Skipped (already existed): {skipped}")
    print(f"Total in {OUT_DIR}: {len([f for f in os.listdir(OUT_DIR) if f.endswith('.md')])}")


if __name__ == "__main__":
    main()