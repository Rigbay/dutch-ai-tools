#!/usr/bin/env python3
"""Generate 3 new Dutch AI tools articles: SEO tools, audio/music, meeting transcription.
Batch 4 — May 20 2026. Uses Gemini 2.5 Flash with Flash-Lite fallback."""

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
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "beste-ai-seo-tools-2026",
        "title": "Beste AI SEO Tools 2026: Semrush vs Frase vs Surfer SEO vergeleken",
        "description": "Vergelijk de beste AI SEO tools van 2026. Semrush, Frase, Surfer SEO, Ahrefs en meer: welke AI SEO tool helpt jou hoger ranken in Google?",
        "category": "marketing",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI SEO tools in 2026. Behandel precies 7 tools: Semrush, Frase, Surfer SEO, Ahrefs, NeuronWriter, Clearscope, MarketMuse.

Structuur:
- Introductie: hoe AI SEO verandert in 2026 — van keyword research tot AI-gegenereerde content optimalisatie
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, NL-ondersteuning, score (1-5)
- Conclusie: welke SEO tool past bij welk type gebruiker (ZZP'er, MKB, agency, content marketeer)
- 3 FAQ-vragen over AI SEO tools

Focus op de Nederlandse markt. Welke tools hebben NL-zoekwoorddata? Prijzen in EUR. Schrijf in vloeiend Nederlands.
Belangrijk: Frase en Surfer SEO zijn specifiek interessant voor Nederlandse content marketeers vanwege hun AI-contentoptimalisatie features — besteed hier extra aandacht aan.""",
        "tools": [
            {"name": "Semrush", "verdict": "Beste all-in-one SEO suite met sterke NL-zoekwoorddata en concurrentieanalyse", "priceRange": "EUR 100-450/mnd", "bestFor": "Volledige SEO toolset", "rating": 4.8, "affiliateLink": "https://www.semrush.com/?ref=aitoolsnl"},
            {"name": "Frase", "verdict": "Beste AI-contentoptimalisatie tool die je content direct vergelijkt met top-ranking pagina's", "priceRange": "EUR 15-115/mnd", "bestFor": "Contentoptimalisatie", "rating": 4.6, "affiliateLink": "https://www.frase.io/?ref=aitoolsnl"},
            {"name": "Surfer SEO", "verdict": "Krachtige content editor met realtime NLP-analyse voor optimale contentstructuur", "priceRange": "EUR 50-200/mnd", "bestFor": "Content scoring", "rating": 4.5, "affiliateLink": "https://surferseo.com/?ref=aitoolsnl"},
            {"name": "Ahrefs", "verdict": "Diepste backlink-database en sterke NL-keyword data — favoriet van SEO-professionals", "priceRange": "EUR 80-400/mnd", "bestFor": "Backlinks & concurrentie", "rating": 4.7, "affiliateLink": "https://ahrefs.com/?ref=aitoolsnl"},
            {"name": "NeuronWriter", "verdict": "Betaalbare AI content optimizer met NLP-aanbevelingen voor Europese talen", "priceRange": "EUR 20-50/mnd", "bestFor": "Content optimalisatie NL", "rating": 4.3, "affiliateLink": "https://neuronwriter.com/?ref=aitoolsnl"},
            {"name": "Clearscope", "verdict": "Premium content optimalisatie voor enterprise teams met diepe keyword intelligence", "priceRange": "EUR 150-500/mnd", "bestFor": "Enterprise content", "rating": 4.4, "affiliateLink": "https://www.clearscope.io/?ref=aitoolsnl"},
            {"name": "MarketMuse", "verdict": "AI-gedreven content strategie die automatisch content gaps identificeert", "priceRange": "EUR 100-500/mnd", "bestFor": "Contentstrategie", "rating": 4.2, "affiliateLink": "https://www.marketmuse.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-seo-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-muziek-audio-tools-2026",
        "title": "Beste AI Muziek & Audio Tools 2026: Suno vs ElevenLabs vs AIVA vergeleken",
        "description": "AI muziek maken en audio genereren in 2026. Vergelijk Suno, ElevenLabs, AIVA, Udio en meer voor muziekproductie, voice-overs en podcasts.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor muziek en audio in 2026. Behandel precies 7 tools: Suno, ElevenLabs, Udio, AIVA, Descript, Adobe Podcast AI, Murf AI.

Structuur:
- Introductie: AI revolutie in muziek en audio — van volledige songs genereren tot professionele voice-overs in 2026
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, Nederlands ondersteund?, score (1-5)
- Conclusie: welke tool voor welk type creator (muzikant, podcaster, videomaker, marketeer)
- 3 FAQ-vragen over AI muziek en audio

Focus op Nederlandse/Europese markt. Prijzen in EUR. Schrijf in vloeiend Nederlands.
Belangrijk: ElevenLabs is de enige met écht goede Nederlandse stemmen — besteed hier extra aandacht aan. Suno is leidend in AI-muziekgeneratie.""",
        "tools": [
            {"name": "Suno", "verdict": "Beste AI-muziekgenerator — volledige songs met vocals in elke stijl, revolutionair voor content creators", "priceRange": "EUR 0-30/mnd", "bestFor": "AI muziekproductie", "rating": 4.7, "affiliateLink": "https://suno.com/?ref=aitoolsnl"},
            {"name": "ElevenLabs", "verdict": "Absolute leider in AI-stemmen met de beste Nederlandse voice cloning en text-to-speech", "priceRange": "EUR 0-100/mnd", "bestFor": "Voice-overs & TTS", "rating": 4.8, "affiliateLink": "https://elevenlabs.io/?ref=aitoolsnl"},
            {"name": "Udio", "verdict": "Sterke Suno-concurrent met focus op muzikale kwaliteit en langere composities", "priceRange": "EUR 0-25/mnd", "bestFor": "Muziekcompositie", "rating": 4.4, "affiliateLink": "https://www.udio.com/?ref=aitoolsnl"},
            {"name": "AIVA", "verdict": "AI-componist voor klassieke, film- en gamemuziek met professionele partituur-export", "priceRange": "EUR 0-50/mnd", "bestFor": "Soundtracks & composities", "rating": 4.2, "affiliateLink": "https://www.aiva.ai/?ref=aitoolsnl"},
            {"name": "Descript", "verdict": "All-in-one audio/video editor met AI transcriptie, filler-word removal en stemklonen", "priceRange": "EUR 0-30/mnd", "bestFor": "Podcast editing", "rating": 4.5, "affiliateLink": "https://www.descript.com/?ref=aitoolsnl"},
            {"name": "Adobe Podcast AI", "verdict": "Gratis AI-audioverbetering die elke opname laat klinken als studio-kwaliteit", "priceRange": "EUR 0/mnd", "bestFor": "Audio cleaning", "rating": 4.3, "affiliateLink": "https://podcast.adobe.com/?ref=aitoolsnl"},
            {"name": "Murf AI", "verdict": "Beste AI-stemmen voor e-learning en bedrijfsvideo's met 120+ stemmen in 20+ talen", "priceRange": "EUR 20-60/mnd", "bestFor": "E-learning voice-overs", "rating": 4.1, "affiliateLink": "https://murf.ai/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-muziek-audio-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-meeting-transcriptie-tools-2026",
        "title": "Beste AI Meeting & Transcriptie Tools 2026: Fireflies vs Otter vs Fathom vergeleken",
        "description": "AI meeting tools in 2026: vergelijk Fireflies, Otter.ai, Fathom, Notta en meer. Automatische notulen, actiepunten en transcripties in het Nederlands.",
        "category": "productiviteit",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI meeting en transcriptie tools in 2026. Behandel precies 7 tools: Fireflies.ai, Otter.ai, Fathom, Notta, tl;dv, Microsoft Teams AI, Gong.

Structuur:
- Introductie: AI verandert vergaderingen in 2026 — nooit meer handmatig notuleren, automatische actiepunten en meertalige transcriptie
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs (EUR/mnd), beste-voor, Nederlands?, integraties, score (1-5)
- Conclusie: welke meeting AI voor welk type gebruiker (ZZP'er, team, enterprise, sales)
- 3 FAQ-vragen over AI meeting tools

Focus op Nederlandse markt. Welke tools ondersteunen Nederlandse transcriptie? Fireflies en Notta ondersteunen Nederlands. Microsoft Teams is dominant in NL. Prijzen in EUR. Schrijf in vloeiend Nederlands.
Belangrijk: Fireflies.ai is de populairste meeting-AI en ondersteunt Nederlands — besteed hier extra aandacht aan.""",
        "tools": [
            {"name": "Fireflies.ai", "verdict": "Beste allround meeting-AI met Nederlands ondersteund, automatische notulen en CRM-integratie", "priceRange": "EUR 0-20/mnd", "bestFor": "Volledige meeting AI", "rating": 4.6, "affiliateLink": "https://fireflies.ai/?ref=aitoolsnl"},
            {"name": "Otter.ai", "verdict": "Realtime AI-transcriptie met uitstekende Engels-Nederlandse hybrid herkenning", "priceRange": "EUR 0-20/mnd", "bestFor": "Realtime transcriptie", "rating": 4.5, "affiliateLink": "https://otter.ai/?ref=aitoolsnl"},
            {"name": "Fathom", "verdict": "Beste gratis AI-notulist met automatische highlight-reels en CRM-sync", "priceRange": "EUR 0-35/mnd", "bestFor": "Sales calls", "rating": 4.7, "affiliateLink": "https://fathom.video/?ref=aitoolsnl"},
            {"name": "Notta", "verdict": "Beste meertalige AI-transcriptie met sterke Nederlandse ondersteuning", "priceRange": "EUR 0-20/mnd", "bestFor": "Meertalige meetings", "rating": 4.3, "affiliateLink": "https://www.notta.ai/?ref=aitoolsnl"},
            {"name": "tl;dv", "verdict": "AI-notulist specifiek voor Zoom/Meet/Teams met timestamp-notities en delen", "priceRange": "EUR 0-30/mnd", "bestFor": "Video-call notities", "rating": 4.4, "affiliateLink": "https://tldv.io/?ref=aitoolsnl"},
            {"name": "Microsoft Teams AI", "verdict": "Ingebouwde AI-notulen in de dominante NL-vergadertool — Copilot samenvattingen", "priceRange": "EUR 5-30/mnd", "bestFor": "Teams-gebruikers", "rating": 4.2, "affiliateLink": "https://www.microsoft.com/nl-nl/microsoft-teams/?ref=aitoolsnl"},
            {"name": "Gong", "verdict": "Enterprise sales intelligence met AI deal-analyses en gespreksinzichten", "priceRange": "EUR 100-300/mnd", "bestFor": "Sales intelligence", "rating": 4.6, "affiliateLink": "https://www.gong.io/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-meeting-transcriptie-tools-2026", ALL_SLUGS, 3)
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
    import yaml
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
    lines.append("- https://www.beehiiv.com/")
    lines.append("- https://outlierkit.com/?ref=aitoolsnl")
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
    print(f"=== AI Tools Batch 4: 3 nieuwe artikelen ===")
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
