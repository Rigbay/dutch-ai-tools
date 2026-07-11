#!/usr/bin/env python3
"""Generate 4 Dutch consumer comparison articles — June 11, 2026 cron. Underserved high-volume niches."""
import os, time, requests, yaml, sys
from datetime import date

# API key from .env (canonical source, not private/gemini-api-key)
env_path = os.path.expanduser("~/.hermes/.env")
API_KEY = None
with open(env_path) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.strip().split("=", 1)[1]
            break
if not API_KEY:
    print("FATAL: No GEMINI_API_KEY found in ~/.hermes/.env")
    sys.exit(1)

# Affiliate link resolver
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
from affiliate_resolver import resolve_affiliate_link, get_site_affiliate_links

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

    # Resolve per-tool affiliate links through merchants.json
    for tool in defn["tools"]:
        raw_link = tool.get("affiliateLink", "")
        resolved = resolve_affiliate_link(raw_link)
        if resolved:
            tool["affiliateLink"] = resolved
        # If no program exists, keep the plain URL (better than a dead/mismatched link)

    # Site-level affiliate links: for consumer articles, only beehiiv is relevant.
    # AI-tool programs (taskade, writesonic, etc.) don't belong on warmtepomp/laadpaal articles.
    site_links = ["https://www.beehiiv.com/"]

    data = {
        "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
        "category": defn["category"], "rating": avg, "priceRange": defn["priceRange"],
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"],
        "cons": ["Prijzen kunnen wijzigen — check aanbieder", "Subsidies en regels veranderen regelmatig", "Keuze hangt af van je specifieke situatie"],
        "affiliateLinks": site_links,
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste keuze?", "a": "Dat hangt af van je situatie. " + defn["tools"][0]["name"] + " is voor de meeste mensen een prima startpunt."},
            {"q": "Zijn er subsidies beschikbaar?", "a": "Ja, de Nederlandse overheid biedt verschillende subsidies en regelingen. Check de actuele stand op de RVO-website (rvo.nl) voor de nieuwste informatie."},
            {"q": "Hoe kies ik de juiste optie?", "a": "Begin met je use case en budget. Gebruik de vergelijkingstabel hierboven en lees de diepgaande reviews per optie."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"

TOPICS = [
    {
        "slug": "warmtepompen-vergelijken-2026-hybride-full-electric-lucht-water",
        "title": "Warmtepompen Vergelijken 2026: Hybride vs Full Electric vs Lucht-Water — Wat Past Bij Jouw Huis?",
        "description": "Warmtepomp kopen in 2026? Vergelijk hybride, volledig elektrische, lucht-water en bodemwarmtepompen op kosten, subsidie, rendement en geschiktheid voor jouw woning.",
        "category": "huis-tuin",
        "priceRange": "EUR 3.000-25.000 (incl. installatie)",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over warmtepompen vergelijken in 2026. Behandel precies 7 aanbieders/merken: WeHeat (Blackbird hybride), Quatt (hybride), Remeha (Elga Ace), Vaillant (aroTHERM), Daikin (Altherma), NIBE (lucht-water), Alpha Innotec (bodemwarmtepomp).

Structuur:
- Introductie: warmtepomp 2026 — gasprijs blijft volatiel, salderingsregeling afbouwt, ISDE-subsidie, hybrideplicht vanaf 2026? Wat betekent dit voor huiseigenaren
- Per oplossing een ## kop: type, geschikt voor (bouwjaar, isolatie), prijsindicatie (unit + installatie), ISDE-subsidie, terugverdientijd, geluidsniveau, plus- en minpunten, verdict
- Markdown vergelijkingstabel: merk/type, soort (hybride/full electric/bodem), prijsindicatie, ISDE-subsidie, geluidsniveau dB, geschikt voor woningtype, vermogen kW, score (1-5)
- Conclusie: voor appartement, jaren '30 woning, nieuwbouw, groot gezin, klein budget, maximale besparing
- 3 FAQ's

Nederlandse context: gasloos-doelstelling, hybride als tussenstap (Quatt populair in NL), ISDE-subsidie in 2026 (€1.950-4.500 afhankelijk van type/vermogen), salderingsregeling afbouw. WeHeat Blackbird is Nederlands. Vloeiend en toegankelijk Nederlands.""",
        "tools": [
            {"name": "Quatt Hybrid", "verdict": "Populairste hybride in NL — lage instap (€2.799), IoT-gestuurd, bespaart 70-80% gas", "priceRange": "€2.799 (excl. installatie)", "bestFor": "Bestaande woningen (jaren '60-'90)", "rating": 4.6, "affiliateLink": "https://quatt.io/"},
            {"name": "WeHeat Blackbird", "verdict": "Nederlands fabricaat — hybride én full-electric variant, open source aansturing", "priceRange": "€3.200-5.500", "bestFor": "Bewuste kopers / open source", "rating": 4.4, "affiliateLink": "https://weheat.nl/"},
            {"name": "Remeha Elga Ace", "verdict": "Beste hybride van traditioneel merk — 5 kW, stil (32 dB), BDR Thermea-groep", "priceRange": "€2.600-3.800 (excl. installatie)", "bestFor": "Betrouwbaarheid & Service", "rating": 4.5, "affiliateLink": "https://remeha.nl/"},
            {"name": "Vaillant aroTHERM", "verdict": "Beste full-electric lucht-water — 3-12 kW, stil, geschikt voor vloerverwarming", "priceRange": "€5.000-9.000 (excl. installatie)", "bestFor": "Full Electric / Nieuwbouw", "rating": 4.7, "affiliateLink": "https://vaillant.nl/"},
            {"name": "Daikin Altherma", "verdict": "Meest verkochte full-electric in Europa — 3-16 kW, uitgebreid dealernetwerk", "priceRange": "€5.500-10.000 (excl. installatie)", "bestFor": "Grote woningen", "rating": 4.6, "affiliateLink": "https://daikin.nl/"},
            {"name": "NIBE Lucht-Water", "verdict": "Premium Zweeds merk — S-serie extreem stil, tot 60°C aanvoertemperatuur, 20+ jaar garantie", "priceRange": "€7.000-13.000 (excl. installatie)", "bestFor": "Premium & Stil", "rating": 4.8, "affiliateLink": "https://nibe.nl/"},
            {"name": "Alpha Innotec Bodem", "verdict": "Hoogste rendement (COP 4.5+) — bodemwarmtepomp, stabiel jaarrond, hoge investering", "priceRange": "€15.000-25.000 (incl. boringen)", "bestFor": "Maximale Besparing", "rating": 4.3, "affiliateLink": "https://alpha-innotec.nl/"},
        ],
    },
    {
        "slug": "laadpalen-vergelijken-2026-thuislaadpaal-slimme-lader",
        "title": "Laadpalen Vergelijken 2026: Beste Thuislaadpaal en Slimme Lader voor Jouw Elektrische Auto",
        "description": "Thuislaadpaal kopen in 2026? Vergelijk Alfen, Zaptec, Wallbox, Easee, Smappee, Ratio en Myenergi op prijs, laadsnelheid, slimme functies en zonnepanelen-integratie.",
        "category": "huis-tuin",
        "priceRange": "EUR 500-2.500 (excl. installatie)",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over laadpalen/thuislaadstations vergelijken in 2026. Behandel precies 7 aanbieders: Alfen Eve Single Pro, Zaptec Go, Wallbox Pulsar Max, Easee Home, Smappee EV One, Ratio Electric iO7, Myenergi Zappi.

Structuur:
- Introductie: thuislaadpalen 2026 — EV-adoptie in NL (30%+ nieuwverkoop), salderingsregeling afbouw maakt slim laden met zonnepanelen interessanter, load balancing, dynamic pricing
- Per laadpaal een ## kop: beschrijving, max. laadvermogen (kW), load balancing, zonnepanelen-integratie, app/connectiviteit, prijs, plus- en minpunten, verdict
- Markdown vergelijkingstabel: merk, max. kW, fase (1/3), load balancing, solar charging, app-rating, prijsindicatie, score (1-5)
- Conclusie: voor zonnepanelen-bezitters, huurders, zakelijk, nieuwbouw, budget
- 3 FAQ's

Nederlandse context: Alfen is Nederlands (Almere), grootste netwerk. Zaptec populair in nieuwbouwprojecten. Myenergi Zappi beste solar-integratie. Easee is Noors design. Smappee meet op zekeringniveau. Laadpaalsubsidie in sommige gemeentes. Vloeiend en toegankelijk Nederlands.""",
        "tools": [
            {"name": "Alfen Eve Single Pro", "verdict": "Nederlands marktleider — robuust, load balancing, grootste installateursnetwerk, 3-fase tot 22 kW", "priceRange": "€800-1.200", "bestFor": "Betrouwbaarheid & Service", "rating": 4.7, "affiliateLink": "https://alfen.com/"},
            {"name": "Zaptec Go", "verdict": "Beste prijs-kwaliteit — compact, automatische fase-balancing, populair in nieuwbouw en VvE's", "priceRange": "€600-900", "bestFor": "Nieuwbouw & VvE", "rating": 4.6, "affiliateLink": "https://zaptec.com/"},
            {"name": "Wallbox Pulsar Max", "verdict": "Meest flexibel — 22 kW, Bluetooth/WiFi/4G, solar charging, compact design, uitgebreide app", "priceRange": "€750-1.100", "bestFor": "Flexibiliteit & Features", "rating": 4.5, "affiliateLink": "https://wallbox.com/"},
            {"name": "Easee Home", "verdict": "Beste design — Noors minimalisme, uniek Easy-Lock systeem, 3-fase tot 22 kW, app-integrated", "priceRange": "€700-1.000", "bestFor": "Design & Gebruiksgemak", "rating": 4.4, "affiliateLink": "https://easee.com/"},
            {"name": "Smappee EV One", "verdict": "Slimste energiemanagement — meet verbruik op zekeringniveau, dynamic load balancing, Nymea-app", "priceRange": "€900-1.400", "bestFor": "Slimme Energiesturing", "rating": 4.3, "affiliateLink": "https://smappee.com/"},
            {"name": "Ratio Electric iO7", "verdict": "Beste budget — Nederlands, 1-3 fase, load balancing, solar ready, vanaf €499", "priceRange": "€500-800", "bestFor": "Budgetbewust", "rating": 4.2, "affiliateLink": "https://ratio.nl/"},
            {"name": "Myenergi Zappi", "verdict": "Beste solar-integratie — drie eco-modes, laadt 100% op eigen zonnestroom, unieke CT-klem meting", "priceRange": "€900-1.500", "bestFor": "Zonnepanelen-bezitters", "rating": 4.6, "affiliateLink": "https://myenergi.com/"},
        ],
    },
    {
        "slug": "beleggingsapps-vergelijken-2026-degiro-bux-trading212-meesman",
        "title": "Beleggingsapps Vergelijken 2026: DEGIRO vs BUX vs Trading 212 vs Meesman vs eToro — Beste Broker voor Beginnende Beleggers",
        "description": "Beginnen met beleggen in 2026? Vergelijk DEGIRO, BUX, Trading 212, Meesman, eToro, Saxo en Trade Republic op kosten, gebruiksgemak, aanbod en Nederlandse dienstverlening.",
        "category": "persoonlijk",
        "priceRange": "EUR 0-5 per transactie (veel gratis)",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over beleggingsapps vergelijken in 2026. Behandel precies 7 aanbieders: DEGIRO, BUX, Trading 212, Meesman Indexbeleggen, eToro, Saxo Bank, Trade Republic.

Structuur:
- Introductie: beleggen 2026 — recordaantal Nederlandse particuliere beleggers (2+ miljoen), commission-free trading, indexbeleggen vs actief handelen, vermogensbelasting box 3, AI-gestuurde beleggingsadviezen
- Per broker een ## kop: beschrijving, kosten (transactie, valuta, custody), aanbod (aandelen/ETF's/opties/crypto), geschikt voor (beginners, gevorderden, passief), app-rating, AFM/DNB-gereguleerd, plus- en minpunten, verdict
- Markdown vergelijkingstabel: broker, transactiekosten, ETF-aanbod, crypto, fractionele aandelen, NL-dienstverlening, AFM-licentie, minimale inleg, score (1-5)
- Conclusie: voor beginners, indexbeleggers, actieve traders, crypto-interesse, grote portefeuilles, pensioenbeleggen
- 3 FAQ's

Nederlandse context: DEGIRO is Nederlands (Amsterdam), marktleider met AFM-licentie. BUX ook Nederlands (Amsterdam), focus op beginners met fractional shares. Meesman (Den Haag) voor passief indexbeleggen. eToro populair voor social/copy trading maar in Cyprus. Trade Republic (Duitsland, net in NL actief met 2% rente op cash). Box 3 belastingwijziging 2026. Vloeiend en toegankelijk Nederlands.""",
        "tools": [
            {"name": "DEGIRO", "verdict": "Beste allround broker — laagste kosten, grootste aanbod, AFM-gereguleerd, uitgebreide research", "priceRange": "€1,00 per transactie (€0 kernselectie ETF's)", "bestFor": "Serieuze Beleggers", "rating": 4.7, "affiliateLink": "https://degiro.nl/"},
            {"name": "BUX", "verdict": "Beste voor beginners — fractionele aandelen vanaf €10, Nederlands, intuïtieve app, zero commission", "priceRange": "€0 commissie op aandelen/ETF's", "bestFor": "Beginners", "rating": 4.4, "affiliateLink": "https://bux.com/"},
            {"name": "Trading 212", "verdict": "Breedste aanbod — 10.000+ instrumenten, fractioneel, gratis, automatische beleggingen (Pies)", "priceRange": "€0 commissie", "bestFor": "Diversificatie", "rating": 4.3, "affiliateLink": "https://trading212.com/"},
            {"name": "Meesman", "verdict": "Beste voor passief indexbeleggen — lage fondskosten, geen transactiekosten, Nederlands, automatisch", "priceRange": "0,4-0,5% fondskosten per jaar", "bestFor": "Indexbeleggen / Pensioen", "rating": 4.6, "affiliateLink": "https://meesman.nl/"},
            {"name": "eToro", "verdict": "Beste social trading — copy other traders, 5000+ assets, crypto + aandelen in één app", "priceRange": "€0 commissie op aandelen (€1 op crypto, spreads)", "bestFor": "Social & Copy Trading", "rating": 4.1, "affiliateLink": "https://etoro.com/"},
            {"name": "Saxo Bank", "verdict": "Beste voor professionals — 71.000+ instrumenten, institutionele research, opties/futures", "priceRange": "€2-8 per transactie", "bestFor": "Professionals & HNW", "rating": 4.2, "affiliateLink": "https://saxobank.nl/"},
            {"name": "Trade Republic", "verdict": "Beste rente op cash — 2% rente op onbelegd geld, €1 transacties, Duits, sinds 2025 actief in NL", "priceRange": "€1 per transactie (€0 spaarplannen)", "bestFor": "Rente op cash + beleggen", "rating": 4.0, "affiliateLink": "https://traderepublic.com/"},
        ],
    },
    {
        "slug": "rechtsbijstandverzekering-vergelijken-2026-achmea-arag-das-unive",
        "title": "Rechtsbijstandverzekering Vergelijken 2026: Achmea vs ARAG vs DAS vs Univé vs Rechtsbijstand — Beste Dekking & Laagste Premie",
        "description": "Rechtsbijstandverzekering afsluiten in 2026? Vergelijk Achmea, ARAG, DAS, Univé, Centraal Beheer, Nationale Nederlanden en OHRA op premie, dekking en vrije advocaatkeuze.",
        "category": "persoonlijk",
        "priceRange": "EUR 10-35 per maand",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over rechtsbijstandverzekeringen vergelijken in 2026. Behandel precies 7 verzekeraars: Achmea Rechtsbijstand, ARAG, DAS, Univé Rechtsbijstand, Centraal Beheer Achmea, Nationale-Nederlanden, OHRA Rechtsbijstand.

Structuur:
- Introductie: rechtsbijstand 2026 — 2,5 miljoen Nederlanders verzekerd, wachttijd vaak 3 maanden, conflict met buren/werkgever/verhuurder steeds vaker, jurdisch loket alternatief, modulair vs all-in
- Per verzekeraar een ## kop: dekking (consument/verkeer/wonen/arbeid), premie, vrije advocaatkeuze, eigen risico, wachttijd, geschillencommissie, plus- en minpunten, verdict
- Markdown vergelijkingstabel: verzekeraar, maandpremie (basis), modules, vrije advocaatkeuze, eigen risico, wachttijd, score (1-5)
- Conclusie: voor huurders, huiseigenaren, ondernemers, budgetbewust, maximale dekking, gezin met kinderen
- 3 FAQ's

Nederlandse context: ARAG en DAS zijn grootste pure rechtsbijstandsverzekeraars (geen schadeverzekering erbij). Achmea/Univé/Centraal Beheer zijn allround verzekeraars met stapelkorting. Vrije advocaatkeuze is wettelijk recht sinds 2015. Wachttijd: meeste verzekeraars 3 maanden voordat je claimt (om misbruik te voorkomen). Geschillencommissie (Kifid) voor klachten. Modulaire polissen (je kiest alleen wonen of alleen verkeer) zijn goedkoper. Vloeiend en toegankelijk Nederlands.""",
        "tools": [
            {"name": "ARAG", "verdict": "Grootste pure rechtsbijstand — 85+ jaar ervaring, eigen juristen in dienst, hoogste klanttevredenheid", "priceRange": "€14-28/mnd (modulair)", "bestFor": "Juridische Expertise", "rating": 4.6, "affiliateLink": "https://arag.nl/"},
            {"name": "DAS", "verdict": "Beste voor ondernemers — sterke module arbeidsrecht, mediation-specialist, eigen advocaten", "priceRange": "€15-32/mnd (modulair)", "bestFor": "Arbeidsrecht & Ondernemers", "rating": 4.5, "affiliateLink": "https://das.nl/"},
            {"name": "Achmea Rechtsbijstand", "verdict": "Breedste dekking met pakketkorting — combineer met Interpolis/Zilveren Kruis, modulair op te bouwen", "priceRange": "€12-25/mnd (modulair, excl. pakketkorting)", "bestFor": "All-in-One Verzekerd", "rating": 4.4, "affiliateLink": "https://achmea.nl/"},
            {"name": "Univé Rechtsbijstand", "verdict": "Beste prijs-kwaliteit met ledenkorting — coöperatief, geen winstoogmerk, hoge klanttevredenheid", "priceRange": "€11-22/mnd (modulair)", "bestFor": "Prijs-kwaliteit & Coöperatief", "rating": 4.3, "affiliateLink": "https://unive.nl/"},
            {"name": "Centraal Beheer", "verdict": "Laagste instappremie — vanaf €9,99/mnd, Even Apeldoorn bellen-model, modulair, pakketkorting", "priceRange": "€10-20/mnd (modulair)", "bestFor": "Budgetbewust", "rating": 4.1, "affiliateLink": "https://centraalbeheer.nl/"},
            {"name": "Nationale-Nederlanden", "verdict": "Uitgebreidste all-in dekking — standaard inclusief verkeer+wonen+consument, vrije advocaatkeuze", "priceRange": "€18-35/mnd (all-in)", "bestFor": "Maximale Dekking", "rating": 4.2, "affiliateLink": "https://nn.nl/"},
            {"name": "OHRA Rechtsbijstand", "verdict": "Flexibel en transparant — scherpe premie, duidelijke voorwaarden, onderdeel van DELTA LLOYD group", "priceRange": "€10-21/mnd (modulair)", "bestFor": "Transparantie & Flexibel", "rating": 4.0, "affiliateLink": "https://ohra.nl/"},
        ],
    },
]

def main():
    for i, topic in enumerate(TOPICS):
        print(f"[{i+1}/{len(TOPICS)}] {topic['slug']}")
        body = call_gemini(topic["prompt"])
        if not body:
            print(f"  FAILED to generate body for {topic['slug']}")
            continue
        article = build_article(topic, body)
        path = os.path.join(ARTICLES_DIR, f"{topic['slug']}.md")
        with open(path, "w") as f:
            f.write(article)
        print(f"  Written: {path} ({len(article)} chars)")
        time.sleep(2)  # gentle pacing between API calls

    print("\nDone. git status:")
    os.system("git status --short src/content/articles/ | head -20")

if __name__ == "__main__":
    main()
