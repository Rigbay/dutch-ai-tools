#!/usr/bin/env python3
"""
Generate 3 gap-filling AI tools comparison articles via Gemini API.
GPT-NL (near-zero coverage), AI Agents voor bedrijven, Gemini 3.5 launch.
"""
import json
import os
import sys
import time
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
        "slug": "gpt-nl-nederlands-taalmodel-2026",
        "category": "technologie",
        "title_prefix": "GPT-NL: Het Nederlandse AI-Taalmodel 2026",
        "featured": "GPT-NL",
        "tools": [
            {"name": "GPT-NL (TNO/SURF/NFI)", "price": "EUR 0 (publiek, licentie vanaf H2 2026)", "best_for": "Nederlandse overheid, zorg, onderwijs, forensisch onderzoek", "rating": 4.3, "verdict": "Enige AVG/GDPR-compliant Nederlands taalmodel — essentieel voor publieke sector en privacy-gevoelige data"},
            {"name": "GPT-4o (OpenAI)", "price": "EUR 20-200/mnd", "best_for": "Algemene AI-assistentie & content productie", "rating": 4.7, "verdict": "Beste allround voor Nederlands en Engels met sterke meertalige prestaties"},
            {"name": "Claude 4.5 (Anthropic)", "price": "EUR 20-200/mnd", "best_for": "Veilige, ethische AI met lange contextvensters", "rating": 4.6, "verdict": "Beste voor lange documentanalyse en veiligheidskritische toepassingen"},
            {"name": "Gemini 3.5 (Google)", "price": "EUR 23-230/mnd", "best_for": "Multimodale AI met Google-integratie", "rating": 4.7, "verdict": "Krachtigste multimodale model met directe integratie in Google Workspace"},
            {"name": "Llama 4 (Meta, open source)", "price": "Gratis (zelf hosten)", "best_for": "Open-source AI met zelf-host optie", "rating": 4.2, "verdict": "Beste open-source alternatief voor bedrijven die niet afhankelijk willen zijn van Big Tech"},
            {"name": "Mistral Large 3", "price": "EUR 2-10 per 1M tokens", "best_for": "Europees AI-alternatief met API-toegang", "rating": 4.4, "verdict": "Sterkste Europese commerciële LLM met focus op meertaligheid en privacy"},
            {"name": "DeepSeek V3", "price": "Gratis-15/mnd", "best_for": "Budget-vriendelijke AI met sterke codeervaardigheden", "rating": 4.3, "verdict": "Meest kostenefficiënte frontier-model met sterke prestaties in coderen en redeneren"},
        ],
        "extra_context": "GPT-NL is een Nederlands taalmodel ontwikkeld door TNO, SURF en het Nederlands Forensisch Instituut met €13,5 miljoen overheidsbudget. Pre-training is afgerond (feb 2026), eerste 5 pilots lopen (o.a. gemeentelijke AI-assistent Gem met 70.000 gesprekken in 2024, HIP voor begrijpelijke overheidstaal). GPT-NL claimt wereldprimeur: betaalde licentieovereenkomst met ALLE Nederlandse nieuwsuitgevers (NDP Nieuwsmedia) voor trainingsdata. Commerciële uitrol via professionele licenties en SaaS staat gepland voor H2 2026. Het model presteert op samenvattingstaken beter dan GPT-3. Volgende generatie krijgt meertalige ondersteuning en RAG-functionaliteit. Trainingdataset wordt gepubliceerd op HuggingFace. Vergelijk GPT-NL met commerciële alternatieven voor Nederlandse gebruikers.",
        "affiliate_link": "https://gpt-nl.nl/",
    },
    {
        "slug": "beste-ai-agents-nederlandse-bedrijven-2026",
        "category": "business",
        "title_prefix": "Beste AI Agents voor Nederlandse Bedrijven 2026",
        "featured": "Manus AI",
        "tools": [
            {"name": "Manus AI", "price": "EUR 20-200/mnd", "best_for": "Autonoom onderzoek & dataconversies", "rating": 4.7, "verdict": "Meest complete autonome AI-agent voor onderzoekstaken en dataconversies zonder menselijke tussenkomst"},
            {"name": "OpenAI Operator", "price": "EUR 20-200/mnd (ChatGPT Pro)", "best_for": "MKB-procesautomatisering via browser", "rating": 4.5, "verdict": "Gebruiksvriendelijke agent die via browser zelfstandig taken uitvoert — van boeken tot formulieren invullen"},
            {"name": "Devin AI (Cognition)", "price": "EUR 500/mnd", "best_for": "Softwareontwikkeling & code-automatisering", "rating": 4.6, "verdict": "Eerste volwaardige AI-software engineer die zelfstandig code schrijft, test en deployt"},
            {"name": "Copilot Studio (Microsoft)", "price": "EUR 200-2000/mnd", "best_for": "Enterprise agent-bouwer in Microsoft-ecosysteem", "rating": 4.4, "verdict": "Beste voor bedrijven in Microsoft-omgeving die eigen AI-agents willen bouwen zonder code"},
            {"name": "CrewAI", "price": "Open source (gratis) / EUR 50-500/mnd (hosted)", "best_for": "Multi-agent workflows & teamautomatisering", "rating": 4.3, "verdict": "Krachtig open-source framework voor het bouwen van teams van AI-agents met rolverdeling"},
            {"name": "AutoGen (Microsoft Research)", "price": "Open source (gratis)", "best_for": "Multi-agent conversaties & onderzoek", "rating": 4.2, "verdict": "Beste voor developers die complexe multi-agent conversatiesystemen willen bouwen"},
            {"name": "Zapier Central AI", "price": "EUR 30-200/mnd", "best_for": "No-code automations met AI-beslissingen", "rating": 4.3, "verdict": "Meest toegankelijke AI-agent voor MKB — verbindt 7000+ apps met AI-beslissingslogica"},
        ],
        "extra_context": "AI-agents zijn de grootste AI-trend van 2026. Gartner voorspelt dat tegen 2028 minstens 15% van dagelijkse werkbeslissingen autonoom door AI-agents wordt genomen. In Nederland gebruiken twee derde van de bedrijven al AI (67% in 2026, verdubbeling t.o.v. 2023). Het verschil met chatbots: agents voeren taken zelfstandig UIT, niet alleen antwoorden. Ze plannen, gebruiken tools, en leveren resultaten. Nederland loopt voorop in EU met 67% AI-adoptie. Focus op tools die Nederlandse bedrijven kunnen inzetten voor automatisering zonder developers.",
        "affiliate_link": "https://manus.im/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-spraakherkenning-transcriptie-nederlands-2026",
        "category": "productiviteit",
        "title_prefix": "Beste AI Tools voor Spraakherkenning en Transcriptie in het Nederlands 2026",
        "featured": "Whisper (OpenAI)",
        "tools": [
            {"name": "Whisper (OpenAI)", "price": "EUR 0,006/minuut (API) / Gratis (open source)", "best_for": "Beste NL-spraakherkenning via API en offline", "rating": 4.7, "verdict": "Gouden standaard voor Nederlandse spraakherkenning — nauwkeurig, snel en open-source beschikbaar"},
            {"name": "Sonix AI", "price": "EUR 10-30/u", "best_for": "Automatische transcriptie met NL-ondersteuning", "rating": 4.5, "verdict": "Beste voor automatische transcriptie van Nederlandse vergaderingen en interviews met sprekeridentificatie"},
            {"name": "Otter.ai", "price": "Gratis-50/mnd", "best_for": "Real-time NL-vergadertranscriptie", "rating": 4.4, "verdict": "Beste voor live transcriptie in Nederlandse vergaderingen met AI-samenvattingen en actiepunten"},
            {"name": "Amberscript", "price": "EUR 10-20/u", "best_for": "Nederlandse ondertiteling & AV-compliance", "rating": 4.3, "verdict": "Nederlands bedrijf gespecialiseerd in NL-spraakherkenning voor media en ondertiteling"},
            {"name": "Fireflies.ai", "price": "Gratis-19/mnd", "best_for": "NL-vergadernotulen & actiepunten", "rating": 4.2, "verdict": "Beste voor automatische notulen in Nederlandse meetings met geïntegreerde takenlijst"},
            {"name": "Trint AI", "price": "EUR 60-75/mnd", "best_for": "Journalistieke transcriptie met NL", "rating": 4.1, "verdict": "Sterk voor journalistieke transcriptie met Nederlandse taalondersteuning en editor"},
            {"name": "Descript AI", "price": "EUR 24-84/mnd", "best_for": "Video-transcriptie + editing in één", "rating": 4.6, "verdict": "Unieke combinatie van AI-transcriptie en videobewerking — bewerk video als een Word-document"},
        ],
        "extra_context": "Nederlandse spraakherkenning is de afgelopen twee jaar enorm verbeterd. OpenAI Whisper heeft Nederlandse spraakherkenning getransformeerd met near-human accuracy. De markt voor spraak-naar-tekst groeit met 23% per jaar. Belangrijkste usecases in Nederland: vergadernotulen, journalistieke interviews, ondertiteling (AVG-compliance), en academisch onderzoek. Whisper is gratis en open-source — je kunt het lokaal draaien zonder data naar de cloud te sturen. Amberscript is het enige Nederlandse bedrijf in deze categorie.",
        "affiliate_link": "https://openai.com/whisper?ref=aitoolsnl",
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
            import subprocess
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
priceRange: EUR 0-500/maand
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
