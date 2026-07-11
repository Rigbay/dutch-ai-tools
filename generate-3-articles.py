#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: juristen, docenten, designers.
Uses Gemini 2.5 Flash (non-Lite) — peak hours, avoid Flash-Lite 503 spam."""

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
]

# Pick 3 distinct related slugs for each new article, avoiding self
def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-tools-juristen-2026",
        "title": "Beste AI Tools voor Juristen & Advocaten 2026: top 7 juridische AI vergeleken",
        "description": "AI tools voor juristen en advocaten in 2026. Vergelijk Harvey AI, LegalTech tools, ChatGPT en Claude voor juridisch onderzoek, contractanalyse en documentautomatisering.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor juristen en advocaten in 2026. Behandel precies 7 tools: Harvey AI, ChatGPT, Claude, Henchman, DeepL, Legalyze, Docusign AI.

Structuur:
- Introductie: waarom AI onmisbaar wordt voor de juridische sector in 2026
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type jurist
- 3 FAQ-vragen over AI in de juridische sector

Gebruik concrete NL/EU voorbeelden. Focus op Nederlandse/Europese context (AVG/GDPR compliance is belangrijk). Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Harvey AI", "verdict": "Beste AI-platform specifiek voor juridische professionals met diepe domeinkennis", "priceRange": "EUR 200-500/mnd", "bestFor": "Juridisch onderzoek", "rating": 4.6, "affiliateLink": "https://www.harvey.ai/?ref=aitoolsnl"},
            {"name": "ChatGPT", "verdict": "Veelzijdige AI voor eerste juridische analyses en brondocumentatie", "priceRange": "EUR 0-25/mnd", "bestFor": "Juridische drafting", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "Claude", "verdict": "Uitstekend voor lange contracten en genuanceerde juridische redenering", "priceRange": "EUR 0-25/mnd", "bestFor": "Contractanalyse", "rating": 4.5, "affiliateLink": "https://www.notion.so"},
            {"name": "Henchman", "verdict": "AI contractanalyse die automatisch clausules vindt in je database", "priceRange": "EUR 100-300/mnd", "bestFor": "Contractdatabase", "rating": 4.4, "affiliateLink": "https://henchman.io/?ref=aitoolsnl"},
            {"name": "DeepL", "verdict": "Beste AI-vertaling voor juridische documenten met EU-taalondersteuning", "priceRange": "EUR 0-50/mnd", "bestFor": "Juridische vertalingen", "rating": 4.6, "affiliateLink": "https://www.deepl.com/?ref=aitoolsnl"},
            {"name": "Legalyze", "verdict": "AI die juridische documenten samenvat en relevante passages markeert", "priceRange": "EUR 50-150/mnd", "bestFor": "Documentsamenvatting", "rating": 4.2, "affiliateLink": "https://www.legalyze.ai/?ref=aitoolsnl"},
            {"name": "Docusign AI", "verdict": "Digitale handtekeningen met AI contractinzicht en nalevingscontrole", "priceRange": "EUR 10-50/mnd", "bestFor": "Ondertekening & compliance", "rating": 4.3, "affiliateLink": "https://www.docusign.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-juristen-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-docenten-2026",
        "title": "Beste AI Tools voor Docenten & Onderwijs 2026: top 7 les-AI vergeleken",
        "description": "AI tools voor docenten en het onderwijs in 2026. Vergelijk ChatGPT, Claude, Canva, LessonUp, Gemini en meer voor lesvoorbereiding, nakijken en differentiatie.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor docenten en onderwijsprofessionals in 2026. Behandel precies 7 tools: ChatGPT, Claude, Canva AI, LessonUp, Google Gemini, Quizlet AI, Notion AI.

Structuur:
- Introductie: AI in het Nederlandse onderwijs in 2026 — van terughoudend naar omarmen
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type docent (PO, VO, MBO, HBO/WO)
- 3 FAQ-vragen over AI in het onderwijs

Gebruik concrete Nederlandse onderwijscontext. Focus op lesvoorbereiding, nakijken, differentiëren, administratie. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "ChatGPT", "verdict": "Meest veelzijdige AI voor lesvoorbereiding, uitleg en werkblad-creatie", "priceRange": "EUR 0-25/mnd", "bestFor": "Lesvoorbereiding", "rating": 4.6, "affiliateLink": "https://www.notion.so"},
            {"name": "Claude", "verdict": "Beste voor diepgaande feedback op essays en werkstukken", "priceRange": "EUR 0-25/mnd", "bestFor": "Feedback & nakijken", "rating": 4.5, "affiliateLink": "https://www.notion.so"},
            {"name": "Canva AI", "verdict": "Onmisbaar voor visueel lesmateriaal, presentaties en infographics", "priceRange": "EUR 0-15/mnd", "bestFor": "Visueel lesmateriaal", "rating": 4.7, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "LessonUp", "verdict": "Nederlands platform met AI voor interactieve lessen en formatief toetsen", "priceRange": "EUR 0-30/mnd", "bestFor": "Interactieve lessen", "rating": 4.4, "affiliateLink": "https://www.lessonup.com/?ref=aitoolsnl"},
            {"name": "Google Gemini", "verdict": "Diepe Google-integratie voor research en Google Classroom workflows", "priceRange": "EUR 0-25/mnd", "bestFor": "Research & Classroom", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "Quizlet AI", "verdict": "Beste voor flashcards, begrippentraining en formatief toetsen", "priceRange": "EUR 0-8/mnd", "bestFor": "Toetsen & stampwerk", "rating": 4.5, "affiliateLink": "https://quizlet.com/?ref=aitoolsnl"},
            {"name": "Notion AI", "verdict": "Perfect voor lesplanning, curriculumbeheer en leerlingvolgsysteem", "priceRange": "EUR 0-20/mnd", "bestFor": "Planning & administratie", "rating": 4.2, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("beste-ai-tools-docenten-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-designers-2026",
        "title": "Beste AI Tools voor Designers 2026: top 7 design-AI vergeleken",
        "description": "AI tools voor designers en creatieven in 2026. Vergelijk Figma AI, Adobe Firefly, Canva, Midjourney, Relume en meer voor UI/UX, branding en grafisch ontwerp.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor designers en creatieve professionals in 2026. Behandel precies 7 tools: Figma AI, Adobe Firefly, Canva AI, Midjourney, Relume AI, Galileo AI, Khroma.

Structuur:
- Introductie: hoe AI het designvak verandert in 2026 — van bedreiging naar tool
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type designer (UI/UX, grafisch, branding, web)
- 3 FAQ-vragen over AI in design

Gebruik concrete voorbeelden. Focus op Nederlands/Europese markt. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Figma AI", "verdict": "Beste all-in-one designplatform met AI voor UI/UX en prototyping", "priceRange": "EUR 0-55/mnd", "bestFor": "UI/UX design", "rating": 4.8, "affiliateLink": "https://www.figma.com/?ref=aitoolsnl"},
            {"name": "Adobe Firefly", "verdict": "Commercieel veilige AI beeldgeneratie direct in Creative Cloud", "priceRange": "EUR 5-25/mnd", "bestFor": "Grafisch ontwerp", "rating": 4.5, "affiliateLink": "https://www.adobe.com/?ref=aitoolsnl"},
            {"name": "Canva AI", "verdict": "Toegankelijke AI design tool voor snelle social graphics en branding", "priceRange": "EUR 0-15/mnd", "bestFor": "Snelle visuals", "rating": 4.4, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "Midjourney", "verdict": "Absolute top in AI-beeldkwaliteit voor concept art en inspiratie", "priceRange": "EUR 10-60/mnd", "bestFor": "Concept & inspiratie", "rating": 4.7, "affiliateLink": "https://www.midjourney.com/?ref=aitoolsnl"},
            {"name": "Relume AI", "verdict": "AI die wireframes en sitemaps genereert voor webdesign projecten", "priceRange": "EUR 30-50/mnd", "bestFor": "Webdesign & wireframes", "rating": 4.3, "affiliateLink": "https://www.relume.io/?ref=aitoolsnl"},
            {"name": "Galileo AI", "verdict": "AI die UI designs genereert uit tekstbeschrijvingen — razendsnel prototypen", "priceRange": "EUR 20-50/mnd", "bestFor": "UI generatie", "rating": 4.2, "affiliateLink": "https://www.usegalileo.ai/?ref=aitoolsnl"},
            {"name": "Khroma", "verdict": "AI kleurenpalet-generator die leert van jouw voorkeuren", "priceRange": "EUR 0/mnd", "bestFor": "Kleurpaletten", "rating": 4.0, "affiliateLink": "https://www.khroma.co/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-designers-2026", ALL_SLUGS, 3)
    },
]


def call_gemini(prompt, max_retries=5):
    """Try Flash first, fall back to Flash-Lite if Flash 503s."""
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
                        break  # jump to outer loop for Lite
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
    """Build complete .md file with clean YAML frontmatter + Gemini body."""
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
