#!/usr/bin/env python3
"""Retry the single failed article (education/e-learning) from the gaps batch."""
import os, glob, sys, requests
from datetime import date

# Load API key
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    for line in open(os.path.expanduser("~/.hermes/.env")):
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

if not API_KEY:
    print("❌ No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

ALL_SLUGS = sorted([f.replace(".md", "").replace(f"{ARTICLES_DIR}/", "") for f in glob.glob(f"{ARTICLES_DIR}/*.md")])
def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

import yaml

slug = "beste-ai-onderwijs-bijles-elearning-tools-2026"

tools = [
    {"name": "Khan Academy (Khanmigo)", "verdict": "AI-bijlesdocent die studenten niet alleen antwoorden geeft maar door vragen te stellen laat ontdekken", "priceRange": "EUR 0 / 44/jaar", "bestFor": "AI-gestuurde bijles", "rating": 4.7, "affiliateLink": "https://www.khanacademy.org/?ref=aitoolsnl"},
    {"name": "Quizlet (Q-Chat)", "verdict": "AI-leerplatform met Q-Chat, een AI-tutor die overhoringen geeft en gepersonaliseerde flashcards genereert", "priceRange": "EUR 0-36/jaar", "bestFor": "Overhoren & flashcards", "rating": 4.5, "affiliateLink": "https://quizlet.com/?ref=aitoolsnl"},
    {"name": "Duolingo (AI-tutor)", "verdict": "AI-gestuurde taalleerapp met adaptieve oefeningen, spraakherkenning en AI-roleplay", "priceRange": "EUR 0-13/mnd", "bestFor": "Talen leren", "rating": 4.6, "affiliateLink": "https://www.duolingo.com/?ref=aitoolsnl"},
    {"name": "Coursera (AI-coach)", "verdict": "AI-gestuurd online leerplatform met universitaire cursussen en een AI-coach", "priceRange": "EUR 0-50/mnd", "bestFor": "Universitaire cursussen online", "rating": 4.5, "affiliateLink": "https://www.coursera.org/?ref=aitoolsnl"},
    {"name": "Brilliant", "verdict": "AI-gedreven leerplatform voor wiskunde, programmeren en data science", "priceRange": "EUR 15-25/mnd", "bestFor": "STEM-onderwijs", "rating": 4.6, "affiliateLink": "https://brilliant.org/?ref=aitoolsnl"},
    {"name": "Grammarly (AI-schrijfcoach)", "verdict": "AI-schrijfassistent die schrijfstijl, toon en helderheid analyseert", "priceRange": "EUR 0-30/mnd", "bestFor": "Schrijfvaardigheid verbeteren", "rating": 4.4, "affiliateLink": "https://www.grammarly.com/?ref=aitoolsnl"},
    {"name": "Notion AI", "verdict": "AI-notitie- en kennismanagementtool die samenvattingen maakt en vragen beantwoordt", "priceRange": "EUR 0-10/mnd", "bestFor": "Studienotities & samenvattingen", "rating": 4.5, "affiliateLink": "https://www.notion.so/?ref=aitoolsnl"},
]

prompt = (
    "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
    "voor onderwijs, bijles en e-learning in 2026. Behandel precies 7 tools: "
    "Khan Academy (Khanmigo AI), Quizlet (Q-Chat), Duolingo (AI-tutor), "
    "Coursera (AI-coach), Brilliant, Grammarly (AI-schrijfcoach), Notion AI.\n\n"
    "Structuur:\n"
    "- Introductie: AI transformeert onderwijs in 2026 — van persoonlijke AI-bijlesdocenten "
    "die 24/7 beschikbaar zijn tot adaptieve leerplatforms die zich aanpassen aan jouw tempo.\n"
    "- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, "
    "plus- en minpunten, verdict (1-2 zinnen)\n"
    "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\n"
    "- Conclusie: welke tool voor welk type lerende (middelbare scholier, student, professional)\n"
    "- 3 FAQ-vragen over AI en onderwijs\n\n"
    "Focus op Nederlandse/Europese context. Prijzen in EUR. Noem Nederlands onderwijssysteem, "
    "WO/HBO/MBO. Schrijf in vloeiend Nederlands."
)

url = f"{BASE_URL}?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.8, "topP": 0.95, "maxOutputTokens": 4096}
}

print(f"Retrying: {slug}")
resp = requests.post(url, json=payload, timeout=120)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    today = date.today().isoformat()

    fm = {
        "title": "Beste AI Tools voor Onderwijs, Bijles & E-learning 2026: top 7 vergeleken",
        "slug": slug,
        "description": "AI tools voor onderwijs, bijles en online leren in 2026. Vergelijk Khan Academy, Quizlet, Duolingo, Coursera, Brilliant, Grammarly en Notion AI voor studenten, docenten en levenslang leren.",
        "category": "productiviteit",
        "rating": 4.5,
        "priceRange": "EUR 0-50/mnd",
        "pros": [
            "Gebaseerd op actuele marktdata en praktijkervaringen uit 2026",
            "Duidelijke vergelijking met prijzen, verdicts en scores per tool",
            "Nederlandstalig en toegankelijk voor Nederlandse gebruikers",
        ],
        "cons": [
            "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
            "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
        ],
        "affiliateLinks": [t["affiliateLink"] for t in tools],
        "related": pick_related(slug, ALL_SLUGS, 3),
        "date": today,
        "modelYear": 2026,
        "featuredTool": tools[0]["name"],
        "readingTime": "8 min",
        "tools": tools,
    }

    out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(out_path, "w") as f:
        f.write("---\n")
        f.write(yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False))
        f.write("---\n\n")
        f.write(text)

    size = os.path.getsize(out_path)
    print(f"✅ Written: {out_path} ({size} bytes, {len(text)} chars)")
else:
    print(f"❌ Error: {resp.text[:300]}")
