#!/usr/bin/env python3
"""Generate 5 new Dutch AI Tools comparison articles via Gemini API.
Topics: AI chatbots, AI video generation, AI image generation, AI website builders, AI recruitment/HR.
All target high NL search demand with active affiliate coverage (Synthesia, Make, beehiiv, etc.).
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

API_MODELS = ["gemini-2.5-flash-lite", "gemini-2.5-flash"]
ARTICLES_DIR = Path("src/content/articles")

def call_gemini(prompt: str, max_tokens: int = 8000) -> str:
    last_error = None
    for model in API_MODELS:
        for attempt in range(3):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            try:
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.7, "maxOutputTokens": max_tokens, "topP": 0.95,
                    }
                }
                resp = requests.post(
                    f"{url}?key={API_KEY}",
                    headers={"Content-Type": "application/json"},
                    json=payload, timeout=180
                )
                if resp.status_code == 200:
                    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                if resp.status_code == 429:
                    last_error = f"429 on {model} attempt {attempt+1}"
                    import time
                    time.sleep(10 * (attempt + 1))
                    continue
                resp.raise_for_status()
            except Exception as e:
                last_error = f"{model} attempt {attempt+1}: {e}"
                import time
                time.sleep(5)
    raise Exception(f"All models exhausted. Last: {last_error}")

def clean(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:yaml|md|markdown)?\s*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    return text.strip()

ARTICLES = [
    {
        "slug": "tidio-vs-crisp-vs-intercom-vs-zendesk-ai-chatbots-2026",
        "topic": "Tidio vs Crisp vs Intercom vs Zendesk AI chatbots en customer service tools vergelijken voor 2026",
        "category": "business",
        "featured": "Tidio",
        "tools": [
            ("Tidio", "https://www.tidio.com/"),
            ("Crisp", "https://crisp.chat/"),
            ("Intercom", "https://www.intercom.com/"),
            ("Zendesk AI", "https://www.zendesk.com/"),
        ],
    },
    {
        "slug": "synthesia-vs-runway-vs-pika-vs-heygen-ai-video-2026",
        "topic": "Synthesia vs Runway vs Pika vs HeyGen AI video generatie tools vergelijken 2026",
        "category": "creatie",
        "featured": "Synthesia",
        "tools": [
            ("Synthesia", "https://www.synthesia.io?via=hermes"),
            ("Runway", "https://runwayml.com/"),
            ("Pika Labs", "https://pika.art/"),
            ("HeyGen", "https://www.heygen.com/"),
        ],
    },
    {
        "slug": "midjourney-vs-dalle-vs-firefly-vs-stable-diffusion-2026",
        "topic": "Midjourney vs DALL-E vs Adobe Firefly vs Stable Diffusion AI image generators vergelijken 2026",
        "category": "creatie",
        "featured": "Midjourney",
        "tools": [
            ("Midjourney", "https://www.midjourney.com/"),
            ("DALL-E", "https://openai.com/dall-e-3"),
            ("Adobe Firefly", "https://www.adobe.com/products/firefly.html"),
            ("Stable Diffusion", "https://stability.ai/"),
        ],
    },
    {
        "slug": "wix-ai-vs-durable-vs-10web-vs-framer-ai-website-2026",
        "topic": "Wix AI vs Durable vs 10Web vs Framer AI website builders met AI vergelijken 2026",
        "category": "business",
        "featured": "Wix AI",
        "tools": [
            ("Wix AI", "https://www.wix.com/ai"),
            ("Durable", "https://durable.co/"),
            ("10Web", "https://10web.io/"),
            ("Framer AI", "https://www.framer.com/ai"),
        ],
    },
    {
        "slug": "recruitee-vs-teamtailor-vs-homerun-vs-testgorilla-hr-2026",
        "topic": "Recruitee vs Teamtailor vs Homerun vs TestGorilla recruitment HR tools vergelijken 2026",
        "category": "business",
        "featured": "Recruitee",
        "tools": [
            ("Recruitee", "https://recruitee.com/"),
            ("Teamtailor", "https://www.teamtailor.com/"),
            ("Homerun", "https://www.homerun.co/"),
            ("TestGorilla", "https://www.testgorilla.com/"),
        ],
    },
]

# Category-specific tool descriptions for accurate YAML generation
CATEGORY_TOOLS = {
    "tidio-vs-crisp-vs-intercom-vs-zendesk-ai-chatbots-2026": [
        {"name": "Tidio", "verdict": "Beste allround AI-chatbot voor MKB met Lyro AI en live chat integratie",
         "priceRange": "EUR 0-29/mnd", "bestFor": "Kleine tot middelgrote webshops", "rating": 4.6},
        {"name": "Crisp", "verdict": "Beste gedeelde inbox met AI-chatbot en kennisbank voor support teams",
         "priceRange": "EUR 0-95/mnd", "bestFor": "SaaS-bedrijven en startups", "rating": 4.5},
        {"name": "Intercom", "verdict": "Meest geavanceerd AI-platform met Fin AI-agent en proactieve automatisering",
         "priceRange": "EUR 29-139/mnd", "bestFor": "Scale-ups en enterprise", "rating": 4.7},
        {"name": "Zendesk AI", "verdict": "Beste enterprise helpdesk met AI-agents, automatisering en uitgebreide integraties",
         "priceRange": "EUR 19-115/mnd", "bestFor": "Grote teams en enterprise", "rating": 4.4},
    ],
    "synthesia-vs-runway-vs-pika-vs-heygen-ai-video-2026": [
        {"name": "Synthesia", "verdict": "Beste AI-avatar video's — 140+ AI-presentatoren, 120+ talen, ideaal voor training",
         "priceRange": "EUR 22-64/mnd", "bestFor": "Training, L&D en marketing video's", "rating": 4.7},
        {"name": "Runway", "verdict": "Meest creatieve AI-videotool met Gen-3 Alpha, text-to-video en video-to-video",
         "priceRange": "EUR 0-76/mnd", "bestFor": "Creatieve video editors en filmmakers", "rating": 4.6},
        {"name": "Pika Labs", "verdict": "Snelste text-to-video met sterke lipsync en real-time rendering",
         "priceRange": "EUR 0-28/mnd", "bestFor": "Social media creators en snelle clips", "rating": 4.3},
        {"name": "HeyGen", "verdict": "Meest realistische AI-avatars met instant voice cloning en vertaling",
         "priceRange": "EUR 0-72/mnd", "bestFor": "Gepersonaliseerde sales video's", "rating": 4.5},
    ],
    "midjourney-vs-dalle-vs-firefly-vs-stable-diffusion-2026": [
        {"name": "Midjourney", "verdict": "Mooiste artistieke renders — ongeëvenaarde kwaliteit, sterke community en style references",
         "priceRange": "EUR 10-60/mnd", "bestFor": "Professionals en kunstenaars", "rating": 4.8},
        {"name": "DALL-E", "verdict": "Meest toegankelijk via ChatGPT — natuurlijke taal, sterke instructievolging, veilig",
         "priceRange": "EUR 20/mnd (ChatGPT+)", "bestFor": "Beginners en snelle iteraties", "rating": 4.5},
        {"name": "Adobe Firefly", "verdict": "Beste commerciële veiligheid — getraind op gelicenseerde data, diep in Creative Cloud",
         "priceRange": "EUR 0-12/mnd", "bestFor": "Designers en marketing teams", "rating": 4.4},
        {"name": "Stable Diffusion", "verdict": "Meest flexibel en open-source — volledige controle via lokale installatie of API",
         "priceRange": "EUR 0-9/mnd", "bestFor": "Developers en power users", "rating": 4.3},
    ],
    "wix-ai-vs-durable-vs-10web-vs-framer-ai-website-2026": [
        {"name": "Wix AI", "verdict": "Meest complete AI-websitebuilder met natuurlijke taal prompts en volledig CMS",
         "priceRange": "EUR 0-25/mnd", "bestFor": "MKB, ZZP'ers en complete websites", "rating": 4.6},
        {"name": "Durable", "verdict": "Snelste AI-websitegenerator — hele site in 30 seconden, inclusief hosting en CRM",
         "priceRange": "EUR 12-20/mnd", "bestFor": "ZZP'ers die snel online willen", "rating": 4.4},
        {"name": "10Web", "verdict": "Beste AI WordPress — automatische 90+ PageSpeed, AI SEO en migratie",
         "priceRange": "EUR 10-30/mnd", "bestFor": "WordPress gebruikers en optimalisatie", "rating": 4.5},
        {"name": "Framer AI", "verdict": "Mooiste designs — AI genereert design-forward sites, volledige ontwerpvrijheid",
         "priceRange": "EUR 0-25/mnd", "bestFor": "Designers en portfolio's", "rating": 4.3},
    ],
    "recruitee-vs-teamtailor-vs-homerun-vs-testgorilla-hr-2026": [
        {"name": "Recruitee", "verdict": "Beste collaborative ATS — Nederlands/EU, GDPR-first, sterke career site builder",
         "priceRange": "EUR 199-399/mnd", "bestFor": "MKB en scale-ups in Europa", "rating": 4.6},
        {"name": "Teamtailor", "verdict": "Beste employer branding — visueel sterk, social media integratie, krachtige analytics",
         "priceRange": "EUR 350-500/mnd", "bestFor": "Bedrijven met focus op branding", "rating": 4.5},
        {"name": "Homerun", "verdict": "Beste voor MKB — Nederlands, eenvoudig, mooie vacaturepagina's, geen gedoe",
         "priceRange": "EUR 59-159/mnd", "bestFor": "Kleine teams en startups", "rating": 4.4},
        {"name": "TestGorilla", "verdict": "Beste skills-based assessments — 300+ wetenschappelijk gevalideerde tests, bias-vrij",
         "priceRange": "EUR 0-699/mnd", "bestFor": "Skills-based hiring en schaalbaar", "rating": 4.5},
    ],
}

for art in ARTICLES:
    slug = art["slug"]
    filepath = ARTICLES_DIR / f"{slug}.md"

    if filepath.exists():
        print(f"  SKIP (exists): {slug}")
        continue

    t = art["tools"]
    tool_meta = CATEGORY_TOOLS[slug]

    tools_yaml = f"""- name: {t[0][0]}
  verdict: {tool_meta[0]['verdict']}
  priceRange: {tool_meta[0]['priceRange']}
  bestFor: {tool_meta[0]['bestFor']}
  rating: {tool_meta[0]['rating']}
  affiliateLink: {t[0][1]}
