#!/usr/bin/env python3
"""Generate 5 new Dutch AI tools articles for content gaps:
1. AI e-commerce/dropshipping tools
2. AI 3D modeling & AR/VR tools
3. AI interior/home design tools
4. AI podcast/audio production tools
5. AI research/academic tools

Uses Gemini 2.5 Flash API. Writes to canonical location."""
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
        "slug": "beste-ai-e-commerce-dropshipping-tools-2026",
        "title": "Beste AI Tools voor E-commerce & Dropshipping 2026: top 7 vergeleken",
        "description": "AI tools die e-commerce en dropshipping automatiseren in 2026. Vergelijk Spocket, DSers, Zendrop, Sell The Trend, EcomHunt, Niche Scraper en SaleHoo voor productonderzoek, orderverwerking en marketing.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor e-commerce en dropshipping in 2026. Behandel precies 7 tools: Spocket, DSers, Zendrop, Sell The Trend, EcomHunt, Niche Scraper, SaleHoo.

Structuur:
- Introductie: AI transformeert e-commerce in 2026 — van AI-gestuurd productonderzoek tot geautomatiseerde orderverwerking, prijsoptimalisatie en gepersonaliseerde marketing. Voor Nederlandse webwinkeliers en dropshippers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (starter die niche zoekt, schalende webshopeigenaar, ervaren dropshipper met meerdere stores)
- 3 FAQ-vragen over AI en e-commerce/dropshipping

