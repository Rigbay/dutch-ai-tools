#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: overheid, consultancy, financieel.
Batch 8 v2 — May 21 2026. Uses Gemini 2.5 Flash with real article schema."""

import os, json, time, sys, requests
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()

BASE_URL_FLASH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
BASE_URL_LITE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

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
    "beste-ai-seo-tools-2026", "beste-ai-muziek-audio-tools-2026",
    "beste-ai-meeting-transcriptie-tools-2026",
    "beste-ai-vertaaltools-2026", "beste-ai-presentatie-tools-2026",
    "beste-ai-sales-tools-2026",
    "beste-ai-tools-boekhouders-accountants-2026", "beste-ai-tools-makelaars-vastgoed-2026",
    "beste-ai-copywriting-tools-2026", "beste-ai-tools-podcasters-2026",
    "beste-ai-tools-cybersecurity-2026", "beste-ai-tools-cloud-optimalisatie-2026",
    "beste-ai-tools-data-privacy-avg-2026", "beste-ai-tools-lowcode-nocode-2026",
    "beste-ai-tools-api-ontwikkeling-2026",
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-tools-overheid-2026",
        "title": "Beste AI Tools voor de Overheid 2026: Automatisering, Documentverwerking & Burgerzaken",
        "description": "AI in de publieke sector 2026. Vergelijk AI tools voor documentverwerking, burgerzaken, beleidsanalyse en compliance. Specifiek voor Nederlandse overheidsorganisaties.",
        "category": "business",
        "rating": 4.3,
        "priceRange": "EUR 28-2500/mnd of op aanvraag",
        "pros": [
            "NL-specifieke tools voor overheidsautomatisering",
            "AVG-compliance centraal bij elke tool",
            "Praktische vergelijking per overheidslaag"
        ],
        "cons": [
            "Enterprise-tools vaak op aanvraag — geen transparante prijzen",
            "Sommige NL-tools klein en minder volwassen",
            "Aanbestedingstrajecten vertragen adoptie"
        ],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-21",
        "modelYear": 2026,
        "featuredTool": "Microsoft Copilot for Government",
        "readingTime": "8 min",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de Nederlandse overheid in 2026. Behandel precies 7 tools/categorieën: IBM watsonx.governance, Microsoft Copilot for Government 365, Textgain, NLPal, OBI4wan, Palantir AIP, Tykn.

Structuur:
- Introductie: AI in de Nederlandse overheid groeit in 2026 — documentverwerking, burgerzaken, beleidsanalyse. Nadruk op AVG-compliance, transparantie, uitlegbare AI.
- Per tool een ## kop met: beschrijving, prijsindicatie (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR), beste-voor, AVG-compliant?, score (1-5)
- Conclusie: welke tool voor welke overheidslaag (gemeente, provincie, rijksoverheid, waterschap)
- Sluit af met een FAQ-sectie (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de NEDERLANDSE context. Textgain, OBI4wan en NLPal zijn echte NL bedrijven. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "IBM watsonx.governance", "verdict": "Enterprise-grade AI governance platform met transparantie en compliance — leidend in overheidssector", "priceRange": "Op aanvraag", "bestFor": "Grootschalige AI governance", "rating": 4.5, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Microsoft Copilot for Government", "verdict": "AI-assistent geïntegreerd met bestaande Microsoft-overheidslicenties — direct inzetbaar", "priceRange": "EUR 28-55/gebruiker/mnd", "bestFor": "Document- & mailverwerking", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Textgain", "verdict": "Nederlands AI-bedrijf voor text mining bij overheid — hate speech detectie, beleidsanalyse", "priceRange": "Op aanvraag", "bestFor": "Overheidstekstanalyse", "rating": 4.2, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "NLPal", "verdict": "Nederlandse AI-startup voor automatische beleidsanalyse en kamerstuk-monitoring", "priceRange": "Op aanvraag", "bestFor": "Beleidsmonitoring", "rating": 4.0, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "OBI4wan", "verdict": "Nederlands platform voor burgercommunicatie — AI-gestuurde webcare, chatbot en social monitoring", "priceRange": "EUR 500-2500/mnd", "bestFor": "Burgercommunicatie", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Palantir AIP", "verdict": "Grootschalig data-analyseplatform — complexe databronnen integreren en AI-modellen bouwen", "priceRange": "Op aanvraag (enterprise)", "bestFor": "Data-analyse op schaal", "rating": 4.1, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Tykn", "verdict": "Nederlands blockchain-identiteitsplatform — digitale identiteit voor burgers met privacy-by-design", "priceRange": "Op aanvraag", "bestFor": "Digitale identiteit", "rating": 3.9, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "faq": [
            {"q": "Is AI in de Nederlandse overheid AVG-compliant?", "a": "Ja, mits correct geïmplementeerd. De Nederlandse overheid hanteert strikte richtlijnen voor AI-gebruik, waaronder transparantie, menselijke tussenkomst bij beslissingen en dataminimalisatie. Tools als IBM watsonx.governance zijn specifiek ontworpen voor gereguleerde sectoren."},
            {"q": "Welke AI-tool past het best bij een gemeente?", "a": "Voor gemeenten is OBI4wan de beste start — het biedt burgercommunicatie, webcare en een chatbot in één platform. Voor documentverwerking is Microsoft Copilot for Government een logische keuze omdat de meeste gemeenten al op Microsoft werken."},
            {"q": "Hoe zit het met aanbesteding bij AI-tools voor de overheid?", "a": "AI-tools vallen onder de reguliere aanbestedingsregels. Enterprise-tools zoals Palantir en IBM worden doorgaans via een openbare aanbesteding aangeschaft. Kleinere tools zoals Textgain kunnen via een meervoudig onderhandse procedure."},
        ],
        "related": pick_related("beste-ai-tools-overheid-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-consultancy-2026",
        "title": "Beste AI Tools voor Consultancy & Adviesbureaus 2026: Analyse, Rapportage & Strategie",
        "description": "AI voor consultants in 2026: vergelijk tools voor data-analyse, strategieontwikkeling, rapportage en klantpresentaties. Werk slimmer, niet harder.",
        "category": "business",
        "rating": 4.4,
        "priceRange": "EUR 0-75/mnd",
        "pros": [
            "Direct toepasbaar voor alle typen consultants",
            "Mix van gratis en betaalde tools — lage instapdrempel",
            "Concrete tijdbesparing van 10+ uur per week per consultant"
        ],
        "cons": [
            "Enterprise-tools hebben leercurve",
            "Kleinere tools missen integraties met consulting-software",
            "Sommige tools generiek, niet consultancy-specifiek"
        ],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-21",
        "modelYear": 2026,
        "featuredTool": "Fireflies.ai",
        "readingTime": "8 min",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor consultancy en adviesbureaus in 2026. Behandel precies 7 tools: Cogram, Fireflies.ai, Julius AI, Numerous.ai, Qatalog, Craft, Sana AI.

Structuur:
- Introductie: consultancy in 2026 wordt getransformeerd door AI — automatische meetingnotities, AI-strategie-analyse. Consultants besparen 10+ uur per week.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, integraties, score (1-5)
- Conclusie: welke AI tool stack voor welk type consultant (strategie, finance, operations, IT, onafhankelijk ZZP)
- Sluit af met een FAQ-sectie (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de Nederlandse/Europese markt. Accent op tijdbesparing en kwaliteitsverbetering. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Cogram", "verdict": "AI gebouwd voor consultants — automatische meeting notes, CRM-sync en projecttracking in één platform", "priceRange": "EUR 25-75/mnd", "bestFor": "Consultancy meetings", "rating": 4.5, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Fireflies.ai", "verdict": "Automatische meetingtranscriptie met zoekfunctie en AI-samenvattingen — verwerkt Teams, Zoom, Google Meet", "priceRange": "EUR 0-25/mnd", "bestFor": "Meeting intelligence", "rating": 4.4, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Julius AI", "verdict": "AI-data-analist die spreadsheets en datasets in seconden analyseert — grafieken, inzichten, rapportages", "priceRange": "EUR 15-50/mnd", "bestFor": "Data-analyse", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Numerous.ai", "verdict": "AI in Google Sheets en Excel — formules genereren, data categoriseren, trendanalyses met natuurlijke taal", "priceRange": "EUR 8-30/mnd", "bestFor": "Spreadsheet analyse", "rating": 4.2, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Qatalog", "verdict": "Enterprise AI-kennisbeheer — automatisch verbinden van documenten, mensen en projecten in één intelligente laag", "priceRange": "EUR 15-50/mnd", "bestFor": "Kennisbeheer", "rating": 4.1, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Craft", "verdict": "Moderne document- en strategietool met AI-schrijfhulp — favoriet bij strategieconsultants", "priceRange": "EUR 0-12/mnd", "bestFor": "Strategiedocumenten", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Sana AI", "verdict": "Enterprise AI-assistent die bedrijfsdocumenten begrijpt en vragen beantwoordt — interne kennis ontsluiten", "priceRange": "Op aanvraag (enterprise)", "bestFor": "Enterprise knowledge", "rating": 4.0, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "faq": [
            {"q": "Hoeveel tijd bespaart AI een consultant per week?", "a": "Gemiddeld 10-15 uur per week, blijkt uit 2026-onderzoek onder consultants. Meeting transcription tools besparen 3-5 uur, data-analyse tools 4-6 uur, en schrijfassistenten 2-4 uur. De grootste winst zit in het elimineren van handmatig notuleren en spreadsheets doorkruisen."},
            {"q": "Welke AI-tool is het beste voor een startende ZZP-consultant?", "a": "Fireflies.ai (gratis tier) + Craft (gratis tier) vormen de ideale gratis start. Voor €25/maand voeg je Cogram toe voor consultancy-specifieke meeting tracking. Totale minimale stack: €0-25/maand."},
            {"q": "Zijn AI-tools veilig voor vertrouwelijke klantinformatie?", "a": "De meeste genoemde tools hebben enterprise-grade beveiliging en SOC 2-certificering. Controleer altijd de Data Processing Agreement (DPA) en of data binnen de EU blijft — relevant voor Nederlandse consultants met AVG-verplichtingen."},
        ],
        "related": pick_related("beste-ai-tools-consultancy-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-tools-financieel-2026",
        "title": "Beste AI Tools voor de Financiële Sector 2026: Risicoanalyse, Frauddetectie & Rapportage",
        "description": "AI in de financiële sector 2026: vergelijk tools voor risicoanalyse, frauddetectie, compliance en financiële rapportage. Voor banken, verzekeraars en fintechs.",
        "category": "business",
        "rating": 4.5,
        "priceRange": "EUR 0-2500/mnd of op aanvraag",
        "pros": [
            "NL-specifieke tools naast internationale marktleiders",
            "DNB/AFM compliance centraal",
            "Praktische use cases per type financiële organisatie"
        ],
        "cons": [
            "Enterprise-tools hebben hoge instapdrempel",
            "Veel prijzen op aanvraag — niet transparant",
            "Strikte regulering beperkt adoptie bij kleinere spelers"
        ],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-21",
        "modelYear": 2026,
        "featuredTool": "Feedzai",
        "readingTime": "8 min",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de financiële sector in 2026. Behandel precies 7 tools: BUX AI, Owlin, KAS BANK AI Platform, Feedzai, DataSnipper, Ocrolus, ComplyAdvantage.

Structuur:
- Introductie: de Nederlandse financiële sector loopt voorop in AI-adoptie — frauddetectie, beleggingsadviezen, compliance. DNB en AFM stellen strikte eisen.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR), beste-voor, NL-aanwezig?, DNB-compliant?, score (1-5)
- Conclusie: welke AI tool voor welk type financiële organisatie (grootbank, verzekeraar, fintech startup, accountantskantoor)
- Sluit af met een FAQ-sectie (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de NEDERLANDSE context. BUX, Owlin en KAS BANK zijn echte NL bedrijven. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "BUX AI", "verdict": "Nederlands fintech-platform met AI-beleggingsassistent — portfolio-analyse en marktinzichten in natuurlijke taal", "priceRange": "EUR 0-15/mnd", "bestFor": "Beleggingsanalyse", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Owlin", "verdict": "Nederlands AI-platform voor realtime nieuwsanalyse — risico's in supply chain en tegenpartijen direct signaleren", "priceRange": "Op aanvraag (enterprise)", "bestFor": "Risicomonitoring", "rating": 4.4, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "KAS BANK AI", "verdict": "Institutioneel AI-platform van de Nederlandse custodian bank — settlement optimalisatie, liquiditeitsvoorspelling", "priceRange": "Op aanvraag (institutioneel)", "bestFor": "Institutioneel beheer", "rating": 4.0, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Feedzai", "verdict": "Wereldleider in AI-frauddetectie — realtime transactieanalyse met 95%+ detectiegraad, gebruikt door grootbanken", "priceRange": "Op aanvraag (enterprise)", "bestFor": "Frauddetectie", "rating": 4.7, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "DataSnipper", "verdict": "AI-auditplatform dat automatisch documenten leest, kruisverwijst en valideert — standaard bij Big Four accountants", "priceRange": "Op aanvraag (enterprise)", "bestFor": "Audit & compliance", "rating": 4.5, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Ocrolus", "verdict": "AI-documentverwerking voor financiële dienstverleners — bankafschriften en loonstroken automatisch uitlezen", "priceRange": "Op aanvraag", "bestFor": "Documentanalyse", "rating": 4.2, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "ComplyAdvantage", "verdict": "AI-gedreven AML/KYC-sanctiescreening — realtime checks op wereldwijde sanctielijsten en adverse media", "priceRange": "Op aanvraag (enterprise)", "bestFor": "AML compliance", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "faq": [
            {"q": "Moet een AI-tool in de financiële sector DNB-goedgekeurd zijn?", "a": "Nee, niet elke AI-tool heeft aparte DNB-goedkeuring nodig. De financiële instelling zelf is verantwoordelijk voor compliance. Tools moeten wel aantoonbaar voldoen aan DNB-richtlijnen voor uitbesteding en risicobeheer. Bij kernprocessen is voorafgaande toetsing nodig."},
            {"q": "Wat is het verschil tussen frauddetectie en AML-compliance?", "a": "Frauddetectie (zoals Feedzai) richt zich op het onderscheppen van verdachte transacties in realtime. AML/KYC-compliance (zoals ComplyAdvantage) richt zich op het screenen van klanten tegen sanctielijsten en het voorkomen van witwassen. Beide zijn verplicht maar dienen verschillende doelen."},
            {"q": "Is er een betaalbare AI-tool voor kleine accountantskantoren?", "a": "DataSnipper biedt een mid-market tier voor kleinere kantoren — vanaf ongeveer €100/gebruiker/maand. Voor documentverwerking is Ocrolus toegankelijker qua prijsstelling. De combinatie van beide dekt audit en documentverwerking voor een klein kantoor voor circa €200-400/maand."},
        ],
        "related": pick_related("beste-ai-tools-financieel-2026", ALL_SLUGS, 3)
    },
]


def generate_one(article, attempt=1):
    url = BASE_URL_LITE if attempt > 2 else BASE_URL_FLASH
    model = "Flash-Lite" if attempt > 2 else "Flash"
    payload = {
        "contents": [{"parts": [{"text": article["prompt"]}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    resp = requests.post(
        f"{url}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=120
    )
    if resp.status_code == 503 and attempt <= 2:
        print(f"  {model} returned 503, retry {attempt+1}...")
        time.sleep(3)
        return generate_one(article, attempt + 1)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    word_count = len(text.split())
    return text, word_count, model


def write_mdx(article, body):
    tools = article["tools"]
    related = article["related"]
    faq = article["faq"]

    # Build YAML-safe multiline arrays
    def yaml_arr(items, indent=4):
        """Format array for YAML."""
        lines = []
        for item in items:
            if isinstance(item, str):
                lines.append(f"{' ' * indent}- {item}")
            elif isinstance(item, dict):
                lines.append(f"{' ' * indent}-")
                for k, v in item.items():
                    if isinstance(v, (int, float)):
                        lines.append(f"{' ' * (indent+2)}{k}: {v}")
                    else:
                        lines.append(f"{' ' * (indent+2)}{k}: '{v}'")
        return "\n".join(lines)

    pros_yaml = yaml_arr(article["pros"])
    cons_yaml = yaml_arr(article["cons"])
    aff_yaml = yaml_arr(article["affiliateLinks"])
    tools_yaml = yaml_arr(tools, 2)
    related_yaml = yaml_arr(related, 2)
    faq_yaml = yaml_arr(faq, 4)

    mdx = f"""---
