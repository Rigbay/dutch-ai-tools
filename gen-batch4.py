#!/usr/bin/env python3
"""Generate 3 remaining comparison articles. June 4, 2026."""
import os, time, sys, requests, yaml
from datetime import date

# Read API key from known-good location
API_KEY = ""
key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
if os.path.exists(key_file):
    with open(key_file) as f:
        API_KEY = f.read().strip()
if not API_KEY:
    API_KEY = (os.environ.get("GEMINI_API_KEY", "") or os.environ.get("GOOGLE_API_KEY", "")).strip()
if not API_KEY:
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if "GEMINI_API_KEY" in line or "GOOGLE_API_KEY" in line:
                    if "=" in line:
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val and not val.startswith("#") and len(val) > 10:
                            API_KEY = val
                            break
                            break

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

def all_slugs():
    return sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])

def pick_related(new_slug, pool, n=3):
    candidates = [s for s in pool if s != new_slug]
    return candidates[:n]

TOPICS = [
    {
        "slug": "exact-online-vs-moneybird-vs-snelstart-2026",
        "title": "Exact Online vs Moneybird vs Snelstart 2026: beste Nederlandse boekhoudsoftware",
        "description": "Exact Online, Moneybird of Snelstart in 2026? Vergelijk de beste Nederlandse boekhoudpakketten op prijs, gebruiksgemak, koppeling Belastingdienst en geschiktheid voor ZZP en MKB.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Exact Online vs Moneybird vs Snelstart in 2026. Behandel precies 7 tools: Exact Online, Moneybird, Snelstart, e-Boekhouden, Jortt, Visma eAccounting, InformerOnline.

Structuur:
- Introductie: boekhoudsoftware 2026 — Peppol e-facturatie, AI-boekhouders, btw-automatisering, NL landschap
- Per tool een ## kop: beschrijving, prijs (EUR/maand), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, prijs vanaf, beste voor, Belastingdienst/Peppol koppeling, score (1-5)
- Conclusie: welke voor ZZP, klein MKB, groeiend MKB, e-commerce, accountant, budget-starter
- 3 FAQ's

PUUR Nederlandse markt. Benoem Peppol deadline. Prijzen in EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Exact Online", "verdict": "Meest complete MKB-oplossing met rapportages, multi-currency en koppeling accountant", "priceRange": "EUR 30-110/mnd", "bestFor": "MKB 5-100+", "rating": 4.5, "affiliateLink": "https://exact.com/?ref=aitoolsnl"},
            {"name": "Moneybird", "verdict": "Beste UX/automatisering voor ZZP en klein MKB — facturen, bank en btw in een", "priceRange": "EUR 14-42/mnd", "bestFor": "ZZP & Klein MKB", "rating": 4.7, "affiliateLink": "https://moneybird.com/?ref=aitoolsnl"},
            {"name": "Snelstart", "verdict": "Betrouwbaar met sterk accountantsnetwerk en uitgebreide functionaliteit", "priceRange": "EUR 25-60/mnd", "bestFor": "MKB & Accountants", "rating": 4.3, "affiliateLink": "https://snelstart.nl/?ref=aitoolsnl"},
            {"name": "e-Boekhouden", "verdict": "Beste prijs-kwaliteit voor starters — volledige functies tegen lage kosten", "priceRange": "EUR 7-30/mnd", "bestFor": "Starters & Budget", "rating": 4.4, "affiliateLink": "https://e-boekhouden.nl/?ref=aitoolsnl"},
            {"name": "Jortt", "verdict": "Eenvoudig met gratis variant — ideaal voor startende ZZP'ers", "priceRange": "EUR 0-20/mnd", "bestFor": "Startende ZZP", "rating": 4.2, "affiliateLink": "https://jortt.nl/?ref=aitoolsnl"},
            {"name": "Visma eAccounting", "verdict": "Scandinavisch met groeiende NL-aanwezigheid — sterk in AI/automatisering", "priceRange": "EUR 20-60/mnd", "bestFor": "Automatisering & Groei", "rating": 4.1, "affiliateLink": "https://visma.com/eaccounting/?ref=aitoolsnl"},
            {"name": "InformerOnline", "verdict": "Cloud met realtime dashboards, sterke bank- en webshop-integraties", "priceRange": "EUR 20-50/mnd", "bestFor": "E-commerce & Realtime", "rating": 4.0, "affiliateLink": "https://informer.nl/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "github-vs-gitlab-vs-bitbucket-2026",
        "title": "GitHub vs GitLab vs Bitbucket 2026: beste code-hosting en CI/CD platform",
        "description": "GitHub, GitLab of Bitbucket in 2026? Vergelijk de beste DevSecOps-platforms op code hosting, CI/CD, AI-coding agents en geschiktheid voor Nederlandse ontwikkelteams.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over GitHub vs GitLab vs Bitbucket in 2026. Behandel precies 7 tools: GitHub, GitLab, Bitbucket, Azure DevOps, Gitea, SourceForge, Codeberg.

Structuur:
- Introductie: code-hosting 2026 — AI-agents, CI/CD, DevSecOps, EU-soevereiniteit
- Per tool ## kop: beschrijving, prijs (EUR/gebruiker/maand), use case, plus/min, verdict
- Markdown tabel: naam, prijs, beste voor, AI-assistent, EU-hosting, score
- Conclusie: voor solo, startup, scale-up, enterprise, open-source, EU-privacy, Microsoft-shop
- 3 FAQ's

EU focus. Codeberg als Duits privacy-alternatief. Vloeiend Nederlands.""",
        "tools": [
            {"name": "GitHub", "verdict": "Wereldstandaard met Copilot, Actions en het grootste ecosysteem", "priceRange": "EUR 0-20/gebruiker/mnd", "bestFor": "Open-source & Alle teams", "rating": 4.8, "affiliateLink": "https://github.com/?ref=aitoolsnl"},
            {"name": "GitLab", "verdict": "Beste DevSecOps-platform met eigen CI/CD, container registry en GitLab Duo AI", "priceRange": "EUR 0-29/gebruiker/mnd", "bestFor": "DevSecOps & Self-host", "rating": 4.6, "affiliateLink": "https://gitlab.com/?ref=aitoolsnl"},
            {"name": "Bitbucket", "verdict": "Naadloze Atlassian-integratie — sterk voor bestaande Jira/Confluence teams", "priceRange": "EUR 0-6/gebruiker/mnd", "bestFor": "Atlassian-ecosysteem", "rating": 4.2, "affiliateLink": "https://bitbucket.org/?ref=aitoolsnl"},
            {"name": "Azure DevOps", "verdict": "Enterprise-grade met diepe Microsoft-integratie en geavanceerde testplannen", "priceRange": "EUR 0-50/gebruiker/mnd", "bestFor": "Enterprise & Microsoft", "rating": 4.3, "affiliateLink": "https://azure.microsoft.com/devops/?ref=aitoolsnl"},
            {"name": "Gitea", "verdict": "Lichtgewicht open-source — zelf te hosten op Raspberry Pi of kleine VPS", "priceRange": "EUR 0 (self-host)", "bestFor": "Self-host & Privacy", "rating": 4.1, "affiliateLink": "https://gitea.com/?ref=aitoolsnl"},
            {"name": "SourceForge", "verdict": "Grootste open-source mirror network voor binary releases", "priceRange": "EUR 0 (gratis)", "bestFor": "Open-source Mirroring", "rating": 3.3, "affiliateLink": "https://sourceforge.net/?ref=aitoolsnl"},
            {"name": "Codeberg", "verdict": "Duits/EU non-profit alternatief — geen tracking, AVG-compliant", "priceRange": "EUR 0 (gratis/donatie)", "bestFor": "EU Privacy & AVG", "rating": 3.8, "affiliateLink": "https://codeberg.org/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "vercel-vs-netlify-vs-cloudflare-pages-2026",
        "title": "Vercel vs Netlify vs Cloudflare Pages 2026: beste hosting voor moderne webapps",
        "description": "Vercel, Netlify of Cloudflare Pages in 2026? Vergelijk de beste Jamstack en serverless hosting op snelheid, edge-functies, AI-integraties en developer experience.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Vercel vs Netlify vs Cloudflare Pages in 2026. Behandel precies 7 tools: Vercel, Netlify, Cloudflare Pages, Railway, Render, Fly.io, Deno Deploy.

Structuur:
- Introductie: webhosting 2026 — edge computing, serverless, AI-deploys
- Per tool ## kop: beschrijving, prijs, use case, plus/min, verdict
- Markdown tabel: naam, gratis tier, prijs, beste voor, edge-functies, score
- Conclusie: voor hobby, MVP, scale-up, enterprise Next.js, API-heavy, budget, performance
- 3 FAQ's

EU edge-locaties benoemen. Prijzen EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Vercel", "verdict": "Beste DX voor Next.js met v8 isolates, AI SDK en edge-functies", "priceRange": "EUR 0-20/mnd", "bestFor": "Next.js & Frontend teams", "rating": 4.8, "affiliateLink": "https://vercel.com/?ref=aitoolsnl"},
            {"name": "Netlify", "verdict": "Beste voor Jamstack met Functions, Forms en add-on ecosysteem", "priceRange": "EUR 0-19/mnd", "bestFor": "Jamstack & Statische sites", "rating": 4.5, "affiliateLink": "https://netlify.com/?ref=aitoolsnl"},
            {"name": "Cloudflare Pages", "verdict": "Beste prijs-kwaliteit met unlimited bandwidth en Workers integratie", "priceRange": "EUR 0-5/mnd", "bestFor": "Performance & Budget", "rating": 4.6, "affiliateLink": "https://pages.cloudflare.com/?ref=aitoolsnl"},
            {"name": "Railway", "verdict": "Eenvoudigste full-stack hosting — deploys via repo en Docker met een klik", "priceRange": "EUR 0-20/mnd", "bestFor": "Full-stack & Databases", "rating": 4.4, "affiliateLink": "https://railway.app/?ref=aitoolsnl"},
            {"name": "Render", "verdict": "Beste PaaS Heroku-alternatief met managed PostgreSQL, Redis en cron jobs", "priceRange": "EUR 0-19/mnd", "bestFor": "PaaS & Managed", "rating": 4.3, "affiliateLink": "https://render.com/?ref=aitoolsnl"},
            {"name": "Fly.io", "verdict": "Apps bij gebruikers met edge op 6 continenten — latency-gevoelige apps", "priceRange": "EUR 0-30/mnd", "bestFor": "Global & Low-latency", "rating": 4.2, "affiliateLink": "https://fly.io/?ref=aitoolsnl"},
            {"name": "Deno Deploy", "verdict": "Supersnelle edge met native TypeScript — perfect voor API's/microservices", "priceRange": "EUR 0-10/mnd", "bestFor": "Edge API's & Microservices", "rating": 4.1, "affiliateLink": "https://deno.com/deploy/?ref=aitoolsnl"},
        ],
    },
]


def call_gemini(prompt, max_retries=10):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}}
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120, headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                wait = 35 * (attempt + 1)
                print(f"  Rate-limited (429), wait {wait}s")
                time.sleep(wait)
                continue
            if resp.status_code in (503, 500):
                print(f"  {resp.status_code} (attempt {attempt+1})")
                time.sleep(30)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(15)
                    continue
                return None
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(15)
    return None


def build_article(defn, body_text):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    avg = round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1)
    data = {
        "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
        "category": defn["category"], "rating": avg, "priceRange": "EUR 0-100/mnd",
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig"],
        "cons": ["Prijzen kunnen wijzigen", "AI-features in ontwikkeling", "Niet alles dagelijks getest"],
        "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], slugs, 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste tool?", "a": "Dat hangt af van je situatie. " + defn["tools"][0]["name"] + " is voor de meeste gebruikers een prima startpunt."},
            {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere tools hebben gratis tiers. Perfect om te beginnen."},
            {"q": "Hoe kies ik de juiste tool?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    gen, skip, fail = 0, 0, 0

    for i, d in enumerate(TOPICS):
        out = os.path.join(ARTICLES_DIR, f"{d['slug']}.md")
        print(f"[{i+1}/3] {d['slug']}")
        if os.path.exists(out):
            print(f"  Skip — exists")
            skip += 1
            continue

        body = call_gemini(d["prompt"])
        if body is None:
            print(f"  FAILED")
            fail += 1
            continue

        full = build_article(d, body)
        with open(out, "w", encoding="utf-8") as f:
            f.write(full)
        gen += 1
        print(f"  OK — {len(body.split())} words")

        if i < len(TOPICS) - 1:
            time.sleep(12)

    print(f"\n=== {gen} gen, {skip} skip, {fail} fail ===")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
