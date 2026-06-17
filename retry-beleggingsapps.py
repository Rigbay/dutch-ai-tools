#!/usr/bin/env python3
"""Regenerate the truncated beleggingsapps article."""
import os, time, requests, yaml
from datetime import date

key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
with open(key_file) as f:
    API_KEY = f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    candidates = [s for s in slugs if s != new_slug]
    return candidates[:n]

def call_gemini(prompt):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}}
    for attempt in range(8):
        try:
            resp = requests.post(url, json=payload, timeout=120, headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                print(f"  429 wait {35*(attempt+1)}s")
                time.sleep(35*(attempt+1))
                continue
            if resp.status_code in (503, 500):
                print(f"  {resp.status_code} retry in 30s")
                time.sleep(30)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                return None
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(15)
    return None

def build_article(defn, body_text):
    avg = round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1)
    data = {
        "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
        "category": defn["category"], "rating": avg, "priceRange": defn["priceRange"],
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"],
        "cons": ["Prijzen kunnen wijzigen — check aanbieder", "Beleggen brengt risico's met zich mee", "Keuze hangt af van je specifieke situatie"],
        "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste broker voor beginners?", "a": "BUX is specifiek ontworpen voor beginners met fractionele aandelen vanaf €10 en een intuïtieve app. DEGIRO biedt meer diepgang met lage kosten voor de serieuze belegger."},
            {"q": "Zijn er verborgen kosten bij gratis brokers?", "a": "Veel 'gratis' brokers verdienen via spreads, valutamarkups of order flow. Lees de kleine lettertjes. DEGIRO en Meesman zijn transparant over hun kostenmodel."},
            {"q": "Hoeveel geld heb ik nodig om te starten?", "a": "Bij BUX en Trading 212 kun je al vanaf €10 beginnen met fractionele aandelen. Bij Meesman kan dat vanaf €100 per maand. DEGIRO heeft geen minimum maar 1 aandeel moet je wel kunnen betalen."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"

defn = {
    "slug": "beleggingsapps-vergelijken-2026-degiro-bux-trading212-meesman",
    "title": "Beleggingsapps Vergelijken 2026: DEGIRO vs BUX vs Trading 212 vs Meesman vs eToro — Beste Broker voor Beginnende Beleggers",
    "description": "Beginnen met beleggen in 2026? Vergelijk DEGIRO, BUX, Trading 212, Meesman, eToro, Saxo en Trade Republic op kosten, gebruiksgemak, aanbod en Nederlandse dienstverlening.",
    "category": "persoonlijk",
    "priceRange": "EUR 0-5 per transactie (veel gratis)",
    "tools": [
        {"name": "DEGIRO", "verdict": "Beste allround broker — laagste kosten, grootste aanbod, AFM-gereguleerd, uitgebreide research", "priceRange": "€1,00 per transactie (€0 kernselectie ETF's)", "bestFor": "Serieuze Beleggers", "rating": 4.7, "affiliateLink": "https://degiro.nl/"},
        {"name": "BUX", "verdict": "Beste voor beginners — fractionele aandelen vanaf €10, Nederlands, intuïtieve app, zero commission", "priceRange": "€0 commissie op aandelen/ETF's", "bestFor": "Beginners", "rating": 4.4, "affiliateLink": "https://bux.com/"},
        {"name": "Trading 212", "verdict": "Breedste aanbod — 10.000+ instrumenten, fractioneel, gratis, automatische beleggingen (Pies)", "priceRange": "€0 commissie", "bestFor": "Diversificatie", "rating": 4.3, "affiliateLink": "https://trading212.com/"},
        {"name": "Meesman", "verdict": "Beste voor passief indexbeleggen — lage fondskosten, geen transactiekosten, Nederlands, automatisch", "priceRange": "0,4-0,5% fondskosten per jaar", "bestFor": "Indexbeleggen / Pensioen", "rating": 4.6, "affiliateLink": "https://meesman.nl/"},
        {"name": "eToro", "verdict": "Beste social trading — copy other traders, 5000+ assets, crypto + aandelen in één app", "priceRange": "€0 commissie op aandelen (€1 op crypto, spreads)", "bestFor": "Social & Copy Trading", "rating": 4.1, "affiliateLink": "https://etoro.com/"},
        {"name": "Saxo Bank", "verdict": "Beste voor professionals — 71.000+ instrumenten, institutionele research, opties/futures", "priceRange": "€2-8 per transactie", "bestFor": "Professionals & HNW", "rating": 4.2, "affiliateLink": "https://saxobank.nl/"},
        {"name": "Trade Republic", "verdict": "Beste rente op cash — 2% rente op onbelegd geld, €1 transacties, Duits, sinds 2025 actief in NL", "priceRange": "€1 per transactie (€0 spaarplannen)", "bestFor": "Rente op cash + beleggen", "rating": 4.0, "affiliateLink": "https://traderepublic.com/"},
    ],
}

# Shorter, more focused prompt to avoid truncation
prompt = """Schrijf een Nederlands artikel van 1000-1200 woorden over beleggingsapps vergelijken in 2026. Behandel 7 aanbieders: DEGIRO, BUX, Trading 212, Meesman Indexbeleggen, eToro, Saxo Bank, Trade Republic.

Structuur:
- Introductie (2 korte paragrafen): recordaantal Nederlandse beleggers, commission-free trading, box 3
- Per broker exact 3-4 zinnen: naam bold, één zin wat het is, prijs, beste use case, plus/min
- Markdown vergelijkingstabel: broker, transactiekosten, fractional shares, crypto, NL-dienstverlening, AFM, score 1-5
- Conclusie tabel (welke broker voor wie: beginner, indexbelegger, actieve trader, crypto, pensioen)
- 3 FAQ's (kort)

Nederlandse context: DEGIRO (Amsterdam, AFM). BUX (Amsterdam, beginners). Meesman (Den Haag, passief). Trade Republic met 2% rente. Vloeiend Nederlands. Houd het bondig — geen lange alinea's."""

print("Regenerating beleggingsapps...")
body = call_gemini(prompt)
if not body:
    print("FAILED")
    exit(1)

article = build_article(defn, body)
path = os.path.join(ARTICLES_DIR, f"{defn['slug']}.md")
with open(path, "w") as f:
    f.write(article)
print(f"Written: {path} ({len(article)} chars, {len(article.splitlines())} lines)")
