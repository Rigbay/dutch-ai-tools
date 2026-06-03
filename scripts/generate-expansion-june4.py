#!/usr/bin/env python3
"""
Generate 5 new AI tools comparison articles using Gemini API.
Targets gaps in the dutch-ai-tools site — marketing, development, technologie.
Run: python3 scripts/generate-expansion-june4.py
"""
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = SITE_ROOT / "src" / "content" / "articles"

API_KEY_FILE = os.path.expanduser("~/.hermes/private/gemini-api-key")
try:
    GEMINI_API_KEY = open(API_KEY_FILE).read().strip()
except Exception as e:
    print(f"ERROR: Cannot read API key: {e}", file=sys.stderr)
    sys.exit(1)

TOPICS = [
    {
        "slug": "beste-ai-tools-marketing-automation-2026",
        "category": "marketing",
        "title_prefix": "Beste AI Tools voor Marketing Automation 2026",
        "featured": "HubSpot AI",
        "tools": [
            {"name": "HubSpot AI", "price": "EUR 50-4500/mnd", "best_for": "Allround marketing automation & CRM", "rating": 4.7, "verdict": "Meest complete AI-platform voor marketing automation met ingebouwde CRM"},
            {"name": "ActiveCampaign AI", "price": "EUR 29-149/mnd", "best_for": "E-mail automation & klantsegmentatie", "rating": 4.6, "verdict": "Beste voor e-mail automations met AI-gedreven segmentatie"},
            {"name": "Klaviyo AI", "price": "EUR 20-2000/mnd", "best_for": "E-commerce marketing automation", "rating": 4.5, "verdict": "Toonaangevend voor e-commerce met AI-productaanbevelingen"},
            {"name": "Brevo (Sendinblue) AI", "price": "EUR 0-99/mnd", "best_for": "Betaalbare automation voor MKB", "rating": 4.3, "verdict": "Uitstekende prijs-kwaliteit voor MKB met AI-planningsoptimalisatie"},
            {"name": "MoEngage AI", "price": "EUR 100-1000/mnd", "best_for": "Mobiele & omnichannel automations", "rating": 4.4, "verdict": "Sterk in mobiele customer journeys en AI-gedreven personalisatie"},
            {"name": "GetResponse AI", "price": "EUR 15-100/mnd", "best_for": "Alles-in-één voor kleine bedrijven", "rating": 4.2, "verdict": "Complete marketing suite met AI-webinar- en landingpagebuilder"},
            {"name": "Salesforce Marketing Cloud Engagement", "price": "EUR 500-5000/mnd", "best_for": "Enterprise omnichannel automation", "rating": 4.6, "verdict": "Enterprise-oplossing met krachtige AI voor personalisatie op schaal"},
        ],
        "affiliate_link": "https://www.hubspot.com/products/marketing?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-videomarketing-2026",
        "category": "marketing",
        "title_prefix": "Beste AI Tools voor Videomarketing 2026",
        "featured": "Synthesia AI",
        "tools": [
            {"name": "Synthesia AI", "price": "EUR 29-300/mnd", "best_for": "AI-videoproductie met avatars", "rating": 4.7, "verdict": "Beste voor AI-avatars en snelle videoproductie zonder camera"},
            {"name": "Descript AI", "price": "EUR 24-84/mnd", "best_for": "Video-editing & transcriptie", "rating": 4.6, "verdict": "Krachtigste AI-video-editor met tekstgebaseerde bewerking en schermopnames"},
            {"name": "Runway ML Gen-3", "price": "EUR 15-95/mnd", "best_for": "AI-videogeneratie & -bewerking", "rating": 4.5, "verdict": "Beste voor AI-videogeneratie en geavanceerde visuele effecten"},
            {"name": "HeyGen AI", "price": "EUR 24-240/mnd", "best_for": "AI-presentatoren & vertaling", "rating": 4.4, "verdict": "Ideaal voor meertalige video's met AI-presentatoren en lipsync"},
            {"name": "Opus Clip AI", "price": "EUR 19-99/mnd", "best_for": "Short-form video uit lange content", "rating": 4.3, "verdict": "Beste voor het automatisch knippen van korte clips voor sociale media"},
            {"name": "Kapwing AI", "price": "Gratis-50/mnd", "best_for": "Snelle videobewerking & samenwerking", "rating": 4.2, "verdict": "Toegankelijke AI-video editor voor teams met automatische ondertiteling"},
            {"name": "Veed.io AI", "price": "EUR 12-40/mnd", "best_for": "Social media video creation", "rating": 4.1, "verdict": "Gebruiksvriendelijke AI voor sociale media video's en ondertiteling"},
        ],
        "affiliate_link": "https://www.synthesia.io/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-mlops-platform-engineering-2026",
        "category": "development",
        "title_prefix": "Beste AI Tools voor MLOps & Platform Engineering 2026",
        "featured": "MLflow AI",
        "tools": [
            {"name": "MLflow", "price": "Open source (gratis)", "best_for": "ML-experiment tracking & model management", "rating": 4.6, "verdict": "Meest gebruikte open-source MLOps-platform voor experiment tracking en modelregistratie"},
            {"name": "Kubeflow AI", "price": "Open source (gratis)", "best_for": "ML-pipelines op Kubernetes", "rating": 4.4, "verdict": "Beste voor ML-pipelines op Kubernetes met schaalbare training en serving"},
            {"name": "Weights & Biases", "price": "Gratis-500/mnd", "best_for": "Experiment tracking & hyperparameter tuning", "rating": 4.7, "verdict": "Toonaangevend voor AI-experiment tracking en samenwerking tussen data scientists"},
            {"name": "Dagster AI", "price": "Open source (gratis)", "best_for": "Data pipeline orchestration", "rating": 4.5, "verdict": "Moderne data orchestrator met AI-ondersteuning voor pipeline beheer"},
            {"name": "Neptune AI", "price": "Gratis-200/mnd", "best_for": "ML-metadata management & monitoring", "rating": 4.3, "verdict": "Sterk in ML-metadata management en model monitoring voor teams"},
            {"name": "Valohai AI", "price": "EUR 100-1000/mnd", "best_for": "Enterprise MLOps & GPU-beheer", "rating": 4.2, "verdict": "Enterprise MLOps met GPU-orchestratie en reproduceerbare ML-pipelines"},
            {"name": "Azure Machine Learning", "price": "EUR 10-500/mnd", "best_for": "End-to-end MLOps in Microsoft-cloud", "rating": 4.5, "verdict": "Volledig MLOps-platform in Azure met geautomatiseerde ML-pipelines en model deployment"},
        ],
        "affiliate_link": "https://mlflow.org/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-prompt-engineering-2026",
        "category": "technologie",
        "title_prefix": "Beste AI Tools voor Prompt Engineering 2026",
        "featured": "Anthropic Console",
        "tools": [
            {"name": "Anthropic Console", "price": "Gratis", "best_for": "Prompt testing & evaluation voor Claude", "rating": 4.7, "verdict": "Beste voor het testen en verbeteren van prompts met real-time evaluaties op Claude-modellen"},
            {"name": "OpenAI Playground", "price": "Gratis (tokenkosten)", "best_for": "GPT prompt prototyping & parameter tuning", "rating": 4.6, "verdict": "Meest toegankelijke playground voor GPT-prompt prototyping met temperatuur- en token-instellingen"},
            {"name": "LangSmith", "price": "Gratis-99/mnd", "best_for": "Prompt tracing & LLM observability", "rating": 4.5, "verdict": "Krachtigste tool voor LLM observability, prompt tracing en evaluatie van chain-outputs"},
            {"name": "PromptPerfect", "price": "EUR 20-100/mnd", "best_for": "Automatische prompt optimalisatie", "rating": 4.3, "verdict": "Beste voor het automatisch optimaliseren van prompts voor verschillende LLM-modellen"},
            {"name": "Dust.tt", "price": "Gratis-50/mnd", "best_for": "Prompt management & versioning", "rating": 4.2, "verdict": "Sterk in prompt versioning en samenwerking voor teams die met LLM's werken"},
            {"name": "Portkey AI", "price": "Gratis-200/mnd", "best_for": "LLM gateway & prompt routing", "rating": 4.4, "verdict": "LLM-gateway met prompt routing en fallback voor meerdere modelproviders"},
            {"name": "Agenta AI", "price": "Open source (gratis)", "best_for": "Prompt versioning & A/B testing", "rating": 4.1, "verdict": "Open-source platform voor prompt versioning en A/B-testen van LLM-prompts"},
        ],
        "affiliate_link": "https://console.anthropic.com/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-web-analytics-conversie-2026",
        "category": "marketing",
        "title_prefix": "Beste AI Tools voor Web Analytics & Conversieoptimalisatie 2026",
        "featured": "Google Analytics 4 AI",
        "tools": [
            {"name": "Google Analytics 4 AI", "price": "Gratis", "best_for": "Web analytics & predictive metrics", "rating": 4.6, "verdict": "Beste gratis AI-webanalyse met voorspellende metrieken en automatische inzichten"},
            {"name": "Hotjar AI", "price": "EUR 29-99/mnd", "best_for": "Heatmaps & session recordings", "rating": 4.5, "verdict": "Meest complete tool voor AI-gedreven heatmaps en session recording analyse"},
            {"name": "Microsoft Clarity", "price": "Gratis", "best_for": "Gratis heatmaps & session replay", "rating": 4.3, "verdict": "Uitstekende gratis heatmap-tool met AI-sessieanalyse en frustratie-signalen"},
            {"name": "Plausible AI", "price": "EUR 9-69/mnd", "best_for": "Privacy-vriendelijke analytics", "rating": 4.4, "verdict": "Beste privacy-first webanalyse zonder cookies, met AI-trenddetectie"},
            {"name": "Heap AI", "price": "EUR 100-500/mnd", "best_for": "Automatic event tracking & analytics", "rating": 4.5, "verdict": "Beste voor automatische event tracking met AI-gedreven gedragsanalyse"},
            {"name": "Amplitude AI", "price": "Gratis-1000/mnd", "best_for": "Product analytics & user behavior", "rating": 4.6, "verdict": "Toonaangevend in product analytics met AI voor churn- en conversievoorspelling"},
            {"name": "Mixpanel AI", "price": "Gratis-500/mnd", "best_for": "Product & funnel analytics", "rating": 4.4, "verdict": "Sterk in funnel- en retentie-analyse met AI-gedreven gebruikerssegmentatie"},
        ],
        "affiliate_link": "https://marketingplatform.google.com/about/analytics/?ref=aitoolsnl",
    },
]


