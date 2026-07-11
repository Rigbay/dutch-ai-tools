#!/usr/bin/env python3
"""Generate 3 new Dutch AI Tools comparison articles via Gemini API.
Topics: podcast tools, online course platforms, cybersecurity for SMBs.
"""

import os, json, requests, re
from pathlib import Path

# Load .env file
env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set")
    exit(1)

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = Path("src/content/articles")

def call_gemini(prompt: str, max_tokens: int = 8000) -> str:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7, "maxOutputTokens": max_tokens, "topP": 0.95,
        }
    }
    resp = requests.post(
        f"{API_URL}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        json=payload, timeout=120
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

def clean(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:yaml|md|markdown)?\s*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    return text.strip()

ARTICLES = [
    {
        "slug": "riverside-vs-descript-vs-alitu-podcast-2026",
        "topic": "Riverside vs Descript vs Alitu podcast opname en bewerking tools vergelijken voor 2026",
        "category": "content",
        "featured": "Riverside.fm",
        "tools": [
            ("Riverside.fm", "https://riverside.fm/"),
            ("Descript", "https://www.descript.com/"),
            ("Alitu", "https://alitu.com/"),
            ("Podcastle", "https://podcastle.ai/"),
        ],
    },
    {
        "slug": "teachable-vs-thinkific-vs-kajabi-cursussen-2026",
        "topic": "Teachable vs Thinkific vs Kajabi online cursus platforms vergelijken voor 2026",
        "category": "business",
        "featured": "Teachable",
        "tools": [
            ("Teachable", "https://teachable.com/"),
            ("Thinkific", "https://www.thinkific.com/"),
            ("Kajabi", "https://kajabi.com/"),
            ("Podia", "https://www.podia.com/"),
        ],
    },
    {
        "slug": "darktrace-vs-crowdstrike-vs-sentinelone-mkb-2026",
        "topic": "Darktrace vs CrowdStrike vs SentinelOne AI-cybersecurity voor het MKB vergelijken 2026",
        "category": "business",
        "featured": "CrowdStrike",
        "tools": [
            ("Darktrace", "https://darktrace.com/"),
            ("CrowdStrike", "https://www.crowdstrike.com/"),
            ("SentinelOne", "https://www.sentinelone.com/"),
            ("Bitdefender", "https://www.bitdefender.com/"),
        ],
    },
]

for art in ARTICLES:
    slug = art["slug"]
    filepath = ARTICLES_DIR / f"{slug}.md"
    
    if filepath.exists():
        print(f"  SKIP (exists): {slug}")
        continue
    
    t = art["tools"]
    
    tools_yaml = f"""- name: {t[0][0]}
  verdict: Beste allround podcast opname en bewerking tool met studiokwaliteit
  priceRange: EUR 0-24/mnd
  bestFor: Professionele podcasters
  rating: 4.5
  affiliateLink: {t[0][1]}
- name: {t[1][0]}
  verdict: Meest innovatieve AI-bewerking met transcriptie-gebaseerde editing
  priceRange: EUR 0-24/mnd
  bestFor: Snelle videopodcast bewerking
  rating: 4.6
  affiliateLink: {t[1][1]}
- name: {t[2][0]}
  verdict: Beste alles-in-één tool voor podcasters die niet technisch willen zijn
  priceRange: EUR 0-38/mnd
  bestFor: Beginners en solopreneurs
  rating: 4.3
  affiliateLink: {t[2][1]}
- name: {t[3][0]}
  verdict: Veelzijdig alternatief met sterke AI-stem features
  priceRange: EUR 0-24/mnd
  bestFor: Content creators die audio én video doen
  rating: 4.2
  affiliateLink: {t[3][1]}"""

    prompt = f"""Je bent een Nederlandse tech-copywriter voor Dutch AI Tools. Schrijf een compleet, diepgaand vergelijkingsartikel in het Nederlands over:

{art['topic']}

FORMAT — exact Markdown met frontmatter zoals hieronder. VERVANG ALLE placeholders zoals [prijs], [score], [use case] met echte, accurate waarden voor 2026. GEEN "[vul in]" tekst achterlaten.

---
title: 'Beste {art['topic'].split('vergelijken')[0].strip()} in 2026: Eerlijke Vergelijking + Prijzen'
slug: '{slug}'
description: '[155 karakters NL meta description met de toolnamen en "vergelijken", "2026", "NL" keywords]'
category: '{art['category']}'
rating: 4.4
priceRange: EUR 0-99/mnd
pros:
- Complete 2026 vergelijking van de belangrijkste tools in deze categorie
- Eerlijke voor- en nadelen per tool met actuele prijzen
- Praktisch NL-advies voor zowel beginners als gevorderden
cons:
- Prijzen kunnen wijzigen — check altijd de actuele aanbieder
- De beste tool hangt af van je specifieke use case en budget
affiliateLinks:
- https://www.beehiiv.com/
- https://www.make.com/en/register?pc=hermesai
date: 2026-06-07
modelYear: 2026
featuredTool: {art['featured']}
readingTime: 9 min
tools:
{tools_yaml}
related:
- beste-ai-automation-tools-2026
- beste-ai-tools-kleine-ondernemers-2026
draft: false
faq:
- q: [NL vraag over de categorie]
  a: [NL antwoord — 3-4 concrete zinnen met specifieke aanbeveling]
- q: [NL vraag over prijs/kosten]
  a: [NL antwoord — 3-4 zinnen met prijsranges en tips]
- q: [NL vraag over beginners vs gevorderden]
  a: [NL antwoord — 3-4 zinnen met tool-aanbeveling per niveau]
---

# [H1 titel — pakkend, met "{art['topic'].split('vergelijken')[0].strip()} 2026"]

[Inleiding: 4-5 zinnen waarom deze vergelijking relevant is in 2026. Noem {t[0][0]}, {t[1][0]}, {t[2][0]} en {t[3][0]} bij naam. Benoem dat AI een steeds grotere rol speelt in deze tools.]

## 1. {t[0][0]}: [Ondertitel met belangrijkste USP in 2026]

[4 alinea's. Beschrijf:]
- Wat {t[0][0]} doet en voor wie het bedoeld is
- De belangrijkste AI-features in 2026
- Actueel prijsmodel met concrete EUR-bedragen
- Eerlijke pluspunten én minpunten
- Specifiek Nederlands advies: voor wie wel/niet

**Prijs:** EUR [concreet bedrag-range]/mnd
**Beste voor:** [specifieke use case in NL]
**Score:** [x.x]/5

## 2. {t[1][0]}: [Ondertitel met USP]

[Zelfde grondige structuur als tool 1 — 4 alinea's]

**Prijs:** EUR [concreet bedrag]/mnd
**Beste voor:** [use case]
**Score:** [x.x]/5

## 3. {t[2][0]}: [Ondertitel met USP]

[Zelfde structuur — 4 alinea's]

**Prijs:** EUR [concreet bedrag]/mnd
**Beste voor:** [use case]
**Score:** [x.x]/5

## 4. {t[3][0]}: [Ondertitel met USP — Eervolle Vermelding]

[2-3 alinea's — korter maar informatief]

**Prijs:** EUR [concreet bedrag]/mnd
**Beste voor:** [use case]
**Score:** [x.x]/5

## Vergelijkingstabel: {t[0][0]} vs {t[1][0]} vs {t[2][0]} vs {t[3][0]}

| Tool | Prijs (vanaf) | Beste voor | AI-features | Score |
|------|--------------|------------|-------------|-------|
| [{t[0][0]}]({t[0][1]}) | EUR [prijs]/mnd | [use case] | [key AI feature] | [score]/5 |
| [{t[1][0]}]({t[1][1]}) | EUR [prijs]/mnd | [use case] | [key AI feature] | [score]/5 |
| [{t[2][0]}]({t[2][1]}) | EUR [prijs]/mnd | [use case] | [key AI feature] | [score]/5 |
| [{t[3][0]}]({t[3][1]}) | EUR [prijs]/mnd | [use case] | [key AI feature] | [score]/5 |

## Ons Oordeel: Welke Tool Past Bij Jou?

[4 alinea's met concrete aanbevelingen:]
- **Beste allround keuze:** [tool] — [1-2 zinnen waarom]
- **Beste budget:** [tool] — [1-2 zinnen]
- **Beste voor teams/gevorderden:** [tool] — [1-2 zinnen]
- **Aanbeveling per gebruiksscenario:** [2-3 specifieke scenario's met toolmatch]
- Slotzin die de lezer uitnodigt de gratis trials te proberen

---

*Dit artikel bevat affiliate links. Als je via onze links een aankoop doet, ontvangen wij een kleine commissie — zonder extra kosten voor jou. Dit helpt ons om onafhankelijke, Nederlandstalige AI-vergelijkingen te blijven maken.*

REGELS:
- ALLE content in het Nederlands
- Prijzen concreet en accuraat voor 2026, in EUR
- Gebruik de aangeleverde affiliate URLs in de vergelijkingstabel
- Minimaal 1500 woorden
- GEEN "[vul in]", "[prijs]", "[score]" of andere placeholders achterlaten — alles écht invullen
- FAQ met 3 echte vragen en antwoorden"""

    print(f"\n  Generating: {slug}...")
    try:
        result = call_gemini(prompt, max_tokens=8192)
        cleaned = clean(result)
        filepath.write_text(cleaned + "\n", encoding="utf-8")
        print(f"  ✓ Written ({len(cleaned)} chars): {slug}")
    except Exception as e:
        print(f"  ✗ FAILED: {slug} — {e}")

print("\n=== DONE ===")
print(f"New articles in {ARTICLES_DIR}/")
for art in ARTICLES:
    fp = ARTICLES_DIR / f"{art['slug']}.md"
    exists = "✓" if fp.exists() else "✗"
    print(f"  {exists} {art['slug']}")
