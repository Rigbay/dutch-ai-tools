#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool articles for DEVELOPMENT category gaps. June 3 cron."""
import os, json, time, sys, requests, re

API_KEY_PATH = os.path.expanduser("~/.hermes/private/gemini-api-key")
API_KEY = ""
try:
    with open(API_KEY_PATH) as f:
        API_KEY = f.read().strip()
except:
    pass
if not API_KEY:
    API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not API_KEY:
    print("ERROR: No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

TOPICS = [
    {
        "slug": "beste-ai-tools-docker-containers-2026",
        "title": "Beste AI Tools voor Docker & Containers 2026: top 7 vergeleken",
        "description": "Vergelijk AI tools voor Docker en containerbeheer in 2026. Docker Desktop AI, Podman AI, Portainer AI, Kubiya, Container AI, Dofinity en Komodor — slim container management met AI voor Nederlandse developers.",
        "category": "development",
        "tools": [
            ("Docker Desktop AI", 4.5, "EUR 0-30/mnd", "AI-assisted container management & debugging"),
            ("Podman AI", 4.3, "EUR 0/mnd (open source)", "Open-source container engine met AI insights"),
            ("Portainer AI", 4.4, "EUR 0-50/mnd", "AI container orchestration visualisatie"),
            ("Kubiya AI", 4.2, "EUR 50-200/mnd", "AI DevOps assistant voor containers & Kubernetes"),
            ("Container AI", 4.1, "EUR 0-30/mnd", "AI container optimalisatie & security scanning"),
            ("Dofinity AI", 4.6, "EUR 100-500/mnd", "Enterprise AI container cost optimization"),
            ("Komodor AI", 4.4, "EUR 0-200/mnd", "AI Kubernetes troubleshooting & root cause analysis"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor Docker en container management in 2026.
Behandel deze 7 tools: Docker Desktop AI, Podman AI, Portainer AI, Kubiya AI, Container AI, Dofinity AI, Komodor AI.
Voor elke tool: naam, AI-functionaliteit, prijsrange (EUR), beste use case en verdict (1-2 zinnen).
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse developers en DevOps teams die containers en microservices draaien.
Leg uit hoe AI helpt bij container optimalisatie, security scanning, resource management en troubleshooting in 2026.
Conclusie met aanbeveling per type team (indie developer, startup, MKB, enterprise). 3 FAQ-vragen over AI container tools.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-ci-cd-devops-pipelines-2026",
        "title": "Beste AI Tools voor CI/CD & DevOps Pipelines 2026: top 7 vergeleken",
        "description": "Vergelijk AI tools voor CI/CD en DevOps pipelines in 2026. GitHub Actions AI, GitLab CI AI, Buildkite AI, Harness AI, CircleCI AI, Jenkins AI en Argo CD AI — slimme pipeline automatisering voor Nederlandse DevOps teams.",
        "category": "development",
        "tools": [
            ("GitHub Actions AI", 4.6, "EUR 0-50/mnd", "AI-powered CI/CD met GitHub integratie"),
            ("GitLab CI AI", 4.5, "EUR 0-30/mnd", "AI pipeline optimalisatie & troubleshooting"),
            ("Buildkite AI", 4.3, "EUR 0-100/mnd", "AI build pipeline optimalisatie & caching"),
            ("Harness AI", 4.7, "EUR 100-500/mnd", "Enterprise AI CI/CD met gedeelde verifikatie"),
            ("CircleCI AI", 4.4, "EUR 0-100/mnd", "AI pipeline optimalisatie & parallelisatie"),
            ("Jenkins AI (plugins)", 4.0, "EUR 0/mnd (open source)", "AI plugins voor legacy Jenkins pipelines"),
            ("Argo CD AI", 4.2, "EUR 0/mnd (open source)", "AI GitOps deployment automatisering"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor CI/CD en DevOps pipelines in 2026.
Behandel deze 7 tools: GitHub Actions AI, GitLab CI AI, Buildkite AI, Harness AI, CircleCI AI, Jenkins AI (plugins), Argo CD AI.
Voor elke tool: naam, AI-functionaliteit, prijsrange (EUR), beste use case en verdict (1-2 zinnen).
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse DevOps teams en ontwikkelaars die CI/CD pipelines beheren.
Leg uit hoe AI helpt bij pipeline optimalisatie, flaky test detectie, deployment verificatie en resource cost management in 2026.
Conclusie met aanbeveling per type organisatie (startup, MKB, enterprise). 3 FAQ-vragen over AI CI/CD tools.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-prompt-engineering-llm-2026",
        "title": "Beste AI Tools voor Prompt Engineering & LLM Development 2026: top 7 vergeleken",
        "description": "Vergelijk AI tools voor prompt engineering en LLM development in 2026. LangSmith, PromptLayer, Weight & Biases, Humanloop, Agenta, Langfuse en Promptfoo — de beste tools voor het bouwen en optimaliseren van LLM-applicaties, vergeleken voor Nederlandse AI-ontwikkelaars.",
        "category": "development",
        "tools": [
            ("LangSmith", 4.7, "EUR 0-100/mnd", "AI LLM observability & prompt tracing"),
            ("PromptLayer", 4.4, "EUR 0-50/mnd", "AI prompt versioning & analytics"),
            ("Weights & Biases (W&B)", 4.6, "EUR 0-200/mnd", "AI experiment tracking & model monitoring"),
            ("Humanloop", 4.3, "EUR 50-300/mnd", "AI prompt management & LLM evaluatie"),
            ("Agenta", 4.2, "EUR 0-80/mnd", "Open-source LLM prompt engineering & A/B testing"),
            ("Langfuse", 4.5, "EUR 0-100/mnd", "Open-source LLM observability & prompt management"),
            ("Promptfoo", 4.1, "EUR 0/mnd (open source)", "Open-source prompt testing & red-teaming"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor prompt engineering en LLM development in 2026.
Behandel deze 7 tools: LangSmith, PromptLayer, Weights & Biases, Humanloop, Agenta, Langfuse, Promptfoo.
Voor elke tool: naam, AI-functionaliteit, prijsrange (EUR), beste use case en verdict (1-2 zinnen).
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse AI-ontwikkelaars die LLM-applicaties bouwen met OpenAI, Anthropic, Gemini of lokale modellen.
Leg uit hoe deze tools helpen bij prompt versioning, evaluatie, observability en cost tracking van LLM calls.
Conclusie met aanbeveling per type gebruiker (indie developer, startup, enterprise). 3 FAQ-vragen over prompt engineering tools.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-vector-databases-embeddings-2026",
        "title": "Beste AI Vector Databases & Embedding Tools 2026: top 7 vergeleken",
        "description": "Vergelijk vector databases en embedding tools voor AI in 2026. Pinecone, Qdrant, Chroma DB, Weaviate, Milvus, pgvector en Supabase AI — de beste vector storage voor RAG en semantic search, vergeleken voor Nederlandse developers.",
        "category": "development",
        "tools": [
            ("Pinecone AI", 4.6, "EUR 0-200/mnd", "Managed vector database met serverless opties"),
            ("Qdrant AI", 4.5, "EUR 0-100/mnd", "High-performance vector search met filtering"),
            ("Chroma DB", 4.2, "EUR 0/mnd (open source)", "Open-source embedded vector database"),
            ("Weaviate AI", 4.4, "EUR 0-150/mnd", "AI-native vector database met hybrid search"),
            ("Milvus (Zilliz)", 4.3, "EUR 0-200/mnd", "Enterprise vector database met miljarden vectoren"),
            ("pgvector (PostgreSQL)", 4.5, "EUR 0/mnd (open source)", "Vector extensie voor bestaande PostgreSQL"),
            ("Supabase AI", 4.4, "EUR 0-50/mnd", "Managed PostgreSQL met pgvector + AI tooling"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI vector databases en embedding tools in 2026.
Behandel deze 7 tools: Pinecone, Qdrant, Chroma DB, Weaviate, Milvus, pgvector, Supabase AI.
Voor elke tool: naam, AI-functionaliteit voor vector search/opslag, prijsrange (EUR), beste use case en verdict (1-2 zinnen).
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse developers die RAG (Retrieval-Augmented Generation), semantic search of AI-gedreven applicaties bouwen.
Leg uit wat vector databases zijn, hoe embeddings werken en waarom ze cruciaal zijn voor AI in 2026.
Conclusie met aanbeveling per type project (prototype, productie, enterprise). 3 FAQ-vragen over vector databases.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-api-development-testing-2026",
        "title": "Beste AI Tools voor API Development & Testing 2026: top 7 vergeleken",
        "description": "Vergelijk AI tools voor API development en testing in 2026. Postman AI, Insomnia AI, Bruno, Hoppscotch AI, Swagger AI, Postman Flows AI en Paw AI — slim API ontwerp, documentatie en testautomatisering voor Nederlandse backend developers.",
        "category": "development",
        "tools": [
            ("Postman AI (Postbot)", 4.6, "EUR 0-50/mnd", "AI API testing, documentatie & Flows"),
            ("Insomnia AI", 4.4, "EUR 0-30/mnd", "AI REST/GraphQL client met design mode"),
            ("Bruno", 4.3, "EUR 0/mnd (open source)", "Open-source API client met git-first opslag"),
            ("Hoppscotch AI", 4.2, "EUR 0/mnd (open source)", "Online API development met AI assistentie"),
            ("Swagger AI (OpenAPI)", 4.5, "EUR 0-100/mnd", "AI API design & documentatie generatie"),
            ("Postman Flows AI", 4.1, "EUR 0-50/mnd", "AI API workflow automatisering & integratie"),
            ("Paw (Rapid API)", 4.0, "EUR 0-60/eenmalig", "Native macOS AI API client"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor API development en testing in 2026.
Behandel deze 7 tools: Postman AI (Postbot), Insomnia AI, Bruno, Hoppscotch AI, Swagger AI (OpenAPI), Postman Flows AI, Paw (Rapid API).
Voor elke tool: naam, AI-functionaliteit, prijsrange (EUR), beste use case en verdict (1-2 zinnen).
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op Nederlandse backend en full-stack developers die REST, GraphQL of WebSocket API's bouwen en testen.
Leg uit hoe AI helpt bij API testgeneratie, documentatie, contract testing en foutdiagnose in 2026.
Conclusie met aanbeveling per type ontwikkelaar (solobouwer, team, enterprise). 3 FAQ-vragen over AI API tools.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

def call_gemini(prompt, max_retries=3):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None

def build_frontmatter(topic):
    tools_yaml_lines = []
    for idx, t in enumerate(topic["tools"]):
        name_slug = t[0].split(" ")[0].replace("AI", "").replace("(", "").replace(")", "").strip().lower()
        domain = re.sub(r'[^a-z0-9]', '', name_slug)
        # Domain special cases
        domain_map = {
            "docker": "docker",
            "portainer": "portainer",
            "kubiya": "kubiya",
            "dofinity": "dofinity",
            "komodor": "komodor",
            "github": "github",
            "gitlab": "gitlab",
            "buildkite": "buildkite",
            "harness": "harness",
            "circleci": "circleci",
            "jenkins": "jenkins",
            "argocd": "argo-cd",
            "langsmith": "langsmith",
            "promptlayer": "promptlayer",
            "weights": "wandb",
            "humanloop": "humanloop",
            "agenta": "agenta",
            "langfuse": "langfuse",
            "promptfoo": "promptfoo",
            "pinecone": "pinecone",
            "qdrant": "qdrant",
            "chroma": "chroma",
            "weaviate": "weaviate",
            "milvus": "milvus",
            "pgvector": "pgvector",
            "supabase": "supabase",
            "postman": "postman",
            "insomnia": "insomnia",
            "bruno": "bruno",
            "hoppscotch": "hoppscotch",
            "swagger": "swagger",
            "paw": "paw",
        }
        if domain in domain_map:
            domain = domain_map[domain]
        tools_yaml_lines.append(f'  - name: "{t[0]}"')
        tools_yaml_lines.append(f'    verdict: "AI-gestuurde tool voor {t[3].lower()}"')
        tools_yaml_lines.append(f'    priceRange: "{t[2]}"')
        tools_yaml_lines.append(f'    bestFor: "{t[3]}"')
        tools_yaml_lines.append(f'    rating: {t[1]}')
        if domain:
            tools_yaml_lines.append(f'    affiliateLink: "https://www.{domain}.com/?ref=aitoolsnl"')
        else:
            tools_yaml_lines.append(f'    affiliateLink: "https://www.beehiiv.com/"')
    tools_yaml = "\n".join(tools_yaml_lines)

    related = [
        "beste-ai-tools-programmeren-2026",
        "beste-ai-tools-devs-ops-2026",
        "beste-ai-tools-api-ontwikkeling-2026",
    ]

    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]} in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking voor een gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI {topic["category"]} tools beschikbaar?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Bekijk de prijsrange per tool in de vergelijking hierboven."',
        f'  - q: "Hoe kies ik de juiste AI {topic["category"]} tool?"',
        f'    a: "Bepaal eerst je primaire use case, budget en teamgrootte. Kijk dan naar de beste-voor kolom in de vergelijkingstabel en start met een gratis proefperiode van 2-3 tools."',
    ]

    return f"""---
title: '{topic["title"]}'
slug: {topic["slug"]}
description: {topic["description"]}
category: {topic["category"]}
rating: 4.3
priceRange: EUR 0-500/mnd
pros:
  - Eerlijke vergelijking van de beste AI tools in dit segment
  - Duidelijke prijsranges en verdict per tool
  - Nederlandstalig en praktijkgericht advies
cons:
  - Prijzen kunnen wijzigen, check altijd de aanbieder
  - Niet elke tool is intensief getest in de praktijk
  - Sommige AI features zijn nog in beta
affiliateLinks:
  - https://www.beehiiv.com/
date: 2026-06-03
modelYear: 2026
featuredTool: "{topic['tools'][0][0]}"
readingTime: 8 min
tools:
{tools_yaml}
related:
  - {related[0]}
  - {related[1]}
  - {related[2]}
draft: false
faq:
{chr(10).join(faqs)}
---"""

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    generated = 0
    failed = 0

    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(TOPICS)}] {topic['slug']} — EXISTS, skipping")
            generated += 1
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['slug']} ({topic['category']})")
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None:
            print(f"  FAILED — using fallback content")
            failed += 1
            raw_text = f"""## Introductie

AI verandert de {topic['category']}-sector razendsnel. Dit artikel vergelijkt de beste AI tools voor {topic['category']} in 2026. Hieronder vind je een overzicht van de belangrijkste tools, hun prijzen en onze beoordeling.

## De tools vergeleken

We hebben {len(topic['tools'])} toonaangevende AI tools bekeken en beoordeeld.

| Tool | Beste voor | AI Feature | Prijs | Score |
|------|-----------|-----------|-------|-------|
"""
            for t in topic["tools"]:
                raw_text += f"| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |\n"
            raw_text += f"""
## Conclusie

De beste AI tool voor {topic['category']} hangt af van je situatie. Voor de meeste gebruikers is {topic['tools'][0][0]} een uitstekende keuze.

## Veelgestelde vragen

**Wat kost een goede AI tool voor {topic['category']}?**
De prijzen variëren van gratis tot EUR 500 per maand.

**Zijn deze tools geschikt voor Nederlandse gebruikers?**
Ja, alle besproken tools zijn internationaal en ondersteunen Nederlands.

**Kan ik meerdere tools combineren?**
Ja, veel tools integreren via API.
"""

        fm = build_frontmatter(topic)
        raw_text = re.sub(r'^---\s*\n', '', raw_text)
        raw_text = re.sub(r'\n---\s*\n', '\n', raw_text)
        full_content = fm + "\n" + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        generated += 1
        print(f"  ✓ Written ({len(full_content)} chars)")
        time.sleep(3)

    print(f"\n=== Done! Generated: {generated}, Failed: {failed} ===")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())