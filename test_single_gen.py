#!/usr/bin/env python3
"""Generate one huis-tuin article as test."""
import os, requests, json, time, random

env_path = os.path.expanduser('~/.hermes/.env')
key = None
with open(env_path) as f:
    for line in f:
        if 'GEMINI_API_KEY' in line and not line.startswith('#'):
            key = line.strip().split('=',1)[1]
            break

url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'
prompt = """Je bent een Nederlandse tech-journalist die gespecialiseerd is in AI tools voor bedrijven en professionals. Schrijf een compleet vergelijkingsartikel over:

ONDERWERP: Beste slimme thermostaten 2026 voor Nederlandse huishoudens
CATEGORIE: huis-tuin
DOELGROEP: Nederlandse huiseigenaren en bewoners die energie willen besparen met slimme thermostaten
AANBIEDERS: Google Nest, Tado, Honeywell, Netatmo, Bosch, Eve

STRUCTUUR voor de body (na ===BODY===):
1. ## Inleiding (2-3 alinea's)
2. ## Snel advies (3 bullets: "Kies X als je...")
3. ## Vergelijking per aanbieder (5-7 secties met ### koppen)
4. ## Waar op letten? (3-4 alinea's)
5. ## Vergelijkingstabel (Markdown tabel)
6. ## Conclusie (1-2 alinea's)
7. ## Veelgestelde vragen (> FAQ blocks)

OUTPUT FORMAT — TWEE DELEN gescheiden door ===BODY===:

EERST de JSON metadata (géén body_markdown veld!):
{
  "title": "Beste slimme thermostaten 2026 voor Nederlandse huishoudens",
  "description": "Vergelijk de top slimme thermostaten in Nederland 2026. Welke thermostaat bespaart het meest op energiekosten en past het beste bij jouw situatie?",
  "category": "huis-tuin",
  "rating": 4.3,
  "priceRange": "€150-€500 eenmalig",
  "pros": ["Energiebesparing tot 30%", "Eenvoudige installatie en app", "Integratie met slimme huissystemen"],
  "cons": ["Initieel hoge aanschafkosten", "Mogelijke privacy risico's", "Afhankelijk van internetconnectie"],
  "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator", "https://taskade.com/?via=55nfr2"],
  "featuredTool": "Google Nest",
  "readingTime": "8 min",
  "tools": [
    {"name": "Google Nest", "verdict": "Beste allround slimme thermostaat met Google integratie.", "priceRange": "€200-€400", "bestFor": "Nieuwe huiseigenaren", "rating": 4.7, "affiliateLink": "https://example.com"},
    {"name": "Tado", "verdict": "Sterk in energiebesparing en automatische planning.", "priceRange": "€150-€300", "bestFor": "Energiebewuste huishoudens", "rating": 4.5, "affiliateLink": "https://example.com"},
    {"name": "Honeywell", "verdict": "Betrouwbare optie met solide basisfunctionaliteit.", "priceRange": "€120-€250", "bestFor": "Budget bewuste gebruikers", "rating": 4.2, "affiliateLink": "https://example.com"}
  ],
  "faq": [{"q": "Hoeveel energie kan ik besparen?", "a": "Gemiddeld 15-30% afhankelijk van gebruik en isolatie."}]
}

DAN ===BODY=== op een eigen regel.

DAARNA de volledige artikeltekst in Markdown (800+ woorden). Dit mag gewone newlines bevatten, géén \\n escapes nodig.

BELANGRIJK: Schrijf levendig Nederlands. Geen superlatieven. Echte prijzen. Minimaal5 tools. Minimaal 800 woorden body. Géén markdown fences om de hele output."""

print("Sending request...")
start = time.time()
payload = {'contents': [{'parts': [{'text': prompt}]}], 'generationConfig': {'temperature': 0.7, 'maxOutputTokens': 4000}}
try:
    resp = requests.post(url, json=payload, timeout=180)
    print(f"Status {resp.status_code}, time {time.time()-start:.1f}s")
    if resp.status_code == 200:
        data = resp.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        print(f"Response length: {len(text)} chars")
        # Save to test file
        with open('test_output.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Saved to test_output.txt")
    else:
        print(f"Error: {resp.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")