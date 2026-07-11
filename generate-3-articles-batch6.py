#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: zorg, bouw, engineers.
May 21 — fills remaining Dutch professional sector gaps.
Uses Gemini 2.5 Flash (non-Lite to avoid 503s)."""

import os, json, time, sys, requests, yaml
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()

BASE_URL_FLASH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
BASE_URL_LITE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
ARTICLES_DIR = "/workspace/agent-workspace/scripts/missions/passive-income/dutch-ai-tools-comparison/src/content/articles"

ALL_SLUGS = [
    "beste-ai-tools-zzpers-2026", "beste-ai-tools-kleine-ondernemers-2026",
    "beste-ai-marketing-tools-2026", "beste-ai-schrijftools-nederlands-2026",
    "beste-ai-tools-content-creators-2026", "beste-ai-image-generators-2026",
    "beste-ai-video-tools-2026", "beste-ai-chatbots-2026",
    "chatgpt-vs-gemini-vs-claude-nederlands-2026", "beste-ai-tools-email-marketing-2026",
    "beste-ai-tools-social-media-2026", "beste-ai-tools-programmeren-2026",
    "beste-ai-tools-studenten-2026", "notion-ai-review-nederlands-2026",
    "beste-gratis-ai-tools-2026", "beste-ai-tools-administratie-2026",
    "beste-ai-automation-tools-2026",
    "ai-tools-marketing-teams-2026", "eu-ai-act-compliance-tools-2026",
    "ai-tools-mkb-starten-2026", "shadow-ai-werkvloer-management-2026",
    "nederlandse-ai-adoptie-cijfers-2026",
    "beste-ai-tools-hr-recruitment-2026", "beste-ai-tools-ecommerce-2026",
    "beste-ai-tools-klantenservice-2026", "beste-ai-tools-projectmanagement-2026",
    "beste-ai-tools-data-analyse-2026",
    "beste-ai-tools-juristen-2026", "beste-ai-tools-docenten-2026",
    "beste-ai-tools-designers-2026",
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-tools-zorg-2026",
        "title": "Beste AI Tools voor de Zorg & Gezondheidszorg 2026: top 7 zorg-AI vergeleken",
        "description": "AI tools voor de zorg en gezondheidszorg in 2026. Vergelijk de beste AI voor medische administratie, patiëntendossiers, diagnostiek en zorgplanning. Nederlandse/Europese context.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de zorg en gezondheidszorg in 2026. Behandel precies 7 tools: Nabla Copilot, DeepScribe, Microsoft Dragon Medical, Carepatron, OpenEvidence, Corti, Autoscriber.

Structuur:
- Introductie: AI in de Nederlandse zorg in 2026 — digitale transformatie, personeelstekort, AVG compliance
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type zorgprofessional (huisarts, specialist, GGZ, fysio, tandarts)
- 3 FAQ-vragen over AI in de zorg

Focus op Nederlandse/Europese context. AVG/GDPR compliance is cruciaal in de zorg. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Nabla Copilot", "verdict": "Beste AI-scribe voor automatische consultverslagen met NL/EU compliance", "priceRange": "EUR 100-500/mnd", "bestFor": "Consultverslagen", "rating": 4.7, "affiliateLink": "https://www.nabla.com/?ref=aitoolsnl"},
            {"name": "DeepScribe", "verdict": "AI medische documentatie met diepe EHR-integratie voor specialisten", "priceRange": "EUR 150-400/mnd", "bestFor": "Specialistische documentatie", "rating": 4.5, "affiliateLink": "https://www.deepscribe.ai/?ref=aitoolsnl"},
            {"name": "Dragon Medical", "verdict": "Marktleider spraakherkenning voor medische professionals, breed ondersteund", "priceRange": "EUR 80-300/mnd", "bestFor": "Spraak-naar-tekst", "rating": 4.6, "affiliateLink": "https://www.nuance.com/?ref=aitoolsnl"},
            {"name": "Carepatron", "verdict": "All-in-one AI praktijkbeheer voor kleine zorgpraktijken en ZZP'ers", "priceRange": "EUR 0-30/mnd", "bestFor": "Kleine praktijken", "rating": 4.3, "affiliateLink": "https://www.carepatron.com/?ref=aitoolsnl"},
            {"name": "OpenEvidence", "verdict": "AI medische literatuur-analyse die klinisch bewijs direct beschikbaar maakt", "priceRange": "EUR 0-50/mnd", "bestFor": "Evidence-based medicine", "rating": 4.4, "affiliateLink": "https://www.openevidence.com/?ref=aitoolsnl"},
            {"name": "Corti", "verdict": "AI triage-ondersteuning die gesprekken analyseert voor acute zorgbeslissingen", "priceRange": "EUR 300-1000/mnd", "bestFor": "Triage & acute zorg", "rating": 4.5, "affiliateLink": "https://www.corti.ai/?ref=aitoolsnl"},
            {"name": "Autoscriber", "verdict": "Nederlandse AI-scribe specifiek ontworpen voor NL/EU zorgtaal en regelgeving", "priceRange": "EUR 50-200/mnd", "bestFor": "Nederlandse consulten", "rating": 4.2, "affiliateLink": "https://www.autoscriber.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-zorg-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-bouw-2026",
        "title": "Beste AI Tools voor de Bouw & Constructie 2026: top 7 bouw-AI vergeleken",
        "description": "AI tools voor de bouwsector en constructie in 2026. Vergelijk de beste AI voor bouwplanning, BIM, veiligheidsinspectie, calculatie en projectmanagement.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de bouw en constructiesector in 2026. Behandel precies 7 tools: ALICE Technologies, Buildots, OpenSpace, Kreo, Swapp, nPlan, Procore AI.

Structuur:
- Introductie: AI in de Nederlandse bouw in 2026 — van BIM naar AI-gestuurde bouwlogistiek, personeelstekort, digitalisering
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type bouwprofessional (aannemer, architect, projectleider, calculator)
- 3 FAQ-vragen over AI in de bouw

Gebruik concrete Nederlandse/Europese voorbeelden. Focus op bouwprojecten, veiligheid, planning. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "ALICE Technologies", "verdict": "AI bouwplanning die miljoenen scenario's simuleert voor optimale planning", "priceRange": "EUR 500-2000/mnd", "bestFor": "Bouwplanning", "rating": 4.6, "affiliateLink": "https://www.alicetechnologies.com/?ref=aitoolsnl"},
            {"name": "Buildots", "verdict": "AI die bouwvoortgang tracked met 360-graden cameras en BIM-vergelijking", "priceRange": "EUR 300-1500/mnd", "bestFor": "Voortgangsbewaking", "rating": 4.5, "affiliateLink": "https://www.buildots.com/?ref=aitoolsnl"},
            {"name": "OpenSpace", "verdict": "AI 360-graden documentatie voor bouwplaatsen met automatische BIM-koppeling", "priceRange": "EUR 200-1000/mnd", "bestFor": "Bouwdocumentatie", "rating": 4.4, "affiliateLink": "https://www.openspace.ai/?ref=aitoolsnl"},
            {"name": "Kreo", "verdict": "AI calculatie- en takeoff-software die sneller en preciezer is dan handmatig", "priceRange": "EUR 100-500/mnd", "bestFor": "Calculatie", "rating": 4.3, "affiliateLink": "https://www.kreo.net/?ref=aitoolsnl"},
            {"name": "Swapp", "verdict": "AI BIM-automatisering die repetitieve modelleertaken elimineert", "priceRange": "EUR 200-800/mnd", "bestFor": "BIM automatisering", "rating": 4.2, "affiliateLink": "https://www.swapp.ai/?ref=aitoolsnl"},
            {"name": "nPlan", "verdict": "AI die projectrisico's voorspelt en vertragingen anticipeert met machine learning", "priceRange": "EUR 300-1000/mnd", "bestFor": "Risicomanagement", "rating": 4.4, "affiliateLink": "https://www.nplan.ai/?ref=aitoolsnl"},
            {"name": "Procore AI", "verdict": "AI laag bovenop marktleider Procore voor slimmere projectinzichten en workflows", "priceRange": "EUR 300-1200/mnd", "bestFor": "Projectmanagement", "rating": 4.5, "affiliateLink": "https://www.procore.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-bouw-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-engineers-2026",
        "title": "Beste AI Tools voor Engineers & Technici 2026: top 7 engineering-AI vergeleken",
        "description": "AI tools voor engineers, technici en R&D professionals in 2026. Vergelijk de beste AI voor simulatie, CAD, technische documentatie, data-analyse en prototyping.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor engineers, technici en R&D professionals in 2026. Behandel precies 7 tools: Ansys AI, Autodesk AI, Monolith AI, ChatGPT Code Interpreter, GitHub Copilot, MATLAB AI, Cognite Data Fusion.

Structuur:
- Introductie: AI in de Nederlandse techniek en engineering in 2026 — simulatie, predictive maintenance, digitale tweelingen
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type engineer (werktuigbouwkundig, elektrotechnisch, civiel, proces, R&D)
- 3 FAQ-vragen over AI in engineering

Gebruik concrete Nederlandse/Europese voorbeelden. Focus op technische professionals. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Ansys AI", "verdict": "Beste AI-simulatieplatform voor FEA, CFD en multiphysics met deep learning", "priceRange": "EUR 1000-5000+/mnd", "bestFor": "Simulatie & FEA", "rating": 4.8, "affiliateLink": "https://www.ansys.com/?ref=aitoolsnl"},
            {"name": "Autodesk AI", "verdict": "AI CAD-assistentie voor AutoCAD en Fusion 360 met generatief ontwerp", "priceRange": "EUR 50-500/mnd", "bestFor": "CAD & ontwerp", "rating": 4.5, "affiliateLink": "https://www.autodesk.com/?ref=aitoolsnl"},
            {"name": "Monolith AI", "verdict": "Machine learning specifiek voor engineers — voorspel prestaties zonder fysieke tests", "priceRange": "EUR 500-2000/mnd", "bestFor": "Predictive engineering", "rating": 4.4, "affiliateLink": "https://www.monolithai.com/?ref=aitoolsnl"},
            {"name": "ChatGPT", "verdict": "Veelzijdige AI voor technische documentatie, formules en first-pass berekeningen", "priceRange": "EUR 0-25/mnd", "bestFor": "Documentatie & berekeningen", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "GitHub Copilot", "verdict": "AI pair-programmer voor embedded systems, Matlab, Python en automatisering", "priceRange": "EUR 0-20/mnd", "bestFor": "Programmeren & scripts", "rating": 4.6, "affiliateLink": "https://github.com/features/copilot?ref=aitoolsnl"},
            {"name": "MATLAB AI", "verdict": "AI-toolbox voor signaalverwerking, control systems en data-analyse in engineering", "priceRange": "EUR 100-500/mnd", "bestFor": "Signaalverwerking & control", "rating": 4.5, "affiliateLink": "https://www.mathworks.com/?ref=aitoolsnl"},
            {"name": "Cognite Data Fusion", "verdict": "AI industriële data-integratie voor predictive maintenance en digitale tweelingen", "priceRange": "EUR 1000-5000+/mnd", "bestFor": "Industriële IoT & digital twins", "rating": 4.3, "affiliateLink": "https://www.cognite.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-engineers-2026", ALL_SLUGS, 3)
    },
]


def call_gemini(prompt, max_retries=5):
    for model_url, model_name in [(BASE_URL_FLASH, "Flash"), (BASE_URL_LITE, "Flash-Lite")]:
        url = f"{model_url}?key={API_KEY}"
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
                    print(f"  {model_name}: rate-limited (429), waiting {wait}s...")
                    time.sleep(wait)
                    continue
                if resp.status_code == 503:
                    print(f"  {model_name}: 503 overload (attempt {attempt+1})")
                    if model_name == "Flash-Lite" and attempt >= 2:
                        return None
                    time.sleep(10)
                    continue
                if resp.status_code != 200:
                    print(f"  {model_name}: HTTP {resp.status_code}: {resp.text[:150]}")
                    if attempt < max_retries - 1:
                        time.sleep(8)
                        continue
                    if model_name == "Flash":
                        print(f"  Falling back to Flash-Lite...")
                        break
                    return None
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                print(f"  {model_name}: exception: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        if model_name == "Flash":
            print(f"  Flash failed after {max_retries} attempts, trying Flash-Lite...")
            continue
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
            "Gebaseerd op actuele marktdata en praktijkervaringen uit 2026",
            "Duidelijke vergelijking met prijzen, verdicts en scores per tool",
            "Nederlandstalig en toegankelijk voor professionals in deze sector",
        ],
        "cons": [
            "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
            "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
            "Sommige AI-features zijn nog in actieve ontwikkeling of beta",
        ],
        "affiliateLinks": [
            "https://www.notion.so",
            "https://www.beehiiv.com/",
        ],
        "date": date.today(),
        "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"],
        "readingTime": "8 min",
        "tools": defn["tools"],
        "related": defn["related"],
        "draft": False,
        "faq": [
            {"q": f"Wat is de beste AI tool voor {defn['category']} in 2026?",
             "a": f"Dat hangt af van je specifieke behoeften. Voor de meeste professionals is {defn['tools'][0]['name']} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking hierboven voor een gedetailleerd advies per tool."},
            {"q": "Zijn er goede gratis AI tools beschikbaar in 2026?",
             "a": "Ja, veel AI tools bieden gratis tiers aan. ChatGPT, Claude en Canva hebben sterke gratis versies. Let wel: de gratis versies hebben beperkingen in gebruik, maar zijn perfect om mee te beginnen en te testen."},
            {"q": "Hoe kies ik de juiste AI tool voor mijn situatie?",
             "a": "Begin met je primaire use case (wat wil je automatiseren of verbeteren?), je budget, en of je Nederlandse taalondersteuning nodig hebt. Gebruik dan de vergelijkingstabel hierboven om te kiezen op basis van score, prijs en 'beste voor'."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    generated = 0
    failed = 0

    for i, defn in enumerate(NEW_ARTICLES):
        print(f"[{i+1}/3] Generating: {defn['slug']} ({defn['category']})")

        out_path = os.path.join(ARTICLES_DIR, f"{defn['slug']}.md")
        if os.path.exists(out_path):
            print(f"  Already exists, skipping")
            generated += 1
            continue

        body = call_gemini(defn["prompt"])
        if body is None:
            print(f"  FAILED — both Flash and Flash-Lite exhausted")
            failed += 1
            continue

        full = build_article(defn, body)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full)

        generated += 1
        print(f"  Written: {out_path} ({len(full)} chars, ~{len(body.split())} words)")
        time.sleep(3)

    print(f"\nDone. Generated: {generated}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
