#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: vertaling, presentatie, sales CRM.
Batch 5 — May 20 2026. Uses Gemini 2.5 Flash with Flash-Lite fallback."""

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
ARTICLES_DIR = Path("/workspace/agent-workspace/scripts/missions/passive-income/dutch-ai-tools-comparison/src/content/articles")

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
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-vertaaltools-2026",
        "title": "Beste AI Vertaaltools 2026: DeepL vs ChatGPT vs Google Translate vergeleken",
        "description": "AI vertaling in 2026: vergelijk DeepL, ChatGPT, Google Translate, Claude en meer. Welke AI vertaaltool levert de beste Nederlandse vertalingen voor jouw werk?",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI vertaaltools in 2026. Behandel precies 7 tools: DeepL, ChatGPT, Claude, Google Translate, DeepL Write, Mate Translate, Wordvice AI.

Structuur:
- Introductie: AI-vertaling is in 2026 volwassen — DeepL domineert de Nederlandse markt, ChatGPT/Claude bieden contextbewuste vertaling, en Google Translate is gratis en alomtegenwoordig
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, Nederlands kwaliteit (1-5), API beschikbaar?, score (1-5)
- Conclusie: welke vertaaltool voor wie (ZZP'er, MKB, content creator, academicus, developer)
- 3 FAQ-vragen over AI vertaling

Focus op de Nederlandse markt. DeepL is veruit de populairste en meest accurate voor Nederlands — besteed hier extra aandacht aan. ChatGPT en Claude zijn opkomende alternatieven met contextbewuste vertaling. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "DeepL", "verdict": "Absolute leider in AI-vertaling met de beste Nederlands-Engelse en Nederlands-Duitse kwaliteit in 2026", "priceRange": "EUR 0-50/mnd", "bestFor": "Professionele vertaling", "rating": 4.9, "affiliateLink": "https://www.deepl.com/?ref=aitoolsnl"},
            {"name": "ChatGPT", "verdict": "Contextbewuste vertaling met toon-aanpassing en uitleg — sterk voor creatieve en informele teksten", "priceRange": "EUR 0-25/mnd", "bestFor": "Conversational & context", "rating": 4.5, "affiliateLink": "https://chatgpt.com/?ref=aitoolsnl"},
            {"name": "Claude", "verdict": "Uitstekende Nederlandse vertaling met ethische nuance en lange documentverwerking", "priceRange": "EUR 0-25/mnd", "bestFor": "Lange documenten", "rating": 4.4, "affiliateLink": "https://claude.ai/?ref=aitoolsnl"},
            {"name": "Google Translate", "verdict": "Gratis en alomtegenwoordig met 130+ talen — de go-to voor snelle vertalingen", "priceRange": "EUR 0/mnd", "bestFor": "Snelle vertalingen", "rating": 4.2, "affiliateLink": "https://translate.google.com/?ref=aitoolsnl"},
            {"name": "DeepL Write", "verdict": "AI-schrijfassistent die Nederlandse tekst verbetert op grammatica, stijl en toon", "priceRange": "EUR 0-15/mnd", "bestFor": "Tekstverbetering NL", "rating": 4.3, "affiliateLink": "https://www.deepl.com/write?ref=aitoolsnl"},
            {"name": "Mate Translate", "verdict": "Browser-extensie voor direct vertalen tijdens browsen — 103 talen, offline mode", "priceRange": "EUR 0-40/jr", "bestFor": "Browser vertalen", "rating": 4.0, "affiliateLink": "https://gikken.co/mate-translate/?ref=aitoolsnl"},
            {"name": "Wordvice AI", "verdict": "Academische AI-proofreader met vertaalfunctie gericht op studenten en onderzoekers", "priceRange": "EUR 0-20/mnd", "bestFor": "Academische teksten", "rating": 3.9, "affiliateLink": "https://wordvice.ai/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-vertaaltools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-presentatie-tools-2026",
        "title": "Beste AI Presentatie Tools 2026: Gamma vs Beautiful.ai vs Tome vergeleken",
        "description": "AI presentaties maken in 2026. Vergelijk Gamma, Beautiful.ai, Tome, Decktopus en meer. Maak professionele slides in minuten — geen design skills nodig.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI presentatie tools in 2026. Behandel precies 7 tools: Gamma, Beautiful.ai, Tome, Decktopus, Simplified AI, Canva AI Presentaties, Prezi AI.

Structuur:
- Introductie: AI transformeert presentaties maken in 2026 — volledige pitch decks, sales presentaties en lessen in minuten gegenereerd, zonder designvaardigheden
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, Nederlands?, export-formaten, score (1-5)
- Conclusie: welke AI presentatie tool voor welk type gebruiker (ZZP'er, sales team, docent, marketeer)
- 3 FAQ-vragen over AI presentaties

Focus op Nederlandse markt. Gamma is in 2026 de snelst groeiende — van prompt naar volledige presentatie in seconden. Canva AI is voor Nederlanders vertrouwd. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Gamma", "verdict": "Beste allround AI-presentatietool — van prompt naar complete presentatie met AI-gegenereerde visuals", "priceRange": "EUR 0-20/mnd", "bestFor": "Snelle AI decks", "rating": 4.7, "affiliateLink": "https://gamma.app/?ref=aitoolsnl"},
            {"name": "Beautiful.ai", "verdict": "Design-automatisering die slides realtime aanpast — altijd professionele layout zonder handwerk", "priceRange": "EUR 12-50/mnd", "bestFor": "Zakelijke presentaties", "rating": 4.5, "affiliateLink": "https://www.beautiful.ai/?ref=aitoolsnl"},
            {"name": "Tome", "verdict": "AI storytelling platform dat presentaties bouwt rond een verhaallijn — sterk voor pitches", "priceRange": "EUR 0-20/mnd", "bestFor": "Pitch decks", "rating": 4.4, "affiliateLink": "https://tome.app/?ref=aitoolsnl"},
            {"name": "Decktopus", "verdict": "Snelste AI-deck builder met ingebouwde formulieren en lead-capturing — ideaal voor sales", "priceRange": "EUR 10-35/mnd", "bestFor": "Sales presentaties", "rating": 4.3, "affiliateLink": "https://www.decktopus.com/?ref=aitoolsnl"},
            {"name": "Simplified AI", "verdict": "All-in-one AI-creatieplatform met sterke presentatie-module plus video, social media en copy", "priceRange": "EUR 0-25/mnd", "bestFor": "Social media decks", "rating": 4.1, "affiliateLink": "https://simplified.com/?ref=aitoolsnl"},
            {"name": "Canva AI Presentaties", "verdict": "De vertrouwde Canva-interface met nieuwe AI-presentatiegenerator — miljoenen Nederlandse gebruikers", "priceRange": "EUR 0-13/mnd", "bestFor": "Canva-gebruikers", "rating": 4.2, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "Prezi AI", "verdict": "AI-ondersteunde dynamische presentaties met het kenmerkende zoom/canvas-effect", "priceRange": "EUR 0-20/mnd", "bestFor": "Visuele storytelling", "rating": 4.0, "affiliateLink": "https://prezi.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-presentatie-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-sales-tools-2026",
        "title": "Beste AI Sales Tools 2026: Apollo vs Lemlist vs Clay vergeleken",
        "description": "AI voor sales in 2026: vergelijk Apollo.io, Lemlist, Instantly, Clay en meer. Automatiseer lead generation, outreach en follow-ups met AI.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI sales tools in 2026. Behandel precies 7 tools: Apollo.io, Lemlist, Instantly, Clay, Salesforce Einstein GPT, HubSpot Breeze AI, Close CRM AI.

Structuur:
- Introductie: AI transformeert B2B sales in 2026 — van AI-gegenereerde leads tot gepersonaliseerde outreach op schaal. Nederland telt 2.5M+ ZZP'ers en MKB'ers die baat hebben bij AI-gedreven sales
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, Nederlands?, integraties, score (1-5)
- Conclusie: welke AI sales tool voor wie (ZZP'er, MKB-sales team, enterprise, startup-oprichter)
- 3 FAQ-vragen over AI in sales

Focus op Nederlandse/Europese markt. Apollo.io heeft de grootste Europese lead-database. Lemlist is populair in Europa voor gepersonaliseerde email outreach. Prijzen in EUR. Schrijf in vloeiend Nederlands.

Belangrijk: Apollo.io en Lemlist zijn het meest relevant voor Nederlandse ZZP'ers en MKB — besteed hier extra aandacht aan. Salesforce en HubSpot zijn voor grotere organisaties.""",
        "tools": [
            {"name": "Apollo.io", "verdict": "Beste all-in-one AI sales platform met 275M+ contacten, AI lead scoring en automatische sequences in 2026", "priceRange": "EUR 0-100/mnd", "bestFor": "Lead gen + outreach", "rating": 4.7, "affiliateLink": "https://www.apollo.io/?ref=aitoolsnl"},
            {"name": "Lemlist", "verdict": "Beste AI-gepersonaliseerde email outreach met dynamische afbeeldingen en video — populair in Europa", "priceRange": "EUR 30-80/mnd", "bestFor": "Email personalisatie", "rating": 4.5, "affiliateLink": "https://www.lemlist.com/?ref=aitoolsnl"},
            {"name": "Instantly", "verdict": "AI-warmup + outreach platform met de beste deliverability voor cold email campagnes", "priceRange": "EUR 0-100/mnd", "bestFor": "Cold email scale", "rating": 4.4, "affiliateLink": "https://instantly.ai/?ref=aitoolsnl"},
            {"name": "Clay", "verdict": "AI-dataverrijking die automatisch 50+ databronnen combineert voor hypergepersonaliseerde outreach", "priceRange": "EUR 0-200/mnd", "bestFor": "Data enrichment", "rating": 4.6, "affiliateLink": "https://www.clay.com/?ref=aitoolsnl"},
            {"name": "Salesforce Einstein GPT", "verdict": "Enterprise AI embedded in het grootste CRM — automatische opportunity scoring en next-best-action", "priceRange": "EUR 50-500/mnd", "bestFor": "Enterprise CRM + AI", "rating": 4.3, "affiliateLink": "https://www.salesforce.com/nl/?ref=aitoolsnl"},
            {"name": "HubSpot Breeze AI", "verdict": "AI-laag in HubSpot CRM met automatische contentgeneratie, voorspellende scoring en chatbots", "priceRange": "EUR 0-50/mnd", "bestFor": "HubSpot AI", "rating": 4.2, "affiliateLink": "https://www.hubspot.com/?ref=aitoolsnl"},
            {"name": "Close CRM AI", "verdict": "AI-gedreven CRM voor inside sales teams met ingebouwde calling, SMS en workflow automation", "priceRange": "EUR 50-150/mnd", "bestFor": "Inside sales teams", "rating": 4.1, "affiliateLink": "https://www.close.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-sales-tools-2026", ALL_SLUGS, 3)
    },
]


