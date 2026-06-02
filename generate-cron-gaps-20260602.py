#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles for critical content gaps:
1. AI tools voor QA, testautomatisering & code review (development — 11 articles)
2. AI tools voor Google Ads, SEA & betaalde advertenties (marketing — 12 articles)
3. AI tools voor IoT, smarthome & domotica (technologie — 11 articles)

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
        "slug": "beste-ai-tools-qa-testen-code-review-2026",
        "title": "Beste AI Tools voor QA, Testautomatisering & Code Review 2026: top 7 vergeleken",
        "description": "AI tools voor QA-testing, testautomatisering en code review in 2026. Vergelijk Selenium AI, Playwright, Testim, Functionize, GitHub Copilot Code Review, Diffblue Cover en Applitools voor betere softwarekwaliteit.",
        "category": "development",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor QA, testautomatisering en code review in 2026. Behandel precies 7 tools: "
            "Selenium AI, Playwright, Testim, Functionize, GitHub Copilot Code Review, Diffblue Cover, Applitools.\\n\\n"
            "Structuur:\\n"
            "- Introductie: AI transformeert software testen en kwaliteitsborging in 2026 — van "
            "zelflerende testscripts tot AI-code review die bugs vindt voordat ze in productie komen. "
            "Voor Nederlandse developers, QA-engineers en DevOps-teams die sneller willen leveren met hogere kwaliteit.\\n"
            "- Per tool een ## kop met: beschrijving, prijsrange, beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\\n"
            "- Conclusie: welke tool voor welk team (startup, mkb, enterprise)\\n"
            "- 3 FAQ-vragen over AI en software testen\\n\\n"
            "Focus op praktische, Nederlandse context. Prijzen in EUR. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Selenium AI", "verdict": "AI-extensie op de klassieke Selenium-testautomatisering — zelfherstellende testscripts die zich aanpassen aan UI-wijzigingen zonder handmatig onderhoud", "priceRange": "EUR 0-150/mnd", "bestFor": "Enterprise testautomatisering", "rating": 4.3, "affiliateLink": "https://www.selenium.ai/?ref=aitoolsnl"},
            {"name": "Playwright", "verdict": "Microsofts AI-gedreven testframework met automatische locator-optimalisatie, visuele regression testing en cross-browser testautomatisering — razendsnel en betrouwbaar", "priceRange": "EUR 0 (open source)", "bestFor": "Cross-browser testing", "rating": 4.7, "affiliateLink": "https://playwright.dev/?ref=aitoolsnl"},
            {"name": "Testim", "verdict": "AI-gebaseerd testplatform dat leert van gebruikersgedrag en automatisch robuuste end-to-end tests genereert — vermindert testonderhoud met 70%", "priceRange": "EUR 50-500/mnd", "bestFor": "E2E testautomatisering", "rating": 4.4, "affiliateLink": "https://www.testim.io/?ref=aitoolsnl"},
            {"name": "Functionize", "verdict": "AI-testplatform met Natural Language Processing — schrijf tests in gewoon Engels en AI voert ze uit, met zelfherstellende testscripts bij UI-wijzigingen", "priceRange": "EUR 100-400/mnd", "bestFor": "No-code testautomatisering", "rating": 4.2, "affiliateLink": "https://www.functionize.com/?ref=aitoolsnl"},
            {"name": "GitHub Copilot Code Review", "verdict": "AI-code review assistant die pull requests analyseert op bugs, beveiligingslekken en codekwaliteit — direct geïntegreerd in GitHub-werkflow", "priceRange": "EUR 10-25/mnd", "bestFor": "Code review & PR-checking", "rating": 4.6, "affiliateLink": "https://github.com/features/copilot?ref=aitoolsnl"},
            {"name": "Diffblue Cover", "verdict": "AI die automatisch unit tests schrijft voor Java-code — genereert test coverage tot 90% zonder handmatig testscripts te schrijven", "priceRange": "EUR 20-200/mnd", "bestFor": "Automatische unit testgeneratie", "rating": 4.1, "affiliateLink": "https://www.diffblue.com/?ref=aitoolsnl"},
            {"name": "Applitools", "verdict": "AI-gestuurde visuele testing met Ultrafast Grid — detecteert pixel-perfecte visuele verschillen cross-browser, cross-device met AI-analyse", "priceRange": "EUR 30-300/mnd", "bestFor": "Visuele regression testing", "rating": 4.5, "affiliateLink": "https://applitools.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-qa-testen-code-review-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-google-ads-sea-advertenties-2026",
        "title": "Beste AI Tools voor Google Ads, SEA & Betaalde Advertenties 2026: top 7 vergeleken",
        "description": "AI tools voor Google Ads, SEA en online adverteren in 2026. Vergelijk Google Ads AI, Adzooma, Optmyzr, Pattern89, Albert.ai, WordStream en AdEspresso voor slimmere advertentiecampagnes.",
        "category": "marketing",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor Google Ads, SEA en betaalde advertenties in 2026. Behandel precies 7 tools: "
            "Google Ads AI (Performance Max), Adzooma, Optmyzr, Pattern89, Albert.ai, WordStream, AdEspresso.\\n\\n"
            "Structuur:\\n"
            "- Introductie: AI transformeert SEA en betaalde advertenties in 2026 — van automatische "
            "biedingsoptimalisatie tot AI-gegenereerde advertentieteksten, slimme doelgroepsegmentatie "
            "en voorspellende campagneanalyse. Voor Nederlandse marketeers en adverteerders.\\n"
            "- Per tool een ## kop met: beschrijving, prijsrange, beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\\n"
            "- Conclusie: welke tool voor welk campagnetype (branding, performance, lokale advertenties)\\n"
            "- 3 FAQ-vragen over AI en SEA\\n\\n"
            "Focus op Nederlandse context: marktplaats, Google Ads NL, Nederlandse biedstrategieën, "
            "BTW op advertentiekosten. Prijzen in EUR. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Google Ads AI (Performance Max)", "verdict": "Volautomatische AI-campagne van Google die biedingen, creatives, doelgroepen en kanalen optimaliseert — hoogste conversiepotentieel met minimale handmatige inzet", "priceRange": "EUR 0 (op advertentiebudget)", "bestFor": "Alles-in-één AI-adverteren", "rating": 4.6, "affiliateLink": "https://ads.google.com/?ref=aitoolsnl"},
            {"name": "Adzooma", "verdict": "AI-gedreven advertentieoptimalisatie tool die Google Ads, Facebook Ads en Microsoft Ads analyseert en automatisch optimalisaties voorstelt — met één klik doorvoeren", "priceRange": "EUR 0-100/mnd", "bestFor": "Multi-platform optimalisatie", "rating": 4.4, "affiliateLink": "https://www.adzooma.com/?ref=aitoolsnl"},
            {"name": "Optmyzr", "verdict": "AI-PPC management platform met geautomatiseerde regels, A/B-testen, budgetoptimalisatie en slimme bid management voor Google Ads en Microsoft Ads", "priceRange": "EUR 49-249/mnd", "bestFor": "PPC-specialisten & bureaus", "rating": 4.5, "affiliateLink": "https://www.optmyzr.com/?ref=aitoolsnl"},
            {"name": "Pattern89", "verdict": "AI-advertentievoorspeller die analyseert welke creative-elementen, targeting en timing de hoogste ROI geven — voorspelt campagneprestaties voordat je lanceert", "priceRange": "EUR 100-500/mnd", "bestFor": "Creative optimalisatie & voorspelling", "rating": 4.3, "affiliateLink": "https://pattern89.com/?ref=aitoolsnl"},
            {"name": "Albert.ai", "verdict": "Autonome AI-marketeer die volledige advertentiecampagnes beheert — van budgetverdeling tot creative optimalisatie — zonder menselijke tussenkomst", "priceRange": "EUR 500-5000/mnd", "bestFor": "Volledig autonome campagnes", "rating": 4.2, "affiliateLink": "https://albert.ai/?ref=aitoolsnl"},
            {"name": "WordStream Advisor", "verdict": "AI-gestuurd advertentieplatform met 20-punts optimalisatiechecklist, slimme biedingen en dashboards voor Google, Facebook en Instagram Ads", "priceRange": "EUR 50-200/mnd", "bestFor": "Kleine bedrijven & mkb", "rating": 4.3, "affiliateLink": "https://www.wordstream.com/?ref=aitoolsnl"},
            {"name": "AdEspresso", "verdict": "AI-A/B-test tool voor Facebook, Instagram en Google Ads — automatisch testen van creatives, targeting en copy met slimme statistische analyse", "priceRange": "EUR 40-200/mnd", "bestFor": "Social media A/B-testen", "rating": 4.1, "affiliateLink": "https://adespresso.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-google-ads-sea-advertenties-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-iot-smarthome-domotica-2026",
        "title": "Beste AI Tools voor IoT, Smart Home & Domotica 2026: top 7 vergeleken",
        "description": "AI tools voor IoT, smart home en domotica in 2026. Vergelijk Google Home, Apple HomeKit, Amazon Alexa, Home Assistant, Hubitat, Samsung SmartThings en IFTTT voor een slim en geautomatiseerd Nederlands huishouden.",
        "category": "technologie",
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools "
            "voor IoT, smart home en domotica in 2026. Behandel precies 7 tools: "
            "Google Home (Nest), Apple HomeKit, Amazon Alexa, Home Assistant, Hubitat, Samsung SmartThings, IFTTT.\\n\\n"
            "Structuur:\\n"
            "- Introductie: AI maakt het slimme huis in 2026 slimmer dan ooit — van stemassistenten "
            "die je gewoontes leren tot zelflerende thermostaten, beveiliging met gezichtsherkenning "
            "en geautomatiseerde energiebesparing. Voor Nederlanders die hun huis toekomstbestendig willen maken.\\n"
            "- Per tool een ## kop met: beschrijving, prijsrange, beste use case, "
            "plus- en minpunten, verdict (1-2 zinnen)\\n"
            "- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)\\n"
            "- Conclusie: welke tool voor welk type gebruiker (beginners, tech-liefhebbers, volledige automatisering)\\n"
            "- 3 FAQ-vragen over AI en slimme huizen\\n\\n"
            "Focus op Nederlandse context: ondersteuning voor Nederlandse spraak, energiebesparing "
            "in Nederlandse huizen, p1-meter integratie, compatibiliteit met Nederlandse apparatuur. "
            "Prijzen in EUR. Schrijf in vloeiend Nederlands."
        ),
        "tools": [
            {"name": "Google Home (Nest)", "verdict": "AI-ecosysteem van Google met Nederlands sprekende Google Assistant, zelflerende Nest Thermostat, slimme beveiligingscamera's met gezichtsherkenning — beste integratie met Google-diensten", "priceRange": "EUR 30-300 (apparaten)", "bestFor": "Google-gebruikers & beginners", "rating": 4.6, "affiliateLink": "https://store.google.com/nl/?ref=aitoolsnl"},
            {"name": "Apple HomeKit", "verdict": "Apple's slimme huisplatform met AI-automatiseringen, Siri-stemassistent en end-to-end encryptie — focus op privacy en naadloze Apple-integratie", "priceRange": "EUR 0 (gratis platform, eigen apparaten)", "bestFor": "Apple-gebruikers & privacybewusten", "rating": 4.5, "affiliateLink": "https://www.apple.com/home-app/?ref=aitoolsnl"},
            {"name": "Amazon Alexa", "verdict": "Amazon's AI-stemassistent met Nederlands begrip, duizenden Skills, slimme routines en ingebouwde beveiligingsfeatures — breedste apparaatcompatibiliteit", "priceRange": "EUR 25-150 (apparaten)", "bestFor": "Veelzijdige stemassistentie", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/alexa/?ref=aitoolsnl"},
            {"name": "Home Assistant", "verdict": "Open-source AI-huisautomatisering met lokale verwerking, ondersteuning voor 2000+ apparaten en geavanceerde automatiseringen — volledige controle en privacy", "priceRange": "EUR 0 (open source, eigen hardware)", "bestFor": "Tech-liefhebbers & maximale controle", "rating": 4.8, "affiliateLink": "https://www.home-assistant.io/?ref=aitoolsnl"},
            {"name": "Hubitat", "verdict": "Lokaal AI-domoticaplatform dat zonder cloud werkt — razendsnelle reactietijden, geavanceerde regels en breed apparaatbereik met ingebouwde beveiliging", "priceRange": "EUR 100-200 (hub)", "bestFor": "Lokale automatisering zonder cloud", "rating": 4.3, "affiliateLink": "https://hubitat.com/?ref=aitoolsnl"},
            {"name": "Samsung SmartThings", "verdict": "AI-slimme huisplatform van Samsung met gebruiksvriendelijke app, slimme routines en brede apparaatondersteuning — goed voor beginners en gevorderden", "priceRange": "EUR 0-80 (hub + apparaten)", "bestFor": "Beginners & Samsung-ecosysteem", "rating": 4.2, "affiliateLink": "https://www.smartthings.com/?ref=aitoolsnl"},
            {"name": "IFTTT", "verdict": "AI-automatiseringsplatform dat 800+ apps en apparaten verbindt met eenvoudige 'als dit, dan dat'-regels — perfect voor het koppelen van verschillende domoticasystemen", "priceRange": "EUR 0-5/mnd", "bestFor": "Cross-platform automatisering", "rating": 4.1, "affiliateLink": "https://ifttt.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-iot-smarthome-domotica-2026", ALL_SLUGS, 3)
    },
]

