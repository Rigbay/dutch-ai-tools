#!/usr/bin/env python3
"""Retry beleggingsapps article with shorter prompt to avoid truncation."""
import os, time, requests, yaml
from datetime import date

key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
with open(key_file) as f:
    API_KEY=f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    return [s for s in slugs if s != new_slug][:n]

prompts = [
    """Schrijf een Nederlandse introductie van 2 paragrafen over beleggingsapps in 2026. 
    Recordaantal van 2+ miljoen NL huishoudens belegt. Commission-free trading. Box 3 belastingwijziging. Fractionele aandelen. AI-adviezen. Toegankelijk, vloeiend Nederlands. Geen markdown headers.""",

    """Beschrijf DEGIRO in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking. 
    Wat: Nederlandse broker sinds 2008, Amsterdam. Kosten: €1 per transactie, €0 op kernselectie ETF's. Aanbod: 50+ beurzen, 100.000+ producten. Voordelen: AFM-gereguleerd, laagste kosten, beste research. Nadelen: geen fractionele aandelen, geen crypto, verouderde app. Verdict: beste allround broker voor serieuze beleggers. Score: 4.7/5.""",

    """Beschrijf BUX in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking.
    Wat: Nederlandse broker sinds 2014, Amsterdam, focus op beginners. Kosten: €0 commissie op aandelen/ETF's. Aanbod: 2.000+ aandelen en ETF's, fractionele aandelen vanaf €10, crypto (BUX Zero). Voordelen: intuïtieve app, Nederlands, fractioneel, geen minimum. Nadelen: beperkt aanbod vs DEGIRO, geen opties, geen research tools. Verdict: beste voor beginners. Score: 4.4/5.""",

    """Schrijf over Trading 212 in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking.
    Wat: Britse broker sinds 2004, populair in NL. Kosten: €0 commissie, geen platformfee. Aanbod: 10.000+ instrumenten, fractionele aandelen, automatische Pies (mandjes). Voordelen: breedste aanbod, gratis, automatisch beleggen, goede app. Nadelen: gereguleerd in Cyprus (niet AFM), klantenservice matig, onduidelijk verdienmodel (PFOF). Verdict: beste voor diversificatie. Score: 4.3/5.""",

    """Schrijf over Meesman Indexbeleggen in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking.
    Wat: Nederlandse indexbelegger sinds 2011, Den Haag. Kosten: 0,4-0,5% fondskosten per jaar, geen transactiekosten. Aanbod: breed gespreide indexfondsen (wereld, Europa, obligaties). Voordelen: passief en simpel, automatisch maandelijks, Nederlands, AFM-vergunning, fiscaal transparant. Nadelen: geen losse aandelen, geen app (alleen web), alleen indexfondsen. Verdict: beste voor passief indexbeleggen en pensioen. Score: 4.6/5.""",

    """Schrijf over eToro in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking.
    Wat: Israëlische broker sinds 2007, social trading platform. Kosten: €0 commissie op aandelen, €1 op crypto, spread op andere. Aanbod: 5.000+ instruments, aandelen, ETF's, crypto, copy trading, Smart Portfolios. Voordelen: social/copy trading uniek, crypto + aandelen in één app, demo-account. Nadelen: gereguleerd in Cyprus (niet AFM), verborgen spreads, beperkt research. Verdict: beste voor social/copy trading. Score: 4.1/5.""",

    """Schrijf over Saxo Bank in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking.
    Wat: Deense bank sinds 1992, actief in NL voor professionals. Kosten: €2-8 per transactie, 0,12% custody fee. Aanbod: 71.000+ instrumenten, opties, futures, obligaties, forex. Voordelen: institutionele research, breedste professionele aanbod, AFM/DNB-gereguleerd. Nadelen: hoge kosten, complex voor beginners, minimale storting €2.000. Verdict: beste voor professionals en vermogenden. Score: 4.2/5.""",

    """Schrijf over Trade Republic in 5 zinnen in het Nederlands voor een beleggingsapp-vergelijking.
    Wat: Duitse broker sinds 2015, sinds 2025 actief in Nederland. Kosten: €1 per transactie, €0 bij spaarplannen. Aanbod: 9.000+ aandelen/ETF's, fractionele spaarplannen, 2% rente op onbelegd cash. Voordelen: 2% rente op cash, eenvoudig, lage kosten, BaFin-gereguleerd, NL-IBAN. Nadelen: geen crypto, beperkte research, nieuw in NL dus beperkte track record. Verdict: beste voor rente op cash + beleggen. Score: 4.0/5.""",

    """Schrijf een Nederlandse conclusie van 2 paragrafen voor een beleggingsapp-vergelijking met aanbevelingen per type belegger.
    - Beginner: BUX
    - Indexbelegger: Meesman
    - Actieve trader: DEGIRO
    - Diversificatie: Trading 212
    - Social/copy trader: eToro
    - Professional: Saxo Bank
    - Cash-rente: Trade Republic
    Vloeiend, concluderend, praktisch advies.""",
]

def call_gemini(prompt):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}}
    for attempt in range(5):
        try:
            resp = requests.post(url, json=payload, timeout=60, headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                time.sleep(35*(attempt+1)); continue
            if resp.status_code in (503, 500):
                time.sleep(30); continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}")
                return None
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Ex: {e}"); time.sleep(15)
    return None

print("Generating beleggingsapps in segments...")
parts = []
for i, p in enumerate(prompts):
    print(f"  Part {i+1}/{len(prompts)}")
    result = call_gemini(p)
    if result:
        parts.append(result.strip())
    else:
        print(f"  FAILED part {i+1}")
        parts.append(f"[Sectie {i+1}]")
    time.sleep(1)

body = "\n\n".join(parts)

# Build full article
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

avg = round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1)
data = {
    "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
    "category": defn["category"], "rating": avg, "priceRange": defn["priceRange"],
    "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"],
    "cons": ["Prijzen kunnen wijzigen — check aanbieder", "Beleggen brengt risico's met zich mee", "Keuze hangt af van je specifieke situatie"],
    "affiliateLinks": ["https://www.beehiiv.com/"],
    "date": str(date.today()), "modelYear": 2026,
    "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
    "tools": defn["tools"], "related": pick_related(defn["slug"], 3),
    "draft": False,
    "faq": [
        {"q": "Wat is de beste broker voor beginners?", "a": "BUX is specifiek ontworpen voor beginners met fractionele aandelen vanaf €10 en een intuïtieve app. DEGIRO biedt meer diepgang met lagere kosten voor wie al wat ervaring heeft."},
        {"q": "Zijn er verborgen kosten bij 'gratis' brokers?", "a": "Veel 'gratis' brokers verdienen via spreads (prijsverschil tussen koop/verkoop), valutamarkups of payment-for-order-flow. Lees altijd de kleine lettertjes. DEGIRO en Meesman zijn het transparantst over hun kostenmodel."},
        {"q": "Hoeveel geld heb ik nodig om te starten met beleggen?", "a": "Bij BUX en Trading 212 kun je al vanaf €10 beginnen met fractionele aandelen. Meesman heeft een minimum van €100 per maand. DEGIRO heeft geen minimumbedrag, maar een heel aandeel moet je wel kunnen betalen."},
    ]
}
fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
article = f"---\n{fm}---\n\n{body}"

path = os.path.join(ARTICLES_DIR, f"{defn['slug']}.md")
with open(path, "w") as f:
    f.write(article)
print(f"\nWritten: {path} ({len(article)} chars, {len(article.splitlines())} lines)")