def call_gemini(prompt):
    """Call Gemini API via native generateContent endpoint."""
    import urllib.request
    import urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "Je bent een Nederlandse AI-tools journalist. Je schrijft eerlijke, vergelijkende artikelen in het Nederlands voor AI Tools NL, een site die AI tools vergelijkt voor Nederlandse ondernemers. Je artikelen zijn SEO-geoptimaliseerd, hebben een natuurlijke toon en bevatten praktische aanbevelingen. Gebruik markdown voor opmaak. Schrijf minstens 1000 woorden per artikel. Gebruik geen generieke of oppervlakkige content.\n\n" + prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 6144
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return content
    except Exception as e:
        print(f"ERROR calling Gemini: {e}", file=sys.stderr)
        if hasattr(e, 'read'):
            try:
                err_body = e.read().decode()
                print(f"Response body: {err_body}", file=sys.stderr)
            except:
                pass
        return None


def build_prompt(topic):
    """Build generation prompt for a topic."""
    tools_list = "\n".join([
        f"- {t['name']}: prijs {t['price']}, beste voor {t['best_for']}, score {t['rating']}/5"
        for t in topic['tools']
    ])

    return f"""Schrijf een compleet artikel in het Nederlands over {topic['title_prefix']}.

Gebruik de volgende structuur:
1. **Inleiding** (2 alinea's) — Waarom dit onderwerp relevant is in 2026 voor Nederlandse ondernemers.
2. **Tabel: De 7 beste {topic['title_prefix'].lower()}** — Een duidelijke vergelijkingstabel.
3. **Reviews per tool** — Korte review per tool (2-3 zinnen) met wie het beste past.
4. **Vergelijking: welk tool past bij welk type bedrijf?** — 3-4 scenario's.
5. **Waar op letten bij kiezen?** — 3-4 alinea's met criteria.
6. **Veelgestelde vragen** — 3 FAQ's met antwoorden.
7. **Conclusie** — Wie moet welke tool kiezen.

Gebruik deze tools in het artikel:
{tools_list}

Affiliate link voor de toonaangevende tool: {topic['affiliate_link']}

Eisen:
- Schrijf minstens 1000 woorden
- Gebruik concrete voorbeelden en scenario's
- SEO-vriendelijk met natuurlijke zoekwoorden
- Geef eerlijke voor- en nadelen
- Gebruik markdown opmaak
- Alles in het Nederlands
- GEEN YAML frontmatter, ALLEEN het artikel body
- Voeg geen titel/heading toe — schrijf direct de inleiding"""


