#!/usr/bin/env python3
"""
Generate 2 gap-filling AI tools comparison articles via Gemini API.
Finance/accounting + education — zero coverage, deferred from June 4 runs.
"""
import json
import os
import sys
import time
import subprocess
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = SITE_ROOT / "src" / "content" / "articles"

API_KEY_FILE = os.path.expanduser("~/.hermes/private/gemini-api-key")
try:
    GEMINI_API_KEY = open(API_KEY_FILE).read().strip()
except Exception as e:
    print(f"ERROR: Cannot read API key: {e}", file=sys.stderr)
    sys.exit(1)

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

today = date.today().isoformat()

TOPICS = [
    {
        "slug": "beste-ai-tools-finance-accounting-nederland-2026",
        "category": "business",
        "title_prefix": "Beste AI Tools voor Finance en Accounting in Nederland 2026",
        "featured": "Vic.ai",
        "tools": [
            {"name": "Vic.ai", "price": "EUR 20-50 per 1000 facturen", "best_for": "Autonome factuurverwerking zonder menselijke tussenkomst", "rating": 4.7, "verdict": "Beste voor bedrijven die factuurverwerking volledig willen automatiseren — leert van correcties en wordt slimmer"},
            {"name": "Pandle (Nederlands)", "price": "EUR 15-30/mnd", "best_for": "Nederlandse ZZP-boekhouding met AI", "rating": 4.3, "verdict": "Beste Nederlandse AI-boekhoudtool voor ZZP'ers en kleine ondernemers — BTW-aangifte en inkomstenbelasting inbegrepen"},
            {"name": "Moneybird (Nederlands)", "price": "EUR 28-55/mnd", "best_for": "Nederlandse MKB-facturatie en boekhouding", "rating": 4.4, "verdict": "Meest complete Nederlandse boekhoudoplossing met AI-suggesties voor categorisatie en slimme factuurherkenning"},
            {"name": "Exact Online (Nederlands)", "price": "EUR 40-120/mnd", "best_for": "MKB ERP met AI-gestuurde financiële rapportage", "rating": 4.5, "verdict": "Nederlandse grootmacht in business software — AI voorspelt cashflow en detecteert afwijkingen in real-time"},
            {"name": "Yuki (Nederlands, Visma)", "price": "EUR 30-90/mnd", "best_for": "Zelflerende robotboekhouder voor administratiekantoren", "rating": 4.2, "verdict": "Beste voor administratiekantoren die cliëntboekhouding willen automatiseren met AI-documentherkenning"},
            {"name": "Invoice2go (Bill.com)", "price": "EUR 5-30/mnd", "best_for": "ZZP-facturatie met AI-sjablonen", "rating": 4.0, "verdict": "Simpelste tool voor ZZP'ers die snel professionele offertes en facturen willen sturen met AI-assistentie"},
            {"name": "Twinfield (Wolters Kluwer, Nederlands)", "price": "EUR 35-85/mnd", "best_for": "MKB online boekhouden met AI-controle en audit trails", "rating": 4.3, "verdict": "Nederlandse cloudboekhoud-grootmacht met ingebouwde AI die fouten detecteert vóór de accountant ze ziet"},
        ],
        "extra_context": "De boekhoudsector is een van de meest disruptieve domeinen voor AI in Nederland. Exact, Visma/Yuki en Wolters Kluwer domineren de Nederlandse markt en investeren allemaal zwaar in AI. Gelderse AI-startup Vic.ai haalde $52 miljoen op voor autonome factuurverwerking en claimt 90% van de facturen zonder menselijke tussenkomst te verwerken. Nederlandse boekhouders worstelen met personeelstekorten — AI-boekhouden is een antwoord op de 22% vacaturegraad in de sector (NBA, 2026). De EU AI Act raakt finance bijzonder hard vanwege risicoclassificatie van AI-beslissingen in kredietverlening en fraude-detectie. Focus: tools die Nederlandse ondernemers en accountants NU kunnen gebruiken — met NL-specifieke BTW- en IB-integratie. De 7 tools hier bestrijken het hele spectrum: van simpele ZZP-facturatie tot autonome enterprise factuurverwerking.",
        "affiliate_link": "https://vic.ai/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-onderwijs-nederland-2026",
        "category": "onderwijs",
        "title_prefix": "Beste AI Tools voor het Onderwijs in Nederland 2026",
        "featured": "LessonUp AI",
        "tools": [
            {"name": "LessonUp AI (Nederlands)", "price": "EUR 9-25/mnd", "best_for": "Nederlandse lesvoorbereiding met AI-assistentie", "rating": 4.5, "verdict": "Beste Nederlandse tool voor leraren — AI genereert interactieve lessen, quizzen en toetsen in het Nederlands"},
            {"name": "Magister Learn (Nederlands)", "price": "EUR 5-15/leerling/jaar", "best_for": "Nederlandse leerlingvolgsysteem met AI-analyses", "rating": 4.3, "verdict": "Standaard in 85% van Nederlandse scholen — AI voorspelt studie-uitval en geeft docenten vroegsignalen"},
            {"name": "Snappet AI (Nederlands)", "price": "EUR 12-25/leerling/jaar", "best_for": "Adaptief Nederlands basisonderwijs op tablets", "rating": 4.4, "verdict": "Nederlands marktleider in adaptief leren — AI past opgaven per kind aan op basis van 100+ miljoen data-analyses"},
            {"name": "Khan Academy AI (Khanmigo)", "price": "EUR 9/student/jaar", "best_for": "AI-tutor voor wiskunde, taal en science in het Nederlands", "rating": 4.6, "verdict": "Beste AI-tutor met Nederlandse ondersteuning — beantwoordt vragen als een persoonlijke bijlesdocent, niet als antwoordenboek"},
            {"name": "FeedbackFruits AI", "price": "EUR 5-15/student/jaar", "best_for": "AI-feedback op schrijfopdrachten in hoger onderwijs", "rating": 4.5, "verdict": "Nederlands-Amsterdamse scale-up — AI geeft studenten direct feedback op academisch schrijven, peer review en samenwerking"},
            {"name": "Quillbot voor Nederlands", "price": "EUR 5-20/mnd", "best_for": "AI-schrijfassistent voor NT2 en taalonderwijs", "rating": 4.2, "verdict": "Beste parafraseer- en grammaticatool met Nederlandse ondersteuning — ideaal voor NT2-studenten en schrijfonderwijs"},
            {"name": "SOMtoday AI (Nederlands)", "price": "EUR 3-10/leerling/jaar", "best_for": "Nederlands voortgezet onderwijs administratie + AI-inzichten", "rating": 4.1, "verdict": "Op een na grootste Nederlandse leerlingvolgsysteem — AI helpt mentoren bij risicosignalering en trendanalyses"},
        ],
        "extra_context": "De Nederlandse onderwijssector staat op een kantelpunt met AI. Surf (ICT-coöperatie onderwijs) investeert tientallen miljoenen in AI-infrastructuur voor universiteiten en hogescholen. Het Nationaal Onderwijslab AI (NOLAI) is in 2022 opgericht met €80 miljoen voor verantwoorde AI in het onderwijs. GPT-NL gaat expliciet over onderwijs als usecase. Uitdaging: 58% van docenten voelt zich niet voldoende toegerust om AI in de klas te gebruiken (Kennisnet, 2025). Nederlandse scholen worstelen met privacy (AVG) — EU AI Act classificeert onderwijs-AI als 'hoog risico' voor leerlingbeoordeling. De markt is sterk Nederlands met LessonUp, Snappet, Magister, SOMtoday en FeedbackFruits die allemaal Nederlandse roots hebben. Focus: tools voor po, vo, mbo, hbo en wo — van adaptief basisonderwijs tot academische peer review.",
        "affiliate_link": "https://lessonup.com/nl/?ref=aitoolsnl",
    },
]


