#!/usr/bin/env python3
"""Generate 2 new Dutch AI tools articles: verzekeringen, fitness.
Batch 9b — May 22 2026. Uses Gemini 2.5 Flash, proper yaml.dump frontmatter."""
import os, time, sys, yaml
import requests
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()

BASE_URL_FLASH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

ALL_SLUGS = sorted(f.stem for f in ARTICLES_DIR.glob("*.md"))

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

def generate_one(prompt, attempt=1):
    url = BASE_URL_FLASH
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    resp = requests.post(f"{url}?key={API_KEY}", headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    if resp.status_code == 503 and attempt <= 2:
        print(f"  503, retry {attempt+1}...")
        time.sleep(3)
        return generate_one(prompt, attempt + 1)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return text, len(text.split())

ARTICLES = [
    {
        "slug": "beste-ai-tools-verzekeringen-2026",
        "title": "Beste AI Tools voor Verzekeringen 2026: Risicobeoordeling, Claimsverwerking & Frauddetectie",
        "description": "AI in de verzekeringssector 2026. Vergelijk tools voor risicobeoordeling, schadeafhandeling, frauddetectie en klantbediening.",
        "category": "business",
        "rating": 4.4,
        "priceRange": "EUR 0-2500/mnd of op aanvraag",
        "pros": ["NL-specifieke tools voor de verzekeringsmarkt", "DNB/AFM relevante compliance tools inbegrepen", "Praktische vergelijking per type verzekeraar"],
        "cons": ["Enterprise-tools vaak op aanvraag", "Regelgeving vertraagt adoptie bij kleinere spelers", "Sommige tools overlappen functioneel"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-22",
        "modelYear": 2026,
        "featuredTool": "FRISS",
        "readingTime": "9 min",
        "tools": [
            {"name": "FRISS", "verdict": "NL marktleider AI-frauddetectie voor verzekeraars", "priceRange": "Op aanvraag", "bestFor": "Frauddetectie", "rating": 4.6, "affiliateLink": "https://www.notion.so"},
            {"name": "Tractable", "verdict": "AI-computervisie voor automatische schadebeoordeling auto", "priceRange": "Op aanvraag", "bestFor": "Schadeafhandeling", "rating": 4.5, "affiliateLink": "https://www.notion.so"},
            {"name": "Shift Technology", "verdict": "Wereldleider AI-claimsverwerking en fraudedetectie", "priceRange": "Op aanvraag", "bestFor": "Claims intelligence", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
            {"name": "Zelros", "verdict": "AI-platform voor gepersonaliseerde verzekeringsadviezen", "priceRange": "Op aanvraag", "bestFor": "Klantbediening", "rating": 4.2, "affiliateLink": "https://www.notion.so"},
            {"name": "Anansi", "verdict": "NL insurtech AI-platform voor embedded verzekeringen", "priceRange": "Op aanvraag", "bestFor": "Embedded insurance", "rating": 4.0, "affiliateLink": "https://www.notion.so"},
            {"name": "Omnius", "verdict": "AI-documentverwerking verzekeringen", "priceRange": "EUR 500-2000/mnd", "bestFor": "Documentverwerking", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "Akur8", "verdict": "AI-pricingplatform met transparante uitlegbare modellen", "priceRange": "Op aanvraag", "bestFor": "Pricing", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("beste-ai-tools-verzekeringen-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Is AI in de verzekeringssector betrouwbaar?", "a": "De tools worden al gebruikt door Nederlandse grootverzekeraars. FRISS verwerkt realtime risicoscoring. DNB vereist dat AI-beslissingen uitlegbaar zijn — tools zoals Akur8 zijn hiervoor ontworpen."},
            {"q": "Wat kost AI voor een kleine verzekeraar?", "a": "Kleine spelers kunnen starten met Omnius (EUR 500-2000/mnd). FRISS en Shift Technology bieden modulaire pakketten. Totale instapkosten: circa EUR 800-2000/mnd."},
            {"q": "Hoe zit het met AVG bij verzekerings-AI?", "a": "Alle tools opereren onder AVG-compliance. Verzekeraars moeten een DPIA uitvoeren. NL tools zoals FRISS en Anansi hebben AVG ingebouwd. Internationale tools verwerken data doorgaans binnen de EU."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de verzekeringssector in 2026. Behandel precies 7 tools: FRISS, Tractable, Shift Technology, Zelros, Anansi, Omnius, Akur8.

Structuur:
- Introductie: AI in de Nederlandse verzekeringssector groeit hard in 2026 — automatische schadeafhandeling, risicobeoordeling. DNB en AFM stimuleren verantwoorde AI.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR), beste-voor, NL-aanwezig?, score (1-5)
- Conclusie: welke tool voor welk type verzekeraar (schade, leven, zorg, insurtech startup)
- Sluit af met een FAQ-sectie (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de NEDERLANDSE context. FRISS en Anansi zijn Nederlandse bedrijven. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
    },
    {
        "slug": "beste-ai-tools-fitness-2026",
        "title": "Beste AI Tools voor Fitness & Personal Training 2026: Workouts, Voeding & Progressie",
        "description": "AI fitness tools in 2026: vergelijk AI-gestuurde workout apps, voedingscoaches, bewegingsanalyse en personal training platforms.",
        "category": "business",
        "rating": 4.2,
        "priceRange": "EUR 0-50/mnd",
        "pros": ["Betaalbaar — alle tools onder EUR 50/mnd", "Direct bruikbaar zonder installatie", "AI-personalisatie vervangt dure trainers deels"],
        "cons": ["Geen tool vervangt volledig een menselijke coach", "Nauwkeurigheid bewegingsanalyse varieert", "Privacy bij gezondheidsdata blijft aandachtspunt"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-22",
        "modelYear": 2026,
        "featuredTool": "Whoop",
        "readingTime": "8 min",
        "tools": [
            {"name": "Whoop", "verdict": "AI-herstelcoach met polsband — meet slaap, HRV en strain", "priceRange": "EUR 20-30/mnd", "bestFor": "Hersteloptimalisatie", "rating": 4.5, "affiliateLink": "https://www.notion.so"},
            {"name": "Fitbod", "verdict": "AI-krachttrainingsapp op basis van apparatuur en progressie", "priceRange": "EUR 10-15/mnd", "bestFor": "Krachttraining", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
            {"name": "Oura", "verdict": "Slimme ring met AI-slaapanalyse en readiness score", "priceRange": "EUR 6/mnd", "bestFor": "Holistische gezondheid", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "Kaia Health", "verdict": "AI-fysiotherapie via telefooncamera met realtime correcties", "priceRange": "EUR 15-30/mnd", "bestFor": "Hersteltraining", "rating": 4.2, "affiliateLink": "https://www.notion.so"},
            {"name": "Freeletics", "verdict": "AI-gestuurde bodyweight en HIIT-training", "priceRange": "EUR 0-15/mnd", "bestFor": "Thuis-workouts", "rating": 4.1, "affiliateLink": "https://www.notion.so"},
            {"name": "Tempo", "verdict": "AI-thuisgym met 3D-sensoren en realtime vormcorrectie", "priceRange": "EUR 30-50/mnd", "bestFor": "Thuis krachttraining", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "Zing Coach", "verdict": "AI-personal trainer via selfie-camera analyse", "priceRange": "EUR 10-20/mnd", "bestFor": "AI training", "rating": 4.0, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("beste-ai-tools-fitness-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Kan een AI-trainer een echte personal trainer vervangen?", "a": "Deels. AI-tools zoals Fitbod en Zing Coach genereren gepersonaliseerde schema's. Maar menselijke coaches bieden motivatie en complexe bewegingscorrecties. De ideale combi: AI voor dagelijkse workouts, coach voor techniek."},
            {"q": "Welke AI-fitness tool werkt zonder extra hardware?", "a": "Freeletics (gratis) + Fitbod (EUR 10-15/mnd) vormen de beste hardware-loze stack. Beide werken volledig op je telefoon. Totale kosten: EUR 10-15/mnd."},
            {"q": "Zijn AI-gezondheidsapps veilig met mijn data?", "a": "De meeste tools voldoen aan GDPR/AVG. Whoop en Oura hebben SOC 2-certificering. Let op: fitnessdata kan verzekeringsrelevant zijn. Lees altijd de privacyvoorwaarden."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor fitness en personal training in 2026. Behandel precies 7 tools: Whoop, Fitbod, Oura, Kaia Health, Freeletics, Tempo, Zing Coach.

Structuur:
- Introductie: AI personaliseert fitness in 2026 — geen generieke schema's meer maar adaptieve training op basis van data (slaap, herstel, prestaties).
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, hardware-nodig?, score (1-5)
- Conclusie: welke tool voor welk type sporter (krachttrainer, duursporter, herstellend, thuis-fitness, gym-eigenaar)
- Sluit af met een FAQ-sectie (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de Nederlandse/Europese markt. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
    },
]

for i, article in enumerate(ARTICLES):
    print(f"[{i+1}/2] {article['slug']}...")
    try:
        text, wc = generate_one(article.pop("prompt"))
        fm = {k: v for k, v in article.items()}
        yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, width=200)
        content = f"---\n{yaml_str}---\n\n{text}\n"
        path = ARTICLES_DIR / f"{article['slug']}.md"
        path.write_text(content, encoding="utf-8")
        print(f"  OK: {wc} words -> {path}")
    except Exception as e:
        print(f"  FAIL: {e}")
        sys.exit(1)

print("\nDone: 2/2 OK")