def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """Call Gemini API and return the generated text."""
    if not API_KEY:
        print("  FATAL: No API key found!")
        return None
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192,
        }
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=180)
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:300]}")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                return None
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
    return None

def build_frontmatter(article: dict, body: str) -> str:
    """Build YAML frontmatter with tools, related links, FAQ."""
    tools_yaml_lines = []
    for t in article["tools"]:
        tools_yaml_lines.append(
            f'  - name: {t["name"]}\n'
            f'    verdict: {t["verdict"]}\n'
            f'    priceRange: {t["priceRange"]}\n'
            f'    bestFor: {t["bestFor"]}\n'
            f'    rating: {t["rating"]}\n'
            f'    affiliateLink: {t["affiliateLink"]}'
        )
    tools_yaml = "\n".join(tools_yaml_lines)

    pros = [
        f'- {"AI-gedreven toolvergelijking met actuele data uit 2026"}',
        f'- {"Duidelijke prijsranges, verdict en score per tool in Nederlandstalige context"}',
        f'- {"Praktisch en eerlijk advies met FAQ voor Nederlandse gebruikers"}',
    ]
    cons = [
        f'- {"Prijzen en features kunnen wijzigen — check altijd de actuele aanbieder"}',
        f'- {"Niet elke tool is dagelijks getest met intensief Nederlands gebruik"}',
        f'- {"Sommige AI-features zijn nog in actieve ontwikkeling of beta"}',
    ]
    pros_yaml = "\n".join(pros)
    cons_yaml = "\n".join(cons)

    affiliate_links_yaml = "\n".join(
        f'  - {t["affiliateLink"]}' for t in article["tools"]
    )

    related_yaml = "\n".join(
        f"  - {slug}" for slug in article["related"]
    )

    today = date.today().isoformat()

    # Extract FAQ from generated body
    faq_items = _extract_faq(body) if body else []

    faq_yaml = ""
    if faq_items:
        faq_yaml = "\n".join(
            f'  - q: {item["q"]}\n    a: {item["a"]}'
            for item in faq_items
        )
    else:
        # Default FAQ if extraction fails
        faq_yaml = (
            '  - q: Wat is de beste AI tool voor dit onderwerp in 2026?\n'
            '    a: Dat hangt af van je specifieke behoeften en budget. Lees de volledige vergelijking hierboven voor een gedetailleerd advies per tool.\n'
            '  - q: Zijn er goede gratis AI tools beschikbaar in 2026?\n'
            '    a: Ja, veel tools bieden een gratis tier of proefperiode aan. Bekijk de prijzen en functies per tool in de vergelijkingstabel.\n'
            '  - q: Hoe kies ik de juiste AI tool voor mijn situatie?\n'
            '    a: Begin met het bepalen van je belangrijkste behoeften, budget en technische vereisten. Gebruik dan de vergelijkingstabel hierboven om je keuze te maken.'
        )

    fm = (
        f"---\n"
        f"title: \"{article['title']}\"\n"
        f"slug: {article['slug']}\n"
        f"description: {article['description']}\n"
        f"category: {article['category']}\n"
        f"rating: {sum(t['rating'] for t in article['tools']) / len(article['tools']):.1f}\n"
        f"priceRange: EUR 0-200/mnd\n"
        f"pros:\n{pros_yaml}\n"
        f"cons:\n{cons_yaml}\n"
        f"affiliateLinks:\n{affiliate_links_yaml}\n"
        f"related:\n{related_yaml}\n"
        f"date: '{today}'\n"
        f"modelYear: 2026\n"
        f"featuredTool: {article['tools'][0]['name']}\n"
        f"readingTime: 8 min\n"
        f"tools:\n{tools_yaml}\n"
        f"faq:\n{faq_yaml}\n"
        f"---\n\n"
    )
    return fm

