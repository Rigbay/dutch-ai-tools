#!/usr/bin/env python3
import os, json, time, sys, requests, yaml
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BASE_URL_FLASH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/tmp/dutch-ai-tools/src/content/articles"

ALL_SLUGS = [
    "beste-ai-chatbots-2026", "beste-ai-image-generators-2026",
    "beste-ai-video-tools-2026", "chatgpt-vs-gemini-vs-claude-nederlands-2026",
    "beste-ai-tools-programmeren-2026", "beste-ai-muziek-audio-tools-2026",
    "beste-ai-voice-cloning-voice-over-2026",
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

NEW_ARTICLES = [
    {
        "slug": "midjourney-vs-dall-e-3-vs-stable-diffusion-2026",
        "title": "Midjourney vs DALL-E 3 vs Stable Diffusion 2026: welke AI beeldgenerator is de beste?",
        "description": "Een diepgaande vergelijking van Midjourney, DALL-E 3 (ChatGPT) en Stable Diffusion in 2026. Welke tool levert de mooiste AI beelden voor jouw project?",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden waarin Midjourney, DALL-E 3 en Stable Diffusion worden vergeleken in 2026. Behandel precies 7 tools/platforms: Midjourney v7, DALL-E 3 (OpenAI), Stable Diffusion XL/3, Adobe Firefly, Canva Magic Media, Leonardo.ai en Google Imagen 3.

Structuur:
- Introductie: De staat van AI beeldgeneratie in 2026
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor wie (fotografen, marketeers, hobbyisten)
- 3 FAQ-vragen over AI beeldgeneratie

Schrijf in vloeiend, professioneel Nederlands. Focus op beeldkwaliteit, gebruiksgemak en commerciële inzetbaarheid.""",
        "tools": [
            {"name": "Midjourney v7", "verdict": "Onbetwiste leider in artistieke kwaliteit en fotorealisme", "priceRange": "EUR 10-60/mnd", "bestFor": "Hoogste kwaliteit", "rating": 4.9, "affiliateLink": "https://www.midjourney.com/?ref=aitoolsnl"},
            {"name": "DALL-E 3", "verdict": "Beste begrijp van complexe prompts dankzij ChatGPT integratie", "priceRange": "EUR 0-25/mnd", "bestFor": "Gebruiksgemak", "rating": 4.6, "affiliateLink": "https://www.notion.so"},
            {"name": "Stable Diffusion 3", "verdict": "Maximale controle en open-source mogelijkheden voor gevorderden", "priceRange": "EUR 0-50/mnd", "bestFor": "Controle & Open Source", "rating": 4.7, "affiliateLink": "https://stability.ai/?ref=aitoolsnl"},
            {"name": "Adobe Firefly", "verdict": "Commercieel veilig en perfect geïntegreerd in Photoshop", "priceRange": "EUR 5-25/mnd", "bestFor": "Commercieel gebruik", "rating": 4.5, "affiliateLink": "https://www.adobe.com/?ref=aitoolsnl"},
            {"name": "Leonardo.ai", "verdict": "Geweldige webinterface met veel finetuning opties", "priceRange": "EUR 0-30/mnd", "bestFor": "Finetuning", "rating": 4.4, "affiliateLink": "https://leonardo.ai/?ref=aitoolsnl"},
            {"name": "Canva Magic Media", "verdict": "Simpele tool direct in je design workflow", "priceRange": "EUR 0-15/mnd", "bestFor": "Snel resultaat", "rating": 4.1, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "Google Imagen 3", "verdict": "Sterke all-rounder met focus op realisme en tekst in beeld", "priceRange": "EUR 0/mnd", "bestFor": "Tekst in beeld", "rating": 4.3, "affiliateLink": "https://deepmind.google/technologies/imagen-3/?ref=aitoolsnl"},
        ],
        "related": pick_related("midjourney-vs-dall-e-3-vs-stable-diffusion-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "elevenlabs-vs-murf-ai-vs-play-ht-2026",
        "title": "ElevenLabs vs Murf AI vs Play.ht 2026: de beste AI stemmen vergeleken",
        "description": "Welke AI voice generator is de beste in 2026? Vergelijk ElevenLabs, Murf AI en Play.ht voor voice-overs, audioboeken en video content in het Nederlands.",
        "category": "creatie",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI voice generators in 2026. Behandel precies 7 tools: ElevenLabs, Murf AI, Play.ht, Lovo.ai, WellSaid Labs, Speechify en OpenAI Voice.

Structuur:
- Introductie: De opkomst van niet-van-echt-te-onderscheiden AI stemmen in 2026
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor podcasters, videomakers en e-learning
- 3 FAQ-vragen over AI stemmen en voice cloning

Focus op de kwaliteit van de Nederlandse stemmen (natuurlijkheid, intonatie). Schrijf in vloeiend Nederlands.""",
        "tools": [
            {"name": "ElevenLabs", "verdict": "Meest natuurlijke stemmen en beste voice cloning op de markt", "priceRange": "EUR 0-100/mnd", "bestFor": "Natuurlijkheid", "rating": 4.9, "affiliateLink": "https://elevenlabs.io/?from=aitoolsnl"},
            {"name": "Murf AI", "verdict": "Uitstekend platform voor professionele voice-overs met veel controle", "priceRange": "EUR 0-60/mnd", "bestFor": "Professionele voice-over", "rating": 4.6, "affiliateLink": "https://murf.ai/?lmref=aitoolsnl"},
            {"name": "Play.ht", "verdict": "Enorm aanbod aan stemmen en goede integraties voor websites", "priceRange": "EUR 0-90/mnd", "bestFor": "Stemmen aanbod", "rating": 4.5, "affiliateLink": "https://play.ht/?fp_ref=aitoolsnl"},
            {"name": "Lovo.ai", "verdict": "Goede mix van stemmen en video-editing features", "priceRange": "EUR 0-50/mnd", "bestFor": "Content creators", "rating": 4.3, "affiliateLink": "https://lovo.ai/?ref=aitoolsnl"},
            {"name": "WellSaid Labs", "verdict": "Focus op high-end corporate e-learning stemmen", "priceRange": "EUR 40-200/mnd", "bestFor": "E-learning", "rating": 4.4, "affiliateLink": "https://wellsaidlabs.com/?ref=aitoolsnl"},
            {"name": "Speechify", "verdict": "Beste voor tekst-naar-spraak en audioboeken met bekende stemmen", "priceRange": "EUR 0-30/mnd", "bestFor": "Audioboeken", "rating": 4.5, "affiliateLink": "https://speechify.com/?ref=aitoolsnl"},
            {"name": "OpenAI Voice", "verdict": "Indrukwekkende conversatie-AI stemmen direct in ChatGPT", "priceRange": "EUR 0-25/mnd", "bestFor": "Interactie", "rating": 4.7, "affiliateLink": "https://www.notion.so"},
        ],
        "related": pick_related("elevenlabs-vs-murf-ai-vs-play-ht-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "github-copilot-vs-cursor-vs-codeium-2026",
        "title": "GitHub Copilot vs Cursor vs Codeium 2026: de beste AI code editors",
        "description": "Vergelijking van de beste AI tools voor programmeurs in 2026. Welke AI assistent helpt je sneller coderen: GitHub Copilot, Cursor of Codeium?",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI assistenten voor software development in 2026. Behandel precies 7 tools: GitHub Copilot, Cursor, Codeium, Tabnine, Replit Ghostwriter, Amazon Q Developer en Sourcegraph Cody.

Structuur:
- Introductie: Hoe AI-pair programming de standaard is geworden in 2026
- Per tool een ## kop met: beschrijving, prijsrange (EUR), beste use case, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs, beste-voor, score (1-5)
- Conclusie: welke tool voor solo-devs vs enterprise teams
- 3 FAQ-vragen over AI in development (security, privacy)

Schrijf in vloeiend Nederlands, gebruik technische termen waar nodig maar houd het toegankelijk.""",
        "tools": [
            {"name": "GitHub Copilot", "verdict": "De marktleider met de breedste ondersteuning en integratie", "priceRange": "EUR 10-40/mnd", "bestFor": "Ecosysteem", "rating": 4.7, "affiliateLink": "https://github.com/features/copilot?ref=aitoolsnl"},
            {"name": "Cursor", "verdict": "De beste AI-native editor die code begrijpt als geen ander", "priceRange": "EUR 0-20/mnd", "bestFor": "AI-Native Ervaring", "rating": 4.9, "affiliateLink": "https://cursor.sh/?ref=aitoolsnl"},
            {"name": "Codeium", "verdict": "Beste gratis alternatief met krachtige features voor individuen", "priceRange": "EUR 0-15/mnd", "bestFor": "Prijs/Kwaliteit", "rating": 4.6, "affiliateLink": "https://codeium.com/?ref=aitoolsnl"},
            {"name": "Tabnine", "verdict": "Focus op privacy en lokale modellen voor enterprise", "priceRange": "EUR 0-15/mnd", "bestFor": "Privacy & Enterprise", "rating": 4.4, "affiliateLink": "https://www.tabnine.com/?ref=aitoolsnl"},
            {"name": "Replit Ghostwriter", "verdict": "Perfecte AI assistent voor cloud-native development", "priceRange": "EUR 0-20/mnd", "bestFor": "Cloud-Native", "rating": 4.3, "affiliateLink": "https://replit.com/?ref=aitoolsnl"},
            {"name": "Amazon Q Developer", "verdict": "Beste keuze voor developers die diep in het AWS ecosysteem zitten", "priceRange": "EUR 0-20/mnd", "bestFor": "AWS Integratie", "rating": 4.2, "affiliateLink": "https://aws.amazon.com/q/developer/?ref=aitoolsnl"},
            {"name": "Sourcegraph Cody", "verdict": "Uitblinkend in het begrijpen van je gehele codebase", "priceRange": "EUR 0-10/mnd", "bestFor": "Context Begrip", "rating": 4.5, "affiliateLink": "https://about.sourcegraph.com/cody?ref=aitoolsnl"},
        ],
        "related": pick_related("github-copilot-vs-cursor-vs-codeium-2026", ALL_SLUGS, 3)
    },
]

def call_gemini(prompt):
    url = f"{BASE_URL_FLASH}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    try:
        resp = requests.post(url, json=payload, timeout=180)
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Exception: {e}")
    return None

def build_article(defn, body_text):
    data = {
        "title": defn["title"],
        "slug": defn["slug"],
        "description": defn["description"],
        "category": defn["category"],
        "rating": round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1),
        "priceRange": "EUR 0-100/mnd",
        "pros": ["Vergelijking van top-tier tools", "Actuele 2026 marktdata", "Focus op Nederlandse context"],
        "cons": ["Prijzen onder voorbehoud", "Sommige features in beta"],
        "affiliateLinks": ["https://www.notion.so"],
        "date": date.today(),
        "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"],
        "readingTime": "8 min",
        "tools": defn["tools"],
        "related": defn["related"],
        "draft": False,
        "faq": [
            {"q": "Wat is de beste tool?", "a": f"Voor de meeste gebruikers is {defn['tools'][0]['name']} de beste keuze."},
            {"q": "Is er een gratis versie?", "a": "De meeste tools bieden een beperkte gratis versie aan."},
            {"q": "Werkt het in het Nederlands?", "a": "Ja, alle besproken tools ondersteunen de Nederlandse taal goed."}
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"

def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    for defn in NEW_ARTICLES:
        print(f"Generating {defn['slug']}...")
        body = call_gemini(defn["prompt"])
        if body:
            full = build_article(defn, body)
            with open(os.path.join(ARTICLES_DIR, f"{defn['slug']}.md"), "w") as f:
                f.write(full)
            print(f"Success!")
        else:
            print(f"Failed to generate {defn['slug']}")
        time.sleep(2)

if __name__ == "__main__":
    main()
