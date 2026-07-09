#!/usr/bin/env python3
"""Generate 5 Dutch consumer comparison articles — July 9, 2026 cron. V6: Ollama fallback."""
import os, time, requests, json, sys, re
from datetime import date

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b"  # Fast, capable, good multilingual
ARTICLES_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    return [s for s in slugs if s != new_slug][:n]

def call_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 4096}
    }
    for attempt in range(3):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                time.sleep(10)
                continue
            return resp.json()["response"]
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(10)
    return None

def parse_response(raw):
    """Parse response with ===BODY=== delimiter."""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        raw = "\n".join(lines)
    
    parts = raw.split("===BODY===")
    if len(parts) < 2:
        for delim in ["---BODY---", "###BODY###", "***BODY***"]:
            parts = raw.split(delim)
            if len(parts) >= 2:
                break
    
    if len(parts) < 2:
        print("  No BODY delimiter found")
        return None
    
    json_part = parts[0].strip()
    body_part = parts[1].strip()
    
    if json_part.endswith("```"):
        json_part = json_part[:-3].strip()
    
    # Fix JSON string
    fixed = []
    in_str = False
    esc = False
    for ch in json_part:
        if esc:
            fixed.append(ch); esc = False; continue
        if ch == '\\':
            fixed.append(ch); esc = True; continue
        if ch == '"':
            in_str = not in_str; fixed.append(ch); continue
        if in_str and ch == '\n':
            fixed.append('\\n')
        elif in_str and ch == '\r':
            fixed.append('\\r')
        elif in_str and ch == '\t':
            fixed.append('\\t')
        else:
            fixed.append(ch)
    
    try:
        data = json.loads(''.join(fixed))
        data["body"] = body_part
        return data
    except json.JSONDecodeError as e:
        print(f"  JSON parse failed at pos {e.pos}: {''.join(fixed)[max(0,e.pos-50):e.pos+50]}")
        return None

def write_article(data, slug):
    today = date.today().isoformat()
    
    fm = "---\n"
    fm += f"title: '{data['title']}'\n"
    fm += f"slug: {slug}\n"
    fm += f"description: '{data['description']}'\n"
    fm += f"category: {data['category']}\n"
    fm += f"rating: {data['rating']}\n"
    fm += f"priceRange: {data['priceRange']}\n"
    fm += "pros:\n"
    for p in data.get('pros', []):
        fm += f"- {p}\n"
    fm += "cons:\n"
    for c in data.get('cons', []):
        fm += f"- {c}\n"
    fm += "affiliateLinks:\n"
    for link in data.get('affiliateLinks', []):
        fm += f"  - {link}\n"
    fm += f"date: {today}\n"
    fm += f"modelYear: 2026\n"
    fm += f"featuredTool: {data.get('featuredTool', data['tools'][0]['name'])}\n"
    fm += f"readingTime: {data.get('readingTime', '8 min')}\n"
    fm += "tools:\n"
    for t in data['tools']:
        fm += f"- name: {t['name']}\n"
        fm += f"  verdict: {t['verdict']}\n"
        fm += f"  priceRange: {t['priceRange']}\n"
        fm += f"  bestFor: {t['bestFor']}\n"
        fm += f"  rating: {t['rating']}\n"
        fm += f"  affiliateLink: {t['affiliateLink']}\n"
    
    related = pick_related(slug, 3)
    fm += "related:\n"
    for r in related:
        fm += f"  - {r}\n"
    fm += "draft: false\n"
    fm += "faq:\n"
    for faq in data.get('faq', []):
        fm += f"- q: \"{faq['q']}\"\n"
        fm += f"  a: '{faq['a']}'\n"
    fm += "---\n\n"
    
    full = fm + data['body']
    
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(path, 'w') as f:
        f.write(full)
    print(f"  Written: {path} ({len(full)} chars)")
    return True

# ===== ARTICLE DEFINITIONS =====