def _extract_faq(body: str):
    """Extract FAQ from generated article body. Looks for FAQ section."""
    if not body:
        return []
    lines = body.split("\n")
    in_faq = False
    faq_items = []
    current_q = None
    current_a_parts = []

    for line in lines:
        stripped = line.strip()
        # Detect FAQ heading
        if stripped.lower().startswith("## faq") or stripped.lower().startswith("## veelgestelde"):
            in_faq = True
            continue
        if not in_faq:
            continue
        # Detect start of next section
        if stripped.startswith("## ") and "faq" not in stripped.lower() and "vraag" not in stripped.lower():
            break
        # Extract numbered questions
        q_match = re.match(r'^\d+\.\s*\*\*(.*?)\*\*\s*$', stripped) or re.match(r'^\d+\.\s*(.*?)\s*$', stripped)
        if q_match and current_q is None:
            current_q = q_match.group(1).strip().strip('?') + '?'
            current_a_parts = []
            continue
        elif q_match and current_q:
            # Save previous
            if current_q and current_a_parts:
                faq_items.append({"q": current_q[:120], "a": " ".join(current_a_parts)[:300]})
            current_q = q_match.group(1).strip().strip('?') + '?'
            current_a_parts = []
            continue
        if current_q and stripped and not stripped.startswith("##"):
            current_a_parts.append(stripped)

    # Save last
    if current_q and current_a_parts:
        faq_items.append({"q": current_q[:120], "a": " ".join(current_a_parts)[:300]})

    return faq_items[:3]

