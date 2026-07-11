#!/usr/bin/env python3
"""Generate 4 new Dutch AI tools comparison articles: Google Ads vs Meta vs TikTok,
Google Drive vs Dropbox vs OneDrive, Salesforce vs HubSpot vs Zoho CRM, Figma vs Canva vs Sketch.
June 4, 2026 — Hermes cron autonomous run."""
import os, json, time, sys, requests, yaml
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
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
    """Pick N related slugs avoiding self-reference. Prefer same-category."""
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "google-ads-vs-meta-ads-vs-tiktok-ads-2026",
        "title": "Google Ads vs Meta Ads vs TikTok Ads 2026: beste advertentieplatform vergeleken",
        "description": "Google Ads, Meta Ads of TikTok Ads in 2026? Vergelijk de beste online advertentieplatforms op targeting, kosten, ROI en gebruiksvriendelijkheid voor Nederlandse adverteerders.",
        "category": "marketing",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Google Ads vs Meta Ads vs TikTok Ads in 2026. Behandel precies 7 tools: Google Ads, Meta Ads (Facebook/Instagram), TikTok Ads, LinkedIn Ads, Pinterest Ads, Microsoft Advertising, Snapchat Ads.

Structuur:
- Introductie: het Nederlandse online advertentielandschap in 2026 — cookieloze targeting, AI campagnes, kosten per platform
- Per platform een ## kop met: beschrijving, prijsmodel (CPC/CPM range in EUR), beste use case (e-commerce, B2B, brand awareness, etc.), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 platforms: naam, gemiddelde CPC (EUR), beste-voor, score (1-5)
- Conclusie: welk platform voor welke type adverteerder (lokale winkel, e-commerce, B2B, startup, groot merk)
- 3 FAQ-vragen over online adverteren in Nederland