def format_tool_yaml(topic):
    """Format tools section as YAML lines."""
    lines = []
    for t in topic['tools']:
        lines.append('  - name: "' + t['name'] + '"')
        lines.append('    verdict: "' + t['verdict'] + '"')
        lines.append('    priceRange: "' + t['price'] + '"')
        lines.append('    bestFor: "' + t['best_for'] + '"')
        lines.append('    rating: ' + str(t['rating']))
        lines.append('    affiliateLink: "' + topic['affiliate_link'] + '"')
    return '\n'.join(lines)


def create_article_file(topic, body):
    """Create the markdown article file."""
    tools_yaml_str = format_tool_yaml(topic)

    description_map = {
        "beste-ai-tools-marketing-automation-2026": "Vergelijk de beste AI tools voor marketing automation in 2026. HubSpot, ActiveCampaign, Klaviyo, Brevo, MoEngage en GetResponse voor geautomatiseerde marketingcampagnes.",
        "beste-ai-tools-videomarketing-2026": "Vergelijk de beste AI tools voor videomarketing in 2026. Synthesia, Descript, Runway, HeyGen, Opus Clip en Kapwing voor AI-videoproductie en -bewerking.",
        "beste-ai-tools-mlops-platform-engineering-2026": "Vergelijk de beste AI tools voor MLOps & platform engineering in 2026. MLflow, Kubeflow, Weights & Biases, Dagster, Neptune, Valohai en Azure ML voor ML-operationalisatie.",
        "beste-ai-tools-prompt-engineering-2026": "Vergelijk de beste AI tools voor prompt engineering in 2026. Anthropic Console, OpenAI Playground, LangSmith, PromptPerfect, Dust, Portkey en Agenta voor prompt optimalisatie en beheer.",
        "beste-ai-tools-web-analytics-conversie-2026": "Vergelijk de beste AI tools voor web analytics & conversieoptimalisatie in 2026. Google Analytics 4, Hotjar, Clarity, Plausible, Heap, Amplitude en Mixpanel voor data-gedreven optimalisatie.",
    }

    desc = description_map.get(topic['slug'], 'Vergelijk de beste AI tools voor dit segment in 2026.')

    lines = []
    lines.append("---")
    lines.append("title: '" + topic['title_prefix'] + ": top 7 vergeleken'")
    lines.append("slug: " + topic['slug'])
    lines.append('description: "' + desc + '"')
    lines.append("category: " + topic['category'])
    lines.append('rating: 4.4')
    lines.append("priceRange: EUR 0-5000/mnd")
    lines.append("pros:")
    lines.append("  - Up-to-date vergelijking van de beste AI tools in dit segment")
    lines.append("  - Met focus op Nederlandse markt en ondernemers")
    lines.append("  - Duidelijke aanbevelingen per use case en budget")
    lines.append("cons:")
    lines.append("  - Prijzen kunnen wijzigen, check altijd de aanbieder")
    lines.append("  - Sommige AI-functies zijn nog in beta of early access")
    lines.append("  - Niet elke tool is intensief getest in Nederlandse praktijk")
    lines.append("affiliateLinks:")
    lines.append("  - " + topic['affiliate_link'])
    lines.append("date: " + date.today().isoformat())
    lines.append("modelYear: 2026")
    lines.append('featuredTool: "' + topic['featured'] + '"')
    lines.append("readingTime: 9 min")
    lines.append("tools:")
    lines.append(tools_yaml_str)
    lines.append("related:")
    # Pick related articles based on category
    if topic['category'] == 'marketing':
        lines.append('  - "beste-ai-marketing-tools-2026"')
        lines.append('  - "beste-ai-email-marketing-tools-2026"')
        lines.append('  - "ai-voor-seo-2026"')
    elif topic['category'] == 'development':
        lines.append('  - "beste-ai-tools-programmeren-2026"')
        lines.append('  - "claude-code-vs-cursor-vs-windsurf-2026"')
        lines.append('  - "github-copilot-vs-cursor-vs-codeium-2026"')
    elif topic['category'] == 'technologie':
        lines.append('  - "beste-super-ai-agents-2026"')
        lines.append('  - "ai-trends-2026-nederland"')
        lines.append('  - "beste-ai-tools-cloud-optimalisatie-2026"')
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    total = len(TOPICS)
    success = 0

    for i, topic in enumerate(TOPICS, 1):
        slug = topic['slug']
        article_path = ARTICLES_DIR / f"{slug}.md"

        if article_path.exists():
            print(f"[{i}/{total}] SKIP {slug} — already exists")
            success += 1
            continue

        print(f"[{i}/{total}] Generating {slug} ({topic['category']})...")
        prompt = build_prompt(topic)
        body = call_gemini(prompt)

        if not body:
            print(f"  FAILED: Gemini returned no content", file=sys.stderr)
            continue

        # Remove code fences if present
        body = body.replace("```markdown", "").replace("```", "").strip()

        if len(body) < 200:
            print(f"  FAILED: Body too short ({len(body)} chars)", file=sys.stderr)
            continue

        content = create_article_file(topic, body)
        article_path.write_text(content, encoding='utf-8')
        print(f"  OK: {slug} — {len(body)} chars, {len(body.split())} words")
        success += 1

        # Rate limit — sleep between calls
        if i < total:
            time.sleep(3)

    print(f"\nDone: {success}/{total} articles generated")
    if success > 0:
        print(f"Articles directory: {ARTICLES_DIR}")
        print("Next step: git add + commit + push")


if __name__ == "__main__":
    main()