def generate_article(topic, retries=3):
    prompt = f"""Je bent een Nederlandse techjournalist die objectieve, diepgaande vergelijkingsartikelen schrijft voor een Nederlandstalige AI-tools vergelijkingssite. Je schrijft vanuit kennis van de Nederlandse markt — inclusief prijzen in euro's, relevantie voor Nederlandse gebruikers, en Europese context.

Schrijf een compleet vergelijkingsartikel in het Nederlands over dit onderwerp:

TITEL: {topic['title_prefix']}
CATEGORIE: {topic['category']}
UITGELICHT PRODUCT: {topic['featured']}

VERGELIJK DEZE TOOLS (7 tools, deze volgorde aanhouden):
"""
    for i, t in enumerate(topic['tools']):
        prompt += f"\n{i+1}. {t['name']} — Prijs: {t['price']} — Beste voor: {t['best_for']} — Rating: {t['rating']}/5 — Oordeel: {t['verdict']}"

    prompt += f"""

EXTRA CONTEXT (verwerk in het artikel):
{topic['extra_context']}

STRUCTUUR VAN HET ARTIKEL:
- Begin met een pakkende introductie (2-3 alinea's) die de urgentie of relevantie van dit onderwerp voor Nederlandse gebruikers schetst
- Gebruik daarna een genummerde lijst (1 t/m 7) waarin je elke tool in detail bespreekt: wat het is, voor wie, plus- en minpunten, en de prijs in euro's
- Sluit af met een 'Welke AI-tool past bij jou?' sectie die gebruikers helpt kiezen op basis van hun situatie (budget, teamgrootte, usecase)
- Voeg een conclusie toe over de algemene richting van deze tools in 2026

FORMAT: Schrijf in vloeiend, toegankelijk Nederlands. Gebruik tussenkopjes. Wees kritisch en eerlijk — niet elke tool is voor iedereen. Gebruik actuele 2026-informatie. Vermeld prijzen in euro's. Minimum 1500 woorden.

Schrijf nu het volledige artikel:"""

    for attempt in range(retries):
        try:
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 8192,
                    "topP": 0.95,
                }
            })

            cmd = [
                "curl", "-s", "--max-time", "180",
                "-H", "Content-Type: application/json",
                "-d", payload,
                GEMINI_URL
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=190)
            if result.returncode != 0:
                print(f"  curl error: {result.stderr}", file=sys.stderr)
                time.sleep(2)
                continue

            data = json.loads(result.stdout)

            if "error" in data:
                print(f"  API error: {data['error'].get('message', str(data['error']))}", file=sys.stderr)
                if attempt < retries - 1:
                    time.sleep(3)
                continue

            candidates = data.get("candidates", [])
            if not candidates:
                print(f"  No candidates in response", file=sys.stderr)
                time.sleep(2)
                continue

            text = candidates[0]["content"]["parts"][0]["text"]
            if not text or len(text) < 500:
                print(f"  Response too short ({len(text)} chars)", file=sys.stderr)
                time.sleep(2)
                continue

            return text

        except Exception as e:
            print(f"  Exception attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(3)

    return None


def build_frontmatter(topic):
    pros = [
        "Diepgaande Nederlandse marktanalyse",
        "Actuele prijzen en beschikbaarheid in 2026",
        "Eerlijke vergelijking met alternatieven"
    ]
    cons = [
        "Prijzen en functies veranderen snel",
        "Gebaseerd op specificaties, niet op fysieke tests"
    ]

    tools_data = topic['tools']

    fm = f"""---
title: '{topic["title_prefix"]} — volledige vergelijking'
slug: {topic["slug"]}
description: 'Vergelijking van de {topic["title_prefix"].lower()} voor Nederlandse gebruikers. Objectieve beoordeling met prijzen in euro's en praktische keuzehulp.'
category: {topic["category"]}
rating: {sum(t["rating"] for t in tools_data) / len(tools_data):.1f}
priceRange: EUR 0-200/maand
pros:
"""
    for p in pros:
        fm += f"- {p}\n"
    fm += "cons:\n"
    for c in cons:
        fm += f"- {c}\n"

    fm += "affiliateLinks:\n"
    fm += f"  - {topic['affiliate_link']}\n"
    fm += f"date: '{today}'\n"
    fm += "modelYear: 2026\n"
    fm += f"featuredTool: {topic['featured'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-')}\n"
    fm += "readingTime: 9 min\n"
    fm += "tools:\n"

    for t in tools_data:
        fm += f"- name: {t['name']}\n"
        fm += f"  verdict: {t['verdict']}\n"
        fm += f"  priceRange: {t['price']}\n"
        fm += f"  bestFor: {t['best_for']}\n"
        fm += f"  rating: {t['rating']}\n"
        fm += f"  affiliateLink: {topic['affiliate_link']}\n"

    fm += "related:\n"
    fm += "  - ai-trends-2026-nederland\n"
    fm += "  - nederlandse-ai-adoptie-cijfers-2026\n"
    fm += "  - ai-avg-compliance-tools-2026\n"
    fm += "---\n\n"

    return fm


def main():
    for topic in TOPICS:
        slug = topic['slug']
        out_path = ARTICLES_DIR / f"{slug}.md"

        if out_path.exists():
            print(f"SKIP: {slug} already exists")
            continue

        print(f"Generating: {slug}...")
        body = generate_article(topic)

        if not body:
            print(f"FAILED: {slug} after retries", file=sys.stderr)
            continue

        frontmatter = build_frontmatter(topic)
        full_article = frontmatter + body

        out_path.write_text(full_article, encoding='utf-8')
        print(f"  Wrote: {out_path} ({len(full_article)} chars)")
        time.sleep(2)  # rate limit

    print("\nDone.")


if __name__ == "__main__":
    main()
