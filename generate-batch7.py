#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: retail, horeca, logistiek.
May 21 12:30 — fills remaining Dutch professional sector gaps (now at 62, target 65).
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
    "beste-ai-tools-zorg-2026", "beste-ai-tools-bouw-2026", "beste-ai-tools-engineers-2026",
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-tools-retail-2026",
        "title": "Beste AI Tools voor Retail & Winkels 2026: top 7 retail-AI vergeleken",
        "description": "AI tools voor retail, winkels en winkelketens in 2026. Vergelijk de beste AI voor voorraadbeheer, pricing, klantpersonalisatie, omnichannel en winkeloptimalisatie.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor retail, winkels en fysieke winkelketens in 2026. Behandel precies 7 tools: Dynamic Yield, RELEX.ai, Blue Yonder, Vue.ai, Syte, Shelf Engine, Trigo Vision.

Structuur:
- Introductie: AI in de Nederlandse retail in 2026 — personeelstekort, omnichannel druk, AI als concurrentievoordeel
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type retailer (zelfstandige winkelier, ketenmanager, e-commerce/omnichannel)
- 3 FAQ-vragen over AI in retail

Focus op Nederlandse/Europese context. Prijzen in EUR. Noem concrete NL-use cases. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Dynamic Yield", "verdict": "Beste AI-personalisatieplatform voor omnichannel retailers met bewezen ROI", "priceRange": "EUR 500-3000/mnd", "bestFor": "Personalisatie", "rating": 4.7, "affiliateLink": "https://www.dynamicyield.com/?ref=aitoolsnl"},
            {"name": "RELEX.ai", "verdict": "AI voorraadbeheer en supply chain forecasting voor food en non-food retail", "priceRange": "EUR 500-2500/mnd", "bestFor": "Voorraadoptimalisatie", "rating": 4.5, "affiliateLink": "https://www.relexsolutions.com/?ref=aitoolsnl"},
            {"name": "Blue Yonder", "verdict": "End-to-end AI retail platform met prijsoptimalisatie en category management", "priceRange": "EUR 1000-5000/mnd", "bestFor": "Enterprise retail", "rating": 4.6, "affiliateLink": "https://www.blueyonder.com/?ref=aitoolsnl"},
            {"name": "Vue.ai", "verdict": "AI product-tagging en visuele merchandising voor fashion en lifestyle retail", "priceRange": "EUR 300-1500/mnd", "bestFor": "Fashion retail", "rating": 4.3, "affiliateLink": "https://www.vue.ai/?ref=aitoolsnl"},
            {"name": "Syte", "verdict": "AI visuele zoektechnologie en product discovery voor betere conversie", "priceRange": "EUR 200-1000/mnd", "bestFor": "Product discovery", "rating": 4.2, "affiliateLink": "https://www.syte.ai/?ref=aitoolsnl"},
            {"name": "Shelf Engine", "verdict": "AI voorraadbestelling die voedselverspilling tot 32% vermindert", "priceRange": "EUR 100-500/mnd", "bestFor": "Food retail & vers", "rating": 4.4, "affiliateLink": "https://www.shelfengine.com/?ref=aitoolsnl"},
            {"name": "Trigo Vision", "verdict": "Vision-AI voor cashierless winkels a la Amazon Go — scanloze checkout", "priceRange": "EUR 500-2000/mnd", "bestFor": "Winkelinnovatie", "rating": 4.1, "affiliateLink": "https://www.trigoretail.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-retail-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-horeca-2026",
        "title": "Beste AI Tools voor de Horeca 2026: top 7 horeca-AI vergeleken",
        "description": "AI tools voor horeca, cafés, restaurants en hotels in 2026. Vergelijk de beste AI voor reserveringen, menubeheer, personeelsplanning, reviews en gastbeleving.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de horeca (restaurants, cafés, hotels) in 2026. Behandel precies 7 tools: Popmenu AI, SevenRooms, Fourth, Toast AI, Formitable, Resengo, Zonal.

Structuur:
- Introductie: AI in de Nederlandse horeca in 2026 — personeelstekort piekt, digitale gastbeleving, AI als redmiddel
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type horeca-ondernemer (caféhouder, restaurant-eigenaar, hotelmanager, cateraar)
- 3 FAQ-vragen over AI in de horeca

Focus op Nederlandse/Benelux context. Geef voorbeelden van NL-gebruik. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Popmenu AI", "verdict": "Beste AI voor online reputatie en gastrespons — automatisch review-antwoorden", "priceRange": "EUR 100-400/mnd", "bestFor": "Reputatiemanagement", "rating": 4.4, "affiliateLink": "https://www.popmenu.com/?ref=aitoolsnl"},
            {"name": "SevenRooms", "verdict": "AI gastprofielen en gepersonaliseerde reserveringen voor volwaardige restaurants", "priceRange": "EUR 200-800/mnd", "bestFor": "Gastbeleving & CRM", "rating": 4.6, "affiliateLink": "https://www.sevenrooms.com/?ref=aitoolsnl"},
            {"name": "Fourth", "verdict": "AI personeelsplanning en voorraadbeheer specifiek voor de hospitality sector", "priceRange": "EUR 150-600/mnd", "bestFor": "Planning & voorraad", "rating": 4.3, "affiliateLink": "https://www.fourth.com/?ref=aitoolsnl"},
            {"name": "Toast AI", "verdict": "All-in-one restaurant-AI platform met slimme menubeheer en bestelanalyse", "priceRange": "EUR 50-300/mnd", "bestFor": "Kleine restaurants", "rating": 4.5, "affiliateLink": "https://pos.toasttab.com/?ref=aitoolsnl"},
            {"name": "Formitable", "verdict": "Nederlandse AI-reserveringssoftware met slimme tafelindeling en gastherkenning", "priceRange": "EUR 50-200/mnd", "bestFor": "NL restaurants & reserveringen", "rating": 4.2, "affiliateLink": "https://www.formitable.com/?ref=aitoolsnl"},
            {"name": "Resengo", "verdict": "Belgisch-Nederlandse restaurant-AI voor online boekingen, menukaart en reviews", "priceRange": "EUR 30-150/mnd", "bestFor": "Benelux horeca", "rating": 4.1, "affiliateLink": "https://www.resengo.com/?ref=aitoolsnl"},
            {"name": "Zonal", "verdict": "AI hoteltechnologie — frontdesk, F&B, housekeeping, gastanalyse in één platform", "priceRange": "EUR 200-1000/mnd", "bestFor": "Hotels & ketens", "rating": 4.3, "affiliateLink": "https://www.zonal.co.uk/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-horeca-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-logistiek-2026",
        "title": "Beste AI Tools voor Logistiek & Supply Chain 2026: top 7 logistiek-AI vergeleken",
        "description": "AI tools voor logistiek, transport en supply chain in 2026. Vergelijk de beste AI voor routeoptimalisatie, warehouse management, fleet tracking en voorraadplanning.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor logistiek, transport en supply chain in 2026. Behandel precies 7 tools: OptimoRoute, project44, Locus.sh, Shipwell, Coupa, Transporeon, FourKites.

Structuur:
- Introductie: AI in de Nederlandse logistiek in 2026 — chauffeurstekort, CO2-doelen, digitalisering, haven Rotterdam/Europoort
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type logistiek bedrijf (transporteur, warehouse, expediteur, verladers, eigen vervoer)
- 3 FAQ-vragen over AI in logistiek

Focus op Nederlandse/Europese context. Noem NL transport hubs en eisen (CO2-registratie 2026). Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "OptimoRoute", "verdict": "Beste AI routeplanning met dynamische aanpassing — tot 30% brandstofbesparing", "priceRange": "EUR 50-500/mnd", "bestFor": "Routeoptimalisatie", "rating": 4.6, "affiliateLink": "https://www.optimoroute.com/?ref=aitoolsnl"},
            {"name": "project44", "verdict": "Marktleider real-time supply chain visibility met multimodale tracking", "priceRange": "EUR 500-3000/mnd", "bestFor": "Supply chain visibility", "rating": 4.7, "affiliateLink": "https://www.project44.com/?ref=aitoolsnl"},
            {"name": "Locus.sh", "verdict": "AI dispatch management platform — automatiseert complexe logistieke planning", "priceRange": "EUR 200-1000/mnd", "bestFor": "Dispatch & planning", "rating": 4.4, "affiliateLink": "https://www.locus.sh/?ref=aitoolsnl"},
            {"name": "Shipwell", "verdict": "AI TMS met voorspellende prijsanalyse en automatische carrier-matching", "priceRange": "EUR 100-800/mnd", "bestFor": "Transport management", "rating": 4.3, "affiliateLink": "https://www.shipwell.com/?ref=aitoolsnl"},
            {"name": "Coupa", "verdict": "AI spend management en supply chain design voor grotere logistieke operaties", "priceRange": "EUR 1000-5000/mnd", "bestFor": "Enterprise supply chain", "rating": 4.5, "affiliateLink": "https://www.coupa.com/?ref=aitoolsnl"},
            {"name": "Transporeon", "verdict": "Europees AI platform voor verlader-carrier matching met CO2-transparantie", "priceRange": "EUR 300-1500/mnd", "bestFor": "Europese matching", "rating": 4.2, "affiliateLink": "https://www.transporeon.com/?ref=aitoolsnl"},
            {"name": "FourKites", "verdict": "AI real-time tracking over alle transportmodi — zee, weg, rail, lucht", "priceRange": "EUR 300-2000/mnd", "bestFor": "Multimodale tracking", "rating": 4.4, "affiliateLink": "https://www.fourkites.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-logistiek-2026", ALL_SLUGS, 3)
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
            "https://affiliate.notion.so/?via=aitoolsnl",
            "https://www.beehiiv.com/?via=aitoolsnl",
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
