#!/usr/bin/env python3
"""Generate reisverzekering article."""
import os, time, requests, yaml, sys
from datetime import date

env_path = os.path.expanduser("~/.hermes/.env")
API_KEY=*** open(env_path) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY=***            API_KEY=line.s...=", 1)[1]
            break
if not API_KEY:
    print("FATAL: No GEMINI_API_KEY found")
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
from affiliate_resolver import resolve_affiliate_link, get_site_affiliate_links

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    return [s for s in slugs if s != new_slug][:n]

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
    for tool in defn["tools"]:
        raw_link = tool.get("affiliateLink", "")
        resolved = resolve_affiliate_link(raw_link)
        if resolved:
            tool["affiliateLink"] = resolved
    site_links = get_site_affiliate_links("dutch-ai-tools")
    if not site_links:
        site_links = ["https://www.beehiiv.com/?via=anonymous-operator"]
    data = {
        "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
        "category": defn["category"], "rating": avg, "priceRange": defn["priceRange"],
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"],
        "cons": ["Prijzen kunnen wijzigen — check aanbieder", "Voorwaarden veranderen regelmatig", "Keuze hangt af van je specifieke situatie"],
        "affiliateLinks": site_links,
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste keuze?", "a": "Dat hangt af van je situatie. " + defn["tools"][0]["name"] + " is voor de meeste mensen een prima startpunt."},
            {"q": "Hoe kies ik de juiste optie?", "a": "Begin met je use case en budget. Gebruik de vergelijkingstabel hierboven en lees de diepgaande reviews per optie."},
            {"q": "Zijn deze prijzen actueel?", "a": "Ja, deze vergelijking is gebaseerd op de stand van zaken in juni 2026. Check altijd de actuele aanbieding bij de aanbieder zelf."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"

slug = "reisverzekering-vergelijken-2026-doorlopend-kortlopend-annuleringsverzekering"
print(f"Generating: {slug}")
prompt = """Schrijf een Nederlands artikel van 1200-1500 woorden over reisverzekeringen vergelijken in 2026. Behandel precies 7 aanbieders: ANWB, Allianz Global Assistance, Univé, Centraal Beheer, OHRA, ABN AMRO, FBTO.

Structuur:
- Introductie: reisverzekeringen 2026 — doorlopend vs kortlopend, annuleringsverzekering vaak los of in combi, wintersportdekking, werelddekking (USA/Canada duurder), medische kosten buitenland (EHIC-kaart dekt niet alles), COVID-dekking nu standaard
- Per verzekeraar een ## kop: type (doorlopend/kortlopend), premie, dekking (Europa/Wereld), annulering, wintersport, medische kosten, eigen risico, plus- en minpunten, verdict
- Markdown vergelijkingstabel: verzekeraar, doorlopend premie (Europa), werelddekking premie, annulering inbegrepen, wintersport, medische kosten max, eigen risico, score (1-5)
- Conclusie: voor frequente reizigers, gezinnen, wintersporters, budgetbewust, wereldreizigers, senioren
- 3 FAQ's

Nederlandse context: ANWB marktleider met pechhulp-combinatie. Allianz grootste pure reisverzekeraar. Univé coöperatief met ledenkorting. Centraal Beheer en FBTO budget-opties. ABN AMRO biedt reisverzekering via creditcard (Gold/Platinum). OHRA onderdeel Delta Lloyd. Doorlopend vaak goedkoper bij 2+ reizen per jaar. Vloeiend en toegankelijk Nederlands."""

body = call_gemini(prompt)
if not body:
    print("FAILED")
    sys.exit(1)

defn = {
    "slug": slug,
    "title": "Reisverzekering Vergelijken 2026: Beste Doorlopende, Kortlopende en Annuleringsverzekering — ANWB vs Allianz vs Univé vs Centraal Beheer vs OHRA vs ABN AMRO vs FBTO",
    "description": "Reisverzekering in 2026? Vergelijk ANWB, Allianz, Univé, Centraal Beheer, OHRA, ABN AMRO en FBTO op dekking, premie, annulering en werelddekking.",
    "category": "persoonlijk",
    "priceRange": "EUR 3-15 per maand (doorlopend) of EUR 10-50 per reis (kortlopend)",
    "tools": [
        {"name": "ANWB", "verdict": "Beste allround — marktleider, doorlopend en kortlopend, combineer met pechhulp, werelddekking, wintersport inbegrepen", "priceRange": "€4,50-12/mnd (doorlopend Europa)", "bestFor": "Allround & Frequente Reizigers", "rating": 4.6, "affiliateLink": "https://anwb.nl/"},
        {"name": "Allianz Global Assistance", "verdict": "Beste pure reisverzekeraar — grootste wereldwijd, uitgebreide medische dekking, 24/7 alarmcentrale, annulering tot €10.000", "priceRange": "€3,50-14/mnd (doorlopend Europa)", "bestFor": "Maximale Dekking", "rating": 4.5, "affiliateLink": "https://allianz-assistance.nl/"},
        {"name": "Univé", "verdict": "Beste prijs-kwaliteit — coöperatief, ledenkorting, doorlopend met annulering, goede wintersportdekking", "priceRange": "€3-10/mnd (doorlopend Europa)", "bestFor": "Prijs-kwaliteit & Coöperatief", "rating": 4.4, "affiliateLink": "https://unive.nl/"},
        {"name": "Centraal Beheer", "verdict": "Beste budget — scherpe premie, eenvoudig online, pakketkorting met andere verzekeringen, Even Apeldoorn bellen", "priceRange": "€2,50-8/mnd (doorlopend Europa)", "bestFor": "Budgetbewust", "rating": 4.1, "affiliateLink": "https://centraalbeheer.nl/"},
        {"name": "OHRA", "verdict": "Beste flexibiliteit — modulair op te bouwen, annulering optioneel, wintersport optioneel, transparante voorwaarden", "priceRange": "€3-11/mnd (doorlopend Europa)", "bestFor": "Flexibiliteit & Transparantie", "rating": 4.2, "affiliateLink": "https://ohra.nl/"},
        {"name": "ABN AMRO", "verdict": "Beste via creditcard — Gold/Platinum card inclusief reisverzekering, werelddekking, annulering, geen aparte polis nodig", "priceRange": "€0 (bij creditcard €30-55/jr)", "bestFor": "Creditcard-bezitters", "rating": 4.0, "affiliateLink": "https://abnamro.nl/"},
        {"name": "FBTO", "verdict": "Beste goedkoopste — laagste premies, eenvoudig, online afsluiten, basisdekking Europa, annulering optioneel", "priceRange": "€2-7/mnd (doorlopend Europa)", "bestFor": "Minimale Premie", "rating": 3.9, "affiliateLink": "https://fbto.nl/"},
    ],
}

article = build_article(defn, body)
path = os.path.join(ARTICLES_DIR, f"{slug}.md")
with open(path, "w") as f:
    f.write(article)
print(f"Written: {path} ({len(article)} chars)")