Focus op Nederlandse markt. Concrete CPC ranges (Google €0.50-3 EUR, Meta €0.30-2 EUR, TikTok €0.20-1.50 EUR voor NL). Vloeiend Nederlands. Praktische budgetadviezen.""",
        "tools": [
            {"name": "Google Ads", "verdict": "Breedste bereik met zoekintentie — mensen zoeken actief naar jouw product", "priceRange": "EUR 0.50-3 CPC", "bestFor": "Zoekintentie & Shopping", "rating": 4.8, "affiliateLink": "https://ads.google.com/?ref=aitoolsnl"},
            {"name": "Meta Ads", "verdict": "Beste targeting op interesses, gedrag en lookalike audiences — grootste sociale bereik", "priceRange": "EUR 0.30-2 CPC", "bestFor": "Social & Branding", "rating": 4.7, "affiliateLink": "https://business.facebook.com/?ref=aitoolsnl"},
            {"name": "TikTok Ads", "verdict": "Hoogste engagement voor jongere doelgroepen met virale short-form video ads", "priceRange": "EUR 0.20-1.50 CPC", "bestFor": "Gen Z & Creatieve campagnes", "rating": 4.6, "affiliateLink": "https://ads.tiktok.com/?ref=aitoolsnl"},
            {"name": "LinkedIn Ads", "verdict": "Ongeëvenaarde B2B targeting op functie, branche en bedrijfsgrootte", "priceRange": "EUR 3-10 CPC", "bestFor": "B2B & Recruitment", "rating": 4.4, "affiliateLink": "https://business.linkedin.com/?ref=aitoolsnl"},
            {"name": "Pinterest Ads", "verdict": "Visuele discovery met hoge koopintentie — ideaal voor lifestyle en interieur", "priceRange": "EUR 0.20-1.50 CPC", "bestFor": "Lifestyle & Inspiratie", "rating": 4.2, "affiliateLink": "https://ads.pinterest.com/?ref=aitoolsnl"},
            {"name": "Microsoft Advertising", "verdict": "Kleine concurrentie, lagere CPC's — bereikt de 10% die niet op Google zoekt", "priceRange": "EUR 0.30-2 CPC", "bestFor": "Budget & Aanvullend", "rating": 4.1, "affiliateLink": "https://ads.microsoft.com/?ref=aitoolsnl"},
            {"name": "Snapchat Ads", "verdict": "AR filters en lenses voor interactieve campagnes bij jongste doelgroep", "priceRange": "EUR 0.15-1 CPC", "bestFor": "AR & Jongeren 13-24", "rating": 4.0, "affiliateLink": "https://ads.snapchat.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("google-ads-vs-meta-ads-vs-tiktok-ads-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "google-drive-vs-dropbox-vs-onedrive-2026",
        "title": "Google Drive vs Dropbox vs OneDrive 2026: beste cloudopslag vergeleken",
        "description": "Google Drive, Dropbox of OneDrive in 2026? Vergelijk de beste cloudopslag op prijs, opslagruimte, samenwerken, beveiliging en AI-features voor Nederlandse gebruikers.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Google Drive vs Dropbox vs OneDrive in 2026. Behandel precies 7 tools: Google Drive/Google One, Dropbox, Microsoft OneDrive, iCloud Drive, pCloud, Internxt, Proton Drive.

Structuur:
- Introductie: cloudopslag in 2026 — AI-zoeken, zero-knowledge encryptie, prijzenoorlog, Nederlandse adoptie
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), opslagruimte (gratis/betaald), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, gratis opslag, prijs per TB (EUR), beste-voor, score (1-5)
- Conclusie: welke voor welk type gebruiker (student, ZZP, klein bedrijf, privacy-bewust, Apple-gebruiker, enterprise)
- 3 FAQ-vragen over cloudopslag en privacy

Focus op Nederlandse/Europese context. Prijzen in EUR. AVG-compliance benoemen bij EU-gebaseerde tools. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Google Drive/One", "verdict": "Beste allround met 15GB gratis, Gemini AI-zoeken en naadloze Workspace-integratie", "priceRange": "EUR 0-20/mnd", "bestFor": "Algemeen & Google-ecosysteem", "rating": 4.7, "affiliateLink": "https://one.google.com/?ref=aitoolsnl"},
            {"name": "Dropbox", "verdict": "Beste sync-technologie en samenwerkingsfeatures, maar duurder dan concurrenten", "priceRange": "EUR 0-18/mnd", "bestFor": "Bestanden sync & delen", "rating": 4.5, "affiliateLink": "https://dropbox.com/?ref=aitoolsnl"},
            {"name": "Microsoft OneDrive", "verdict": "Onmisbaar voor Microsoft 365-gebruikers met 1TB per gebruiker inbegrepen", "priceRange": "EUR 0-10/mnd", "bestFor": "Microsoft 365 gebruikers", "rating": 4.6, "affiliateLink": "https://onedrive.live.com/?ref=aitoolsnl"},
            {"name": "iCloud Drive", "verdict": "Naadloos in Apple-ecosysteem, maar beperkt buiten Apple-apparaten", "priceRange": "EUR 0-10/mnd", "bestFor": "Apple gebruikers", "rating": 4.3, "affiliateLink": "https://icloud.com/?ref=aitoolsnl"},
            {"name": "pCloud", "verdict": "Beste prijs met lifetime-abonnementen, zero-knowledge encryptie en EU-servers (Luxemburg)", "priceRange": "EUR 0-5/mnd", "bestFor": "Budget & privacy", "rating": 4.4, "affiliateLink": "https://pcloud.com/?ref=aitoolsnl"},
            {"name": "Internxt", "verdict": "Spaans privacy-first alternatief met end-to-end encryptie en AVG-compliance by design", "priceRange": "EUR 0-10/mnd", "bestFor": "AVG & Privacy-first", "rating": 4.2, "affiliateLink": "https://internxt.com/?ref=aitoolsnl"},
            {"name": "Proton Drive", "verdict": "Zwitserse zero-knowledge encryptie van Proton — volledige privacy met vertrouwde beveiliging", "priceRange": "EUR 0-13/mnd", "bestFor": "Maximale privacy", "rating": 4.3, "affiliateLink": "https://proton.me/drive?ref=aitoolsnl"},
        ],
        "related": pick_related("google-drive-vs-dropbox-vs-onedrive-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "salesforce-vs-hubspot-vs-zoho-crm-2026",
        "title": "Salesforce vs HubSpot vs Zoho CRM 2026: beste CRM software vergeleken",
        "description": "Salesforce, HubSpot of Zoho CRM in 2026? Vergelijk de beste CRM software op prijs, gebruiksgemak, AI-features, integraties en schaalbaarheid voor Nederlandse bedrijven.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Salesforce vs HubSpot vs Zoho CRM in 2026. Behandel precies 7 tools: Salesforce, HubSpot CRM, Zoho CRM, Pipedrive, Microsoft Dynamics 365, Monday CRM, Teamleader.

Structuur:
- Introductie: CRM in 2026 — AI-gedreven salestools, voorspellende analytics, Nederlandse CRM-adoptie
- Per tool een ## kop met: beschrijving, prijsrange (EUR/gebruiker/maand), beste use case (MKB, enterprise, sales, marketing), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR), beste-voor, score (1-5)
- Conclusie: welke CRM voor welk type bedrijf (ZZP, MKB 5-50 man, MKB 50-250, enterprise, sales-gedreven, marketing-gedreven, Nederlands/Belgisch)
- 3 FAQ-vragen over CRM-keuze

Focus op Nederlandse/Belgische markt. Teamleader specifiek als Benelux-speler benoemen. Prijzen in EUR. Vloeiend Nederlands. Concrete implementatietips.""",
        "tools": [
            {"name": "Salesforce", "verdict": "De onbetwiste enterprise-standaard met Einstein AI en ongeëvenaarde schaalbaarheid", "priceRange": "EUR 25-300/gebruiker/mnd", "bestFor": "Enterprise & Maatwerk", "rating": 4.7, "affiliateLink": "https://salesforce.com/?ref=aitoolsnl"},
            {"name": "HubSpot CRM", "verdict": "Beste gratis startpunt met soepele groei naar marketing en service hubs", "priceRange": "EUR 0-100/gebruiker/mnd", "bestFor": "MKB & Inbound marketing", "rating": 4.6, "affiliateLink": "https://hubspot.com/?ref=aitoolsnl"},
            {"name": "Zoho CRM", "verdict": "Meeste waar voor je geld met Canvas AI-studio en 40+ geïntegreerde Zoho-apps", "priceRange": "EUR 0-45/gebruiker/mnd", "bestFor": "Budget & All-in-one", "rating": 4.5, "affiliateLink": "https://zoho.com/crm/?ref=aitoolsnl"},
            {"name": "Pipedrive", "verdict": "Visueel sterk en gebruiksvriendelijk — gemaakt door salesmensen voor salesmensen", "priceRange": "EUR 12-60/gebruiker/mnd", "bestFor": "Sales-pijplijn focus", "rating": 4.5, "affiliateLink": "https://pipedrive.com/?ref=aitoolsnl"},
            {"name": "Microsoft Dynamics 365", "verdict": "Naadloze integratie met Office en Azure AI — ideaal voor Microsoft-first organisaties", "priceRange": "EUR 50-150/gebruiker/mnd", "bestFor": "Microsoft-ecosysteem", "rating": 4.3, "affiliateLink": "https://dynamics.microsoft.com/?ref=aitoolsnl"},
            {"name": "Monday CRM", "verdict": "Flexibele CRM op het visuele Monday-platform — eenvoudig aanpasbaar zonder code", "priceRange": "EUR 12-28/gebruiker/mnd", "bestFor": "Visuele teams", "rating": 4.3, "affiliateLink": "https://monday.com/crm/?ref=aitoolsnl"},
            {"name": "Teamleader", "verdict": "Belgisch/Nederlands CRM met facturatie en urenregistratie — specifiek voor Benelux MKB", "priceRange": "EUR 25-60/gebruiker/mnd", "bestFor": "Benelux MKB", "rating": 4.2, "affiliateLink": "https://teamleader.eu/?ref=aitoolsnl"},
        ],
        "related": pick_related("salesforce-vs-hubspot-vs-zoho-crm-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "figma-vs-canva-vs-sketch-2026",
        "title": "Figma vs Canva vs Sketch 2026: beste designtools vergeleken",
        "description": "Figma, Canva of Sketch in 2026? Vergelijk de beste designsoftware op samenwerking, gebruiksgemak, AI-functies, prijs en geschiktheid voor Nederlandse designers en marketeers.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Figma vs Canva vs Sketch in 2026. Behandel precies 7 tools: Figma, Canva, Sketch, Adobe Express, Framer, Penpot, CorelDRAW.

Structuur:
- Introductie: designtools in 2026 — AI-generatie, realtime samenwerken, browser-based vs native, de democratisering van design
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (UI/UX, social media, branding, print, web design), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR), beste-voor, score (1-5)
- Conclusie: welke tool voor wie (UI/UX designer, marketeer, social media manager, ZZP ondernemer, print designer, web developer, student)
- 3 FAQ-vragen over de beste designtools in 2026

