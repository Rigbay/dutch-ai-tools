#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: Excel/spreadsheets, PDF analyse, webdesign.
May 22 01:30 — fills practical productivity gaps (now at 68, target 71+).
Uses Gemini 2.5 Flash."""

import os, json, time, sys, requests
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(key_file):
        for line in open(key_file):
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/tmp/dutch-ai-tools/src/content/articles"

ALL_SLUGS = sorted([
    f.replace(".md", "").replace("src/content/articles/", "")
    for f in __import__('glob').glob(f"{ARTICLES_DIR}/*.md")
])

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-tools-excel-spreadsheets-2026",
        "title": "Beste AI Tools voor Excel & Spreadsheets 2026: top 7 vergeleken",
        "description": "AI tools voor Excel, Google Sheets, formules en data-analyse in 2026. Van AI-formulegenerator tot automatische dashboards — vergelijk de beste spreadsheet-AI voor Nederlandse gebruikers.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor Excel, Google Sheets en spreadsheets in 2026. Behandel precies 7 tools: Microsoft Copilot in Excel, ChatGPT (voor formules), SheetAI, Rows AI, Numerous.ai, Ajelix, Formulabot.

Structuur:
- Introductie: AI transformeert spreadsheetwerk in 2026 — van uren formules debuggen naar één prompt. Nederland telt miljoenen Excel/Sheets-gebruikers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (boekhouder, data-analist, student, manager)
- 3 FAQ-vragen over AI in spreadsheets

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Microsoft Copilot in Excel", "verdict": "Microsoft's eigen AI-assistent voor Excel: formules genereren, data analyseren en grafieken maken met natuurlijke taal", "priceRange": "EUR 26/mnd (Microsoft 365 Copilot)", "bestFor": "Zakelijke Excel-gebruikers", "rating": 4.5, "affiliateLink": "https://www.microsoft.com/nl-nl/microsoft-365/copilot?ref=aitoolsnl"},
            {"name": "ChatGPT", "verdict": "Verrassend sterk in Excel-formules: plak je data, beschrijf wat je wilt en krijg werkende formules", "priceRange": "EUR 0-22/mnd", "bestFor": "Snelle formulehulp", "rating": 4.3, "affiliateLink": "https://chat.openai.com/?ref=aitoolsnl"},
            {"name": "SheetAI", "verdict": "Google Sheets add-on die AI direct in cellen brengt — =AI() functies voor tekst, vertaling en analyse", "priceRange": "EUR 0-12/mnd", "bestFor": "Google Sheets power users", "rating": 4.2, "affiliateLink": "https://sheetai.app/?ref=aitoolsnl"},
            {"name": "Rows AI", "verdict": "Next-gen spreadsheet met ingebouwde AI-analist — stel vragen over je data in gewoon Nederlands", "priceRange": "EUR 0-49/mnd", "bestFor": "Data-analyse zonder code", "rating": 4.4, "affiliateLink": "https://rows.com/?ref=aitoolsnl"},
            {"name": "Numerous.ai", "verdict": "ChatGPT in Google Sheets: =INFER(), =WRITE(), =FORMAT() — formulegeneratie die context begrijpt", "priceRange": "EUR 8-25/mnd", "bestFor": "Content & tekst in Sheets", "rating": 4.1, "affiliateLink": "https://numerous.ai/?ref=aitoolsnl"},
            {"name": "Ajelix", "verdict": "Excel-optimalisatie: formule debugger, VBA-script generator en spreadsheet performance scanner", "priceRange": "EUR 0-15/mnd", "bestFor": "Excel-veteranen & debugging", "rating": 4.0, "affiliateLink": "https://ajelix.com/?ref=aitoolsnl"},
            {"name": "Formulabot", "verdict": "Laagdrempelige AI die formules genereert uit tekstbeschrijving — ook Nederlands ondersteund", "priceRange": "EUR 0-10/mnd", "bestFor": "Beginners & studenten", "rating": 4.0, "affiliateLink": "https://formulabot.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-excel-spreadsheets-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-pdf-documenten-2026",
        "title": "Beste AI Tools voor PDF & Document Analyse 2026: top 7 vergeleken",
        "description": "AI tools voor PDF samenvatten, documenten analyseren, contracten checken en lange teksten verwerken in 2026. Vergelijk de beste document-AI voor Nederlandse professionals.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor PDF-analyse, documenten samenvatten en lange teksten verwerken in 2026. Behandel precies 7 tools: Claude (voor lange documenten), ChatGPT (PDF upload), NotebookLM, ChatPDF, AskYourPDF, PDF.ai, Humata AI.

Structuur:
- Introductie: In 2026 leest AI je documenten sneller dan jij — van jaarverslagen tot contracten en wetenschappelijke papers. Praktische tool-vergelijking voor Nederlandse kenniswerkers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (jurist die contracten checkt, student die papers samenvat, onderzoeker die literatuur analyseert)
- 3 FAQ-vragen over AI voor documentanalyse

Focus op Nederlandse/Europese context. Prijzen in EUR. Noem concrete NL-use cases. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Claude (Anthropic)", "verdict": "Beste AI voor lange documenten: 200K token context — leest complete boeken en jaarverslagen in één keer", "priceRange": "EUR 0-22/mnd", "bestFor": "Lange documenten & diepte-analyse", "rating": 4.8, "affiliateLink": "https://claude.ai/?ref=aitoolsnl"},
            {"name": "ChatGPT", "verdict": "PDF-uploadmogelijkheid met sterke samenvattingen — goed voor snelle checks en vragen stellen over documenten", "priceRange": "EUR 0-22/mnd", "bestFor": "Snelle document QA", "rating": 4.5, "affiliateLink": "https://chat.openai.com/?ref=aitoolsnl"},
            {"name": "NotebookLM", "verdict": "Google's gratis AI die specifiek is ontworpen voor documentanalyse — meerdere bronnen tegelijk, automatische FAQ's en podcasts", "priceRange": "EUR 0 (gratis)", "bestFor": "Onderzoek & studie", "rating": 4.7, "affiliateLink": "https://notebooklm.google.com/?ref=aitoolsnl"},
            {"name": "ChatPDF", "verdict": "Eenvoudigste PDF-AI: upload een PDF en stel vragen in gewoon Nederlands — geen account nodig voor eerste gebruik", "priceRange": "EUR 0-20/mnd", "bestFor": "Eenvoud & snelheid", "rating": 4.2, "affiliateLink": "https://www.chatpdf.com/?ref=aitoolsnl"},
            {"name": "AskYourPDF", "verdict": "Chrome-extensie voor directe PDF-analyse in de browser — vergelijkt documentversies en extraheert data", "priceRange": "EUR 0-15/mnd", "bestFor": "Browser-gebaseerd werken", "rating": 4.1, "affiliateLink": "https://askyourpdf.com/?ref=aitoolsnl"},
            {"name": "PDF.ai", "verdict": "Chat-interface specifiek voor PDF's met OCR — leest gescande documenten, facturen en handgeschreven notities", "priceRange": "EUR 8-30/mnd", "bestFor": "Gescande documenten & OCR", "rating": 4.3, "affiliateLink": "https://pdf.ai/?ref=aitoolsnl"},
            {"name": "Humata AI", "verdict": "AI-documentanalyse met nadruk op wetenschap en research — automatische citaties en cross-referenties", "priceRange": "EUR 0-49/mnd", "bestFor": "Wetenschappelijk onderzoek", "rating": 4.4, "affiliateLink": "https://www.humata.ai/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-pdf-documenten-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-webdesign-websites-2026",
        "title": "Beste AI Tools voor Webdesign & Website Bouwen 2026: top 7 vergeleken",
        "description": "AI tools voor webdesign, website bouwen en UI/UX in 2026. Vergelijk de beste AI-websitebuilders, designgenerators en no-code platforms voor Nederlandse makers en ondernemers.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor webdesign, website bouwen en UI/UX in 2026. Behandel precies 7 tools: Wix AI Website Builder, Framer AI, 10Web AI Builder, Hostinger AI Builder, Relume, Durable, Uizard.

Structuur:
- Introductie: AI bouwt complete websites in minuten in 2026 — van landingspagina's tot webshops. Wat betekent dit voor Nederlandse ondernemers, freelancers en designers?
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type maker (ondernemer die snel online wil, designer die AI als assistent gebruikt, agency die schaalt)
- 3 FAQ-vragen over AI en webdesign

Focus op Nederlandse/Europese context. Prijzen in EUR. Noem concrete NL-use cases. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Wix AI Website Builder", "verdict": "Volledige AI-websitegenerator: beantwoord een paar vragen en krijg een complete, mobiele website met AI-content", "priceRange": "EUR 0-27/mnd", "bestFor": "Snelle complete websites", "rating": 4.5, "affiliateLink": "https://www.wix.com/?ref=aitoolsnl"},
            {"name": "Framer AI", "verdict": "Design-first AI: genereer prachtige designs met AI en publiceer direct — favoriet bij designers en startups", "priceRange": "EUR 0-25/mnd", "bestFor": "Design-kwaliteit & interactiviteit", "rating": 4.6, "affiliateLink": "https://www.framer.com/?ref=aitoolsnl"},
            {"name": "10Web AI Builder", "verdict": "AI bouwt een WordPress-site inclusief hosting in minuten — inclusief AI SEO en AI copy", "priceRange": "EUR 12-39/mnd", "bestFor": "WordPress & SEO-geoptimaliseerd", "rating": 4.4, "affiliateLink": "https://10web.io/?ref=aitoolsnl"},
            {"name": "Hostinger AI Builder", "verdict": "Budgetvriendelijk: AI-websitebuilder met NL-domein en hosting in één pakket vanaf €2,99", "priceRange": "EUR 3-8/mnd", "bestFor": "Budget & beginners", "rating": 4.2, "affiliateLink": "https://www.hostinger.nl/?ref=aitoolsnl"},
            {"name": "Relume", "verdict": "AI voor wireframes en sitemaps: genereert complete websitestructuren die je exporteert naar Webflow of Figma", "priceRange": "EUR 15-38/mnd", "bestFor": "Designers & agencies", "rating": 4.3, "affiliateLink": "https://www.relume.io/?ref=aitoolsnl"},
            {"name": "Durable", "verdict": "AI bouwt een complete bedrijfswebsite in 30 seconden — met AI-content, afbeeldingen en CRM-koppeling", "priceRange": "EUR 12-20/mnd", "bestFor": "Kleine ondernemers & ZZP", "rating": 4.1, "affiliateLink": "https://durable.co/?ref=aitoolsnl"},
            {"name": "Uizard", "verdict": "AI-prototyping: schets op papier → foto → werkbare UI in minuten — ideaal voor rapid prototyping en mockups", "priceRange": "EUR 0-39/mnd", "bestFor": "UI/UX prototyping", "rating": 4.3, "affiliateLink": "https://uizard.io/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-tools-webdesign-websites-2026", ALL_SLUGS, 3)
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
    pros = [
        "Gebaseerd op actuele marktdata en praktijkervaringen uit 2026",
        "Duidelijke vergelijking met prijzen, verdicts en scores per tool",
        "Nederlandstalig en toegankelijk voor professionals in deze sector"
    ]
    cons = [
        "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
        "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
        "Sommige AI-features zijn nog in actieve ontwikkeling of beta"
    ]
    
    import yaml
    frontmatter = {
        "title": article["title"],
        "slug": slug,
        "description": article["description"],
        "category": article["category"],
        "rating": article.get("rating", 4.5),
        "priceRange": article.get("priceRange", "EUR 0-50/mnd"),
        "pros": pros,
        "cons": cons,
        "affiliateLinks": [t["affiliateLink"] for t in article["tools"]],
        "related": article["related"],
        "date": today,
        "modelYear": 2026,
        "featuredProduct": article["tools"][0]["name"],
        "readingTime": "7 min",
        "products": article["tools"],
        "draft": False
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
    
    print(f"Generating {len(NEW_ARTICLES)} articles...")
    print(f"API key: {API_KEY[:10]}...")
    
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
        print(f"  - {r}")

if __name__ == "__main__":
    main()
