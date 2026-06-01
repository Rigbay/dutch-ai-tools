#!/usr/bin/env python3
"""Generate 5 new Dutch AI tools articles for critical content gaps:
1. AI financiën, boekhouding & belasting (0 articles)
2. AI reizen & vakantieplanning (1 article)
3. AI fitness, sport & gezondheid (2 articles)
4. AI fotografie & beeldbewerking (2 articles)
5. AI onderwijs, bijles & e-learning (2 articles)

Uses Gemini 2.5 Flash API. Writes to canonical /workspace/dutch-ai-tools/src/content/articles."""
import os, json, time, sys, glob as globmod, requests
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(key_file):
        for line in open(key_file):
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

ALL_SLUGS = sorted([
    f.replace(".md", "").replace(f"{ARTICLES_DIR}/", "")
    for f in globmod.glob(f"{ARTICLES_DIR}/*.md")
])

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-financiele-boekhouding-tools-2026",
        "title": "Beste AI Tools voor Financiën, Boekhouding & Belasting 2026: top 7 vergeleken",
        "description": "AI tools voor financiën, boekhouding en belasting in 2026. Vergelijk Exact Online, Moneybird, e-Boekhouden, SnelStart, Informer, Xero en QuickBooks voor Nederlandse ondernemers en zzp'ers.",
        "category": "business",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor financiën, boekhouding en belasting in 2026. Behandel precies 7 tools: "
            "Exact Online, Moneybird, e-Boekhouden.nl, SnelStart, Informer, Xero, QuickBooks.\n\n"
            "Structuur:\n"
            "- Introductie: AI transformeert financiële administratie in 2026 — van automatische "
            "factuurverwerking tot AI-gestuurde btw-aangiftes en realtime kasstroomprognoses. "
            "Voor Nederlandse zzp'ers, mkb'ers en accountants die grip willen houden op hun financiën.\n"
            "- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\n"
            "- Conclusie: welke tool voor welk type gebruiker (zzp'er, mkb met personeel, accountant)\n"
            "- 3 FAQ-vragen over AI en financiële administratie\n\n"
            "Focus op Nederlandse context: btw-aangifte, iDEAL, SEPA, KVK, jaarlijkse aangifte "
            "inkomstenbelasting. Prijzen in EUR. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Exact Online", "verdict": "Marktleider in Nederland met AI-gestuurde factuurherkenning, automatische btw-berekening en slimme kasstroomprognoses — volledig Nederlands", "priceRange": "EUR 15-80/mnd", "bestFor": "MKB met personeel", "rating": 4.6, "affiliateLink": "https://www.exact.com/nl/exact-online?ref=aitoolsnl"},
            {"name": "Moneybird", "verdict": "AI-gedreven boekhouding speciaal voor zzp'ers — automatische factuurverwerking, btw-aangifte en bankkoppeling in één", "priceRange": "EUR 15-35/mnd", "bestFor": "Zzp'ers & freelancers", "rating": 4.5, "affiliateLink": "https://www.moneybird.nl/?ref=aitoolsnl"},
            {"name": "e-Boekhouden.nl", "verdict": "Nederlandse AI-boekhouding met automatische categorisatie van banktransacties en slimme btw-herkenning — eenvoudig en betaalbaar", "priceRange": "EUR 10-30/mnd", "bestFor": "Budgetvriendelijk mkb", "rating": 4.3, "affiliateLink": "https://www.e-boekhouden.nl/?ref=aitoolsnl"},
            {"name": "SnelStart", "verdict": "AI-boekhouding met ingebouwde btw-aangifte, automatische factuurscanning en realtime rapportages — populaire keuze in Nederland", "priceRange": "EUR 20-50/mnd", "bestFor": "Groeiende ondernemingen", "rating": 4.4, "affiliateLink": "https://www.snelstart.nl/?ref=aitoolsnl"},
            {"name": "Informer", "verdict": "AI-platform met geïntegreerde CRM, voorraadbeheer en boekhouding — automatische factuurverwerking en credit management", "priceRange": "EUR 25-75/mnd", "bestFor": "MKB met voorraad", "rating": 4.2, "affiliateLink": "https://www.informer.nl/?ref=aitoolsnl"},
            {"name": "Xero", "verdict": "Internationale AI-boekhouding met sterke bankkoppelingen, automatische reconciliatie en slimme cashflow forecasting", "priceRange": "EUR 12-50/mnd", "bestFor": "Internationale handel", "rating": 4.5, "affiliateLink": "https://www.xero.com/nl/?ref=aitoolsnl"},
            {"name": "QuickBooks", "verdict": "AI-gestuurde boekhouding van Intuit met automatische onkostencategorisatie, factuurtracking en belastingvoorbereiding", "priceRange": "EUR 15-60/mnd", "bestFor": "Amerikaanse connectie", "rating": 4.1, "affiliateLink": "https://quickbooks.intuit.com/nl/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-financiele-boekhouding-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-reizen-vakantieplanning-tools-2026",
        "title": "Beste AI Tools voor Reizen & Vakantieplanning 2026: top 7 vergeleken",
        "description": "AI tools voor reisplanning, vluchtboeking en vakantieorganisatie in 2026. Vergelijk Google Travel, TripIt, Hopper, Kayak, Roadtrippers, PackPoint en Roam Around voor de beste reiservaring.",
        "category": "technologie",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor reizen en vakantieplanning in 2026. Behandel precies 7 tools: "
            "Google Travel (Gemini), TripIt, Hopper, Kayak, Roadtrippers, PackPoint, Roam Around.\n\n"
            "Structuur:\n"
            "- Introductie: AI transformeert reisplanning in 2026 — van gepersonaliseerde "
            "reissuggesties tot prijsvoorspellingen, automatische reisroutes en slimme paklijsten. "
            "Voor Nederlandse reizigers die tijd willen besparen en de beste deals willen vinden.\n"
            "- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\n"
            "- Conclusie: welke tool voor welk type reiziger (budgetreiziger, zakenreiziger, gezin, backpacker)\n"
            "- 3 FAQ-vragen over AI en reisplanning\n\n"
            "Focus op Nederlandse/Europese context. Prijzen in EUR. Noem Schiphol, NS, "
            "Eurostar als relevant. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Google Travel (Gemini)", "verdict": "AI-gestuurde reisplanner van Google met gepersonaliseerde aanbevelingen, prijsvergelijking en automatische reisroutes op basis van Gmail-data", "priceRange": "EUR 0 (gratis)", "bestFor": "Alles-in-één reisplanning", "rating": 4.7, "affiliateLink": "https://www.google.com/travel/?ref=aitoolsnl"},
            {"name": "TripIt", "verdict": "AI-reisorganisator die al je reserveringen automatisch in één reisroute samenvoegt uit e-mailbevestigingen — onmisbaar voor zakenreizigers", "priceRange": "EUR 0-49/jaar", "bestFor": "Zakenreizigers", "rating": 4.5, "affiliateLink": "https://www.tripit.com/?ref=aitoolsnl"},
            {"name": "Hopper", "verdict": "AI-prijsvoorspeller die aangeeft wanneer je het beste kunt boeken voor vluchten en hotels — met 'freeze the price' garantie", "priceRange": "EUR 0 (gratis)", "bestFor": "Prijsbewuste reizigers", "rating": 4.4, "affiliateLink": "https://www.hopper.com/?ref=aitoolsnl"},
            {"name": "Kayak", "verdict": "AI-zoekmachine voor vluchten, hotels en huurauto's met prijsvergelijking, prijsalerts en Explore-functie voor budgetvriendelijke bestemmingen", "priceRange": "EUR 0 (gratis)", "bestFor": "Vergelijken & boeken", "rating": 4.5, "affiliateLink": "https://www.kayak.nl/?ref=aitoolsnl"},
            {"name": "Roadtrippers", "verdict": "AI-roadtrip planner die routes optimaliseert met bezienswaardigheden, accommodaties en eetgelegenheden onderweg — ideaal voor Europese roadtrips", "priceRange": "EUR 0-30/jaar", "bestFor": "Roadtrips & camperreizen", "rating": 4.2, "affiliateLink": "https://roadtrippers.com/?ref=aitoolsnl"},
            {"name": "PackPoint", "verdict": "AI-paklijst generator die op basis van bestemming, reisduur, activiteiten en weersverwachting een gepersonaliseerde paklijst maakt", "priceRange": "EUR 0-3/mnd", "bestFor": "Inpakken & organiseren", "rating": 4.3, "affiliateLink": "https://packpoint.app/?ref=aitoolsnl"},
            {"name": "Roam Around", "verdict": "AI-reisroute generator die in seconden een complete dag-tot-dag reisplanning maakt met bezienswaardigheden, restaurants en activiteiten", "priceRange": "EUR 0-10/mnd", "bestFor": "Snelle reisplanning", "rating": 4.1, "affiliateLink": "https://www.roamaround.io/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-reizen-vakantieplanning-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-fitness-sport-gezondheid-tools-2026",
        "title": "Beste AI Tools voor Fitness, Sport & Gezondheid 2026: top 7 vergeleken",
        "description": "AI tools voor fitness, sport en gezondheid in 2026. Vergelijk Freeletics, Whoop, MyFitnessPal, Strava, Fitbod, Aaptiv en Sleep Cycle voor training, voeding, slaap en herstel.",
        "category": "technologie",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor fitness, sport en gezondheid in 2026. Behandel precies 7 tools: "
            "Freeletics, Whoop, MyFitnessPal, Strava, Fitbod, Aaptiv, Sleep Cycle.\n\n"
            "Structuur:\n"
            "- Introductie: AI transformeert persoonlijke gezondheid in 2026 — van AI-trainers die "
            "je workouts aanpassen op basis van hersteldata tot slaapoptimalisatie en "
            "gepersonaliseerde voedingsadviezen. Voor Nederlanders die slimmer willen trainen.\n"
            "- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\n"
            "- Conclusie: welke tool voor welk type gebruiker (sporter, hardloper, krachtsporter, gezondheidsoptimist)\n"
            "- 3 FAQ-vragen over AI en fitness/gezondheid\n\n"
            "Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Freeletics", "verdict": "AI-trainer die op basis van je feedback, doelen en prestaties elke workout personaliseert — geen sportschool nodig, alleen je eigen lichaamsgewicht", "priceRange": "EUR 0-50/jaar", "bestFor": "Thuisworkouts zonder apparatuur", "rating": 4.6, "affiliateLink": "https://www.freeletics.com/?ref=aitoolsnl"},
            {"name": "Whoop", "verdict": "AI-herstel- en prestatie tracker met een slimme band die slaap, herstel, belasting en gezondheid 24/7 analyseert met gepersonaliseerd advies", "priceRange": "EUR 18/mnd", "bestFor": "Herstel & prestatie-optimalisatie", "rating": 4.5, "affiliateLink": "https://www.whoop.com/?ref=aitoolsnl"},
            {"name": "MyFitnessPal", "verdict": "AI-voedings- en calorietracker met de grootste voedingsdatabase — scan barcodes, log maaltijden met AI-fotoherkenning en krijg gepersonaliseerde macro-adviezen", "priceRange": "EUR 0-20/mnd", "bestFor": "Voeding & calorietracking", "rating": 4.4, "affiliateLink": "https://www.myfitnesspal.com/?ref=aitoolsnl"},
            {"name": "Strava", "verdict": "AI-hardloop- en fietsapp met routeplanning, prestatieanalyse, segmentvergelijkingen en een sociale community — onmisbaar voor Nederlandse hardlopers en fietsers", "priceRange": "EUR 0-12/mnd", "bestFor": "Hardlopen & fietsen", "rating": 4.7, "affiliateLink": "https://www.strava.com/?ref=aitoolsnl"},
            {"name": "Fitbod", "verdict": "AI-krachttrainingsapp die op basis van beschikbare apparatuur, spiervolume en trainingshistorie elke workout optimaliseert voor maximale spiergroei", "priceRange": "EUR 0-13/mnd", "bestFor": "Krachttraining in de sportschool", "rating": 4.3, "affiliateLink": "https://www.fitbod.me/?ref=aitoolsnl"},
            {"name": "Aaptiv", "verdict": "AI-audiogestuurde fitnessapp met duizenden workouts onder begeleiding van coaches — van hardlopen tot yoga en krachttraining", "priceRange": "EUR 10-15/mnd", "bestFor": "Begeleide audio-workouts", "rating": 4.2, "affiliateLink": "https://aaptiv.com/?ref=aitoolsnl"},
            {"name": "Sleep Cycle", "verdict": "AI-slaaptracker die je slaapfasen analyseert via geluidsdetectie en je wekt in de lichtste slaapfase voor een fris ontwaken", "priceRange": "EUR 0-10/mnd", "bestFor": "Slaapoptimalisatie", "rating": 4.4, "affiliateLink": "https://www.sleepcycle.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-fitness-sport-gezondheid-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-fotografie-beeldbewerking-tools-2026",
        "title": "Beste AI Tools voor Fotografie & Beeldbewerking 2026: top 7 vergeleken",
        "description": "AI tools voor fotografie en beeldbewerking in 2026. Vergelijk Adobe Photoshop AI, Luminar Neo, Topaz Photo AI, Canva Foto AI, Capture One AI, Remini en Let's Enhance voor professionele fotobewerking.",
        "category": "creatie",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor fotografie en beeldbewerking in 2026. Behandel precies 7 tools: "
            "Adobe Photoshop (AI-features), Luminar Neo, Topaz Photo AI, Canva Foto AI, "
            "Capture One (AI), Remini, Let's Enhance.\n\n"
            "Structuur:\n"
            "- Introductie: AI transformeert fotobewerking in 2026 — van automatische "
            "objectverwijdering en AI-upscaling tot generatieve uitbreiding van foto's. "
            "Voor Nederlandse fotografen, marketeers en content creators.\n"
            "- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\n"
            "- Conclusie: welke tool voor welk type gebruiker (amateurfotograaf, professionele fotograaf, social media creator)\n"
            "- 3 FAQ-vragen over AI en fotobewerking\n\n"
            "Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Adobe Photoshop (AI)", "verdict": "Industriestandaard met generatieve AI-vulling, object selectie op basis van AI, neurale filters en AI-gestuurde maskers — ongelooflijk krachtig", "priceRange": "EUR 25/mnd", "bestFor": "Professionele fotobewerking", "rating": 4.8, "affiliateLink": "https://www.adobe.com/nl/products/photoshop.html?ref=aitoolsnl"},
            {"name": "Luminar Neo", "verdict": "AI-gedreven fotobewerking met automatische luchtvervanging, gezichtsverbetering, achtergrondverwijdering en AI-verlichting aanpassing", "priceRange": "EUR 10-15/mnd", "bestFor": "Snelle AI-bewerking", "rating": 4.5, "affiliateLink": "https://skylum.com/nl/luminar-neo?ref=aitoolsnl"},
            {"name": "Topaz Photo AI", "verdict": "AI-gespecialiseerd in foto-optimalisatie: denoise, upscale, sharpen en gezichtsherstel in één tool met verbluffende resultaten", "priceRange": "EUR 159/eenmalig", "bestFor": "Ruisverwijdering & upscaling", "rating": 4.7, "affiliateLink": "https://www.topazlabs.com/topaz-photo-ai?ref=aitoolsnl"},
            {"name": "Canva Foto AI", "verdict": "AI-fotobewerking in Canva's design platform — achtergrondverwijdering, AI-magic edit, bulksgewijs bewerken en automatische kleurcorrectie", "priceRange": "EUR 0-13/mnd", "bestFor": "Social media & marketing visuals", "rating": 4.4, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "Capture One (AI)", "verdict": "Professionele RAW-ontwikkelaar met AI-gestuurde kleurcorrectie, gezichtsherkenning, selectieve aanpassingen en tethered shooting", "priceRange": "EUR 24/mnd", "bestFor": "RAW-fotografie workflow", "rating": 4.6, "affiliateLink": "https://www.captureone.com/?ref=aitoolsnl"},
            {"name": "Remini", "verdict": "AI-fotoherstel en -verbetering — maakt oude, korrelige of onscherpe foto's haarscherp met indrukwekkende AI-upscaling en gezichtsherstel", "priceRange": "EUR 0-10/mnd", "bestFor": "Oude foto's herstellen", "rating": 4.3, "affiliateLink": "https://remini.ai/?ref=aitoolsnl"},
            {"name": "Let's Enhance", "verdict": "AI-beeldoptimalisatie voor e-commerce en print — upscale zonder kwaliteitsverlies, kleurcorrectie, compressor en formatconversie", "priceRange": "EUR 0-10/mnd", "bestFor": "E-commerce productfoto's", "rating": 4.2, "affiliateLink": "https://letsenhance.io/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-fotografie-beeldbewerking-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-onderwijs-bijles-elearning-tools-2026",
        "title": "Beste AI Tools voor Onderwijs, Bijles & E-learning 2026: top 7 vergeleken",
        "description": "AI tools voor onderwijs, bijles en online leren in 2026. Vergelijk Khan Academy (Khanmigo), Quizlet, Duolingo, Coursera AI, Brilliant, Grammarly en Notion AI voor studenten, docenten en levenslang leren.",
        "category": "productiviteit",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor onderwijs, bijles en e-learning in 2026. Behandel precies 7 tools: "
            "Khan Academy (Khanmigo AI), Quizlet (Q-Chat), Duolingo (AI-tutor), "
            "Coursera (AI-coach), Brilliant, Grammarly (AI-schrijfcoach), Notion AI.\n\n"
            "Structuur:\n"
            "- Introductie: AI transformeert onderwijs in 2026 — van persoonlijke AI-bijlesdocenten "
            "die 24/7 beschikbaar zijn tot adaptieve leerplatforms die zich aanpassen aan jouw tempo. "
            "Voor Nederlandse studenten, scholieren en professionals die zich willen blijven ontwikkelen.\n"
            "- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\n"
            "- Conclusie: welke tool voor welk type lerende (middelbare scholier, student, professional)\n"
            "- 3 FAQ-vragen over AI en onderwijs\n\n"
            "Focus op Nederlandse/Europese context. Prijzen in EUR. Noem Nederlands onderwijssysteem, "
            "WO/HBO/MBO. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Khan Academy (Khanmigo)", "verdict": "AI-bijlesdocent die studenten niet alleen antwoorden geeft maar door vragen te stellen laat ontdekken — een revolutie in gepersonaliseerd leren", "priceRange": "EUR 0 (gratis) / 44/jaar", "bestFor": "AI-gestuurde bijles", "rating": 4.7, "affiliateLink": "https://www.khanacademy.org/?ref=aitoolsnl"},
            {"name": "Quizlet (Q-Chat)", "verdict": "AI-leerplatform met Q-Chat, een AI-tutor die overhoringen geeft, uitleg verschaft en gepersonaliseerde flashcards genereert op basis van de lesstof", "priceRange": "EUR 0-36/jaar", "bestFor": "Overhoren & flashcards", "rating": 4.5, "affiliateLink": "https://quizlet.com/?ref=aitoolsnl"},
            {"name": "Duolingo (AI-tutor)", "verdict": "AI-gestuurde taalleerapp met adaptieve oefeningen, spraakherkenning, AI-roleplay gesprekken en gepersonaliseerde lessuggesties", "priceRange": "EUR 0-13/mnd", "bestFor": "Talen leren", "rating": 4.6, "affiliateLink": "https://www.duolingo.com/?ref=aitoolsnl"},
            {"name": "Coursera (AI-coach)", "verdict": "AI-gestuurd online leerplatform met universitaire cursussen, gepersonaliseerde leerroutes en een AI-coach die vragen beantwoordt en uitleg geeft", "priceRange": "EUR 0-50/mnd", "bestFor": "Universitaire cursussen online", "rating": 4.5, "affiliateLink": "https://www.coursera.org/?ref=aitoolsnl"},
            {"name": "Brilliant", "verdict": "AI-gedreven leerplatform voor wiskunde, programmeren en data science — interactieve lessen die zich aanpassen aan jouw niveau en tempo", "priceRange": "EUR 15-25/mnd", "bestFor": "STEM-onderwijs", "rating": 4.6, "affiliateLink": "https://brilliant.org/?ref=aitoolsnl"},
            {"name": "Grammarly (AI-schrijfcoach)", "verdict": "AI-schrijfassistent die niet alleen spelfouten corrigeert maar ook schrijfstijl, toon en helderheid analyseert — ideaal voor essays en scripties", "priceRange": "EUR 0-30/mnd", "bestFor": "Schrijfvaardigheid verbeteren", "rating": 4.4, "affiliateLink": "https://www.grammarly.com/?ref=aitoolsnl"},
            {"name": "Notion AI", "verdict": "AI-notitie- en kennismanagementtool die samenvattingen maakt, vragen beantwoordt over je aantekeningen en helpt bij het structureren van studiemateriaal", "priceRange": "EUR 0-10/mnd", "bestFor": "Studienotities & samenvattingen", "rating": 4.5, "affiliateLink": "https://www.notion.so/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-onderwijs-bijles-elearning-tools-2026", ALL_SLUGS, 3)
    },
]