ARTICLES = [
    {
        "slug": "dating-apps-vergelijken-2026-tinder-bumble-happn-breeze",
        "prompt": """Je bent een Nederlandse consumentenjournalist. Schrijf een diepgaand vergelijkingsartikel over de beste dating apps in Nederland in 2026.

VERGELIJK DEZE 6 TOOLS:
1. Tinder — de grootste, swipe-gebaseerd, EUR 0-25/mnd
2. Bumble — vrouwen maken eerste zet, EUR 0-33/mnd
3. Happn — locatie-gebaseerd, kruist paden, EUR 0-25/mnd
4. Breeze — geen chat, meteen op date, EUR 0 per match (betaal per date)
5. Lexa.nl — Nederlandse dating site met app, EUR 0-30/mnd
6. Inner Circle — selectief, screening, EUR 0-40/mnd

OUTPUT FORMAT:
Eerst een JSON metadata blok, dan ===BODY===, dan de volledige markdown body.

JSON metadata:
{
  "title": "Beste Dating Apps 2026: Tinder vs Bumble vs Happn vs Breeze — Welke Past Bij Jou?",
  "description": "Vergelijking van de 6 beste dating apps in Nederland in 2026. Eerlijke scores, prijzen en verdicts voor Tinder, Bumble, Happn, Breeze, Lexa en Inner Circle.",
  "category": "persoonlijk",
  "rating": 4.3,
  "priceRange": "EUR 0-40/mnd",
  "pros": [
    "Eerlijke 2026 vergelijking van de populairste dating apps in Nederland",
    "Duidelijke prijsranges, scores en verdicts per app",
    "Nederlandstalig en praktijkgericht advies met FAQ"
  ],
  "cons": [
    "Prijzen kunnen wijzigen — check altijd de actuele aanbieder",
    "Niet elke app is dagelijks getest met intensief gebruik",
    "Ervaringen verschillen per stad en leeftijdsgroep"
  ],
  "affiliateLinks": [
    "https://tinder.com/?ref=aitoolsnl"
  ],
  "featuredTool": "Breeze",
  "readingTime": "9 min",
  "tools": [
    {"name": "Tinder", "verdict": "Grootste gebruikersbestand in Nederland — beste kans op matches, maar veel oppervlakkig swipen", "priceRange": "EUR 0-25/mnd", "bestFor": "Maximale matches en keuzevrijheid", "rating": 4.2, "affiliateLink": "https://tinder.com/?ref=aitoolsnl"},
    {"name": "Bumble", "verdict": "Vrouwen maken eerste zet — minder druk op mannen, kwalitatief betere gesprekken", "priceRange": "EUR 0-33/mnd", "bestFor": "Vrouwen die controle willen, mannen die minder afwijzing ervaren", "rating": 4.3, "affiliateLink": "https://bumble.com/?ref=aitoolsnl"},
    {"name": "Happn", "verdict": "Uniek locatie-concept — je ziet mensen die je in het echt bent tegengekomen, romantisch maar kleiner bereik", "priceRange": "EUR 0-25/mnd", "bestFor": "Stedelingen die spontane ontmoetingen willen digitaliseren", "rating": 3.8, "affiliateLink": "https://www.happn.com/?ref=aitoolsnl"},
    {"name": "Breeze", "verdict": "Meest innovatief — geen chat, meteen op date. Filtert tijdverspillers eruit maar minder controle vooraf", "priceRange": "EUR 0 + datekosten", "bestFor": "Serieuze daters die geen zin hebben in eindeloos chatten", "rating": 4.4, "affiliateLink": "https://breeze.social/?ref=aitoolsnl"},
    {"name": "Lexa.nl", "verdict": "Grootste Nederlandse datingplatform — serieuze gebruikers, maar interface voelt gedateerd", "priceRange": "EUR 0-30/mnd", "bestFor": "30+ daters die een serieuze relatie zoeken in Nederland", "rating": 3.9, "affiliateLink": "https://www.lexa.nl/?ref=aitoolsnl"},
    {"name": "Inner Circle", "verdict": "Meest exclusief — screening houdt kwaliteit hoog, maar wachtlijst en hoge prijs zijn drempels", "priceRange": "EUR 0-40/mnd", "bestFor": "Hoogopgeleide professionals die kwaliteit boven kwantiteit stellen", "rating": 4.1, "affiliateLink": "https://www.theinnercircle.co/?ref=aitoolsnl"}
  ],
  "faq": [
    {"q": "Welke dating app heeft de meeste gebruikers in Nederland in 2026?", "a": "Tinder heeft nog steeds het grootste gebruikersbestand in Nederland, gevolgd door Bumble. Voor serieuze relaties is Lexa.nl het grootste Nederlandse platform."},
    {"q": "Wat is de beste gratis dating app?", "a": "Tinder en Bumble bieden de beste gratis ervaring met voldoende functionaliteit. Breeze is gratis te gebruiken — je betaalt alleen per date die je afspreekt."},
    {"q": "Welke dating app is het beste voor een serieuze relatie?", "a": "Lexa.nl, Breeze en Inner Circle richten zich het meest op serieuze relaties. Bumble heeft ook een relatie-modus. Tinder is meer casual, maar wordt ook voor relaties gebruikt."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (2000+ woorden) met:
- Een pakkende introductie over dating apps in Nederland in 2026
- Per tool: een sectie met Wat het is, Voor wie, Pluspunten (5), Minpunten (4-5)
- Een vergelijkingstabel (markdown table) met alle 6 tools
- Een "Welke app past bij jou?" sectie met aanbevelingen per type dater
- Een conclusie
- Gebruik Nederlandse voorbeelden, prijzen in EUR, en noem specifieke NL-context (Randstad vs platteland, studenten vs professionals)
- Schrijf in een toegankelijke, nuchtere Nederlandse stijl — geen marketingtaal"""
    },
    {
        "slug": "budget-apps-vergelijken-2026-dyme-flow-spendee-ynab",
        "prompt": """Je bent een Nederlandse consumentenjournalist. Schrijf een diepgaand vergelijkingsartikel over de beste budget apps in Nederland in 2026.

VERGELIJK DEZE 6 TOOLS:
1. Dyme — Nederlandse app, koppelt bankrekeningen, inzicht in abonnementen, EUR 0-4/mnd
2. Flow (voorheen Spendle) — Nederlands, automatisch categoriseren, EUR 0-3/mnd
3. YNAB (You Need A Budget) — zero-based budgeting, EUR 15/mnd of 99/jaar
4. Spendee — shared wallets voor huishoudens, EUR 0-5/mnd
5. Grip (ABN AMRO) — gratis voor ABN klanten, automatische categorisatie
6. Wallet by BudgetBakers — bankkoppeling, multi-currency, EUR 0-5/mnd

OUTPUT FORMAT:
Eerst een JSON metadata blok, dan ===BODY===, dan de volledige markdown body.

JSON metadata:
{
  "title": "Beste Budget Apps 2026: Dyme vs Flow vs YNAB vs Spendee — Grip op Je Geld",
  "description": "Vergelijking van de 6 beste budget apps in Nederland in 2026. Eerlijke scores, prijzen en verdicts voor Dyme, Flow, YNAB, Spendee, Grip en Wallet by BudgetBakers.",
  "category": "persoonlijk",
  "rating": 4.4,
  "priceRange": "EUR 0-15/mnd",
  "pros": [
    "Eerlijke 2026 vergelijking van de beste budget apps voor Nederlandse gebruikers",
    "Duidelijke prijsranges, scores en verdicts per app",
    "Nederlandstalig en praktijkgericht advies met FAQ"
  ],
  "cons": [
    "Prijzen kunnen wijzigen — check altijd de actuele aanbieder",
    "Niet elke app is dagelijks getest met intensief gebruik",
    "Bankkoppelingen kunnen per bank verschillen in kwaliteit"
  ],
  "affiliateLinks": [
    "https://dyme.app/?ref=aitoolsnl"
  ],
  "featuredTool": "Dyme",
  "readingTime": "8 min",
  "tools": [
    {"name": "Dyme", "verdict": "Beste Nederlandse budget app — automatische abonnementendetectie en bankkoppeling maken het de meest complete keuze", "priceRange": "EUR 0-4/mnd", "bestFor": "Nederlanders die grip willen op abonnementen én uitgaven", "rating": 4.5, "affiliateLink": "https://dyme.app/?ref=aitoolsnl"},
    {"name": "Flow", "verdict": "Sterk in automatisch categoriseren — Nederlandse app die slim leert van je uitgavenpatroon", "priceRange": "EUR 0-3/mnd", "bestFor": "Gebruikers die minimale handmatige invoer willen", "rating": 4.2, "affiliateLink": "https://flowyour.money/?ref=aitoolsnl"},
    {"name": "YNAB", "verdict": "Gouden standaard voor zero-based budgeting — duur maar ongeëvenaard in methodiek en educatie", "priceRange": "EUR 15/mnd", "bestFor": "Serieuze budgetteerders die hun financiële mindset willen veranderen", "rating": 4.6, "affiliateLink": "https://www.ynab.com/?ref=aitoolsnl"},
    {"name": "Spendee", "verdict": "Beste voor huishoudens — shared wallets maken gezamenlijk budgetteren eenvoudig", "priceRange": "EUR 0-5/mnd", "bestFor": "Stellen en gezinnen die samen budgetteren", "rating": 4.0, "affiliateLink": "https://www.spendee.com/?ref=aitoolsnl"},
    {"name": "Grip (ABN AMRO)", "verdict": "Gratis en automatisch voor ABN klanten — beperkt maar voldoende voor basaal inzicht", "priceRange": "EUR 0 (ABN klanten)", "bestFor": "ABN AMRO klanten die snel inzicht willen zonder extra app", "rating": 3.8, "affiliateLink": "https://www.abnamro.nl/nl/prive/betalen/grip/index.html?ref=aitoolsnl"},
    {"name": "Wallet by BudgetBakers", "verdict": "Meest flexibel — multi-currency en uitgebreide rapportages, maar bankkoppeling in NL wisselend", "priceRange": "EUR 0-5/mnd", "bestFor": "Gebruikers met internationale financiën of meerdere valuta", "rating": 4.1, "affiliateLink": "https://budgetbakers.com/?ref=aitoolsnl"}
  ],
  "faq": [
    {"q": "Welke budget app werkt het beste met Nederlandse banken?", "a": "Dyme en Flow zijn specifiek gebouwd voor de Nederlandse markt en hebben de beste PSD2-koppelingen met Nederlandse banken. Grip werkt alleen met ABN AMRO."},
    {"q": "Is YNAB de hoge prijs waard?", "a": "Voor serieuze budgetteerders die hun financiële gedrag willen veranderen: ja. De zero-based methode en educatie zijn ongeëvenaard. Voor alleen inzicht in uitgaven zijn Dyme of Flow voldoende."},
    {"q": "Kan ik een budget app koppelen aan een gezamenlijke rekening?", "a": "Ja, Spendee en Wallet by BudgetBakers ondersteunen shared wallets. Dyme kan ook meerdere rekeningen koppelen maar is minder gericht op gezamenlijk budgetteren."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (2000+ woorden) met:
- Een pakkende introductie over budgetteren in Nederland in 2026 (inflatie, energieprijzen, waarom budget apps relevanter zijn dan ooit)
- Per tool: een sectie met Wat het is, Voor wie, Pluspunten (5), Minpunten (4-5)
- Een vergelijkingstabel (markdown table) met alle 6 tools
- Een "Welke app past bij jou?" sectie met aanbevelingen per type gebruiker (student, gezin, freelancer, belegger)
- Een conclusie
- Gebruik Nederlandse voorbeelden, prijzen in EUR, en noem specifieke NL-context (IBAN-koppeling, PSD2, Nederlandse banken)
- Schrijf in een toegankelijke, nuchtere Nederlandse stijl — geen marketingtaal"""
    },
    {
        "slug": "taal-apps-vergelijken-2026-duolingo-babbel-busuu-memrise",
        "prompt": """Je bent een Nederlandse consumentenjournalist. Schrijf een diepgaand vergelijkingsartikel over de beste taal leer apps in 2026.

VERGELIJK DEZE 6 TOOLS:
1. Duolingo — gamified, gratis, grootste talenaanbod, EUR 0-14/mnd (Super)
2. Babbel — gestructureerde lessen, focus op conversatie, EUR 0-14/mnd
3. Busuu — community feedback van native speakers, EUR 0-12/mnd
4. Memrise — focus op vocabulaire met echte video's, EUR 0-9/mnd
5. Mondly — AR/VR features, 41 talen, EUR 0-10/mnd
6. Preply — 1-op-1 live tutoring met native speakers, EUR 10-40/uur

OUTPUT FORMAT:
Eerst een JSON metadata blok, dan ===BODY===, dan de volledige markdown body.

JSON metadata:
{
  "title": "Beste Taal Apps 2026: Duolingo vs Babbel vs Busuu vs Memrise — Welke Leert Je Echt een Taal?",
  "description": "Vergelijking van de 6 beste taal leer apps in 2026. Eerlijke scores, prijzen en verdicts voor Duolingo, Babbel, Busuu, Memrise, Mondly en Preply.",
  "category": "persoonlijk",
  "rating": 4.5,
  "priceRange": "EUR 0-40/uur",
  "pros": [
    "Eerlijke 2026 vergelijking van de populairste taal leer apps",
    "Duidelijke prijsranges, scores en verdicts per app",
    "Nederlandstalig en praktijkgericht advies met FAQ"
  ],
  "cons": [
    "Prijzen kunnen wijzigen — check altijd de actuele aanbieder",
    "Niet elke app is dagelijks getest met intensief gebruik",
    "Leerresultaten verschillen sterk per persoon en doeltaal"
  ],
  "affiliateLinks": [
    "https://www.duolingo.com/?ref=aitoolsnl"
  ],
  "featuredTool": "Babbel",
  "readingTime": "9 min",
  "tools": [
    {"name": "Duolingo", "verdict": "Beste gratis optie — gamification maakt leren verslavend, maar brengt je niet verder dan A2/B1 niveau", "priceRange": "EUR 0-14/mnd", "bestFor": "Beginners die een taal willen proeven zonder kosten", "rating": 4.3, "affiliateLink": "https://www.duolingo.com/?ref=aitoolsnl"},
    {"name": "Babbel", "verdict": "Beste voor conversatie — gestructureerde lessen met realistische dialogen, ontwikkeld door taalkundigen", "priceRange": "EUR 0-14/mnd", "bestFor": "Reizigers en expats die snel praktisch willen kunnen praten", "rating": 4.5, "affiliateLink": "https://www.babbel.com/?ref=aitoolsnl"},
    {"name": "Busuu", "verdict": "Unieke community-feedback — native speakers corrigeren je oefeningen, McGraw-Hill gecertificeerd", "priceRange": "EUR 0-12/mnd", "bestFor": "Leerders die echte feedback willen van moedertaalsprekers", "rating": 4.4, "affiliateLink": "https://www.busuu.com/?ref=aitoolsnl"},
    {"name": "Memrise", "verdict": "Beste voor vocabulaire — korte video's van locals maken woorden memorabel, maar grammatica is beperkt", "priceRange": "EUR 0-9/mnd", "bestFor": "Visuele leerders die snel woordenschat willen opbouwen", "rating": 4.1, "affiliateLink": "https://www.memrise.com/?ref=aitoolsnl"},
    {"name": "Mondly", "verdict": "Meest innovatief — AR en VR maken leren interactief, maar diepgang is beperkt vergeleken met Babbel/Busuu", "priceRange": "EUR 0-10/mnd", "bestFor": "Tech-liefhebbers die taal leren via AR/VR willen ervaren", "rating": 3.9, "affiliateLink": "https://www.mondly.com/?ref=aitoolsnl"},
    {"name": "Preply", "verdict": "Beste voor serieuze leerders — 1-op-1 tutoring met native speakers, duur maar meest effectief", "priceRange": "EUR 10-40/uur", "bestFor": "Gemotiveerde leerders die snel vloeiend willen worden", "rating": 4.6, "affiliateLink": "https://preply.com/?ref=aitoolsnl"}
  ],
  "faq": [
    {"q": "Welke taal app is het beste om Nederlands te leren?", "a": "Voor Nederlands als tweede taal zijn Babbel en Busuu de beste keuzes — beide hebben gestructureerde NT2-programma's. Preply biedt 1-op-1 lessen met Nederlandse docenten."},
    {"q": "Kan ik echt een taal leren met alleen een app?", "a": "Apps brengen je tot A2/B1 niveau (basisconversatie). Voor vloeiendheid (B2/C1) heb je aanvullende methoden nodig zoals tutoring (Preply), taalcursussen of onderdompeling."},
    {"q": "Welke app is het beste voor kinderen?", "a": "Duolingo is het meest kindvriendelijk door de gamified aanpak. Duolingo ABC is specifiek voor jonge kinderen die leren lezen. Mondly Kids is ook een goede optie."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (2000+ woorden) met:
- Een pakkende introductie over taal leren in 2026 (globalisering, thuiswerken, waarom Nederlanders talen leren)
- Per tool: een sectie met Wat het is, Voor wie, Pluspunten (5), Minpunten (4-5)
- Een vergelijkingstabel (markdown table) met alle 6 tools
- Een "Welke app past bij jou?" sectie met aanbevelingen per type leerders (vakantieganger, expat, student, professional, talenknobbel)
- Een conclusie
- Gebruik Nederlandse voorbeelden, prijzen in EUR, en noem specifieke NL-context (Nederlanders die Duits/Frans/Spaans leren, expats die Nederlands leren)
- Schrijf in een toegankelijke, nuchtere Nederlandse stijl — geen marketingtaal"""
    },
    {
        "slug": "bbq-vergelijken-2026-gas-houtskool-elektrisch-pellet",
        "prompt": """Je bent een Nederlandse consumentenjournalist. Schrijf een diepgaand vergelijkingsartikel over de beste BBQ types in Nederland in 2026.

VERGELIJK DEZE 6 BBQ-TYPES (met concrete voorbeelden):
1. Houtskool BBQ — klassieke smaak, Weber Master-Touch GBS E-5750, EUR 100-400
2. Gas BBQ — snel en schoon, Weber Spirit II E-310, EUR 300-1000
3. Elektrische BBQ — balkonvriendelijk, Weber Q 1400, EUR 100-300
4. Pellet BBQ — slow cooking, Traeger Pro 575, EUR 500-1500
5. Kamado BBQ — keramisch, The Bastard Large, EUR 500-2000
6. Tafel BBQ — compact, LotusGrill, EUR 30-100

OUTPUT FORMAT:
Eerst een JSON metadata blok, dan ===BODY===, dan de volledige markdown body.

JSON metadata:
{
  "title": "Beste BBQ 2026: Gas vs Houtskool vs Elektrisch vs Pellet — Welke Past Bij Jouw Tuin of Balkon?",
  "description": "Vergelijking van de 6 beste BBQ types in 2026. Eerlijke scores, prijzen en verdicts voor houtskool, gas, elektrisch, pellet, kamado en tafel BBQ's.",
  "category": "huis-tuin",
  "rating": 4.6,
  "priceRange": "EUR 30-2000",
  "pros": [
    "Eerlijke 2026 vergelijking van alle BBQ types voor Nederlandse huishoudens",
    "Duidelijke prijsranges, scores en verdicts per type",
    "Nederlandstalig en praktijkgericht advies met FAQ"
  ],
  "cons": [
    "Prijzen kunnen wijzigen — check altijd de actuele aanbieder",
    "Niet elk model is dagelijks getest met intensief gebruik",
    "Smaakvoorkeuren zijn subjectief — probeer indien mogelijk uit"
  ],
  "affiliateLinks": [
    "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"
  ],
  "featuredTool": "Gas BBQ (Weber Spirit II)",
  "readingTime": "9 min",
  "tools": [
    {"name": "Houtskool BBQ", "verdict": "Beste voor pure grillsmaak — onverslaanbaar in smaak maar traag in opstarten en lastiger schoon te maken", "priceRange": "EUR 100-400", "bestFor": "Barbecue-puristen die smaak boven gemak stellen", "rating": 4.5, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Gas BBQ", "verdict": "Beste allrounder — snel op temperatuur, schoon, precieze temperatuurcontrole, ideaal voor frequente gebruikers", "priceRange": "EUR 300-1000", "bestFor": "Gezinnen die vaak en snel willen barbecueën zonder gedoe", "rating": 4.7, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Elektrische BBQ", "verdict": "Beste voor balkons — rookvrij, compact, direct klaar, maar mist de authentieke BBQ-smaak", "priceRange": "EUR 100-300", "bestFor": "Appartementbewoners met balkon die niet mogen stoken", "rating": 3.8, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Pellet BBQ", "verdict": "Beste voor slow cooking — automatische temperatuurregeling, unieke rooksmaak, maar duur en traag", "priceRange": "EUR 500-1500", "bestFor": "BBQ-liefhebbers die low & slow willen gaan (brisket, pulled pork)", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Kamado BBQ", "verdict": "Meest veelzijdig — grillen, roken, bakken, pizza's. Houdt temperatuur perfect vast maar is zwaar en duur", "priceRange": "EUR 500-2000", "bestFor": "Enthousiaste koks die het hele jaar door willen barbecueën", "rating": 4.6, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Tafel BBQ", "verdict": "Beste voor picknicks en kleine ruimtes — compact, snel, goedkoop, maar beperkte capaciteit", "priceRange": "EUR 30-100", "bestFor": "Studenten, kampeerders en kleine balkons", "rating": 3.7, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"}
  ],
  "faq": [
    {"q": "Mag ik een houtskool BBQ op mijn balkon gebruiken?", "a": "Dit hangt af van je huurcontract en VvE-reglement. Veel appartementencomplexen verbieden houtskool- en gas-BBQ's vanwege rookoverlast. Een elektrische BBQ is dan de beste (en vaak enige) optie."},
    {"q": "Wat is het beste BBQ merk in Nederland?", "a": "Weber is het populairste merk in Nederland vanwege de bouwkwaliteit en garantie. The Bastard is toonaangevend in kamado's. Voor budget zijn de huismerken van Intratuin en Praxis goede opties."},
    {"q": "Hoeveel moet ik uitgeven aan een goede BBQ?", "a": "Een goede houtskool BBQ heb je vanaf EUR 150 (Weber Compact). Voor gas begint het bij EUR 350. Een pellet BBQ of kamado is een investering vanaf EUR 500, maar gaat 10+ jaar mee."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (2000+ woorden) met:
- Een pakkende introductie over BBQ'en in Nederland in 2026 (zomer, terrasjes, thuis koken trend)
- Per type: een sectie met Wat het is, Voor wie, Pluspunten (5), Minpunten (4-5), en een concreet modelvoorbeeld
- Een vergelijkingstabel (markdown table) met alle 6 types
- Een "Welke BBQ past bij jou?" sectie met aanbevelingen per situatie (gezin met tuin, appartement met balkon, serieuze hobbykok, student, kampeerder)
- Een conclusie
- Gebruik Nederlandse voorbeelden, prijzen in EUR, en noem specifieke NL-context (kleine tuinen, balkons, Nederlands weer, VvE-regels)
- Schrijf in een toegankelijke, nuchtere Nederlandse stijl — geen marketingtaal"""
    },
    {
        "slug": "airco-ventilator-vergelijken-2026-split-unit-mobiel-plafond",
        "prompt": """Je bent een Nederlandse consumentenjournalist. Schrijf een diepgaand vergelijkingsartikel over de beste koeloplossingen voor Nederlandse huizen in 2026.

VERGELIJK DEZE 6 KOELOPLOSSINGEN:
1. Split-unit airco — vaste installatie, meest efficiënt, EUR 800-2500 (incl. installatie)
2. Mobiele airco — verrijdbaar, geen installatie, EUR 200-600
3. Plafondventilator — stil, energiezuinig, EUR 50-300
4. Torenventilator — compact, oscillerend, EUR 30-150
5. Vloerventilator — krachtig, goedkoop, EUR 20-80
6. Ventilator met verneveling — extra koeling door watermist, EUR 50-200

OUTPUT FORMAT:
Eerst een JSON metadata blok, dan ===BODY===, dan de volledige markdown body.

JSON metadata:
{
  "title": "Airco vs Ventilator 2026: Split-Unit, Mobiel of Plafond — Wat Koelt Jouw Huis Het Beste?",
  "description": "Vergelijking van de 6 beste koeloplossingen voor Nederlandse huizen in 2026. Eerlijke scores, prijzen en verdicts voor split-unit airco's, mobiele airco's en ventilatoren.",
  "category": "huis-tuin",
  "rating": 4.5,
  "priceRange": "EUR 20-2500",
  "pros": [
    "Eerlijke 2026 vergelijking van alle koeloplossingen voor Nederlandse huishoudens",
    "Duidelijke prijsranges, scores en verdicts per type",
    "Nederlandstalig en praktijkgericht advies met FAQ"
  ],
  "cons": [
    "Prijzen kunnen wijzigen — check altijd de actuele aanbieder",
    "Niet elk model is dagelijks getest met intensief gebruik",
    "Installatiekosten voor split-units variëren per woning en installateur"
  ],
  "affiliateLinks": [
    "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"
  ],
  "featuredTool": "Split-unit airco",
  "readingTime": "9 min",
  "tools": [
    {"name": "Split-unit airco", "verdict": "Beste koelprestatie — echte airconditioning die een kamer snel en efficiënt koelt, maar hoge aanschaf- en installatiekosten", "priceRange": "EUR 800-2500", "bestFor": "Huisbezitters die structureel willen koelen in warme zomers", "rating": 4.8, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Mobiele airco", "verdict": "Beste compromis — geen installatie nodig, verplaatsbaar, maar minder efficiënt en luider dan split-unit", "priceRange": "EUR 200-600", "bestFor": "Huurders en mensen die flexibel willen koelen zonder vaste installatie", "rating": 4.0, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Plafondventilator", "verdict": "Beste voor constante luchtcirculatie — stil, energiezuinig, verkoelt de hele kamer gelijkmatig zonder koude luchtstroom", "priceRange": "EUR 50-300", "bestFor": "Slaapkamers en woonkamers waar je subtiele verkoeling wilt", "rating": 4.3, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Torenventilator", "verdict": "Beste design — compact, oscillerend, past in elk interieur, maar koelt alleen de persoon ervoor, niet de ruimte", "priceRange": "EUR 30-150", "bestFor": "Kantoren, kleine kamers en designbewuste gebruikers", "rating": 3.9, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Vloerventilator", "verdict": "Beste budget — krachtige luchtstroom voor weinig geld, maar luidruchtig en neemt vloerruimte in", "priceRange": "EUR 20-80", "bestFor": "Studenten, tijdelijke oplossingen en mensen met een klein budget", "rating": 3.6, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Ventilator met verneveling", "verdict": "Beste voor droge hitte — watermist versterkt het koeleffect, maar alleen effectief in lage luchtvochtigheid", "priceRange": "EUR 50-200", "bestFor": "Buiten gebruik op terrassen en balkons tijdens droge zomerdagen", "rating": 3.7, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"}
  ],
  "faq": [
    {"q": "Wat is het verschil in stroomverbruik tussen een airco en ventilator?", "a": "Een split-unit airco verbruikt 0,5-1,5 kW per uur (EUR 0,15-0,45/uur). Een mobiele airco 0,8-1,2 kW. Een ventilator slechts 0,03-0,07 kW (EUR 0,01-0,02/uur). Het verschil in energiekosten is dus aanzienlijk."},
    {"q": "Heb ik een vergunning nodig voor een split-unit airco?", "a": "Voor de meeste woningen niet, maar voor monumentale panden of als de buitenunit zichtbaar is aan de voorgevel kan een vergunning nodig zijn. Check bij je gemeente. Voor huurwoningen heb je toestemming van de verhuurder nodig."},
    {"q": "Kan een airco ook verwarmen?", "a": "Ja, de meeste moderne split-unit airco's zijn warmtepompen die ook kunnen verwarmen. Ze zijn 3-4x efficiënter dan elektrische kachels. Dit maakt ze interessant als bijverwarming in het voor- en najaar."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (2000+ woorden) met:
- Een pakkende introductie over hitte in Nederland in 2026 (warmere zomers, thuiswerken, slecht geïsoleerde huizen)
- Per type: een sectie met Wat het is, Voor wie, Pluspunten (5), Minpunten (4-5)
- Een vergelijkingstabel (markdown table) met alle 6 types
- Een "Welke koeloplossing past bij jou?" sectie met aanbevelingen per situatie (huiseigenaar, huurder, student, slaapkamer, woonkamer, thuiswerker)
- Een conclusie
- Gebruik Nederlandse voorbeelden, prijzen in EUR, en noem specifieke NL-context (Nederlandse zomers, energiekosten, huurwoningen, VvE, isolatie)
- Schrijf in een toegankelijke, nuchtere Nederlandse stijl — geen marketingtaal"""
    }
]

def main():
    success = 0
    for i, art in enumerate(ARTICLES):
        print(f"\n[{i+1}/5] Generating: {art['slug']}")
        
        path = os.path.join(ARTICLES_DIR, f"{art['slug']}.md")
        if os.path.exists(path):
            print(f"  SKIP: already exists")
            continue
        
        raw = call_ollama(art['prompt'])
        if not raw:
            print(f"  FAILED: no response from Ollama")
            continue
        
        data = parse_response(raw)
        if not data:
            print(f"  FAILED: could not parse response")
            debug_path = f"/tmp/gen-debug-{art['slug']}.txt"
            with open(debug_path, 'w') as f:
                f.write(raw)
            print(f"  Raw saved to {debug_path}")
            continue
        
        if write_article(data, art['slug']):
            success += 1
        
        if i < len(ARTICLES) - 1:
            time.sleep(3)
    
    print(f"\n=== DONE: {success}/5 articles generated ===")
    return success

if __name__ == "__main__":
    main()