import re

def main():
    if not API_KEY:
        print("FATAL: No Gemini API key found. Set GEMINI_API_KEY in environment or ~/.hermes/.env")
        sys.exit(1)

    print(f"API Key starts with: {API_KEY[:10]}...")
    print(f"ARTICLES_DIR exists: {os.path.isdir(ARTICLES_DIR)}")
    print(f"Total existing articles: {len(ALL_SLUGS)}")
    print()

    for article in NEW_ARTICLES:
        slug = article["slug"]
        dest = os.path.join(ARTICLES_DIR, f"{slug}.md")

        if os.path.exists(dest):
            print(f"⏭️  SKIP: {slug} already exists")
            continue

        print(f"📝 Generating: {article['title']}")
        print(f"    Slug: {slug}")
        print(f"    Category: {article['category']}")
        print(f"    Tools: {', '.join(t['name'] for t in article['tools'])}")

        # Call Gemini
        body = call_gemini(article["prompt"])
        if not body:
            print(f"    ❌ FAILED: No response from Gemini")
            continue

        # Remove markdown code fences if present
        body = re.sub(r'^```.*?\n', '', body, count=1)
        body = re.sub(r'\n```\s*$', '', body, count=1)

        # Build frontmatter + body
        fm = build_frontmatter(article, body)
        full_content = fm + body

        with open(dest, "w") as f:
            f.write(full_content)

        print(f"    ✅ Written: {len(body)} chars")
        print(f"    📁 {dest}")
        print()
        time.sleep(2)  # Rate limit buffer

    print("✅ Done generating articles")

if __name__ == "__main__":
    main()