def generate_article(article, idx, total):
    slug = article["slug"]
    print(f"\n{'='*60}")
    print(f"[{idx}/{total}] Generating: {slug}")
    print(f"Title: {article['title']}")

    url = f"{BASE_URL}?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": article["prompt"]}]}],
        "generationConfig": {
            "temperature": 0.8,
            "topP": 0.95,
            "maxOutputTokens": 4096,
        }
    }

    resp = requests.post(url, json=payload, timeout=120)
    if resp.status_code != 200:
        print(f"  ❌ API error {resp.status_code}: {resp.text[:300]}")
        return None

    data = resp.json()
    if not data.get("candidates"):
        print(f"  ❌ No candidates in response")
        return None

    text = data["candidates"][0]["content"]["parts"][0]["text"]

    # Build frontmatter
    today = date.today().isoformat()

    import yaml
    frontmatter = {
        "title": article["title"],
        "slug": slug,
        "description": article["description"],
        "category": article["category"],
        "rating": article.get("rating", 4.5),
        "priceRange": article.get("priceRange", "EUR 0-50/mnd"),
        "pros": [
            "Gebaseerd op actuele marktdata en praktijkervaringen uit 2026",
            "Duidelijke vergelijking met prijzen, verdicts en scores per tool",
            "Nederlandstalig en toegankelijk voor Nederlandse gebruikers",
            "Relevant voor de Nederlandse/Europese markt"
        ],
        "cons": [
            "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
            "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
            "Sommige AI-features zijn nog in actieve ontwikkeling of beta"
        ],
        "affiliateLinks": [t["affiliateLink"] for t in article["tools"]],
        "related": article["related"],
        "date": today,
        "modelYear": 2026,
        "featuredTool": article["tools"][0]["name"],
        "readingTime": "8 min",
        "tools": article["tools"],
    }

    fm_yaml = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(out_path, "w") as f:
        f.write("---\n")
        f.write(fm_yaml)
        f.write("---\n\n")
        f.write(text)

    print(f"  ✅ Written to {out_path} ({len(text)} chars)")
    return out_path

def main():
    if not API_KEY:
        print("❌ GEMINI_API_KEY not found")
        sys.exit(1)

    print(f"Generating {len(NEW_ARTICLES)} articles for content gaps...")
    print(f"API key: {API_KEY[:10]}...")
    print(f"Target dir: {ARTICLES_DIR}")
    print(f"Existing articles: {len(ALL_SLUGS)}")

    results = []
    for i, article in enumerate(NEW_ARTICLES, 1):
        result = generate_article(article, i, len(NEW_ARTICLES))
        if result:
            results.append(result)
        if i < len(NEW_ARTICLES):
            time.sleep(3)  # Rate limiting

    print(f"\n{'='*60}")
    print(f"Done! {len(results)}/{len(NEW_ARTICLES)} articles generated.")
    for r in results:
        size = os.path.getsize(r)
        print(f"  ✅ {r} ({size} bytes)")

if __name__ == "__main__":
    main()
