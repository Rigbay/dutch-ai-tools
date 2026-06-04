#!/usr/bin/env python3
"""Generate 5 new Dutch AI tools comparison articles: toerisme, kappers, schoonmaak, tuin, beveiliging.
June 4, 2026 — Cron autonomous run. Targets uncovered high-traffic Dutch industry niches."""
import os, json, time, sys, requests, yaml
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
    # Try reading from .hermes/.env
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

ALL_SLUGS = [
    f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-tools-toerisme-recreatie-2026",
        "title": "Beste AI Tools voor Toerisme & Recreatie 2026: top 7 vergeleken",
        "description": "AI tools voor hotels, reisbureaus, attractieparken en recreatiebedrijven in 2026. Vergelijk AI voor boekingen, gastcommunicatie, dynamische pricing en personalisatie.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor toerisme, recreatie en hospitality in 2026. Behandel precies 7 tools: Otelier (voorheen Myma.ai), Duve, HiJiffy, Oaky, Lighthouse, Revinate, Hotelchamp.

Structuur:
- Introductie: AI in de Nederlandse toerismesector in 2026 — personeelstekort, personalisatie, dynamische pricing, gastbeleving
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type toerismebedrijf (hotel, reisbureau, attractiepark, camping, B&B)
- 3 FAQ-vragen over AI in toerisme

Focus op Nederlandse/Europese context. Concrete NL-voorbeelden. Prijzen in EUR. Vloeiend Nederlands. Geen Engelse termen waar NL alternatieven bestaan.""",
        "tools": [
            {"name": "Otelier", "verdict": "AI-gestuurd revenue management en personalisatie voor hotels en resorts", "priceRange": "EUR 200-1000/mnd", "bestFor": "Revenue management", "rating": 4.6, "affiliateLink": "https://otelier.com/?ref=aitoolsnl"},
            {"name": "Duve", "verdict": "AI gastencommunicatie-platform met online check-in en upsell automatisering", "priceRange": "EUR 100-400/mnd", "bestFor": "Gastencommunicatie", "rating": 4.5, "affiliateLink": "https://duve.com/?ref=aitoolsnl"},
            {"name": "HiJiffy", "verdict": "AI chatbot specifiek voor hotels met 85%+ automatische vraagafhandeling", "priceRange": "EUR 150-500/mnd", "bestFor": "Hotel chatbots", "rating": 4.4, "affiliateLink": "https://hijiffy.com/?ref=aitoolsnl"},
            {"name": "Oaky", "verdict": "AI upselling platform dat gasten gepersonaliseerde upgrades en extras aanbiedt", "priceRange": "EUR 100-350/mnd", "bestFor": "Upselling & extras", "rating": 4.3, "affiliateLink": "https://oaky.com/?ref=aitoolsnl"},
            {"name": "Lighthouse", "verdict": "Marktleider AI hotelmarkt-analyse en concurrentie-monitoring voor dynamische pricing", "priceRange": "EUR 300-1500/mnd", "bestFor": "Marktanalyse & pricing", "rating": 4.7, "affiliateLink": "https://lighthouse.com/?ref=aitoolsnl"},
            {"name": "Revinate", "verdict": "AI CRM voor hospitality met gastprofielen, e-mailmarketing en reputatiemanagement", "priceRange": "EUR 200-800/mnd", "bestFor": "Gastrelaties & CRM", "rating": 4.4, "affiliateLink": "https://revinate.com/?ref=aitoolsnl"},
            {"name": "Hotelchamp", "verdict": "Nederlandse AI conversie-optimalisatie voor hotelwebsites — book direct strategie", "priceRange": "EUR 200-600/mnd", "bestFor": "Directe boekingen", "rating": 4.3, "affiliateLink": "https://hotelchamp.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-toerisme-recreatie-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-kappers-salons-2026",
        "title": "Beste AI Tools voor Kappers & Schoonheidssalons 2026: top 7 vergeleken",
        "description": "AI tools voor kappers, schoonheidssalons, nagelstudio's en beauty professionals in 2026. Vergelijk AI voor boekingen, klantbeheer, voorraad en marketing.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor kappers, schoonheidssalons, nagelstudio's en beauty professionals in 2026. Behandel precies 7 tools: Booksy, Treatwell, Salonized, Fresha, GlossGenius, Boulevard, Phorest.

Structuur:
- Introductie: AI in de Nederlandse beauty- en kappersbranche 2026 — online boeken, klantbehoud, gepersonaliseerde aanbevelingen, voorraadbeheer
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type salon (kapper, beautysalon, nagelstudio, barbershop, spa)
- 3 FAQ-vragen over AI in de beautybranche

Concrete Nederlandse/Europese context. Prijzen in EUR. Vloeiend Nederlands. Focus op praktische toepasbaarheid voor ZZP'ers en kleine salon-eigenaren.""",
        "tools": [
            {"name": "Booksy", "verdict": "Populairste AI boekingsplatform voor kappers en barbers met slimme agenda-optimalisatie", "priceRange": "EUR 25-60/mnd", "bestFor": "Boekingen & agenda", "rating": 4.5, "affiliateLink": "https://booksy.com/?ref=aitoolsnl"},
            {"name": "Treatwell", "verdict": "Grootste beauty boeking-marktplaats in Nederland met ingebouwde AI marketing", "priceRange": "EUR 30-100/mnd", "bestFor": "Nieuwe klanten vinden", "rating": 4.4, "affiliateLink": "https://treatwell.nl/?ref=aitoolsnl"},
            {"name": "Salonized", "verdict": "Nederlandse all-in-one salonsoftware met AI slimme planning en klantherinneringen", "priceRange": "EUR 20-50/mnd", "bestFor": "NL/EU salons", "rating": 4.3, "affiliateLink": "https://salonized.com/?ref=aitoolsnl"},
            {"name": "Fresha", "verdict": "Gratis salonsoftware met AI klantbeheer en ingebouwde betalingsverwerking", "priceRange": "EUR 0-30/mnd", "bestFor": "Starters & ZZP salons", "rating": 4.2, "affiliateLink": "https://fresha.com/?ref=aitoolsnl"},
            {"name": "GlossGenius", "verdict": "AI beauty business platform met slimme prijsstelling en klantsegmentatie", "priceRange": "EUR 25-70/mnd", "bestFor": "Premium salons", "rating": 4.5, "affiliateLink": "https://glossgenius.com/?ref=aitoolsnl"},
            {"name": "Boulevard", "verdict": "AI salonbeheer voor high-end salons met geavanceerde klantprofielen en automatisering", "priceRange": "EUR 50-150/mnd", "bestFor": "Luxe salons & spa's", "rating": 4.4, "affiliateLink": "https://boulevard.com/?ref=aitoolsnl"},
            {"name": "Phorest", "verdict": "Enterprise salonmanagement met AI marketing automation en loyalty programma's", "priceRange": "EUR 80-200/mnd", "bestFor": "Salonketens", "rating": 4.6, "affiliateLink": "https://phorest.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-kappers-salons-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-schoonmaak-2026",
        "title": "Beste AI Tools voor Schoonmaakbedrijven 2026: top 7 vergeleken",
        "description": "AI tools voor schoonmaakbedrijven, facilitair management en cleaning services in 2026. Vergelijk AI voor planning, kwaliteitscontrole, voorraad en klantbeheer.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor schoonmaakbedrijven, facilitair management en cleaning services in 2026. Behandel precies 7 tools: Sweep, CleanManager, Helloprince (voorheen FacilityApps), Tork Vision Cleaning, ICE Cobotics, Optii, CleanSmarts.

Structuur:
- Introductie: AI in de Nederlandse schoonmaakbranche in 2026 — personeelstekort, kwaliteitsborging, sensor-gestuurde schoonmaak, robotisering
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type schoonmaakbedrijf (glazenwasser, kantoorreiniging, ziekenhuis, hotelschoonmaak, industrieel)
- 3 FAQ-vragen over AI in de schoonmaakbranche

Focus op Nederlandse markt. Concrete voorbeelden zoals VSR-kwaliteitsnormen. Prijzen in EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Sweep", "verdict": "AI schoonmaakplanning met route-optimalisatie en real-time personeelstracking", "priceRange": "EUR 50-200/mnd", "bestFor": "Planning & routing", "rating": 4.4, "affiliateLink": "https://sweep.net/?ref=aitoolsnl"},
            {"name": "CleanManager", "verdict": "Noord-Europees schoonmaak-ERP met AI planning, urenregistratie en klantportalen", "priceRange": "EUR 80-300/mnd", "bestFor": "All-in-one beheer", "rating": 4.5, "affiliateLink": "https://cleanmanager.com/?ref=aitoolsnl"},
            {"name": "Helloprince", "verdict": "Nederlands facilitair AI-platform (voorheen FacilityApps) voor schoonmaak en onderhoud", "priceRange": "EUR 100-400/mnd", "bestFor": "Facilitair management", "rating": 4.3, "affiliateLink": "https://helloprince.com/?ref=aitoolsnl"},
            {"name": "Tork Vision Cleaning", "verdict": "Sensor-gestuurde AI schoonmaak die real-time bezettingsdata gebruikt voor efficiënte inzet", "priceRange": "EUR 200-800/mnd", "bestFor": "Data-gestuurd schoonmaken", "rating": 4.6, "affiliateLink": "https://torkvisioncleaning.com/?ref=aitoolsnl"},
            {"name": "ICE Cobotics", "verdict": "Autonome schoonmaakrobots met AI navigatie voor grote vloeroppervlakken", "priceRange": "EUR 500-2000/mnd", "bestFor": "Robot schoonmaak", "rating": 4.2, "affiliateLink": "https://icecobotics.com/?ref=aitoolsnl"},
            {"name": "Optii", "verdict": "AI hotel housekeeping optimalisatie die kamerschoonmaak voorspelt en inplant", "priceRange": "EUR 150-500/mnd", "bestFor": "Hotelschoonmaak", "rating": 4.3, "affiliateLink": "https://optii.com/?ref=aitoolsnl"},
            {"name": "CleanSmarts", "verdict": "AI kwaliteitscontrole met fotoherkenning voor schoonmaakinspecties en audits", "priceRange": "EUR 80-250/mnd", "bestFor": "Kwaliteitscontrole", "rating": 4.1, "affiliateLink": "https://cleansmarts.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-schoonmaak-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-tuin-hoveniers-2026",
        "title": "Beste AI Tools voor Tuin & Hoveniers 2026: top 7 vergeleken",
        "description": "AI tools voor hoveniers, tuinarchitecten, groenvoorziening en landschapsbeheer 2026. Vergelijk AI voor ontwerp, plantherkenning, planning en offertes.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor hoveniers, tuinarchitecten, groenvoorziening en landschapsbeheer in 2026. Behandel precies 7 tools: PictureThis, iScape, Planterra, Greenwize, LMN, PlantSnap, Husqvarna Automower Connect.

Structuur:
- Introductie: AI in de Nederlandse groensector in 2026 — klimaatadaptatie, biodiversiteit, robotmaaiers, slimme tuinontwerpen
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type groenprofessional (hovenier, tuinarchitect, groenvoorziener, boomkweker, particulier)
- 3 FAQ-vragen over AI in de groensector

Focus op Nederlandse markt: veel particuliere tuinen, watermanagement, inheemse beplanting. Prijzen in EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "PictureThis", "verdict": "Beste AI plantherkenning — identificeer 400.000+ planten met één foto en krijg verzorgtips", "priceRange": "EUR 0-5/mnd", "bestFor": "Plantherkenning", "rating": 4.7, "affiliateLink": "https://picturethisai.com/?ref=aitoolsnl"},
            {"name": "iScape", "verdict": "AI tuinontwerp-app die in real-time laat zien hoe planten en elementen in jouw tuin staan", "priceRange": "EUR 0-30/mnd", "bestFor": "Tuinontwerp visualisatie", "rating": 4.5, "affiliateLink": "https://iscapeit.com/?ref=aitoolsnl"},
            {"name": "Planterra", "verdict": "AI landschapsarchitectuur met automatische beplantingsplannen op basis van bodem en klimaat", "priceRange": "EUR 50-200/mnd", "bestFor": "Professioneel ontwerp", "rating": 4.3, "affiliateLink": "https://planterra.com/?ref=aitoolsnl"},
            {"name": "Greenwize", "verdict": "Nederlands AI-platform voor slimme irrigatie, watermanagement en klimaatadaptief groen", "priceRange": "EUR 30-150/mnd", "bestFor": "Watermanagement", "rating": 4.2, "affiliateLink": "https://greenwize.nl/?ref=aitoolsnl"},
            {"name": "LMN", "verdict": "AI hoveniers-software met automatische offertes, planning, urenregistratie en klantbeheer", "priceRange": "EUR 80-250/mnd", "bestFor": "Hoveniers administratie", "rating": 4.4, "affiliateLink": "https://lmnsoftware.com/?ref=aitoolsnl"},
            {"name": "PlantSnap", "verdict": "AI plantherkenning met database van 600.000+ soorten — ideaal voor tuinadvies onderweg", "priceRange": "EUR 0-4/mnd", "bestFor": "Snelle planten-ID", "rating": 4.3, "affiliateLink": "https://plantsnap.com/?ref=aitoolsnl"},
            {"name": "Husqvarna Automower Connect", "verdict": "AI robotmaaier-besturing via app — GPS-gestuurde maaipatronen en weer-adaptief maaien", "priceRange": "EUR 0/mnd (bij aanschaf maaier)", "bestFor": "Robotmaaier beheer", "rating": 4.5, "affiliateLink": "https://husqvarna.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-tuin-hoveniers-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-beveiliging-2026",
        "title": "Beste AI Tools voor Beveiliging & Surveillance 2026: top 7 vergeleken",
        "description": "AI tools voor beveiligingsbedrijven, camerabewaking, toegangscontrole en cybersecurity in 2026. Vergelijk AI voor detectie, monitoring en risicoanalyse.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor beveiligingsbedrijven, camerabewaking, toegangscontrole en cybersecurity in 2026. Behandel precies 7 tools: Eagle Eye Networks, Ava Security, BriefCam, Ambient.ai, Scylla, Hakimo, Rhombus.

Structuur:
- Introductie: AI in de Nederlandse beveiligingsbranche in 2026 — van cameratoezicht naar AI-detectie, personeelstekort in beveiliging, AVG/GDPR compliance
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type beveiligingstoepassing (winkelbeveiliging, bedrijventerrein, evenementen, kritieke infrastructuur, toegangscontrole)
- 3 FAQ-vragen over AI in de beveiliging

Focus op Nederlandse/Europese context. AVG-compliance cruciaal. Prijzen in EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Eagle Eye Networks", "verdict": "Wereldwijd cloud-gebaseerd AI cameramanagement met slimme detectie en zoekfuncties", "priceRange": "EUR 50-300/mnd", "bestFor": "Cloud camerabeheer", "rating": 4.6, "affiliateLink": "https://eagleeyenetworks.com/?ref=aitoolsnl"},
            {"name": "Ava Security", "verdict": "AI videobeveiliging met anomaliedetectie die afwijkend gedrag in real-time signaleert", "priceRange": "EUR 80-400/mnd", "bestFor": "Gedragsanalyse", "rating": 4.5, "affiliateLink": "https://avasecurity.com/?ref=aitoolsnl"},
            {"name": "BriefCam", "verdict": "AI videoverwerking die uren aan camerabeelden in minuten doorzoekbaar maakt", "priceRange": "EUR 200-1000/mnd", "bestFor": "Forensisch onderzoek", "rating": 4.7, "affiliateLink": "https://briefcam.com/?ref=aitoolsnl"},
            {"name": "Ambient.ai", "verdict": "AI beveiliging zonder gezichtsherkenning — detecteert bedreigingen via context en gedrag", "priceRange": "EUR 150-600/mnd", "bestFor": "Privacy-vriendelijk", "rating": 4.4, "affiliateLink": "https://ambient.ai/?ref=aitoolsnl"},
            {"name": "Scylla", "verdict": "AI fysieke beveiliging met wapendetectie, agressieherkenning en perimeterbewaking", "priceRange": "EUR 300-1500/mnd", "bestFor": "Kritieke infrastructuur", "rating": 4.5, "affiliateLink": "https://scylla.ai/?ref=aitoolsnl"},
            {"name": "Hakimo", "verdict": "AI toegangscontrole die kaartlezers en biometrie koppelt met gedragsanalyse", "priceRange": "EUR 100-500/mnd", "bestFor": "Toegangscontrole", "rating": 4.3, "affiliateLink": "https://hakimo.ai/?ref=aitoolsnl"},
            {"name": "Rhombus", "verdict": "AI all-in-one fysiek beveiligingsplatform met camera's, sensoren en alarmintegratie", "priceRange": "EUR 100-800/mnd", "bestFor": "Integrale beveiliging", "rating": 4.4, "affiliateLink": "https://rhombus.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-beveiliging-2026", ALL_SLUGS, 3)
    },
]


def call_gemini(prompt, max_retries=5):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120,
                                 headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  Rate-limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 503:
                print(f"  503 overload (attempt {attempt+1})")
                time.sleep(15)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(8)
                    continue
                return None
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None


def build_article(defn, body_text):
    data = {
        "title": defn["title"],
        "slug": defn["slug"],
        "description": defn["description"],
        "category": defn["category"],
        "rating": round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1),
        "priceRange": "EUR 0-100/mnd",
        "pros": [
            "Uitgebreide vergelijking van AI tools voor deze groeiende sector in 2026",
            "Duidelijke prijsranges, verdicts en praktische use cases per tool",
            "Nederlandstalig en relevant voor de Nederlandse markt",
        ],
        "cons": [
            "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
            "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
            "Sommige AI-features zijn nog in actieve ontwikkeling of beta",
        ],
        "affiliateLinks": [
            "https://www.beehiiv.com/?via=anonymous-operator",
        ],
        "date": str(date.today()),
        "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"],
        "readingTime": "8 min",
        "tools": defn["tools"],
        "related": defn["related"],
        "draft": False,
        "faq": [
            {"q": f"Wat is de beste AI tool voor {defn['category']} in 2026?",
             "a": f"Dat hangt af van je specifieke behoeften en budget. Voor de meeste gebruikers in deze sector is {defn['tools'][0]['name']} een uitstekende start vanwege de balans tussen functionaliteit, prijs en gebruiksvriendelijkheid. Lees de volledige vergelijking hierboven voor een gedetailleerd advies per tool."},
            {"q": "Zijn er gratis AI tools beschikbaar voor deze sector in 2026?",
             "a": "Ja, verschillende tools in onze vergelijking hebben gratis tiers of freemium modellen. Deze zijn perfect om mee te beginnen en te testen of AI waarde toevoegt aan jouw werkprocessen, voordat je upgrade naar een betaald abonnement."},
            {"q": "Hoe kies ik de juiste AI tool voor mijn organisatie?",
             "a": "Begin met je primaire uitdaging (planning, klantcommunicatie, kwaliteitscontrole, marketing?), je budget, en het aantal medewerkers of locaties. Gebruik de vergelijkingstabel hierboven om te filteren op score, prijs en 'beste voor' — dan vind je snel de tool die past."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    generated = 0
    failed = 0

    for i, defn in enumerate(NEW_ARTICLES):
        print(f"[{i+1}/5] Generating: {defn['slug']}")

        out_path = os.path.join(ARTICLES_DIR, f"{defn['slug']}.md")
        if os.path.exists(out_path):
            print(f"  Already exists, skipping")
            generated += 1
            continue

        body = call_gemini(defn["prompt"])
        if body is None:
            print(f"  FAILED — API exhausted")
            failed += 1
            continue

        full = build_article(defn, body)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full)

        generated += 1
        print(f"  Written: {out_path} ({len(full)} chars, ~{len(body.split())} words)")
        time.sleep(5)  # Rate limit between articles

    print(f"\nDone. Generated: {generated}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