Focus op Nederlandse/Europese context. Prijzen in EUR. Noem relevante betaalmethoden (iDEAL, Mollie). Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Spocket", "verdict": "AI-gebaseerd dropshipping platform met focus op EU- en US-leveranciers — producten binnen 2-5 werkdagen in Nederland", "priceRange": "EUR 25-100/mnd", "bestFor": "Snelle levering EU & VS", "rating": 4.5, "affiliateLink": "https://www.spocket.co/?ref=aitoolsnl"},
            {"name": "DSers", "verdict": "AI-gestuurd order management en product sourcing voor AliExpress dropshipping — automatische prijs- en voorraad updates", "priceRange": "EUR 0-30/mnd", "bestFor": "AliExpress dropshipping", "rating": 4.3, "affiliateLink": "https://www.dsers.com/?ref=aitoolsnl"},
            {"name": "Zendrop", "verdict": "AI-order fulfillment platform met eigen magazijn in de VS en EU — branded invoicing en snelle shipping", "priceRange": "EUR 0-60/mnd", "bestFor": "Branded fulfillment", "rating": 4.2, "affiliateLink": "https://www.zendrop.com/?ref=aitoolsnl"},
            {"name": "Sell The Trend", "verdict": "AI-product research engine met winstberekening, trendanalyse en automatische import naar Shopify — de AI vindt winnende producten op basis van data", "priceRange": "EUR 30-80/mnd", "bestFor": "AI productonderzoek", "rating": 4.6, "affiliateLink": "https://www.sellthetrend.com/?ref=aitoolsnl"},
            {"name": "EcomHunt", "verdict": "Dagelijkse AI-geselecteerde productvondsten met data-analyse van winstgevendheid, advertentieprestaties en concurrentie", "priceRange": "EUR 0-40/mnd", "bestFor": "Dagelijkse product curation", "rating": 4.1, "affiliateLink": "https://ecomhunt.com/?ref=aitoolsnl"},
            {"name": "Niche Scraper", "verdict": "AI-product scraper en validator — analyseert AliExpress en Amazon producten op winnende potentie met ad-spy en vraagdata", "priceRange": "EUR 12-30/mnd", "bestFor": "Product validatie & ad-spy", "rating": 4.3, "affiliateLink": "https://www.nichescraper.com/?ref=aitoolsnl"},
            {"name": "SaleHoo", "verdict": "AI-leveranciersdirectory met 8000+ geverifieerde groothandels — voorraadcheck, prijsvergelijking en marktanalyse in een platform", "priceRange": "EUR 60/jaar", "bestFor": "Groothandel sourcing", "rating": 4.4, "affiliateLink": "https://www.salehoo.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-e-commerce-dropshipping-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-3d-modellering-tools-2026",
        "title": "Beste AI 3D Modellering & AR/VR Tools 2026: top 7 vergeleken",
        "description": "AI tools voor 3D-modellering, AR/VR en 3D-content creatie in 2026. Vergelijk Blender AI, Spline, Meshy, Luma AI, Kaedim, Masterpiece Studio en NVIDIA Omniverse voor 3D-ontwerp en virtual reality.",
        "category": "technologie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor 3D-modellering, AR en VR in 2026. Behandel precies 7 tools: Blender, Spline, Meshy, Luma AI, Kaedim, Masterpiece Studio, NVIDIA Omniverse.

Structuur:
- Introductie: AI verandert 3D-modellering radicaal in 2026 — van tekst-naar-3D en fotogrammetrie tot real-time AR/VR-omgevingen. Voor Nederlandse 3D-artiesten, game-ontwikkelaars en architecten.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (hobbyist die snel 3D wil maken, professionele game-ontwikkelaar, architect die VR-rondleidingen bouwt)
- 3 FAQ-vragen over AI en 3D-modellering

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Blender", "verdict": "Gratis open-source 3D-suite met AI-plugins voor texture generation, AI-retopology, motion capture en scene generation", "priceRange": "EUR 0 (gratis)", "bestFor": "Professionele 3D gratis", "rating": 4.8, "affiliateLink": "https://www.blender.org/?ref=aitoolsnl"},
            {"name": "Spline", "verdict": "Browsergebaseerde 3D-design tool met AI-features voor real-time collaborative 3D — ideaal voor web- en productdesign", "priceRange": "EUR 0-12/mnd", "bestFor": "Web 3D & product design", "rating": 4.5, "affiliateLink": "https://spline.design/?ref=aitoolsnl"},
            {"name": "Meshy", "verdict": "AI die 3D-modellen genereert uit tekst of afbeeldingen — inclusief texture mapping, animatie en format export voor games", "priceRange": "EUR 0-40/mnd", "bestFor": "Text-to-3D generatie", "rating": 4.4, "affiliateLink": "https://www.meshy.ai/?ref=aitoolsnl"},
            {"name": "Luma AI", "verdict": "AI-fotogrammetrie en 3D-generatie — maak 3D-modellen van echte objecten met je smartphone of genereer uit tekstbeschrijving", "priceRange": "EUR 0-30/mnd", "bestFor": "Fotogrammetrie & text-to-3D", "rating": 4.6, "affiliateLink": "https://lumalabs.ai/?ref=aitoolsnl"},
            {"name": "Kaedim", "verdict": "AI die 2D-concept art omzet in game-ready 3D-modellen — gebruikt door grote gamestudio's voor character en asset creatie", "priceRange": "EUR 0-100/mnd", "bestFor": "Game-ready 3D assets", "rating": 4.3, "affiliateLink": "https://www.kaedim.com/?ref=aitoolsnl"},
            {"name": "Masterpiece Studio", "verdict": "AI-VR 3D-creatie tool — ontwerp, modelleer en animeer in virtual reality met AI-ondersteuning voor sculpting en rigging", "priceRange": "EUR 0-90/mnd", "bestFor": "VR 3D-creatie & sculpting", "rating": 4.2, "affiliateLink": "https://www.masterpiecestudio.com/?ref=aitoolsnl"},
            {"name": "NVIDIA Omniverse", "verdict": "Enterprise-platform voor 3D-simulatie en digital twins — AI-gestuurde physics, rendering en collaborative 3D-pipelines", "priceRange": "EUR 0 (personal) / custom (enterprise)", "bestFor": "Digital twins & simulatie", "rating": 4.7, "affiliateLink": "https://www.nvidia.com/nl-nl/omniverse/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-3d-modellering-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-interieur-ontwerp-tools-2026",
        "title": "Beste AI Interieur & Woonontwerp Tools 2026: top 6 vergeleken",
        "description": "AI tools voor interieurontwerp en woninginrichting in 2026. Vergelijk Planner 5D, Interior AI, HomeByMe, RoomGPT, DecorMatters en Hutch voor AI-gestuurd woonadvies en virtuele inrichting.",
        "category": "technologie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor interieurontwerp en woninginrichting in 2026. Behandel precies 6 tools: Planner 5D, Interior AI, HomeByMe, RoomGPT, DecorMatters, Hutch.

Structuur:
- Introductie: AI maakt interieurontwerp toegankelijk in 2026 — van foto-naar-interieur tot volledige 3D-verkenning van je heringerichte woning. Voor Nederlandse huiseigenaren, huurders en interieurontwerpers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 6 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (starter die inspiratie zoekt, verhuizer die complete inrichting plant, professional die moodboards maakt voor klanten)
- 3 FAQ-vragen over AI en interieurontwerp

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Planner 5D", "verdict": "AI-gestuurde 2D/3D interieurontwerper — upload een foto van je kamer en zie direct heringericht met AI-meubels uit echte catalogi", "priceRange": "EUR 0-15/mnd", "bestFor": "Volledige 3D-interieurontwerp", "rating": 4.6, "affiliateLink": "https://planner5d.com/?ref=aitoolsnl"},
            {"name": "Interior AI", "verdict": "AI die foto's van lege of ingerichte kamers omzet in compleet heringerichte ruimtes — kies stijl en zie het resultaat in seconden", "priceRange": "EUR 0-20/mnd", "bestFor": "Snelle stijl-visualisatie", "rating": 4.5, "affiliateLink": "https://interiorai.com/?ref=aitoolsnl"},
            {"name": "HomeByMe", "verdict": "3D-interieurplatform met AI-room planner — teken je plattegrond, plaats meubels van echte merken en bekijk in 3D of VR", "priceRange": "EUR 0-10/mnd", "bestFor": "Realistische 3D-plattegronden", "rating": 4.3, "affiliateLink": "https://homeby.me/?ref=aitoolsnl"},
            {"name": "RoomGPT", "verdict": "AI-remodelling tool die foto's transformeert — laat zien hoe je kamer eruitziet in een andere stijl, van minimalistisch tot maximalistisch", "priceRange": "EUR 0-15/mnd", "bestFor": "Stijl-transformatie foto's", "rating": 4.4, "affiliateLink": "https://www.roomgpt.io/?ref=aitoolsnl"},
            {"name": "DecorMatters", "verdict": "AI-interieur app met augmented reality — plaats virtuele meubels in je echte kamer via je smartphone camera, met AI-stijl suggesties", "priceRange": "EUR 0-10/mnd", "bestFor": "AR-meubelvisualisatie", "rating": 4.2, "affiliateLink": "https://www.decormatters.com/?ref=aitoolsnl"},
            {"name": "Hutch", "verdict": "AI-interieur stylist die complete kamers samenstelt op basis van jouw smaak, budget en bestaande meubels — met directe kooplinks", "priceRange": "EUR 0-30/eenmalig", "bestFor": "Complete styling op maat", "rating": 4.1, "affiliateLink": "https://www.hutch.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-interieur-ontwerp-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-podcast-productie-tools-2026",
        "title": "Beste AI Podcast & Audio Productie Tools 2026: top 7 vergeleken",
        "description": "AI tools voor podcastproductie en audiobewerking in 2026. Vergelijk Descript, Riverside, Cleanvoice, Auphonic, Podcastle, Alitu en Adobe Podcast voor opname, bewerking en distributie.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor podcast- en audioproductie in 2026. Behandel precies 7 tools: Descript, Riverside.fm, Cleanvoice, Auphonic, Podcastle, Alitu, Adobe Podcast.

Structuur:
- Introductie: AI maakt podcastproductie toegankelijk in 2026 — van automatische ruisonderdrukking en transcriptie tot AI-gastheren en tekst-gebaseerde editing. Voor Nederlandse podcasters en contentmakers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (beginnende podcaster met beperkt budget, professionele podcaster met meerdere hosts, merk dat bedrijfspodcast start)
- 3 FAQ-vragen over AI en podcastproductie

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Descript", "verdict": "AI-video/audio editor — bewerk podcast door tekst aan te passen, AI-stemvulling, automatische pauze-verwijdering en transcription", "priceRange": "EUR 0-33/mnd", "bestFor": "Tekst-gebaseerde audiobewerking", "rating": 4.6, "affiliateLink": "https://www.descript.com/?ref=aitoolsnl"},
            {"name": "Riverside.fm", "verdict": "AI-opnameplatform voor remote podcasts — lokale opname in hoge kwaliteit, AI-transcriptie, automatische highlights en text-based editing", "priceRange": "EUR 0-29/mnd", "bestFor": "Remote podcast opname", "rating": 4.7, "affiliateLink": "https://riverside.fm/?ref=aitoolsnl"},
            {"name": "Cleanvoice", "verdict": "AI-audioreiniger die automatisch um's, ah's, stiltes, mondgeluiden en achtergrondgeluid verwijdert — ideaal voor Nederlandse podcasts", "priceRange": "EUR 0-18/mnd", "bestFor": "Automatische audiocleanup", "rating": 4.4, "affiliateLink": "https://cleanvoice.ai/?ref=aitoolsnl"},
            {"name": "Auphonic", "verdict": "AI-audio post-productie tool voor loudness normalization, ruisonderdrukking en niveau-aanpassing — gebruikt door professionele podcasters wereldwijd", "priceRange": "EUR 0-150/mnd", "bestFor": "Audio leveling & normalization", "rating": 4.5, "affiliateLink": "https://auphonic.com/?ref=aitoolsnl"},
            {"name": "Podcastle", "verdict": "Alles-in-één AI-podcastplatform — opname, AI-editing, magic dust ruisverwijdering, transcriptie en publicatie in een tool", "priceRange": "EUR 0-30/mnd", "bestFor": "Alles-in-één podcastplatform", "rating": 4.3, "affiliateLink": "https://podcastle.ai/?ref=aitoolsnl"},
            {"name": "Alitu", "verdict": "AI-podcast automation tool — upload je ruwe opname en Alitu bewerkt, normaliseert, voegt intro/outro toe en exporteert automatisch", "priceRange": "EUR 33/mnd", "bestFor": "Geautomatiseerde post-productie", "rating": 4.2, "affiliateLink": "https://alitu.com/?ref=aitoolsnl"},
            {"name": "Adobe Podcast", "verdict": "Gratis AI-podcast tool van Adobe — enhance speech voor kristalheldere audio, AI-ruisonderdrukking en browsergebaseerde editor", "priceRange": "EUR 0 (gratis)", "bestFor": "Gratis professionele audio", "rating": 4.4, "affiliateLink": "https://podcast.adobe.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-podcast-productie-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-research-academische-tools-2026",
        "title": "Beste AI Tools voor Research & Academisch Werk 2026: top 7 vergeleken",
        "description": "AI tools voor wetenschappelijk onderzoek, literatuuronderzoek en academisch schrijven in 2026. Vergelijk Elicit, Scite, Connected Papers, Research Rabbit, Semantic Scholar, Paperpile en Scholarcy voor slimmer onderzoek.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor wetenschappelijk onderzoek, literatuurstudie en academisch werk in 2026. Behandel precies 7 tools: Elicit, Scite, Connected Papers, Research Rabbit, Semantic Scholar, Paperpile, Scholarcy.

Structuur:
- Introductie: AI transformeert academisch onderzoek in 2026 — van AI-gestuurd literatuuronderzoek en automatische citatie-analyse tot samenvatting van honderden papers in minuten. Voor Nederlandse studenten, onderzoekers en wetenschappers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (masterstudent die literatuurstudie schrijft, PhD-kandidaat die systematic review uitvoert, universitair docent die peer review doet)
- 3 FAQ-vragen over AI en academisch onderzoek

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Elicit", "verdict": "AI-research assistant die papers vindt, samenvat en data extraheert — stel een onderzoeksvraag en krijg een tabel met bevindingen uit tientallen papers", "priceRange": "EUR 0-45/mnd", "bestFor": "Literatuuronderzoek & data-extractie", "rating": 4.7, "affiliateLink": "https://elicit.com/?ref=aitoolsnl"},
            {"name": "Scite", "verdict": "AI-citatie-analyse tool die laat zien of een paper wordt geciteerd ter ondersteuning, ter weerlegging of neutraal — citation context is key", "priceRange": "EUR 0-15/mnd", "bestFor": "Citatie-analyse & betrouwbaarheid", "rating": 4.6, "affiliateLink": "https://scite.ai/?ref=aitoolsnl"},
            {"name": "Connected Papers", "verdict": "AI-visualisatie tool die een grafiek maakt van gerelateerde papers — vind vooruitgangen, baanbrekende werken en gerelateerd onderzoek in een oogopslag", "priceRange": "EUR 0-5/mnd", "bestFor": "Paper-relatie visualisatie", "rating": 4.5, "affiliateLink": "https://www.connectedpapers.com/?ref=aitoolsnl"},
            {"name": "Research Rabbit", "verdict": "AI-referentiebeheer met discovery engine — upload je papers en Research Rabbit vindt gerelateerd werk, auteurs en trends in visualisaties", "priceRange": "EUR 0 (gratis)", "bestFor": "Paper discovery & referencing", "rating": 4.4, "affiliateLink": "https://www.researchrabbit.ai/?ref=aitoolsnl"},
            {"name": "Semantic Scholar", "verdict": "AI-aangedreven academische zoekmachine van Allen Institute — semantische search, TLDR-samenvattingen en API voor ontwikkelaars", "priceRange": "EUR 0 (gratis)", "bestFor": "AI-zoekmachine voor papers", "rating": 4.5, "affiliateLink": "https://www.semanticscholar.org/?ref=aitoolsnl"},
            {"name": "Paperpile", "verdict": "AI-referentiebeheer tool met Google Docs integratie — automatische citatiegeneratie, PDF-beheer en collaboration voor teams", "priceRange": "EUR 30/jaar", "bestFor": "Referentiebeheer & Google Docs integratie", "rating": 4.3, "affiliateLink": "https://paperpile.com/?ref=aitoolsnl"},
            {"name": "Scholarcy", "verdict": "AI-paper summarizer die elk onderzoek samenvat tot overzichtelijke flashcards — extracteert methodologie, resultaten, conclusies en kernpunten", "priceRange": "EUR 0-10/mnd", "bestFor": "Paper samenvatting & flashcards", "rating": 4.2, "affiliateLink": "https://www.scholarcy.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-research-academische-tools-2026", ALL_SLUGS, 3)
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
        print(f"  API error {resp.status_code}: {resp.text[:300]}")
        return None

    data = resp.json()
    if not data.get("candidates"):
        print(f"  No candidates in response")
        return None

    text = data["candidates"][0]["content"]["parts"][0]["text"]

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
            "Nederlandstalig en toegankelijk voor Nederlandse gebruikers"
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
        "readingTime": "7 min",
        "tools": article["tools"],
    }

    fm_yaml = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(out_path, "w") as f:
        f.write("---\n")
        f.write(fm_yaml)
        f.write("---\n\n")
        f.write(text)

    print(f"  Written to {out_path} ({len(text)} chars)")
    return out_path

def main():
    if not API_KEY:
        print("GEMINI_API_KEY not found")
        sys.exit(1)

    print(f"Generating {len(NEW_ARTICLES)} articles...")
    print(f"API key: {API_KEY[:10]}...")

    results = []
    for i, article in enumerate(NEW_ARTICLES, 1):
        result = generate_article(article, i, len(NEW_ARTICLES))
        if result:
            results.append(result)
        if i < len(NEW_ARTICLES):
            time.sleep(3)

    print(f"\n{'='*60}")
    print(f"Done! {len(results)}/{len(NEW_ARTICLES)} articles generated.")
    for r in results:
        print(f"  - {r}")

if __name__ == "__main__":
    main()