- name: {t[1][0]}
  verdict: {tool_meta[1]['verdict']}
  priceRange: {tool_meta[1]['priceRange']}
  bestFor: {tool_meta[1]['bestFor']}
  rating: {tool_meta[1]['rating']}
  affiliateLink: {t[1][1]}
- name: {t[2][0]}
  verdict: {tool_meta[2]['verdict']}
  priceRange: {tool_meta[2]['priceRange']}
  bestFor: {tool_meta[2]['bestFor']}
  rating: {tool_meta[2]['rating']}
  affiliateLink: {t[2][1]}
- name: {t[3][0]}
  verdict: {tool_meta[3]['verdict']}
  priceRange: {tool_meta[3]['priceRange']}
  bestFor: {tool_meta[3]['bestFor']}
  rating: {tool_meta[3]['rating']}
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
priceRange: EUR 0-139/mnd
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

**Prijs:** {tool_meta[0]['priceRange']}
**Beste voor:** {tool_meta[0]['bestFor']}
**Score:** {tool_meta[0]['rating']}/5

## 2. {t[1][0]}: [Ondertitel met USP]

[Zelfde grondige structuur als tool 1 — 4 alinea's]

**Prijs:** {tool_meta[1]['priceRange']}
**Beste voor:** {tool_meta[1]['bestFor']}
**Score:** {tool_meta[1]['rating']}/5

## 3. {t[2][0]}: [Ondertitel met USP]

[Zelfde structuur — 4 alinea's]

**Prijs:** {tool_meta[2]['priceRange']}
**Beste voor:** {tool_meta[2]['bestFor']}
**Score:** {tool_meta[2]['rating']}/5

## 4. {t[3][0]}: [Ondertitel met USP — Eervolle Vermelding]

[2-3 alinea's — korter maar informatief]

**Prijs:** {tool_meta[3]['priceRange']}
**Beste voor:** {tool_meta[3]['bestFor']}
**Score:** {tool_meta[3]['rating']}/5

## Vergelijkingstabel: {t[0][0]} vs {t[1][0]} vs {t[2][0]} vs {t[3][0]}

| Tool | Prijs (vanaf) | Beste voor | AI-features | Score |
|------|--------------|------------|-------------|-------|
| [{t[0][0]}]({t[0][1]}) | {tool_meta[0]['priceRange']} | {tool_meta[0]['bestFor']} | [key AI feature] | {tool_meta[0]['rating']}/5 |
| [{t[1][0]}]({t[1][1]}) | {tool_meta[1]['priceRange']} | {tool_meta[1]['bestFor']} | [key AI feature] | {tool_meta[1]['rating']}/5 |
| [{t[2][0]}]({t[2][1]}) | {tool_meta[2]['priceRange']} | {tool_meta[2]['bestFor']} | [key AI feature] | {tool_meta[2]['rating']}/5 |
| [{t[3][0]}]({t[3][1]}) | {tool_meta[3]['priceRange']} | {tool_meta[3]['bestFor']} | [key AI feature] | {tool_meta[3]['rating']}/5 |

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
- FAQ met 3 echte vragen en antwoorden
- EEN artikel voor Synthesia: gebruik EXPLICIET de affiliate URL https://www.synthesia.io?via=hermes in de tool-lijst EN in de vergelijkingstabel"""

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
