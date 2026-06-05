#!/usr/bin/env python3
"""Generate 5 high-value comparison articles for gaps found June 5, 2026."""
import os, time, sys, requests, yaml
from datetime import date

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

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

TOPICS = [
    {
        "slug": "react-vs-vue-vs-svelte-2026",
        "title": "React vs Vue vs Svelte 2026: beste frontend framework voor jouw project",
        "description": "React, Vue of Svelte in 2026? Vergelijk de beste JavaScript frontend frameworks op performance, leercurve, ecosysteem en geschiktheid voor Nederlandse developers.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over React vs Vue vs Svelte in 2026. Behandel precies 7 frameworks: React, Vue, Svelte, Angular, SolidJS, Qwik, Astro.

Structuur:
- Introductie: frontend frameworks 2026 — server components, signals, hydration, het NL developer landschap
- Per framework een ## kop: beschrijving, leercurve, performance, ecosysteem, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, leercurve, bundle size, server components, beste voor, score (1-5)
- Conclusie: welke voor startup, enterprise, solo dev, performance-first, content sites, leerproject
- 3 FAQ's

NL focus. Vloeiend Nederlands. Benoem welke bedrijven in NL deze frameworks gebruiken (Booking.com, bol.com, Adyen, etc.).""",
        "tools": [
            {"name": "React", "verdict": "Grootste ecosysteem met React Server Components en breedste arbeidsmarkt in NL", "priceRange": "Gratis (open-source)", "bestFor": "Enterprise & Schaalbaar", "rating": 4.8, "affiliateLink": "https://react.dev/?ref=aitoolsnl"},
            {"name": "Vue", "verdict": "Beste balans tussen leercurve en functionaliteit — populair bij NL startups en MKB", "priceRange": "Gratis (open-source)", "bestFor": "MKB & Snelle MVP", "rating": 4.6, "affiliateLink": "https://vuejs.org/?ref=aitoolsnl"},
            {"name": "Svelte", "verdict": "Compile-first met minste boilerplate — razendsnel en groeiend in NL", "priceRange": "Gratis (open-source)", "bestFor": "Performance & DX", "rating": 4.5, "affiliateLink": "https://svelte.dev/?ref=aitoolsnl"},
            {"name": "Angular", "verdict": "Enterprise-grade met sterke typing en Google-backing — voor grote NL teams", "priceRange": "Gratis (open-source)", "bestFor": "Enterprise & TypeScript", "rating": 4.3, "affiliateLink": "https://angular.dev/?ref=aitoolsnl"},
            {"name": "SolidJS", "verdict": "React-achtige DX met Svelte-snelheid — signals natively, geen virtual DOM", "priceRange": "Gratis (open-source)", "bestFor": "Performance & React-fans", "rating": 4.2, "affiliateLink": "https://www.solidjs.com/?ref=aitoolsnl"},
            {"name": "Qwik", "verdict": "Resumable JS — laadt alleen wat nodig is, perfect voor content-heavy NL sites", "priceRange": "Gratis (open-source)", "bestFor": "Lighthouse 100 & SEO", "rating": 4.0, "affiliateLink": "https://qwik.dev/?ref=aitoolsnl"},
            {"name": "Astro", "verdict": "Zero JS by default — ideaal voor content-sites en marketingpagina's met frameworks naar keuze", "priceRange": "Gratis (open-source)", "bestFor": "Content & Multi-framework", "rating": 4.4, "affiliateLink": "https://astro.build/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "python-vs-javascript-vs-typescript-2026",
        "title": "Python vs JavaScript vs TypeScript 2026: welke programmeertaal moet je leren?",
        "description": "Python, JavaScript of TypeScript in 2026? Vergelijk de populairste programmeertalen op toepassingen, salaris, AI-relevantie en baankansen in Nederland.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Python vs JavaScript vs TypeScript in 2026. Behandel precies 7 talen: Python, JavaScript, TypeScript, Rust, Go, Kotlin, Swift.

Structuur:
- Introductie: programmeertalen 2026 — AI-tijdperk, stack trends, NL arbeidsmarkt
- Per taal een ## kop: beschrijving, typische use cases, leercurve, salarisindicatie (NL), plus/min, verdict
- Markdown tabel: naam, type, leercurve, gemiddeld NL salaris (EUR), AI/ML geschikt, beste voor, score
- Conclusie: welke voor AI/ML, web dev, mobile, systeem, data, carrièreswitch, hobby
- 3 FAQ's

NL focus. Salarissen in EUR/jaar (bron: Indeed NL, Glassdoor NL). Vloeiend Nederlands.""",
        "tools": [
            {"name": "Python", "verdict": "Koninklijke taal van AI/ML en data science — beste ROI voor carrièreswitch in 2026", "priceRange": "Gratis (open-source)", "bestFor": "AI/ML & Data", "rating": 4.9, "affiliateLink": "https://www.python.org/?ref=aitoolsnl"},
            {"name": "JavaScript", "verdict": "Draait overal — browser, server, mobile, IoT — breedste inzetbaarheid", "priceRange": "Gratis (open-source)", "bestFor": "Full-stack Web", "rating": 4.7, "affiliateLink": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/?ref=aitoolsnl"},
            {"name": "TypeScript", "verdict": "JavaScript met superpowers — type-safety maakt grote NL codebases beheersbaar", "priceRange": "Gratis (open-source)", "bestFor": "Enterprise Web & Teams", "rating": 4.8, "affiliateLink": "https://www.typescriptlang.org/?ref=aitoolsnl"},
            {"name": "Rust", "verdict": "Systeemtaal van de toekomst — Linux kernel, Windows, en nu ook AI-tooling", "priceRange": "Gratis (open-source)", "bestFor": "Systemen & Performance", "rating": 4.6, "affiliateLink": "https://www.rust-lang.org/?ref=aitoolsnl"},
            {"name": "Go", "verdict": "Simpel, snel, schaalbaar — de ruggengraat van cloud-native NL infrastructuren", "priceRange": "Gratis (open-source)", "bestFor": "Cloud & DevOps", "rating": 4.4, "affiliateLink": "https://go.dev/?ref=aitoolsnl"},
            {"name": "Kotlin", "verdict": "Moderne Java-opvolger — standaard voor Android en groeiend in backend (Spring)", "priceRange": "Gratis (open-source)", "bestFor": "Mobile & Enterprise", "rating": 4.3, "affiliateLink": "https://kotlinlang.org/?ref=aitoolsnl"},
            {"name": "Swift", "verdict": "Apple's eigen taal — de enige keuze voor iOS/Mac development in 2026", "priceRange": "Gratis (open-source)", "bestFor": "Apple Ecosystem", "rating": 4.2, "affiliateLink": "https://www.swift.org/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "cursor-vs-copilot-vs-windsurf-2026",
        "title": "Cursor vs Copilot vs Windsurf 2026: beste AI-code assistant voor developers",
        "description": "Cursor, GitHub Copilot of Windsurf in 2026? Vergelijk de beste AI-coding assistants op code-generatie, context-begrip, debug-mogelijkheden en prijs voor Nederlandse developers.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Cursor vs GitHub Copilot vs Windsurf in 2026. Behandel precies 7 AI-code tools: Cursor, GitHub Copilot, Windsurf, Cline, Amazon Q Developer, Tabnine, Codeium.

Structuur:
- Introductie: AI-coding 2026 — van autocomplete naar autonome agents, NL dev adoptie
- Per tool ## kop: beschrijving, IDE-integratie, model-ondersteuning, prijs, plus/min, verdict
- Markdown tabel: naam, prijs (EUR/mnd), IDE's, context window, beste voor, score
- Conclusie: voor solo dev, team, enterprise, budget, open-source, privacy-first
- 3 FAQ's

NL focus. Prijzen in EUR. Vloeiend Nederlands. Benoem welke tools privacy/GDPR-vriendelijk zijn.""",
        "tools": [
            {"name": "Cursor", "verdict": "Beste AI-native IDE met agent-mode en diff-preview — voelt als pair programming", "priceRange": "EUR 0-20/mnd", "bestFor": "AI-first Developer", "rating": 4.8, "affiliateLink": "https://cursor.sh/?ref=aitoolsnl"},
            {"name": "GitHub Copilot", "verdict": "Grootste ecosysteem — naadloze GitHub-integratie met Copilot Chat en agents", "priceRange": "EUR 0-19/mnd", "bestFor": "GitHub Teams", "rating": 4.7, "affiliateLink": "https://github.com/features/copilot/?ref=aitoolsnl"},
            {"name": "Windsurf", "verdict": "Codeium's AI-native IDE met cascade-modus — sterke multi-file refactoring", "priceRange": "EUR 0-15/mnd", "bestFor": "Refactoring & Multi-file", "rating": 4.5, "affiliateLink": "https://codeium.com/windsurf/?ref=aitoolsnl"},
            {"name": "Cline", "verdict": "Open-source VS Code agent — volledige autonomie met bestandssysteem en terminal toegang", "priceRange": "EUR 0 (open-source + eigen API key)", "bestFor": "Autonome Agents & Budget", "rating": 4.3, "affiliateLink": "https://github.com/cline/cline/?ref=aitoolsnl"},
            {"name": "Amazon Q Developer", "verdict": "Gratis voor individuen met diepe AWS-integratie — beste voor cloud-native teams", "priceRange": "EUR 0-20/mnd", "bestFor": "AWS & Cloud-native", "rating": 4.1, "affiliateLink": "https://aws.amazon.com/q/developer/?ref=aitoolsnl"},
            {"name": "Tabnine", "verdict": "Privacy-first met on-premise optie — geschikt voor NL enterprise compliance", "priceRange": "EUR 0-39/mnd", "bestFor": "Enterprise & Privacy", "rating": 4.0, "affiliateLink": "https://www.tabnine.com/?ref=aitoolsnl"},
            {"name": "Codeium", "verdict": "Gratis tier met sterke autocomplete — breedste IDE-ondersteuning van alle tools", "priceRange": "EUR 0-15/mnd", "bestFor": "Multi-IDE & Budget", "rating": 4.2, "affiliateLink": "https://codeium.com/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "supabase-vs-firebase-vs-appwrite-2026",
        "title": "Supabase vs Firebase vs Appwrite 2026: beste backend-as-a-service platform",
        "description": "Supabase, Firebase of Appwrite in 2026? Vergelijk de beste BaaS-platforms op database, auth, realtime-functies, pricing en geschiktheid voor Nederlandse startups en developers.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Supabase vs Firebase vs Appwrite in 2026. Behandel precies 7 platforms: Supabase, Firebase, Appwrite, PocketBase, Convex, NHost, Backendless.

Structuur:
- Introductie: Backend-as-a-Service 2026 — serverless, edge, open-source vs vendor lock-in, NL startup landschap
- Per platform ## kop: beschrijving, database-type, auth, pricing, self-host optie, plus/min, verdict
- Markdown tabel: naam, database, gratis tier, self-host, EU-hosting, beste voor, score
- Conclusie: voor startup MVP, scale-up, enterprise, SQL-fan, document-DB fan, privacy-first, budget
- 3 FAQ's

EU/GDPR focus. NL prijzen EUR. Vloeiend Nederlands. Benoem Supabase's PostgreSQL vs Firebase's NoSQL afweging.""",
        "tools": [
            {"name": "Supabase", "verdict": "PostgreSQL-first met beste open-source ecosysteem — het Firebase-alternatief voor SQL-teams", "priceRange": "EUR 0-25/mnd", "bestFor": "SQL & Open-source", "rating": 4.8, "affiliateLink": "https://supabase.com/?ref=aitoolsnl"},
            {"name": "Firebase", "verdict": "Google's alles-in-één platform — beste voor snelle prototyping met NoSQL en hosting", "priceRange": "EUR 0-pay-as-you-go", "bestFor": "Snelle MVP & NoSQL", "rating": 4.6, "affiliateLink": "https://firebase.google.com/?ref=aitoolsnl"},
            {"name": "Appwrite", "verdict": "Open-source BaaS met sterke self-host optie — volledige controle voor privacy-bewuste teams", "priceRange": "EUR 0-15/mnd", "bestFor": "Self-host & Privacy", "rating": 4.4, "affiliateLink": "https://appwrite.io/?ref=aitoolsnl"},
            {"name": "PocketBase", "verdict": "Ultralicht — één binary met SQLite, auth en file storage, draait op een Raspberry Pi", "priceRange": "EUR 0 (self-host)", "bestFor": "Side Projects & Hobby", "rating": 4.3, "affiliateLink": "https://pocketbase.io/?ref=aitoolsnl"},
            {"name": "Convex", "verdict": "Realtime-first met functionele queries — perfect voor collaborative apps", "priceRange": "EUR 0-25/mnd", "bestFor": "Realtime & Collaborative", "rating": 4.2, "affiliateLink": "https://www.convex.dev/?ref=aitoolsnl"},
            {"name": "NHost", "verdict": "Supabase + Hasura onder één dak met GraphQL — sterk voor data-heavy apps", "priceRange": "EUR 0-25/mnd", "bestFor": "GraphQL & Data-heavy", "rating": 4.1, "affiliateLink": "https://nhost.io/?ref=aitoolsnl"},
            {"name": "Backendless", "verdict": "Volledig visuele backend-bouwer — low-code met echte database-kracht", "priceRange": "EUR 0-149/mnd", "bestFor": "Low-code & Enterprise", "rating": 3.8, "affiliateLink": "https://backendless.com/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "n8n-vs-make-vs-zapier-2026",
        "title": "n8n vs Make vs Zapier 2026: beste no-code automation platform",
        "description": "n8n, Make of Zapier in 2026? Vergelijk de beste no-code automatiseringstools op integraties, prijs, zelf-hostbaarheid en geschiktheid voor Nederlandse ondernemers en MKB.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over n8n vs Make vs Zapier in 2026. Behandel precies 7 tools: n8n, Make, Zapier, Pipedream, Relay.app, Albato, Workato.

Structuur:
- Introductie: automation 2026 — AI-agents, zelf-host tools, GDPR/AVG, NL ondernemerslandschap
- Per tool ## kop: beschrijving, aantal integraties, prijs, self-host mogelijkheid, use case, plus/min, verdict
- Markdown tabel: naam, prijs vanaf, integraties, self-host, AI-functies, beste voor, score
- Conclusie: voor ZZP'er budget, MKB automatisering, enterprise, privacy-first, open-source fan, eenvoudigste start
- 3 FAQ's

NL focus. n8n is van oorsprong Duits (EU). Prijzen EUR. Vloeiend Nederlands.""",
        "tools": [
            {"name": "n8n", "verdict": "Beste open-source automation tool — self-host, EU-gebaseerd, 400+ nodes met AI-extensies", "priceRange": "EUR 0-20/mnd", "bestFor": "Self-host & Open-source", "rating": 4.7, "affiliateLink": "https://n8n.io/?ref=aitoolsnl"},
            {"name": "Make", "verdict": "Visueel krachtigste workflow builder met drag-and-drop — perfect voor complexe scenario's", "priceRange": "EUR 0-29/mnd", "bestFor": "Complexe Workflows", "rating": 4.6, "affiliateLink": "https://www.make.com/?ref=aitoolsnl"},
            {"name": "Zapier", "verdict": "Grootste integratiebibliotheek (6000+) — makkelijkste start voor beginners", "priceRange": "EUR 0-36/mnd", "bestFor": "Beginners & Breed", "rating": 4.5, "affiliateLink": "https://zapier.com/?ref=aitoolsnl"},
            {"name": "Pipedream", "verdict": "Developer-first met volledige code-toegang — onbeperkte gratis tier voor developers", "priceRange": "EUR 0-25/mnd", "bestFor": "Developers & API", "rating": 4.3, "affiliateLink": "https://pipedream.com/?ref=aitoolsnl"},
            {"name": "Relay.app", "verdict": "Nieuwe generatie met AI-pathfinding — automatisch de beste workflow vinden", "priceRange": "EUR 0-15/mnd", "bestFor": "AI-first Automation", "rating": 4.1, "affiliateLink": "https://relay.app/?ref=aitoolsnl"},
            {"name": "Albato", "verdict": "Sterk in embedded automation — perfect voor SaaS-platforms die automations aanbieden", "priceRange": "EUR 0-25/mnd", "bestFor": "Embedded & White-label", "rating": 4.0, "affiliateLink": "https://albato.com/?ref=aitoolsnl"},
            {"name": "Workato", "verdict": "Enterprise automation met governance — SOC2, HIPAA, voor grote NL organisaties", "priceRange": "EUR custom (vanaf 1000/mnd)", "bestFor": "Enterprise & Compliance", "rating": 4.2, "affiliateLink": "https://www.workato.com/?ref=aitoolsnl"},
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


def pick_related(new_slug, pool, n=3):
    candidates = [s for s in pool if s != new_slug]
    return candidates[:n]


def build_article(defn, body_text):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    avg = round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1)
    data = {
        "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
        "category": defn["category"], "rating": avg, "priceRange": "EUR 0-150/mnd",
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig"],
        "cons": ["Prijzen kunnen wijzigen", "AI-features in ontwikkeling", "Niet alles dagelijks getest"],
        "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], slugs, 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste tool?", "a": "Dat hangt af van je situatie. " + defn["tools"][0]["name"] + " is voor de meeste gebruikers een prima startpunt."},
            {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere tools hebben gratis tiers of open-source opties. Perfect om te beginnen."},
            {"q": "Hoe kies ik de juiste tool?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs voor jouw situatie."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    gen, skip, fail = 0, 0, 0

    for i, d in enumerate(TOPICS):
        out = os.path.join(ARTICLES_DIR, f"{d['slug']}.md")
        print(f"[{i+1}/5] {d['slug']}")
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
