#!/usr/bin/env python3
"""Generate 5 new Dutch AI comparison articles: DeepL vs Google Translate, Otter vs Fireflies,
Gamma vs Beautiful AI, Descript vs Podcastle, SurferSEO vs Clearscope.
Batch 11 — May 26 2026. Uses Gemini 2.5 Flash, proper yaml.dump frontmatter."""
import os, time, sys, yaml
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

BASE_URL_FLASH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = Path("/tmp/dutch-ai-tools/src/content/articles")

ALL_SLUGS = sorted(f.stem for f in ARTICLES_DIR.glob("*.md"))

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

def generate_one(prompt, attempt=1):
    url = BASE_URL_FLASH
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    resp = requests.post(f"{url}?key={API_KEY}", headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    if resp.status_code == 503 and attempt <= 2:
        print(f"  503, retry {attempt+1}...")
        time.sleep(3)
        return generate_one(prompt, attempt + 1)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return text, len(text.split())

ARTICLES = [
    {
        "slug": "deepL-vs-google-translate-vs-chatgpt-2026",
        "title": "DeepL vs Google Translate vs ChatGPT Vertalingen 2026: Welke AI Vertaaltool is de Beste?",
        "description": "DeepL, Google Translate of ChatGPT voor vertalingen in 2026? Vergelijk nauwkeurigheid, talen, prijs en privacy in deze uitgebreide vergelijking voor Nederlands.",
        "category": "tools",
        "rating": 4.6,
        "priceRange": "EUR 0-50/mnd",
        "pros": ["Eerlijke vergelijking van de 3 grootste AI-vertaaltools", "NL-specifieke tests (DeepL scoort hoog op Nederlands)", "Praktische use cases per type gebruiker"],
        "cons": ["Prijzen kunnen wijzigen", "Nauwkeurigheid varieert per taalcombinatie", "Niet elke tool ondersteunt alle formaten"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-26",
        "modelYear": 2026,
        "featuredTool": "DeepL",
        "readingTime": "9 min",
        "tools": [
            {"name": "DeepL", "verdict": "Beste AI-vertaaltool voor Nederlands en Europese talen", "priceRange": "EUR 0-25/mnd", "bestFor": "Professionele vertalingen", "rating": 4.7, "affiliateLink": "https://www.notion.so"},
            {"name": "Google Translate", "verdict": "Meeste talen (133+) en beste integratie met Google-ecosysteem", "priceRange": "EUR 0 (gratis)", "bestFor": "Snelle vertalingen", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "ChatGPT", "verdict": "Meest flexibel — vertaalt met context, stijl en nuance, maar minder consistent", "priceRange": "EUR 0-25/mnd", "bestFor": "Creatieve & contextrijke teksten", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("deepL-vs-google-translate-vs-chatgpt-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke AI-vertaaltool is het beste voor Nederlands?",
             "a": "DeepL scoort consistent het hoogst voor Nederlands-Engels en Nederlands-Duits. Voor minder gangbare talen is Google Translate sterker. ChatGPT blinkt uit in contextgevoelige vertalingen zoals marketingteksten."},
            {"q": "Is DeepL gratis genoeg voor professioneel gebruik?",
             "a": "De gratis versie van DeepL is geschikt voor kleine vertalingen (max 1500 tekens). Voor professioneel gebruik is DeepL Pro (EUR 8,99-24,99/mnd) aanbevolen vanwege onbeperkt vertalen, glossary-features en betere privacy."},
            {"q": "Hoe zit het met privacy bij AI-vertaaltools?",
             "a": "DeepL Pro biedt GDPR/AVG-compliance met servers in de EU. Google Translate en ChatGPT verwerken data deels op Amerikaanse servers. Voor gevoelige bedrijfsdocumenten is DeepL de veiligste keuze."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over DeepL vs Google Translate vs ChatGPT voor vertalingen in 2026.

Structuur:
- Introductie: AI-vertalen is in 2026 enorm verbeterd. DeepL, Google Translate en ChatGPT concurreren om de beste vertaalkwaliteit. Welke past bij jou?
- Hoofdsectie per tool (## koppen): DeepL, Google Translate, ChatGPT. Inclusief: hoe het werkt, prijs (EUR), beste voor, plus/minpunten, verdict.
- Uitgebreide functievergelijkingstabel (markdown): tool, talen, gratis-limiet, prijs (EUR/mnd), beste voor NL, integraties, offline?, score
- Conclusie: welke tool voor welke gebruiker (vertaalbureau, marketeer, student, developer die API wil, casual gebruiker)
- Sluit af met FAQ-sectie (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de Nederlandse/Europese context. DeepL is Duits, dus EU-dataverwerking. Prijzen in EUR. Schrijf in vloeiend, nuchter Nederlands.""",
    },
    {
        "slug": "otter-ai-vs-fireflies-vs-fathom-2026",
        "title": "Otter.ai vs Fireflies.ai vs Fathom 2026: Beste AI Meeting Notulist Vergeleken",
        "description": "Vergelijk Otter.ai, Fireflies.ai en Fathom — de top 3 AI meeting assistants van 2026. Automatische notulen, transcripties en actiepunten voor Zoom, Teams en Google Meet.",
        "category": "tools",
        "rating": 4.5,
        "priceRange": "EUR 0-30/mnd",
        "pros": ["Eerlijke vergelijking van de 3 populairste AI-notulisten", "Praktisch: per platform, teamgrootte en budget", "NL-context met GDPR-overwegingen"],
        "cons": ["Prijzen en features kunnen snel veranderen", "Niet elke tool ondersteunt Nederlands even goed", "Gratis versies hebben serieuze beperkingen"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-26",
        "modelYear": 2026,
        "featuredTool": "Fireflies.ai",
        "readingTime": "8 min",
        "tools": [
            {"name": "Fireflies.ai", "verdict": "Meest complete — transcriptie, zoeken, actiepunten, CRM-integraties", "priceRange": "EUR 0-19/mnd", "bestFor": "Verkoopteams & power users", "rating": 4.6, "affiliateLink": "https://www.notion.so"},
            {"name": "Otter.ai", "verdict": "Beste realtime transcripties en samenwerking, sterk in onderwijs", "priceRange": "EUR 0-17/mnd", "bestFor": "Teams & onderwijs", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
            {"name": "Fathom", "verdict": "Meest gebruiksvriendelijk — automatische samenvattingen zonder bot in call", "priceRange": "EUR 0-29/mnd", "bestFor": "Individuen & kleine teams", "rating": 4.5, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("otter-ai-vs-fireflies-vs-fathom-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke AI-notulist werkt het beste met Nederlandse gesprekken?",
             "a": "Fireflies.ai biedt de beste Nederlandse transcriptie. Fathom en Otter.ai ondersteunen Nederlands, maar de nauwkeurigheid is iets lager dan bij Engels. Test alle drie met een Nederlands gesprek voor je een keuze maakt."},
            {"q": "Zijn AI meeting assistants AVG-proof?",
             "a": "Fireflies.ai en Fathom bieden EU-serveropties. Otter.ai verwerkt data voornamelijk in de VS. Check altijd de DPA (Data Processing Agreement) en informeer deelnemers dat een AI-notulist meeluistert."},
            {"q": "Is de gratis versie voldoende?",
             "a": "Voor incidenteel gebruik: ja. Fireflies gratis: 800 min opgeslagen. Otter gratis: 300 min/maand. Fathom gratis: 5 meetings. Voor dagelijks gebruik is een betaald abonnement nodig."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Otter.ai vs Fireflies.ai vs Fathom — de 3 beste AI meeting assistants van 2026.

Structuur:
- Introductie: AI meeting assistants maken automatisch notulen, transcripties en actiepunten. In 2026 zijn Otter.ai, Fireflies.ai en Fathom de top 3. Welke past bij jouw meetings?
- Hoofdsectie per tool (## koppen): Fireflies.ai (meest complete), Otter.ai (samenwerking), Fathom (gebruiksvriendelijk). Per tool: hoe het werkt, met welke platforms het integreert (Zoom/Teams/Meet), prijs in EUR, plus/minpunten, verdict.
- Vergelijkingstabel (markdown): tool, platforms, NL-ondersteuning, gratis limiet, prijs (EUR/mnd), beste-voor, opnameduur, score
- Conclusie: welke voor wie — verkoopteam, projectteam, freelancer, docent, consultant
- Sluit af met FAQ (## Veelgestelde Vragen) met 3 vragen en antwoorden

Focus op Nederlands gebruik. Prijzen in EUR. Schrijf vloeiend Nederlands.""",
    },
    {
        "slug": "gamma-vs-beautiful-ai-vs-tome-2026",
        "title": "Gamma vs Beautiful.ai vs Tome 2026: Beste AI Presentatie Tool Vergeleken",
        "description": "Gamma, Beautiful.ai of Tome? Vergelijk de 3 beste AI-tools voor presentaties in 2026. Automatisch mooie slides, datavisualisatie en samenwerken in realtime.",
        "category": "tools",
        "rating": 4.4,
        "priceRange": "EUR 0-25/mnd",
        "pros": ["Direct toepasbare vergelijking op prijs, functionaliteit en gebruiksgemak", "Praktisch voor NL-marketeers, consultants en teams", "Eerlijke plus- en minpunten per tool"],
        "cons": ["Prijzen kunnen wijzigen", "AI-presentatietools zijn nog in ontwikkeling", "Export naar PowerPoint varieert per tool"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-26",
        "modelYear": 2026,
        "featuredTool": "Gamma",
        "readingTime": "8 min",
        "tools": [
            {"name": "Gamma", "verdict": "Meest veelzijdig — presentaties, docs en websites in één tool", "priceRange": "EUR 0-10/mnd", "bestFor": "Veelzijdige content creators", "rating": 4.6, "affiliateLink": "https://www.notion.so"},
            {"name": "Beautiful.ai", "verdict": "Design-automatisering op topniveau — consistent mooie slides", "priceRange": "EUR 12-40/mnd", "bestFor": "Professionals die design niet willen doen", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
            {"name": "Tome", "verdict": "Beste storytelling — genereert complete verhaallijnen met AI", "priceRange": "EUR 0-16/mnd", "bestFor": "Storytelling & pitches", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("gamma-vs-beautiful-ai-vs-tome-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Kan ik AI-presentaties exporteren naar PowerPoint?",
             "a": "Ja, alle drie: Gamma exporteert naar PDF en PPT, Beautiful.ai naar PPTX (met beperkte bewerkbaarheid), Tome naar PDF. Voor volledige PowerPoint-bewerking is Beautiful.ai het beste."},
            {"q": "Welke tool is het beste voor teams?",
             "a": "Gamma biedt de beste realtime samenwerking (zoals Google Slides). Beautiful.ai heeft team-accounts met shared libraries. Tome is meer gericht op individuele creators. Voor teams van 5+ is Gamma de beste prijs-kwaliteit."},
            {"q": "Hoe zit het met Nederlandse ondersteuning?",
             "a": "Gamma en Tome ondersteunen Nederlands voor AI-tekstgeneratie. Beautiful.ai heeft Nederlandstalige UI maar AI-suggesties primair in Engels. De outputkwaliteit in Nederlands is bij Gamma het hoogst."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Gamma vs Beautiful.ai vs Tome — de 3 beste AI-presentatietools van 2026.

Structuur:
- Introductie: AI-presentatietools maken in 2026 in seconden professionele slides. Gamma, Beautiful.ai en Tome zijn de top 3. Welke is de beste voor jouw presentaties?
- Hoofdsectie per tool (## koppen): Gamma, Beautiful.ai, Tome. Per tool: type tool, hoe AI helpt, prijs (EUR), beste use case, plus/minpunten, verdict (1-2 zinnen).
- Vergelijkingstabel (markdown): tool, AI-slidegeneratie, templates, export, NL-ondersteuning, prijs (EUR/mnd), beste-voor, score
- Conclusie: welke tool voor welke gebruiker (consultant, marketeer, student, startup pitcher, docent)
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Prijzen in EUR. Schrijf nuchter en praktisch Nederlands.""",
    },
    {
        "slug": "descript-vs-podcastle-vs-alitu-2026",
        "title": "Descript vs Podcastle vs Alitu 2026: Beste AI Podcast Tool Vergeleken",
        "description": "Descript, Podcastle of Alitu voor je podcast in 2026? Vergelijk AI-editing, transcriptie, opruimen van ruis, videopodcasting en publicatie in deze uitgebreide review.",
        "category": "tools",
        "rating": 4.3,
        "priceRange": "EUR 0-30/mnd",
        "pros": ["Specifieke podcast-vergelijking — geen generieke audiotools", "Praktische tips voor NL-podcasters", "Eerlijke vergelijking op prijs en gebruiksgemak"],
        "cons": ["Nederlandse AI-spraakherkenning verschilt per tool", "Prijzen fluctueren", "Sommige features alleen in duurste plan"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-26",
        "modelYear": 2026,
        "featuredTool": "Descript",
        "readingTime": "8 min",
        "tools": [
            {"name": "Descript", "verdict": "Revolutionair — bewerk audio alsof het tekst is, met studiokwaliteit AI-stem", "priceRange": "EUR 0-24/mnd", "bestFor": "All-in-one podcast & video", "rating": 4.7, "affiliateLink": "https://www.notion.so"},
            {"name": "Podcastle", "verdict": "Beste prijs-kwaliteit voor audio-only podcasters", "priceRange": "EUR 0-12/mnd", "bestFor": "Budget podcasters", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
            {"name": "Alitu", "verdict": "Gebouwd voor solo podcasters — geautomatiseerde workflow van opname tot publicatie", "priceRange": "EUR 32/mnd", "bestFor": "Automatisering", "rating": 4.2, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("descript-vs-podcastle-vs-alitu-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke podcast tool werkt het beste voor Nederlandstalige content?",
             "a": "Descript heeft de beste Nederlandse transcriptie (via DeepL-integratie). Podcastle ondersteunt Nederlands voor transcriptie maar AI-stemmen zijn Engels. Alitu biedt basis NL-transcriptie. Voor Nederlandstalige podcasts is Descript de beste keuze."},
            {"q": "Kan ik met deze tools ook video opnemen?",
             "a": "Descript en Podcastle ondersteunen videopodcasting. Descript is hierin het sterkst — je kunt video bewerken alsof het een document is. Alitu is puur audio. Voor videopodcasts: kies Descript."},
            {"q": "Wat kost podcastsoftware per maand realistisch?",
             "a": "Starters: Podcastle gratis of EUR 5,99/mnd. Semi-professioneel: Descript EUR 14-24/mnd. Volledig geautomatiseerd: Alitu EUR 32/mnd. Reken ook op hosting (EUR 10-20/mnd) voor je podcast."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Descript vs Podcastle vs Alitu — de 3 beste AI-podcasttools van 2026.

Structuur:
- Introductie: Podcasting groeit in Nederland. AI-tools maken editen, transcriberen en publiceren eenvoudiger. Descript, Podcastle en Alitu zijn de top 3. Welke past bij jouw workflow?
- Hoofdsectie per tool (## koppen): Descript, Podcastle, Alitu. Per tool: kernfunctie, hoe AI helpt, prijs (EUR), beste voor, plus/minpunten, verdict.
- Vergelijkingstabel (markdown): tool, transcriptie NL, video-ondersteuning, AI-stemmen, hosting, prijs (EUR/mnd), beste-voor, score
- Conclusie: welke tool voor welke podcaster (solo beginner, professioneel team, videopodcaster, journalist)
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op Nederlands gebruik. Prijzen in EUR. Schrijf in vloeiend, toegankelijk Nederlands.""",
    },
    {
        "slug": "surferseo-vs-clearscope-vs-marketmuse-2026",
        "title": "SurferSEO vs Clearscope vs MarketMuse 2026: Beste AI Content Optimalisatie Tool",
        "description": "SurferSEO, Clearscope of MarketMuse voor SEO-content in 2026? Vergelijk AI-content scores, zoekwoordanalyse, briefings en SERP-analyse voor betere rankings.",
        "category": "tools",
        "rating": 4.5,
        "priceRange": "EUR 50-500/mnd",
        "pros": ["Diepgaande vergelijking van 3 marktleiders in AI-SEO", "Praktisch voor NL-content marketeers en SEO-specialisten", "Duidelijke prijsopbouw per tool"],
        "cons": ["Enterprise-tools — prijzig voor kleine ondernemers", "Nederlandse SERP-data verschilt per tool", "Leercurve bij MarketMuse is stijl"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": "2026-05-26",
        "modelYear": 2026,
        "featuredTool": "SurferSEO",
        "readingTime": "9 min",
        "tools": [
            {"name": "SurferSEO", "verdict": "Beste allround SEO-content tool — content editor met realtime NL-SERP-analyse", "priceRange": "EUR 59-199/mnd", "bestFor": "Content SEO allround", "rating": 4.6, "affiliateLink": "https://www.notion.so"},
            {"name": "Clearscope", "verdict": "Premium AI-contentoptimalisatie — Google's eigen aanpak van relevante content", "priceRange": "EUR 150-500/mnd", "bestFor": "Enterprise SEO-teams", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
            {"name": "MarketMuse", "verdict": "AI-contentstrategie op schaal — automatiseert content gap analyse en planning", "priceRange": "EUR 79-500/mnd", "bestFor": "Contentstrategie op schaal", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("surferseo-vs-clearscope-vs-marketmuse-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Werken deze tools voor Nederlandse zoekwoorden?",
             "a": "SurferSEO ondersteunt Nederlandse SERP-analyse — je ziet welke termen Nederlandse concurrenten gebruiken. Clearscope en MarketMuse zijn primair Engels, maar NL-content scoort indirect ook met de juiste semantische structuur. SurferSEO is de beste keuze voor puur Nederlandse SEO."},
            {"q": "Wat is het verschil met gratis tools zoals ChatGPT voor SEO?",
             "a": "ChatGPT genereert content maar analyseert niet de SERP. SurferSEO en Clearscope vergelijken jouw concept met de top 20 Google-resultaten en geven datagestuurde optimalisatietips. Voor professionele SEO is dat onmisbaar."},
            {"q": "Is het de investering waard voor een kleine website?",
             "a": "Voor websites met >10.000 bezoekers/maand: absoluut. Start met SurferSEO Essential (EUR 59/mnd). Voor kleinere sites: focus eerst op gratis tools zoals Google Search Console. De AI-SEO tools renderen pas bij serieuze contentvolumes."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over SurferSEO vs Clearscope vs MarketMuse — de 3 beste AI-contentoptimalisatie tools van 2026.

Structuur:
- Introductie: AI-contentoptimalisatie is in 2026 essentieel voor SEO. SurferSEO, Clearscope en MarketMuse helpen content scoren in Google. Welke tool past bij jouw strategie?
- Hoofdsectie per tool (## koppen): SurferSEO, Clearscope, MarketMuse. Per tool: hoe werkt de AI-analyse, prijs (EUR), integraties (WordPress, Google Docs), beste use case, plus/minpunten, verdict.
- Vergelijkingstabel (markdown): tool, NL-SERP, content score, integraties, prijs (EUR/mnd), beste-voor, leercurve, score
- Conclusie: welke voor wie — content marketeer, SEO-bureau, enterprise team, blogger, e-commerce
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de Nederlandse/Europese SEO-markt. Prijzen in EUR. Schrijf nuchter Nederlands. Vermeld dat MarketMuse meer een strategietool is, Clearscope de premium keuze, SurferSEO de beste allrounder.""",
    },
]

for i, article in enumerate(ARTICLES):
    print(f"[{i+1}/5] {article['slug']}...")
    try:
        text, wc = generate_one(article.pop("prompt"))
        fm = {k: v for k, v in article.items()}
        yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, width=200)
        content = f"---\n{yaml_str}---\n\n{text}\n"
        path = ARTICLES_DIR / f"{article['slug']}.md"
        path.write_text(content, encoding="utf-8")
        print(f"  OK: {wc} words -> {path}")
        time.sleep(1)  # Rate limit courtesy
    except Exception as e:
        print(f"  FAIL: {e}")
        sys.exit(1)

print("\nDone: 5/5 OK")