Focus op Nederlandse/Europese context. Figma's overname door Adobe en de opkomst van open-source alternatief Penpot benoemen. Prijzen in EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Figma", "verdict": "De gouden standaard voor UI/UX design met realtime samenwerking en Figma AI in 2026", "priceRange": "EUR 0-45/mnd", "bestFor": "UI/UX Design & Teams", "rating": 4.8, "affiliateLink": "https://figma.com/?ref=aitoolsnl"},
            {"name": "Canva", "verdict": "De meest toegankelijke allrounder — perfect voor social media, presentaties en snelle visuals", "priceRange": "EUR 0-13/mnd", "bestFor": "Marketing & Social media", "rating": 4.7, "affiliateLink": "https://canva.com/?ref=aitoolsnl"},
            {"name": "Sketch", "verdict": "Mac-only krachtpatser met sterke vector-editing en uitgebreid plugin-ecosysteem", "priceRange": "EUR 0-12/mnd", "bestFor": "Mac designers", "rating": 4.3, "affiliateLink": "https://sketch.com/?ref=aitoolsnl"},
            {"name": "Adobe Express", "verdict": "Adobe's antwoord op Canva met Firefly AI en naadloze Creative Cloud integratie", "priceRange": "EUR 0-12/mnd", "bestFor": "Adobe-ecosysteem gebruikers", "rating": 4.4, "affiliateLink": "https://adobe.com/express/?ref=aitoolsnl"},
            {"name": "Framer", "verdict": "Design-tool die direct publiceerbare websites genereert — van mockup naar live in minuten", "priceRange": "EUR 0-25/mnd", "bestFor": "Webdesign & Prototyping", "rating": 4.5, "affiliateLink": "https://framer.com/?ref=aitoolsnl"},
            {"name": "Penpot", "verdict": "Open-source Figma-alternatief met volledige CSS-standaarden en self-host optie — groeiend in Europa", "priceRange": "EUR 0/mnd (gratis)", "bestFor": "Open-source & Privacy", "rating": 4.2, "affiliateLink": "https://penpot.app/?ref=aitoolsnl"},
            {"name": "CorelDRAW", "verdict": "Veteraan voor vectorillustratie en printdesign met sterke AI-ondersteuning in 2026", "priceRange": "EUR 30/mnd of EUR 799 eenmalig", "bestFor": "Print & Illustratie", "rating": 4.1, "affiliateLink": "https://coreldraw.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("figma-vs-canva-vs-sketch-2026", ALL_SLUGS, 3)
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
            "Uitgebreide vergelijking van de beste tools in deze categorie voor 2026",
            "Duidelijke prijsranges, verdicts en praktische use cases per tool",
            "Nederlandstalig en relevant voor de Nederlandse markt",
        ],
        "cons": [
            "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
            "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
            "Sommige AI-features zijn nog in actieve ontwikkeling of beta",
        ],
        "affiliateLinks": [
            "https://www.beehiiv.com/",
        ],
        "date": str(date.today()),
        "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"],
        "readingTime": "8 min",
        "tools": defn["tools"],
        "related": defn["related"],
        "draft": False,
        "faq": [
            {"q": f"Wat is de beste tool in {defn['title'].split(':')[0].strip()} in 2026?",
             "a": f"Dat hangt af van je specifieke behoeften en budget. Voor de meeste gebruikers is {defn['tools'][0]['name']} een uitstekende start vanwege de balans tussen functionaliteit, prijs en gebruiksvriendelijkheid. Lees de volledige vergelijking hierboven voor een gedetailleerd advies per tool."},
            {"q": "Zijn er gratis alternatieven beschikbaar in 2026?",
             "a": "Ja, verschillende tools in onze vergelijking hebben gratis tiers of freemium modellen. Deze zijn perfect om mee te beginnen en te testen voordat je upgrade naar een betaald abonnement."},
            {"q": "Hoe kies ik de juiste tool voor mijn situatie?",
             "a": "Begin met je primaire use case, budget en aantal gebruikers. Gebruik de vergelijkingstabel hierboven om te filteren op score, prijs en 'beste voor' — dan vind je snel de tool die bij jouw situatie past."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    generated = 0
    failed = 0

    for i, defn in enumerate(NEW_ARTICLES):
        print(f"[{i+1}/4] Generating: {defn['slug']}")

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