title: '{article["title"]}'
slug: {article["slug"]}
description: {article["description"]}
category: {article["category"]}
rating: {article["rating"]}
priceRange: {article["priceRange"]}
pros:
{pros_yaml}
cons:
{cons_yaml}
affiliateLinks:
{aff_yaml}
date: {article["date"]}
modelYear: {article["modelYear"]}
featuredTool: {article["featuredTool"]}
readingTime: {article["readingTime"]}
tools:
{tools_yaml}
related:
{related_yaml}
faq:
{faq_yaml}
---

{body}
"""
    path = ARTICLES_DIR / f"{article['slug']}.md"
    path.write_text(mdx, encoding="utf-8")
    return path


def main():
    if not API_KEY:
        print("ERROR: No GEMINI_API_KEY")
        sys.exit(1)

    print(f"Generating {len(NEW_ARTICLES)} articles...")
    results = []

    for i, article in enumerate(NEW_ARTICLES):
        print(f"[{i+1}/{len(NEW_ARTICLES)}] {article['slug']}...")
        try:
            text, wc, model = generate_one(article)
            path = write_mdx(article, text)
            results.append({"slug": article["slug"], "words": wc, "model": model, "ok": True})
            print(f"  OK: {wc} words via {model} -> {path}")
        except Exception as e:
            results.append({"slug": article["slug"], "ok": False, "error": str(e)})
            print(f"  FAIL: {e}")

    ok = sum(1 for r in results if r["ok"])
    print(f"\nDone: {ok}/{len(NEW_ARTICLES)} OK")
    if ok < len(NEW_ARTICLES):
        for r in results:
            if not r["ok"]:
                print(f"  FAILED: {r['slug']} — {r['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
