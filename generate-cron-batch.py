#!/usr/bin/env python3
"""Generate 4 new Dutch AI tools articles: logo/branding, CV/sollicitatie, video editing, beauty/skincare.
Uses Gemini 2.5 Flash API. Writes to canonical location under /workspace/dutch-ai-tools."""

import os, json, time, sys, requests, glob as globmod
from datetime import date

# --- Config ---
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
        "slug": "beste-ai-logo-generators-branding-tools-2026",
        "title": "Beste AI Logo Generators & Branding Tools 2026: top 7 vergeleken",
        "description": "AI logo generators en branding tools voor 2026. Vergelijk Looka, Canva AI, LogoAI, Hatchful, Brandmark, Wix Logo Maker en Tailor Brands voor de perfecte bedrijfsidentiteit.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI logo generators en branding tools in 2026. Behandel precies 7 tools: Looka, Canva AI Logo Generator, LogoAI, Hatchful (Shopify), Brandmark, Wix Logo Maker, Tailor Brands.

Structuur:
- Introductie: AI maakt professioneel logo-ontwerp toegankelijk voor iedereen in 2026 — van startende ondernemers tot gevestigde bedrijven die rebranden. Nederland telt tienduizenden nieuwe bedrijven per jaar die een sterk merk nodig hebben.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (zzp'er die snel een logo wil, designer die merkidentiteit bouwt, groeiend bedrijf dat rebrandt)
- 3 FAQ-vragen over AI logo generatoren

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Looka", "verdict": "AI-branding platform dat complete merkidentiteiten genereert — logo, kleurenpalet, lettertypen en visitekaartjes in één flow", "priceRange": "EUR 0-98/eenmalig", "bestFor": "Complete merkidentiteit", "rating": 4.5, "affiliateLink": "https://www.looka.com/?ref=aitoolsnl"},
            {"name": "Canva AI Logo Generator", "verdict": "Canva's AI maakt logo's op basis van stijlvoorkeuren — naadloos geïntegreerd met Canva's volledige design-ecosysteem", "priceRange": "EUR 0-13/mnd", "bestFor": "Gebruiksgemak & integratie", "rating": 4.4, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "LogoAI", "verdict": "AI die je merkstrategie analyseert en een logo genereert dat past bij je branche en doelgroep", "priceRange": "EUR 25-65/eenmalig", "bestFor": "Merkstrategie-gedreven ontwerp", "rating": 4.2, "affiliateLink": "https://logoai.com/?ref=aitoolsnl"},
            {"name": "Hatchful (Shopify)", "verdict": "Gratis AI-logo generator van Shopify — ideaal voor webshopeigenaren die snel een professioneel logo willen", "priceRange": "EUR 0 (gratis)", "bestFor": "Webshop eigenaren", "rating": 4.0, "affiliateLink": "https://www.shopify.com/nl/tools/logo-maker?ref=aitoolsnl"},
            {"name": "Brandmark", "verdict": "AI die unieke, abstracte logo's genereert op basis van kleur- en stijlvoorkeuren — geen templates", "priceRange": "EUR 29-99/eenmalig", "bestFor": "Uniek & abstract ontwerp", "rating": 4.3, "affiliateLink": "https://brandmark.io/?ref=aitoolsnl"},
            {"name": "Wix Logo Maker", "verdict": "AI-logo tool geïntegreerd met Wix — kies stijlen en krijg direct een logo dat past bij je Wix-website", "priceRange": "EUR 0-25/eenmalig", "bestFor": "Wix-gebruikers", "rating": 4.1, "affiliateLink": "https://www.wix.com/logo/maker?ref=aitoolsnl"},
            {"name": "Tailor Brands", "verdict": "Alles-in-één branding platform van logo tot volledige merkidentiteit inclusief social media templates", "priceRange": "EUR 0-13/mnd", "bestFor": "Social media branding", "rating": 4.2, "affiliateLink": "https://www.tailorbrands.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-logo-generators-branding-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-cv-resume-sollicitatie-tools-2026",
        "title": "Beste AI CV & Sollicitatie Tools 2026: top 7 vergeleken",
        "description": "AI tools voor CV's, sollicitatiebrieven en sollicitatievoorbereiding in 2026. Vergelijk Rezi, Kickresume, Enhancv, Teal, Simplify, Careerflow en Resume.io voor de beste kans op die droombaan.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor CV's, sollicitatiebrieven en sollicitatievoorbereiding in 2026. Behandel precies 7 tools: Rezi, Kickresume, Enhancv, Teal, Simplify, Careerflow, Resume.io.

Structuur:
- Introductie: AI transformeert solliciteren in 2026 — van CV-optimalisatie tot persoonlijke sollicitatiebrieven en sollicitatietraining. Voor Nederlandse werkzoekenden een enorme kans om op te vallen.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (starter die eerste CV maakt, professional die carrièreswitch overweegt, executive die sollicitatietraining zoekt)
- 3 FAQ-vragen over AI en solliciteren

Focus op Nederlandse/Europese context. Prijzen in EUR. Noem ATS-systemen die in NL gebruikt worden. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "Rezi", "verdict": "ATS-optimalisatie specialist — Rezi scant je CV tegen duizenden ATS-systemen en past aan voor maximale match", "priceRange": "EUR 0-29/mnd", "bestFor": "ATS-optimalisatie", "rating": 4.6, "affiliateLink": "https://www.rezi.ai/?ref=aitoolsnl"},
            {"name": "Kickresume", "verdict": "Gebruiksvriendelijke AI met professionele templates — schrijft je hele CV en sollicitatiebrief in minuten", "priceRange": "EUR 0-19/mnd", "bestFor": "Snel een professioneel CV", "rating": 4.4, "affiliateLink": "https://www.kickresume.com/?ref=aitoolsnl"},
            {"name": "Enhancv", "verdict": "Visueel sterke, moderne CV templates met AI-suggesties voor inhoud en bewoording", "priceRange": "EUR 0-24/mnd", "bestFor": "Visueel opvallende CV's", "rating": 4.3, "affiliateLink": "https://enhancv.com/?ref=aitoolsnl"},
            {"name": "Teal", "verdict": "Complete AI-sollicitatie-assistent: CV-builder, sollicitatie tracker en sollicitatiebrief generator in één", "priceRange": "EUR 0-29/mnd", "bestFor": "Volledige sollicitatiecyclus", "rating": 4.5, "affiliateLink": "https://www.tealhq.com/?ref=aitoolsnl"},
            {"name": "Simplify", "verdict": "Gratis Chrome-extensie die sollicitatieformulieren automatisch invult en CV's optimaliseert per vacature", "priceRange": "EUR 0 (gratis)", "bestFor": "Snelle sollicitaties", "rating": 4.2, "affiliateLink": "https://www.simplify.jobs/?ref=aitoolsnl"},
            {"name": "Careerflow", "verdict": "AI-sollicitatieplatform met LinkedIn-optimalisatie, netwerktips en intelligent job matching", "priceRange": "EUR 0-49/mnd", "bestFor": "LinkedIn optimalisatie", "rating": 4.3, "affiliateLink": "https://www.careerflow.ai/?ref=aitoolsnl"},
            {"name": "Resume.io", "verdict": "Bewezen CV-builder met AI-templates en begeleiding — duizenden voorbeelden per branche en functie", "priceRange": "EUR 0-25/mnd", "bestFor": "Branche-specifieke CV's", "rating": 4.1, "affiliateLink": "https://resume.io/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-cv-resume-sollicitatie-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-video-editing-bewerking-tools-2026",
        "title": "Beste AI Video Editing & Bewerking Tools 2026: top 7 vergeleken",
        "description": "AI video editing tools voor 2026: CapCut AI, Adobe Premiere Pro AI, DaVinci Resolve AI, RunwayML, Descript, Veed.io en Wondershare Filmora vergeleken voor Nederlandse videomakers.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI video editing en bewerkingstools in 2026. Behandel precies 7 tools: CapCut (ByteDance), Adobe Premiere Pro (AI-features), DaVinci Resolve (AI), RunwayML, Descript, Veed.io, Wondershare Filmora.

Structuur:
- Introductie: AI verandert videobewerking in 2026 — van automatische ondertiteling tot AI-gebaseerde kleurcorrectie, objectverwijdering en tekst-naar-video. Voor Nederlandse content creators, marketeers en filmmakers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (social media creator, professionele editor, marketing team)
- 3 FAQ-vragen over AI video editing

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "CapCut (ByteDance)", "verdict": "Gratis AI-video editor met krachtige automatische ondertiteling, object removal en motion tracking — extreem populair bij TikTok/Reels creators", "priceRange": "EUR 0-8/mnd", "bestFor": "Social media creators", "rating": 4.6, "affiliateLink": "https://www.capcut.com/?ref=aitoolsnl"},
            {"name": "Adobe Premiere Pro", "verdict": "Professionele standaard met AI-features zoals auto-reframe, scene edit detection, speech-to-text en AI-kleurcorrectie", "priceRange": "EUR 24/mnd", "bestFor": "Professionele filmmakers", "rating": 4.7, "affiliateLink": "https://www.adobe.com/nl/products/premiere.html?ref=aitoolsnl"},
            {"name": "DaVinci Resolve", "verdict": "Gratis professionele editor met AI-gestuurde kleurcorrectie, gezichtsherkenning en noise reduction — industrie-standaard voor color grading", "priceRange": "EUR 0-321/eenmalig", "bestFor": "Color grading & high-end productie", "rating": 4.8, "affiliateLink": "https://www.blackmagicdesign.com/products/davinciresolve?ref=aitoolsnl"},
            {"name": "RunwayML", "verdict": "Generatieve AI voor video: object removal, background replacement, inpainting, text-to-video en green screen zonder chroma key", "priceRange": "EUR 12-76/mnd", "bestFor": "Generatieve AI videobewerking", "rating": 4.5, "affiliateLink": "https://runwayml.com/?ref=aitoolsnl"},
            {"name": "Descript", "verdict": "Bewerk video door tekst aan te passen — AI-editor die audio, transcript en video synchroniseert, ideaal voor podcasts en screencasts", "priceRange": "EUR 0-33/mnd", "bestFor": "Podcasts & screencasts", "rating": 4.4, "affiliateLink": "https://www.descript.com/?ref=aitoolsnl"},
            {"name": "Veed.io", "verdict": "Browsergebaseerde AI-video editor met automatische ondertiteling, vertaling en samenvatting — geen installatie nodig", "priceRange": "EUR 0-30/mnd", "bestFor": "Snelle browser editing", "rating": 4.3, "affiliateLink": "https://www.veed.io/?ref=aitoolsnl"},
            {"name": "Wondershare Filmora", "verdict": "Toegankelijke AI-video editor met ingebouwde AI-copilot, AI motion tracking, AI portrait en AI audio denoise", "priceRange": "EUR 40-80/jaar", "bestFor": "Hobbyisten & semi-professionals", "rating": 4.2, "affiliateLink": "https://filmora.wondershare.nl/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-video-editing-bewerking-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-schoonheid-skincare-beauty-tools-2026",
        "title": "Beste AI Schoonheid & Skincare Tools 2026: top 6 vergeleken",
        "description": "AI tools voor schoonheid, huidverzorging en skincare in 2026. Vergelijk SkinGPT, L'Oréal Skin Genius, Perfect Corp, YouCam Makeup, Neutrogena Skin360 en ChatGPT voor huidanalyse en beauty advies.",
        "category": "technologie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor schoonheid, huidverzorging en skincare in 2026. Behandel precies 6 tools: SkinGPT, L'Oréal Skin Genius, Perfect Corp (AI Beauty), YouCam Makeup, Neutrogena Skin360, ChatGPT (als skincare assistent).

Structuur:
- Introductie: AI transformeert persoonlijke verzorging in 2026 — van huidanalyse met je smartphone tot gepersonaliseerde skincare routines en virtuele make-up try-ons. Voor Nederlandse beauty-liefhebbers.
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 6 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor welk type gebruiker (skincare beginner, beauty professional, iemand met huidproblemen)
- 3 FAQ-vragen over AI en beauty

Focus op Nederlandse/Europese context. Prijzen in EUR. Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "SkinGPT", "verdict": "AI huidanalyse tool die foto's analyseert, huidproblemen identificeert en gepersonaliseerde skincare aanbeveelt", "priceRange": "EUR 0-15/mnd", "bestFor": "Huidanalyse & diagnose", "rating": 4.4, "affiliateLink": "https://www.skingpt.com/?ref=aitoolsnl"},
            {"name": "L'Oréal Skin Genius", "verdict": "AI-powered huidanalyse van L'Oréal — scan je huid met je smartphone voor een persoonlijke huidscore en productadvies", "priceRange": "EUR 0 (gratis)", "bestFor": "Gratis professionele huidscan", "rating": 4.5, "affiliateLink": "https://www.loreal.com/nl/skin-genius/?ref=aitoolsnl"},
            {"name": "Perfect Corp (AI Beauty)", "verdict": "Professionele AI-beauty suite voor virtuele try-ons, huidanalyse en gepersonaliseerde beauty aanbevelingen — gebruikt door grote merken", "priceRange": "EUR 0 (consumer) / custom (business)", "bestFor": "Virtuele make-up try-on", "rating": 4.6, "affiliateLink": "https://www.perfectcorp.com/?ref=aitoolsnl"},
            {"name": "YouCam Makeup", "verdict": "Populairste virtuele make-up app met AI-gezichtsherkenning — probeer duizenden producten virtueel, inclusief huidanalyse", "priceRange": "EUR 0-10/mnd", "bestFor": "Virtuele make-up & tutorials", "rating": 4.5, "affiliateLink": "https://www.youcam.com/?ref=aitoolsnl"},
            {"name": "Neutrogena Skin360", "verdict": "AI-skin scanner van Neutrogena die poriën, rimpels, pigmentatie en droogheid meet — met gepersonaliseerde skincare tips", "priceRange": "EUR 0 (gratis)", "bestFor": "Wetenschappelijke huidanalyse", "rating": 4.3, "affiliateLink": "https://www.neutrogena.com/skin360/?ref=aitoolsnl"},
            {"name": "ChatGPT (Skincare Assistant)", "verdict": "Gratis AI-assistent voor skincare vragen, ingrediëntenanalyse, routine-optimalisatie en productvergelijking op basis van jouw huidtype", "priceRange": "EUR 0-22/mnd", "bestFor": "Skincare kennis & advies", "rating": 4.2, "affiliateLink": "https://chat.openai.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-schoonheid-skincare-beauty-tools-2026", ALL_SLUGS, 3)
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