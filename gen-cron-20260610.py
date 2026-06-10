#!/usr/bin/env python3
"""Generate 5 Dutch consumer comparison articles (June 10, 2026 cron)."""
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
        "category": defn["category"], "rating": avg, "priceRange": "EUR 0-100/mnd",
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"],
        "cons": ["Prijzen kunnen wijzigen — check aanbieder", "AI-features continu in ontwikkeling", "Keuze hangt af van je specifieke situatie"],
        "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste keuze?", "a": "Dat hangt af van je situatie. " + defn["tools"][0]["name"] + " is voor de meeste gebruikers een prima startpunt."},
            {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere opties hebben gratis tiers of proefperiodes. Perfect om te beginnen."},
            {"q": "Hoe kies ik de juiste optie?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"

TOPICS = [
    {
        "slug": "tikkie-vs-wiebetaaltwat-vs-splitwise-vs-bunq-2026",
        "title": "Tikkie vs WieBetaaltWat vs Splitwise vs bunq 2026: beste betaalverzoek-apps vergeleken",
        "description": "Tikkie, WieBetaaltWat, Splitwise of bunq in 2026? Vergelijk de beste Nederlandse betaalverzoek-apps op gemak, kosten, groepsfunctionaliteit en privacy.",
        "category": "persoonlijk",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Tikkie vs WieBetaaltWat vs Splitwise vs bunq in 2026. Behandel precies 7 apps/diensten: Tikkie, WieBetaaltWat, Splitwise, bunq (betaalverzoek), Payconiq, Knab Betalen & Verzoeken, Settle Up.

Structuur:
- Introductie: betaalverzoeken 2026 — Nederland loopt voorop met Tikkie (sinds 2016), 10+ miljoen gebruikers, groepsetentjes, vakanties, samenwonen
- Per tool een ## kop: beschrijving, prijs (gratis of kosten), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, gratis, groepsfunctionaliteit, herinneringen, export, bank-koppeling, score (1-5)
- Conclusie: voor groepsuitjes, samenwonen, vakanties, ondernemers, privacy-bewust, internationaal
- 3 FAQ's

Focus op Nederlandse context. Tikkie (ABN AMRO) dominant. WieBetaaltWat Nederlands alternatief met groepsboekhouding. Splitwise populair voor reizen/samenwonen. bunq met ingebouwde betaalverzoeken. Payconiq voor België grensverkeer. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Tikkie", "verdict": "De standaard in NL — 10M+ gebruikers, 1 minuut setup, via alle banken", "priceRange": "Gratis (geen extra kosten)", "bestFor": "Snelle betaalverzoeken", "rating": 4.8, "affiliateLink": "https://www.tikkie.nl/"},
            {"name": "WieBetaaltWat", "verdict": "Beste groepsboekhouding — automatisch verrekenen, export, ideaal voor samenwonen", "priceRange": "Gratis (basis), €2,99/mnd Premium", "bestFor": "Groepsboekhouding", "rating": 4.5, "affiliateLink": "https://wiebetaaltwat.nl/"},
            {"name": "Splitwise", "verdict": "Beste voor internationale groepen — multi-valuta, web + app, grootste community", "priceRange": "Gratis (basis), €4,99/mnd Pro", "bestFor": "Reizen & Internationaal", "rating": 4.4, "affiliateLink": "https://splitwise.com/"},
            {"name": "bunq", "verdict": "Betaalverzoeken direct in bankapp — request money zonder aparte app, realtime", "priceRange": "€2,99-17,99/mnd (bankrekening)", "bestFor": "All-in-one banking", "rating": 4.2, "affiliateLink": "https://bunq.com/"},
            {"name": "Payconiq", "verdict": "Beste voor Nederland-België — één app voor beide landen, QR-betalingen", "priceRange": "Gratis", "bestFor": "NL-BE grensverkeer", "rating": 4.0, "affiliateLink": "https://payconiq.nl/"},
            {"name": "Knab Betalen & Verzoeken", "verdict": "Zakelijke betaalverzoeken — ideaal voor ZZP'ers en kleine ondernemers met Knab-rekening", "priceRange": "€5-15/mnd (bankrekening)", "bestFor": "ZZP & Zakelijk", "rating": 3.9, "affiliateLink": "https://knab.nl/"},
            {"name": "Settle Up", "verdict": "Simpelste alternatief — offline modus, 15+ talen, handig voor backpackers", "priceRange": "Gratis (basis), €1,99 Premium", "bestFor": "Backpackers & Simpel", "rating": 3.8, "affiliateLink": "https://settleup.io/"},
        ],
    },
    {
        "slug": "online-boodschappen-vergelijken-picnic-ah-jumbo-crisp-2026",
        "title": "Online Boodschappen Vergelijken 2026: Picnic vs AH vs Jumbo vs Crisp vs Flink",
        "description": "Picnic, Albert Heijn Online, Jumbo, Crisp of Flink in 2026? Vergelijk de beste online boodschappendiensten op prijs, bezorgkosten, assortiment en duurzaamheid.",
        "category": "persoonlijk",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over online boodschappen vergelijken in 2026. Behandel precies 7 diensten: Picnic, Albert Heijn Online, Jumbo Online, Crisp, Flink, Getir/Gorillas (samengevoegd), Plus Online.

Structuur:
- Introductie: online boodschappen 2026 — flitsbezorgers geconsolideerd, Picnic gegroeid naar hele NL, AH/Jumbo met eigen platforms, duurzaamheid vs gemak
- Per dienst een ## kop: beschrijving, bezorgkosten, minimale bestelling, beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, bezorgkosten, bezorgtijd, assortiment, eigen merk focus, app-rating, score (1-5)
- Conclusie: voor prijsbewuste gezinnen, gemak/snel, duurzaamheid, lokaal, groot gezin, alleenstaand
- 3 FAQ's

Nederlandse context: Picnic (Nederlands, elektrisch, lage prijzen), AH Online (grootste assortiment), Jumbo (7 zekerheden), Crisp (seizoensproducten, kwaliteit), Flink (flitsbezorging <10min), Plus (lokaal, coöperatief). Vloeiend Nederlands.""",
        "tools": [
            {"name": "Picnic", "verdict": "Beste prijs-kwaliteit — elektrisch bezorgd, lage prijzen, gratis bezorging, eigen merk", "priceRange": "Gratis bezorging (geen min.bedrag)", "bestFor": "Prijsbewust & Duurzaam", "rating": 4.7, "affiliateLink": "https://picnic.app/"},
            {"name": "AH Online", "verdict": "Grootste assortiment — 20.000+ producten, Bonus-aanbiedingen, AH Premium voordelen", "priceRange": "€2,95-5,95 bezorging (€50 min.)", "bestFor": "Assortiment & Bonus", "rating": 4.5, "affiliateLink": "https://ah.nl/"},
            {"name": "Jumbo Online", "verdict": "7 Zekerheden ook online — prijsmatch, niet-goed-geld-terug, uitgebreid vers", "priceRange": "€3,95-5,95 bezorging (€50 min.)", "bestFor": "Klantgericht & Vers", "rating": 4.4, "affiliateLink": "https://jumbo.com/"},
            {"name": "Crisp", "verdict": "Beste kwaliteit — seizoensproducten van lokale leveranciers, 100% vers, geen ultra-bewerkt", "priceRange": "€4,99 bezorging (€40 min.)", "bestFor": "Kwaliteit & Seizoensproducten", "rating": 4.6, "affiliateLink": "https://crisp.nl/"},
            {"name": "Flink", "verdict": "Snelste bezorging — boodschappen in <10 minuten, 24/7 in steden, compact assortiment", "priceRange": "€1,99 bezorging (€10 min.)", "bestFor": "Snelheid & Gemak", "rating": 4.2, "affiliateLink": "https://flink.com/"},
            {"name": "Getir", "verdict": "Flitsbezorger met grootste dark-store netwerk — focus op steden, breed assortiment", "priceRange": "€1,99 bezorging (€10 min.)", "bestFor": "Stedelijke flitsbezorging", "rating": 3.9, "affiliateLink": "https://getir.com/"},
            {"name": "Plus Online", "verdict": "Coöperatieve supermarkt online — lokaal, vers, PLUS-recepten integratie", "priceRange": "€2,99-4,99 bezorging (€50 min.)", "bestFor": "Lokaal & Coöperatief", "rating": 4.0, "affiliateLink": "https://plus.nl/"},
        ],
    },
    {
        "slug": "ziggo-vs-kpn-vs-odido-vs-delta-glasvezel-2026",
        "title": "Ziggo vs KPN vs Odido vs Delta Glasvezel 2026: beste internet, tv en alles-in-1 provider",
        "description": "Ziggo, KPN, Odido of Delta in 2026? Vergelijk de beste Nederlandse providers voor internet, tv en alles-in-1 pakketten op snelheid, prijs en klantenservice.",
        "category": "persoonlijk",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over internet/tv providers vergelijken in 2026. Behandel precies 7 providers: Ziggo, KPN Glasvezel, Odido Glasvezel, Delta Glasvezel, Budget Alles-in-1 (Online.nl), Youfone Internet, Freedom Internet.

Structuur:
- Introductie: internet/tv 2026 — glasvezel dekt >90% NL, Ziggo DOCSIS 3.1 upgrade, 1-8 Gbps beschikbaar, streaming vs traditionele tv, alles-in-1 vs los afnemen
- Per provider een ## kop: beschrijving, prijs (EUR/mnd voor 1Gbps + tv), downloadsnelheid, beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, type netwerk, max downloadsnelheid, prijs 1Gbps+tv, opzegtermijn, klantenservice-score, score (1-5)
- Conclusie: voor snelheid, prijs, klantenservice, glasvezel-only, budget, privacy-bewust
- 3 FAQ's

Focus op Nederlandse markt — Ziggo (VodafoneZiggo, coax + glas), KPN (marktleider glasvezel), Odido (voorheen T-Mobile, agressief geprijsd), Delta (Zeeuws, uitbreidend), Freedom (privacy-first, XS4ALL-erfenis). Vloeiend Nederlands.""",
        "tools": [
            {"name": "Ziggo", "verdict": "Breedste dekking — DOCSIS 3.1 + glasvezel, 1 Gbps download, Ziggo GO app overal", "priceRange": "€35-75/mnd (internet+tv)", "bestFor": "Beschikbaarheid & Ziggo Sport", "rating": 4.3, "affiliateLink": "https://ziggo.nl/"},
            {"name": "KPN Glasvezel", "verdict": "Beste glasvezelnetwerk — 8 Gbps op top-locaties, KPN TV+ box, sterkste klantenservice", "priceRange": "€40-80/mnd (internet+tv)", "bestFor": "Snelheid & Betrouwbaarheid", "rating": 4.6, "affiliateLink": "https://kpn.com/"},
            {"name": "Odido Glasvezel", "verdict": "Scherpste prijzen — 1 Gbps vanaf €27,50, 8 Gbps op geselecteerde adressen, simpele bundels", "priceRange": "€27,50-65/mnd (internet+tv)", "bestFor": "Prijs-kwaliteit", "rating": 4.4, "affiliateLink": "https://odido.nl/"},
            {"name": "Delta Glasvezel", "verdict": "Beste regionale provider — Zeeuws/Vlaams/Drenthe, 8 Gbps, sterke lokale klantenservice", "priceRange": "€30-70/mnd (internet+tv)", "bestFor": "Regio & Snelheid", "rating": 4.5, "affiliateLink": "https://delta.nl/"},
            {"name": "Online.nl", "verdict": "Beste budget alles-in-1 — vanaf €25 voor 100 Mbps + tv, goede basis voor kleine huishoudens", "priceRange": "€25-45/mnd (internet+tv)", "bestFor": "Budget & Kleine huishoudens", "rating": 4.0, "affiliateLink": "https://online.nl/"},
            {"name": "Youfone Internet", "verdict": "Beste maandcontract — geen jaarcontract, KPN-netwerk, scherpe tarieven, simpele pakketten", "priceRange": "€30-55/mnd (internet+tv)", "bestFor": "Flexibiliteit", "rating": 4.1, "affiliateLink": "https://youfone.nl/"},
            {"name": "Freedom Internet", "verdict": "Beste privacy-first — XS4ALL-opvolger, geen datacaps, uitstekende helpdesk, idealistisch", "priceRange": "€42-75/mnd (internet+tv)", "bestFor": "Privacy & Idealisme", "rating": 4.3, "affiliateLink": "https://freedominternet.nl/"},
        ],
    },
    {
        "slug": "zorgverzekering-vergelijken-2026-zilveren-kruis-cz-vgz-menzis",
        "title": "Zorgverzekering Vergelijken 2026: Zilveren Kruis vs CZ vs VGZ vs Menzis vs Ditzo",
        "description": "Zilveren Kruis, CZ, VGZ, Menzis of Ditzo in 2026? Vergelijk de beste Nederlandse zorgverzekeringen op prijs, dekking, vrije zorgkeuze en aanvullende pakketten.",
        "category": "persoonlijk",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over zorgverzekeringen vergelijken in 2026. Behandel precies 7 verzekeraars/labels: Zilveren Kruis, CZ, VGZ, Menzis, Ditzo, FBTO, Anderzorg.

Structuur:
- Introductie: zorgverzekering 2026 — basispakket wettelijk gelijk, premieverschillen €20-40/mnd, naturapolis vs restitutiepolis, eigen risico €385 (onveranderd), aanvullende verzekeringen
- Per verzekeraar een ## kop: beschrijving, prijs (EUR/mnd basisverzekering), vrije zorgkeuze, aanvullende pakketten, beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, basispremie (EUR/mnd, max eigen risico), type polis, vrije zorgkeuze, tandartsdekking, app-rating, score (1-5)
- Conclusie: voor budget, vrije zorgkeuze, tandarts, fysio, gezin, student, chronisch
- 3 FAQ's

Focus op Nederlandse zorgstelsel. Prijzen realistisch voor 2026 (basispremie €145-165/mnd). Naturapolis vs restitutie. Labels onder één concern: Ditzo (ASR), FBTO (Achmea), Anderzorg (CZ). Vloeiend Nederlands.""",
        "tools": [
            {"name": "Zilveren Kruis", "verdict": "Grootste verzekeraar — breed geaccepteerd, sterke app, uitgebreide aanvullende pakketten", "priceRange": "€147,50-162,50/mnd basis", "bestFor": "Zekerheid & Keuzevrijheid", "rating": 4.3, "affiliateLink": "https://zilverenkruis.nl/"},
            {"name": "CZ", "verdict": "Beste zorginkoop — sterke regionale netwerken, goede fysio-dekking, Zuid-NL focus", "priceRange": "€145,50-160,50/mnd basis", "bestFor": "Regionale zorg & Fysio", "rating": 4.4, "affiliateLink": "https://cz.nl/"},
            {"name": "VGZ", "verdict": "Beste voor gezinnen — ruime tandarts-dekking, Mindfulness Coach app, Preventiebudget", "priceRange": "€146,00-161,00/mnd basis", "bestFor": "Gezinnen & Preventie", "rating": 4.2, "affiliateLink": "https://vgz.nl/"},
            {"name": "Menzis", "verdict": "Beste klanttevredenheid — SamenGezond platform, sterke ouderenzorg focus, noordoost NL", "priceRange": "€146,50-160,00/mnd basis", "bestFor": "Klanttevredenheid & Oost-NL", "rating": 4.3, "affiliateLink": "https://menzis.nl/"},
            {"name": "Ditzo", "verdict": "Beste prijs-kwaliteit — online label ASR, lage premie, goede basis, snelle digitale service", "priceRange": "€138,50-152,00/mnd basis", "bestFor": "Budget & Digitaal", "rating": 4.0, "affiliateLink": "https://ditzo.nl/"},
            {"name": "FBTO", "verdict": "Scherpste online premie — Achmea-label, flexibele aanvullende modules, goedkoopste basis", "priceRange": "€137,00-150,00/mnd basis", "bestFor": "Laagste premie", "rating": 3.9, "affiliateLink": "https://fbto.nl/"},
            {"name": "Anderzorg", "verdict": "Beste studenten — CZ-label met lage premie, eenvoudige modules, goede studentendekking", "priceRange": "€139,00-153,00/mnd basis", "bestFor": "Studenten & Jongeren", "rating": 4.1, "affiliateLink": "https://anderzorg.nl/"},
        ],
    },
    {
        "slug": "vakantieparken-vergelijken-center-parcs-landal-roompot-2026",
        "title": "Vakantieparken Vergelijken 2026: Center Parcs vs Landal vs Roompot vs EuroParcs",
        "description": "Center Parcs, Landal, Roompot of EuroParcs in 2026? Vergelijk de beste Nederlandse vakantieparken op prijs, faciliteiten, kindvriendelijkheid en last-minute aanbiedingen.",
        "category": "persoonlijk",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over vakantieparken vergelijken in 2026. Behandel precies 7 ketens: Center Parcs, Landal GreenParks, Roompot, EuroParcs, Droomparken, Summio Parcs, TopParken.

Structuur:
- Introductie: vakantieparken 2026 — populairder dan ooit (staycation trend), prijzen gestegen, last-minute deals, luxe cottages en tiny houses trends, hondvriendelijk
- Per keten een ## kop: beschrijving, prijs (EUR/nacht buiten hoogseizoen), faciliteiten (zwembad, wellness, horeca), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, aantal parken in NL, gem. prijs/nacht laagseizoen, zwembad, hondvriendelijk, kids-faciliteiten, score (1-5)
- Conclusie: voor tropisch zwemparadijs, natuur, budget, luxe, gezinnen, rustzoekers, last-minute, hondenbezitters
- 3 FAQ's

Focus op Nederland. Center Parcs (Aqua Mundo, tropisch zwembad), Landal (natuur, duurzaam), Roompot (grootste aanbod, budget), EuroParcs (design, luxe). Prijzen realistisch 2026. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Center Parcs", "verdict": "Beste zwemparadijs — Aqua Mundo subtropisch zwembad, Market Dome, indoor activiteiten het hele jaar", "priceRange": "€150-450/nacht (4-persoons)", "bestFor": "Subtropisch zwembad & Activiteiten", "rating": 4.5, "affiliateLink": "https://centerparcs.nl/"},
            {"name": "Landal GreenParks", "verdict": "Beste natuur — rustige parken in bos/groen, duurzame cottages, wandel/fiets focus", "priceRange": "€100-350/nacht (4-persoons)", "bestFor": "Natuur & Rust", "rating": 4.4, "affiliateLink": "https://landal.nl/"},
            {"name": "Roompot", "verdict": "Grootste aanbod — 200+ parken, breed prijsbereik, sterke last-minute aanbiedingen", "priceRange": "€80-300/nacht (4-persoons)", "bestFor": "Keuze & Budget", "rating": 4.2, "affiliateLink": "https://roompot.nl/"},
            {"name": "EuroParcs", "verdict": "Beste design — luxe architectuurcottages, wellness-opties, mooiste waterliggingen", "priceRange": "€120-400/nacht (4-persoons)", "bestFor": "Luxe & Design", "rating": 4.3, "affiliateLink": "https://europarcs.nl/"},
            {"name": "Droomparken", "verdict": "Beste prijs-kwaliteit — knusse parken, bosrijke liggingen, gezellige centrumvoorzieningen", "priceRange": "€75-250/nacht (4-persoons)", "bestFor": "Budget & Knus", "rating": 4.0, "affiliateLink": "https://droomparken.nl/"},
            {"name": "Summio Parcs", "verdict": "Beste voor rustzoekers — kleinschalige parken, wellness cottages, adult-only opties", "priceRange": "€90-280/nacht (4-persoons)", "bestFor": "Wellness & Adult-only", "rating": 4.1, "affiliateLink": "https://summioparcs.nl/"},
            {"name": "TopParken", "verdict": "Beste hondvriendelijk — uitgebreide faciliteiten voor honden, omheinde tuinen, losloopgebieden", "priceRange": "€85-275/nacht (4-persoons)", "bestFor": "Hondvriendelijk & Recreatie", "rating": 4.0, "affiliateLink": "https://topparken.nl/"},
        ],
    },
]

gen = 0
for i, d in enumerate(TOPICS):
    out = os.path.join(ARTICLES_DIR, f"{d['slug']}.md")
    print(f"[{i+1}/5] {d['slug']}")
    if os.path.exists(out):
        print(f"  Skip — exists")
        continue
    body = call_gemini(d["prompt"])
    if body is None:
        print(f"  FAILED")
        continue
    full = build_article(d, body)
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)
    gen += 1
    print(f"  OK — {len(body.split())} words")
    if i < len(TOPICS) - 1:
        time.sleep(12)

print(f"\n=== {gen}/5 generated ===")
