#!/usr/bin/env python3
"""Generate 5 new Dutch AI comparison articles for gaps with zero coverage.
Batch — June 10 2026. Uses Gemini 2.5 Flash, proper yaml.dump frontmatter.
Canonical clone: /workspace/kieskeuken/dutch-ai-tools"""

import os, time, sys, yaml, re
import requests
from pathlib import Path

# --- API Key ---
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
    print("FATAL: No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = Path("/workspace/kieskeuken/dutch-ai-tools/src/content/articles")
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

ALL_SLUGS = sorted(f.stem for f in ARTICLES_DIR.glob("*.md"))

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

def generate_one(prompt, attempt=1):
    url = BASE_URL
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    resp = requests.post(f"{url}?key={API_KEY}", headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    if resp.status_code == 503 and attempt <= 3:
        print(f"  503, retry {attempt+1}...")
        time.sleep(5)
        return generate_one(prompt, attempt + 1)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text[:400]}")
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return text, len(text.split())

def build_frontmatter(meta):
    """Build YAML frontmatter that matches existing article format."""
    fm = {}
    fm["title"] = meta["title"]
    fm["slug"] = meta["slug"]
    fm["description"] = meta["description"]
    fm["category"] = meta["category"]
    fm["rating"] = meta["rating"]
    fm["priceRange"] = meta["priceRange"]
    fm["pros"] = meta["pros"]
    fm["cons"] = meta["cons"]
    fm["affiliateLinks"] = meta.get("affiliateLinks", [])
    fm["date"] = meta["date"]
    fm["modelYear"] = meta["modelYear"]
    fm["featuredTool"] = meta["featuredTool"]
    fm["readingTime"] = meta["readingTime"]
    fm["tools"] = meta["tools"]
    fm["related"] = meta["related"]
    fm["faq"] = meta["faq"]
    return fm

def write_article(slug, frontmatter, body_md):
    """Write a full .md article with proper YAML frontmatter."""
    yaml_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    # Fix yaml.dump multiline string issues for description/faq
    content = f"---\n{yaml_str}---\n\n{body_md}"
    path = ARTICLES_DIR / f"{slug}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

ARTICLES = [
    {
        "slug": "aws-vs-azure-vs-google-cloud-2026",
        "title": "AWS vs Azure vs Google Cloud 2026: Beste Cloud Platform voor Nederlandse Bedrijven",
        "description": "AWS, Azure of Google Cloud voor jouw bedrijf in 2026? Vergelijk prijzen, Nederlandse datacenters, AI-diensten, compliance en support van de drie grootste cloudproviders.",
        "category": "technologie",
        "rating": 4.7,
        "priceRange": "EUR 0-50.000+/mnd",
        "pros": [
            "Diepgaande vergelijking van de 3 grootste cloudplatforms met NL-context",
            "Praktische use cases per bedrijfsgrootte en sector",
            "Duidelijk kostenoverzicht inclusief verborgen kosten"
        ],
        "cons": [
            "Cloudprijzen veranderen frequent — check altijd actuele pricing",
            "Features evolueren snel — dit artikel is een momentopname",
            "Niet elk niche-use case wordt behandeld"
        ],
        "affiliateLinks": [],
        "date": "2026-06-10",
        "modelYear": 2026,
        "featuredTool": "AWS",
        "readingTime": "10 min",
        "tools": [
            {"name": "AWS", "verdict": "Grootste aanbod en wereldwijd bereik — beste voor scale-ups en enterprise", "priceRange": "EUR 0-50.000+/mnd", "bestFor": "Schaalbare applicaties en startups", "rating": 4.7},
            {"name": "Microsoft Azure", "verdict": "Beste integratie met Microsoft-ecosysteem en hybride cloud — top voor MKB met MS-stack", "priceRange": "EUR 0-50.000+/mnd", "bestFor": "Microsoft-gedreven organisaties", "rating": 4.6},
            {"name": "Google Cloud", "verdict": "Sterkste AI/ML-diensten en data-analyse — beste voor data-gedreven bedrijven", "priceRange": "EUR 0-50.000+/mnd", "bestFor": "AI, big data en Kubernetes", "rating": 4.5},
        ],
        "related": pick_related("aws-vs-azure-vs-google-cloud-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welk cloud platform is het goedkoopst voor Nederlandse startups?",
             "a": "AWS heeft het meest genereuze free tier-programma (12 maanden gratis voor veel diensten). Google Cloud biedt $300 gratis tegoed voor nieuwe gebruikers. Azure geeft €170 tegoed voor 30 dagen. Voor langdurig lage kosten is Google Cloud vaak voordeliger door sustained-use kortingen, maar AWS is het meest voorspelbaar in pricing."},
            {"q": "Hebben deze cloudproviders datacenters in Nederland?",
             "a": "Ja: Google Cloud heeft een regio in Eemshaven sinds 2018. Microsoft Azure opende in 2024 een Dutch datacenter regio. AWS heeft geen Nederlands datacenter maar wel in Frankfurt, Stockholm en Parijs met uitstekende latency naar NL."},
            {"q": "Welke cloud provider voldoet aan AVG/GDPR?",
             "a": "Alle drie voldoen aan AVG/GDPR — maar de implementatie verschilt. Azure en Google Cloud hebben Nederlandse datacenters wat datasoevereiniteit vereenvoudigt. AWS biedt uitgebreide compliance-certificeringen en EU-dataresidency via Frankfurt. Kies op basis van waar je data fysiek moet staan, niet alleen op papier."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over AWS vs Microsoft Azure vs Google Cloud — de 3 grootste cloudplatforms van 2026, specifiek voor Nederlandse bedrijven.

Structuur:
- Introductie: Cloud computing is de ruggengraat van modern zakendoen. AWS (Amazon), Azure (Microsoft) en Google Cloud domineren de markt. Maar welke past bij jouw Nederlandse bedrijf? We vergelijken op prijs, Nederlandse aanwezigheid, AI/ML-diensten, compliance en support.
- Hoofdsectie per provider (## koppen): AWS, Microsoft Azure, Google Cloud. Per provider: overzicht, Nederlandse datacenters, sterke/zwakke punten, beste use cases, typische kosten, NL-specifieke voordelen.
- Vergelijkingstabel (markdown): provider, NL datacenter, gratis tier, AI/ML sterkte, prijs rekenkracht (EUR/uur), prijs opslag (EUR/GB), beste voor, AVG-compliance score
- Sectie: Kostenvergelijking per use case — kleine webshop (€50-200/mnd), SaaS startup (€500-2000/mnd), enterprise (€5000+/mnd)
- Conclusie: welke provider voor welk type Nederlands bedrijf — MKB met Microsoft-ecosysteem, tech startup, data-gedreven scale-up, enterprise met hybride behoeften, budget-bewuste organisatie

Stijl: Nuchter, Nederlands, praktisch. Geen AI-hype. Vermijd Amerikaanse voorbeelden — focus op wat Nederlandse IT-beslissers moeten weten. Gebruik ## voor hoofdsecties. Schrap alle asterisks rond kopjes behalve de kop zelf."""
    },
    {
        "slug": "lightspeed-vs-mijnwebwinkel-vs-ccvshop-vs-shopify-2026",
        "title": "Lightspeed vs MijnWebwinkel vs CCV Shop vs Shopify 2026: Beste Webshop Platform Nederland",
        "description": "Lightspeed, MijnWebwinkel, CCV Shop of Shopify voor je Nederlandse webshop in 2026? Vergelijk prijzen, koppelingen, betaalmethodes en geschiktheid per branche.",
        "category": "business",
        "rating": 4.6,
        "priceRange": "EUR 15-300/mnd",
        "pros": [
            "Unieke Nederlandse focus — geen Amerikaanse voorbeelden",
            "Praktische vergelijking inclusief iDEAL, Klarna en lokale koppelingen",
            "Reële use cases per branche: kleding, food, B2B, diensten"
        ],
        "cons": [
            "Prijzen en pakketten wijzigen regelmatig",
            "Transaction fees verschillen per betaalmethode",
            "Niet elke niche-functionaliteit wordt behandeld"
        ],
        "affiliateLinks": [],
        "date": "2026-06-10",
        "modelYear": 2026,
        "featuredTool": "Shopify",
        "readingTime": "10 min",
        "tools": [
            {"name": "Shopify", "verdict": "Beste allround webshop-platform met grootste app-ecosysteem — ideaal voor schaalbare webshops", "priceRange": "EUR 27-300/mnd", "bestFor": "Groeiende merken en omnichannel", "rating": 4.7},
            {"name": "MijnWebwinkel", "verdict": "Beste prijs-kwaliteit voor startende Nederlandse webshops — alles in één met NL support", "priceRange": "EUR 25-125/mnd", "bestFor": "Startende ondernemers", "rating": 4.5},
            {"name": "CCV Shop", "verdict": "Meest uitgebreide Nederlandse features (iDEAL, Klarna, facturatie) — beste voor gevestigde NL webshops", "priceRange": "EUR 40-300/mnd", "bestFor": "Middelgrote tot grote NL webshops", "rating": 4.4},
            {"name": "Lightspeed", "verdict": "Sterkste kassakoppeling en voorraadbeheer — beste voor fysieke winkels met online uitbreiding", "priceRange": "EUR 69-250/mnd", "bestFor": "Retail met fysieke vestigingen", "rating": 4.4},
        ],
        "related": pick_related("lightspeed-vs-mijnwebwinkel-vs-ccvshop-vs-shopify-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welk webshop platform is het beste voor een startende ondernemer in Nederland?",
             "a": "MijnWebwinkel biedt de laagste instapkosten (€25/maand) met NL support en vooraf geïntegreerde iDEAL-betalingen. Shopify is duurder maar schaalbaarder als je snel wilt groeien. CCV Shop is iets prijziger maar heeft de beste Nederlandse boekhoudkoppelingen. Start met MijnWebwinkel of Shopify's Basic-plan."},
            {"q": "Kan ik met al deze platforms iDEAL en Klarna aanbieden?",
             "a": "Ja, alle vier ondersteunen iDEAL en Klarna. CCV Shop en MijnWebwinkel hebben deze standaard ingebouwd zonder extra transactiekosten. Shopify rekent 0,25% extra over externe payment gateways (tenzij je Shopify Payments gebruikt). Lightspeed ondersteunt iDEAL via Mollie-koppeling."},
            {"q": "Welk platform is geschikt voor B2B-groothandel?",
             "a": "CCV Shop heeft de beste B2B-features: offertemodule, klantspecifieke prijzen, minimale bestelhoeveelheden en facturatie op rekening — allemaal standaard. Lightspeed biedt B2B-functionaliteit via apps. MijnWebwinkel en Shopify vereisen vaak extra plugins voor volwaardige B2B-functionaliteit."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Lightspeed vs MijnWebwinkel vs CCV Shop vs Shopify — de beste webshop platforms voor Nederlandse ondernemers in 2026.

Structuur:
- Introductie: Een webshop starten in Nederland? De keuze van het platform bepaalt je succes. We vergelijken de vier populairste platforms specifiek voor de Nederlandse markt — inclusief iDEAL, Klarna, boekhoudkoppelingen en BTW-functionaliteit.
- Hoofdsectie per platform (## koppen): Shopify, MijnWebwinkel, CCV Shop, Lightspeed. Per platform: overzicht, prijs (alle pakketten), Nederlandse betaalmethodes (iDEAL, Klarna, AfterPay, etc.), boekhoudkoppelingen (Moneybird, Exact, e-Boekhouden), sterke/zwakke punten, beste branche, verdict.
- Vergelijkingstabel (markdown): platform, instapprijs/mnd, transactiekosten, iDEAL, Klarna, NL boekhoudkoppeling, NL support, apps/plugins, beste voor, score
- Sectie: Welk platform voor welke branche? Kleding/retail, food/horeca, B2B/groothandel, diensten/digitaal, multichannel (fysiek + online)
- Conclusie: aanrader per situatie — absolute beginner, groeiende webshop, fysieke winkel + online, B2B-groothandel, budget onder €50/mnd

Stijl: Nuchter, Nederlands, praktisch. Focus op NL-ondernemers. Gebruik ## voor hoofdsecties. Geen asterisks rond kopjes."""
    },
    {
        "slug": "grammarly-vs-deepl-write-vs-languagetool-2026",
        "title": "Grammarly vs DeepL Write vs LanguageTool 2026: Beste Schrijfassistent voor Nederlands en Engels",
        "description": "Grammarly, DeepL Write of LanguageTool voor foutloos schrijven in 2026? Vergelijk Nederlands-ondersteuning, stijladvies, privacy en integraties van de beste AI-schrijfassistenten.",
        "category": "productiviteit",
        "rating": 4.5,
        "priceRange": "EUR 0-30/mnd",
        "pros": [
            "Directe vergelijking van Nederlands-ondersteuning per tool",
            "Praktisch: welke tool voor welke schrijfcontext (zakelijk, academisch, casual)",
            "Heldere privacyvergelijking — relevant voor AVG en vertrouwelijke documenten"
        ],
        "cons": [
            "Grammarly's Nederlandse ondersteuning is nog in ontwikkeling",
            "DeepL Write is relatief nieuw — features breiden uit",
            "Geen van deze tools vervangt een menselijke corrector voor genuanceerde teksten"
        ],
        "affiliateLinks": [],
        "date": "2026-06-10",
        "modelYear": 2026,
        "featuredTool": "DeepL Write",
        "readingTime": "9 min",
        "tools": [
            {"name": "DeepL Write", "verdict": "Beste voor Nederlands — native NL-ondersteuning met stijl- en toonadvies op moedertaalniveau", "priceRange": "EUR 0-9/mnd", "bestFor": "Nederlandstalige professionals", "rating": 4.7},
            {"name": "LanguageTool", "verdict": "Beste privacy (on-premise optie) en meeste talen — ideaal voor organisaties met strenge dataregels", "priceRange": "EUR 0-20/mnd", "bestFor": "Privacy-bewuste teams", "rating": 4.6},
            {"name": "Grammarly", "verdict": "Beste voor Engelstalig schrijven — ongeëvenaarde stijlanalyse maar beperkte NL-ondersteuning", "priceRange": "EUR 0-30/mnd", "bestFor": "Engelstalige content en internationale teams", "rating": 4.4},
        ],
        "related": pick_related("grammarly-vs-deepl-write-vs-languagetool-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke schrijfassistent werkt het beste voor Nederlandse teksten?",
             "a": "DeepL Write is de beste keuze voor Nederlandstalige teksten — het is ontwikkeld door DeepL (Keuls bedrijf) en begrijpt Nederlandse grammatica, idioom en stijl op moedertaalniveau. LanguageTool is een sterke tweede met uitgebreide Nederlandse regels. Grammarly's Nederlands-ondersteuning staat nog in de kinderschoenen."},
            {"q": "Zijn deze tools veilig voor vertrouwelijke zakelijke documenten?",
             "a": "LanguageTool biedt als enige een on-premise server-optie — alle tekstverwerking blijft binnen je eigen netwerk. DeepL Write verwerkt teksten op DeepL's servers in de EU (AVG-compliant). Grammarly verwerkt data deels in de VS — minder geschikt voor strikt vertrouwelijke documenten."},
            {"q": "Wat is het verschil tussen DeepL Write en DeepL Translate?",
             "a": "DeepL Translate vertaalt tussen talen. DeepL Write is een schrijfassistent die binnen één taal werkt — het verbetert stijl, toon, woordkeuze en grammatica zonder te vertalen. Beide tools zijn onderdeel van hetzelfde DeepL-abonnement (Write Pro is €8,99/maand, inclusief Translate)."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Grammarly vs DeepL Write vs LanguageTool — de beste AI-schrijfassistenten van 2026, specifiek beoordeeld op Nederlands-ondersteuning.

Structuur:
- Introductie: Foutloos schrijven in 2026 is meer dan spellingcontrole. AI-schrijfassistenten geven stijladvies, toonsuggesties en herschrijven zinnen. Maar welke werkt écht goed voor Nederlands? We vergelijken Grammarly, DeepL Write en LanguageTool — met focus op NL-ondersteuning, privacy en prijs.
- Hoofdsectie per tool (## koppen): DeepL Write, LanguageTool, Grammarly. Per tool: wat is het, Nederlands-ondersteuning (grammatica, spelling, stijl, toon), sterke/zwakke punten, privacy/AVG, integraties (browser, Office, Google Docs, etc.), prijs, beste voor.
- Vergelijkingstabel (markdown): tool, NL grammatica, NL stijladvies, talen totaal, privacy (on-premise?), browser-extensie, Office-integratie, gratis versie, prijs pro (EUR/mnd), beste voor, score
- Sectie: Welke tool voor welke schrijver? Nederlandse professional (e-mails, rapporten), student (scripties, essays), internationale marketeer (Engelse content), developer (documentatie), privacy-bewuste organisatie
- Conclusie: aanrader per situatie met verdict van 1-2 zinnen per tool

Stijl: Nuchter, Nederlands, praktisch. Gebruik ## voor hoofdsecties. Geen asterisks rond kopjes."""
    },
    {
        "slug": "unbounce-vs-instapage-vs-leadpages-vs-carrd-2026",
        "title": "Unbounce vs Instapage vs Leadpages vs Carrd 2026: Beste Landing Page Builder Vergeleken",
        "description": "Unbounce, Instapage, Leadpages of Carrd voor landingspagina's in 2026? Vergelijk AI-functies, A/B-testen, conversie-tools, prijzen en integraties van de beste landing page builders.",
        "category": "marketing",
        "rating": 4.6,
        "priceRange": "EUR 0-200/mnd",
        "pros": [
            "Duidelijke use case per marketingdoel — niet elke tool past bij elke campagne",
            "Praktische prijsvergelijking inclusief verborgen kosten (CRM, e-mail, domein)",
            "Focus op conversie-optimalisatie met AI — relevant voor 2026 marketeers"
        ],
        "cons": [
            "Carrds eenvoud is een voordeel én beperking — niet alles kan ermee",
            "Prijsverschil is groot — goedkoopste en duurste schelen factor 20",
            "AI-functies zijn nieuw en verschillen sterk per tool"
        ],
        "affiliateLinks": [],
        "date": "2026-06-10",
        "modelYear": 2026,
        "featuredTool": "Unbounce",
        "readingTime": "9 min",
        "tools": [
            {"name": "Unbounce", "verdict": "Beste AI-slimme conversie-optimalisatie met Smart Traffic die automatisch varianten optimaliseert", "priceRange": "EUR 80-200/mnd", "bestFor": "Professionele marketingteams", "rating": 4.7},
            {"name": "Instapage", "verdict": "Beste voor enterprise en advertentie-landingspagina's met AdMap-functie en personalisatie", "priceRange": "EUR 120-350/mnd", "bestFor": "Enterprise en advertentiecampagnes", "rating": 4.5},
            {"name": "Leadpages", "verdict": "Breedste ecosysteem — landingspagina's + e-mailmarketing + betalingen in één tool", "priceRange": "EUR 40-100/mnd", "bestFor": "Kleine teams die alles-in-één willen", "rating": 4.5},
            {"name": "Carrd", "verdict": "Veruit de goedkoopste — perfect voor simpele landingspagina's en microsites voor één product", "priceRange": "EUR 0-19/jaar", "bestFor": "Solopreneurs en minimale projecten", "rating": 4.3},
        ],
        "related": pick_related("unbounce-vs-instapage-vs-leadpages-vs-carrd-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Wat is de beste landingspagina-builder voor een klein marketingbudget?",
             "a": "Carrd is veruit de goedkoopste (€19/jaar) en verrassend krachtig voor simpele pagina's. Leadpages biedt de beste prijs-kwaliteitverhouding met ingebouwde e-mailmarketing (€40/maand). Unbounce en Instapage zijn voor serieuze campagnes met meetbaar rendement — de hogere prijs verdient zichzelf terug via betere conversie."},
            {"q": "Kan ik A/B-testen met deze landingspagina-builders?",
             "a": "Unbounce en Instapage hebben de sterkste native A/B-testtools, inclusief AI-gestuurde verkeersverdeling. Leadpages ondersteunt A/B-testen via integraties. Carrd heeft geen ingebouwde A/B-testfunctionaliteit — gebruik Google Optimize (gratis) of VWO als workaround."},
            {"q": "Zijn deze tools geschikt voor Nederlandse marketeers?",
             "a": "Ja — alle vier ondersteunen Nederlandse teksten, valuta (EUR) en lokale domeinen (.nl). Let op: de interfaces zijn Engelstalig, maar de pagina's zelf kunnen volledig in het Nederlands. Voor AVG/GDPR: Unbounce en Instapage bieden EU-hosting. Leadpages gebruikt Amerikaanse servers. Carrd is AVG-compliant via DPA-overeenkomst."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Unbounce vs Instapage vs Leadpages vs Carrd — de beste landing page builders van 2026 voor Nederlandse marketeers.

Structuur:
- Introductie: Een goede landingspagina is het verschil tussen een klik en een klant. Maar welke builder past bij jouw marketingstrategie? We vergelijken Unbounce, Instapage, Leadpages en Carrd op AI-functies, A/B-testen, prijs en integraties.
- Hoofdsectie per tool (## koppen): Unbounce, Instapage, Leadpages, Carrd. Per tool: overzicht, AI-functies, A/B-testen, templates, integraties (CRM, e-mailmarketing, analytics), prijs (alle pakketten), sterke/zwakke punten, beste voor, verdict.
- Vergelijkingstabel (markdown): tool, AI-functies, A/B-testen, templates, e-mailmarketing, CRM-integratie, gratis versie, vanafprijs/mnd (EUR), beste voor, score
- Sectie: Welke tool voor welke campagne? Google Ads-verkeer (hoge conversie nodig), leadgeneratie met e-mail, productlancering (één pagina), portfolio/persoonlijke pagina
- Conclusie: aanrader per scenario — solopreneur met beperkt budget, marketingteam van 3-5 personen, enterprise met honderden campagnes, side project of hobby

Stijl: Nuchter, Nederlands, praktisch. Focus op conversie, niet op design. Gebruik ## voor hoofdsecties. Geen asterisks rond kopjes."""
    },
    {
        "slug": "postman-vs-insomnia-vs-bruno-vs-hoppscotch-2026",
        "title": "Postman vs Insomnia vs Bruno vs Hoppscotch 2026: Beste API Client voor Developers",
        "description": "Postman, Insomnia, Bruno of Hoppscotch voor API-ontwikkeling in 2026? Vergelijk Git-sync, GraphQL, omgevingen, open-source en prijs van de beste API-testtools.",
        "category": "development",
        "rating": 4.6,
        "priceRange": "EUR 0-50/mnd",
        "pros": [
            "Praktische vergelijking op features die developers écht gebruiken",
            "Aandacht voor open-source vs. proprietary en vendor lock-in",
            "Duidelijk per workflow: solo dev, team, enterprise"
        ],
        "cons": [
            "Postman's prijsstijgingen en licentiewijzigingen kunnen snel veranderen",
            "API-tools hebben steile leercurves voor geavanceerde features",
            "Niche-features (WebSocket, gRPC, SOAP) verschillen sterk per tool"
        ],
        "affiliateLinks": [],
        "date": "2026-06-10",
        "modelYear": 2026,
        "featuredTool": "Bruno",
        "readingTime": "9 min",
        "tools": [
            {"name": "Bruno", "verdict": "Beste open-source alternatief — Git-native, geen login-verplichting, snel en offline-first", "priceRange": "EUR 0-6/mnd", "bestFor": "Privacy-bewuste developers en teams", "rating": 4.7},
            {"name": "Postman", "verdict": "Meest complete ecosysteem — API-monitoring, mock servers, documentatie en uitgebreide samenwerking", "priceRange": "EUR 0-50/mnd", "bestFor": "Enterprise teams en full API lifecycle", "rating": 4.5},
            {"name": "Insomnia", "verdict": "Beste GraphQL-ondersteuning en moderne design-taal — ideaal voor API-design-first workflows", "priceRange": "EUR 0-10/mnd", "bestFor": "GraphQL en API-design", "rating": 4.5},
            {"name": "Hoppscotch", "verdict": "Lichtste en snelste — browser-gebaseerd, open-source, perfect voor snelle tests zonder installatie", "priceRange": "EUR 0-0/mnd", "bestFor": "Snelle ad-hoc API tests", "rating": 4.4},
        ],
        "related": pick_related("postman-vs-insomnia-vs-bruno-vs-hoppscotch-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke API client is het beste voor teams die Git gebruiken?",
             "a": "Bruno is specifiek ontworpen voor Git-native workflows — al je API-requests worden als platte tekstbestanden opgeslagen die je direct kunt committen. Geen binary exports of cloud-sync nodig. Postman en Insomnia ondersteunen ook Git-sync maar via cloud-lagen of betaalde teams-abonnementen."},
            {"q": "Is er een goed gratis alternatief voor Postman?",
             "a": "Bruno (open-source) en Hoppscotch zijn volledig gratis en dekken 90% van dagelijks API-werk. Bruno draait lokaal met offline-first design. Hoppscotch werkt in de browser zonder installatie. Beide ondersteunen REST, GraphQL en omgevingsvariabelen — de core features van Postman."},
            {"q": "Welke tool werkt het beste met GraphQL?",
             "a": "Insomnia heeft de beste native GraphQL-ervaring: auto-complete schema's, inline documentatie en GraphQL-variabelenbeheer. Postman's GraphQL-ondersteuning is solide maar voelt aangeplakt. Bruno en Hoppscotch ondersteunen GraphQL maar minder uitgebreid dan Insomnia."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Postman vs Insomnia vs Bruno vs Hoppscotch — de beste API clients voor developers in 2026.

Structuur:
- Introductie: Elke developer test APIs. Maar de tool die je kiest bepaalt je workflow, samenwerking en vendor lock-in. Postman domineert, maar open-source alternatieven als Bruno en Hoppscotch winnen snel terrein. We vergelijken ze op features, open-source, prijs en Git-integratie.
- Hoofdsectie per tool (## koppen): Postman, Insomnia, Bruno, Hoppscotch. Per tool: overzicht, REST/GraphQL/SOAP, Git-sync, omgevingen/variabelen, scripts (pre-request, test assertions), teams/samenwerking, prijs, sterke/zwakke punten, beste voor, verdict.
- Vergelijkingstabel (markdown): tool, REST, GraphQL, Git-native, open-source, offline, teams gratis, prijs pro (EUR/mnd), scripts, beste voor, score
- Sectie: Welke tool voor welke workflow? Solo developer (open-source), startup team (goedkoop maar samenwerking), enterprise (compliance en governance), GraphQL-first teams, snelle ad-hoc tests
- Conclusie: aanrader per scenario met verdict van 1-2 zinnen per tool

Stijl: Nuchter, Nederlands, technisch maar toegankelijk. Gebruik ## voor hoofdsecties. Geen asterisks rond kopjes."""
    },
]

def main():
    print(f"=== Generating {len(ARTICLES)} articles ===")
    print(f"Target dir: {ARTICLES_DIR}")
    print(f"Existing articles: {len(ALL_SLUGS)}")
    results = []
    
    for i, article in enumerate(ARTICLES):
        slug = article["slug"]
        tgt = ARTICLES_DIR / f"{slug}.md"
        if tgt.exists():
            print(f"[{i+1}/{len(ARTICLES)}] SKIP {slug} — already exists")
            results.append({"slug": slug, "status": "skipped"})
            continue
        
        print(f"[{i+1}/{len(ARTICLES)}] Generating: {slug}")
        try:
            text, word_count = generate_one(article["prompt"])
            # Strip code fences if any
            text = re.sub(r'^```(?:markdown|md)?\s*\n?', '', text)
            text = re.sub(r'\n?```\s*$', '', text)
            
            # Build frontmatter from meta
            article.pop("prompt", None)
            frontmatter = build_frontmatter(article)
            
            path = write_article(slug, frontmatter, text.strip())
            print(f"  -> {path} ({word_count} words)")
            results.append({"slug": slug, "status": "generated", "words": word_count})
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"slug": slug, "status": "error", "error": str(e)})
        
        # Rate limit: ~5s between articles
        if i < len(ARTICLES) - 1:
            time.sleep(4)
    
    # Summary
    print("\n=== Summary ===")
    for r in results:
        status = r["status"]
        slug = r["slug"]
        if status == "generated":
            print(f"  ✓ {slug} ({r.get('words', '?')} words)")
        elif status == "skipped":
            print(f"  - {slug} (skipped)")
        else:
            print(f"  ✗ {slug}: {r.get('error', 'unknown')}")
    
    generated = sum(1 for r in results if r["status"] == "generated")
    print(f"\nGenerated: {generated}/{len(ARTICLES)}")

if __name__ == "__main__":
    main()