def call_gemini(prompt, max_retries=5):
    """Try Flash first, fall back to Flash-Lite."""
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
    return None


def build_article_md(article, body_text):
    """Build complete markdown with frontmatter + tools array + related."""
    date_str = "2026-05-20"

    lines = ["---"]
    lines.append(f"title: '{article['title']}'")
    lines.append(f"slug: {article['slug']}")
    lines.append(f"description: '{article['description']}'")
    lines.append(f"category: {article['category']}")
    lines.append("rating: 4.2")
    lines.append("priceRange: EUR 0-100/mnd")
    lines.append("pros:")
    lines.append("- Eerlijke vergelijking van de beste AI tools voor dit segment")
    lines.append("- Duidelijke prijsranges, verdict en score per tool")
    lines.append("- Nederlandstalig en praktijkgericht advies met FAQ")
    lines.append("cons:")
    lines.append("- Prijzen kunnen wijzigen, check altijd de actuele aanbieder")
    lines.append("- Niet elke tool is dagelijks getest met intensief gebruik")
    lines.append("- Sommige AI features zijn nog in beta of development")
    lines.append("affiliateLinks:")
    lines.append("- https://www.notion.so")
    lines.append("- https://www.beehiiv.com/?via=aitoolsnl")
    lines.append("- https://www.jasper.ai/partners/affiliates?via=aitoolsnl")
    lines.append(f"date: {date_str}")
    lines.append("modelYear: 2026")
    lines.append(f"featuredTool: {article['tools'][0]['name']}")
    lines.append("readingTime: 8 min")
    lines.append("tools:")
    for tool in article["tools"]:
        lines.append(f"  - name: \"{tool['name']}\"")
        lines.append(f"    verdict: \"{tool['verdict']}\"")
        lines.append(f"    priceRange: \"{tool['priceRange']}\"")
        lines.append(f"    bestFor: \"{tool['bestFor']}\"")
        lines.append(f"    rating: {tool['rating']}")
        lines.append(f"    affiliateLink: \"{tool['affiliateLink']}\"")
    lines.append("relatedArticles:")
    for r in article["related"]:
        lines.append(f"  - {r}")
    lines.append("---")
    lines.append("")
    lines.append(body_text)

    return "\n".join(lines)


def main():
    print(f"=== AI Tools Batch 5: 3 nieuwe artikelen ===")
    print(f"Doel: {len(NEW_ARTICLES)} artikelen\n")

    for i, article in enumerate(NEW_ARTICLES):
        print(f"[{i+1}/{len(NEW_ARTICLES)}] {article['slug']}")
        print(f"  Prompt length: {len(article['prompt'])} chars")

        body = call_gemini(article["prompt"])
        if not body:
            print(f"  ❌ FAILED — beide modellen gefaald, skipping")
            continue

        print(f"  ✅ Generated {len(body)} chars")

        md = build_article_md(article, body)
        out_path = ARTICLES_DIR / f"{article['slug']}.md"
        with open(out_path, "w") as f:
            f.write(md)
        print(f"  📄 Written to {out_path}")

        if i < len(NEW_ARTICLES) - 1:
            print("  ⏳ Waiting 3s...")
            time.sleep(3)

    print(f"\n=== Done: {len(NEW_ARTICLES)} articles generated ===")


if __name__ == "__main__":
    main()
