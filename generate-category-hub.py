#!/usr/bin/env python3
"""
Generate category hub page for Dutch AI Tools site.
Lists all articles grouped by category with internal links.
"""

import re
from pathlib import Path
from datetime import datetime

ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")
OUTPUT_PATH = Path("/workspace/dutch-ai-tools/src/content/articles/categorie-overzicht-2026.md")

# Build article index
articles_by_category = {}
all_articles = []

for f in sorted(ARTICLES_DIR.glob("*.md")):
    if f.name == "categorie-overzicht-2026.md":
        continue
    
    content = f.read_text(encoding="utf-8")
    slug = f.stem
    
    # Extract metadata
    cat_match = re.search(r'^category:\s*(?:"(.+?)"|\'(.+?)\'|(\S+))', content, re.MULTILINE)
    if cat_match:
        cat = cat_match.group(1) or cat_match.group(2) or cat_match.group(3)
        cat = cat.strip()
    else:
        cat = "overig"
    
    title_match = re.search(r'^title:\s*(?:"(.+?)"|\'(.+?)\')', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1) or title_match.group(2)
        title = title.strip()
    else:
        title = slug.replace("-", " ").title()
    
    description_match = re.search(r'^description:\s*(?:"(.+?)"|\'(.+?)\')', content, re.MULTILINE)
    if description_match:
        description = description_match.group(1) or description_match.group(2)
        description = description.strip()
    else:
        description = ""
    
    if cat not in articles_by_category:
        articles_by_category[cat] = []
    
    articles_by_category[cat].append({
        "slug": slug,
        "title": title,
        "description": description[:150] + "..." if len(description) > 150 else description
    })
    
    all_articles.append({
        "slug": slug,
        "title": title,
        "category": cat,
        "description": description[:150] + "..." if len(description) > 150 else description
    })

# Sort categories by article count
sorted_categories = sorted(articles_by_category.items(), key=lambda x: (-len(x[1]), x[0]))

# Generate markdown
markdown = f"""---
title: 'Categorieën Overzicht — Alle AI Tools Vergelijkingen 2026'
slug: categorie-overzicht-2026
description: 'Overzichtspagina met alle AI Tools artikelen per categorie: Business tools, productiviteit, development, creatie, marketing, technologie, persoonlijke apps en huis & tuin. Nederlandse consumentenvergelijkingen.'
category: business
rating: 4.8
priceRange: gratis
pros:
- Volledig overzicht van alle {len(all_articles)} artikelen
- Directe links naar specifieke categorieën
- Gemakkelijk navigeren tussen verwante AI Tools
cons:
- Geen directe tool-vergelijking op deze pagina
- Alleen doorverwijzing naar uitgebreide artikelen
affiliateLinks:
- https://www.beehiiv.com/?via=anonymous-operator
- https://taskade.com/?via=55nfr2
- https://writesonic.com/?via=aitoolsnl
- https://rytr.me?via=hermes-affiliates
- https://www.synthesia.io?via=hermes
- https://www.make.com/en/register?pc=hermesai
- https://www.frase.io/?via=hermes10
date: {datetime.now().strftime('%Y-%m-%d')}
modelYear: 2026
featuredTool: 'Beehiiv'
readingTime: '10 min'
tools: []
related: []
faq:
- q: 'Waar kan ik de beste AI tools voor marketing vinden?'
  a: 'Ga naar de [Marketing Categorie](#marketing) hieronder voor artikelen over AI copywriting, SEO tools, social media automatisering en meer.'
- q: 'Hoe gebruik ik deze overzichtspagina?'
  a: 'Scroll naar de categorie die je interesseert en klik op een artikel link voor een uitgebreide vergelijking met prijzen, functies en affiliate links.'
- q: 'Worden deze artikelen regelmatig bijgewerkt?'
  a: 'Ja, alle artikelen worden minimaal jaarlijks bijgewerkt om nieuwe features, prijswijzigingen en aanbieders te reflecteren.'
---

## Categorieën Overzicht — Alle AI Tools Vergelijkingen 2026

Welkom bij het complete overzicht van alle AI Tools vergelijkingen op Dutch AI Tools. Deze pagina groepeert **{len(all_articles)} artikelen** in {len(sorted_categories)} hoofdcategorieën voor eenvoudige navigatie.

"""

# Add per-category sections
for cat, articles in sorted_categories:
    cat_name = cat.capitalize()
    if cat == "huis-tuin":
        cat_name = "Huis & Tuin"
    elif cat == "persoonlijk":
        cat_name = "Persoonlijk"
    elif cat == "productiviteit":
        cat_name = "Productiviteit"
    
    markdown += f"\n### {cat_name} ({len(articles)} artikelen)\n\n"
    
    for article in sorted(articles, key=lambda x: x["title"]):
        markdown += f"- **[📊 {article['title']}](/{article['slug']}/)**"
        if article["description"]:
            markdown += f" — {article['description']}"
        markdown += "\n"

# Add summary table
markdown += f"""
---

## Statistieken

| Categorie | Artikelen |
|-----------|----------|
"""

for cat, articles in sorted_categories:
    cat_display = cat.capitalize()
    if cat == "huis-tuin":
        cat_display = "Huis & Tuin"
    markdown += f"| {cat_display} | {len(articles)} |\n"

markdown += f"""
| **Totaal** | **{len(all_articles)}** |

---

## Hoe gebruik je dit overzicht?

1. **Kies een categorie** die bij je behoefte past (bijvoorbeeld *Business* voor zakelijke AI tools).
2. **Bekijk de artikelen** in die categorie — elk bevat een complete vergelijking van 5-7 tools.
3. **Lees de vergelijking** met prijzen, voor- en nadelen, en een duidelijke conclusie.
4. **Gebruik de affiliate links** om direct naar de aanbieders te gaan (wij verdienen een kleine commissie zonder extra kosten voor jou).

Alle artikelen zijn geschreven in het Nederlands en gericht op de Nederlandse markt.

---

## Recent Bijgewerkt

"""

# Show recently updated articles (by date in frontmatter, fallback to file mtime)
recent_articles = []
for f in sorted(ARTICLES_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
    if f.name == "categorie-overzicht-2026.md":
        continue
    slug = f.stem
    # Try to extract date
    content = f.read_text(encoding="utf-8")
    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    date = date_match.group(1) if date_match else "2026-06"
    
    title_match = re.search(r'^title:\s*"(.+?)"', content, re.MULTILINE)
    if not title_match:
        title_match = re.search(r"^title:\s*'(.+?)'", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else slug.replace("-", " ").title()
    
    recent_articles.append({"slug": slug, "title": title, "date": date})

for article in recent_articles[:5]:
    markdown += f"- **{article['date']}** — [{article['title']}](/{article['slug']}/)\n"

markdown += f"""

---

## Contact & Suggesties

Heb je vragen over een specifieke AI tool of categorie die je mist? Laat het ons weten via [GitHub Issues](https://github.com/Rigbay/dutch-ai-tools/issues).

*Laatst bijgewerkt: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

# Write output
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(markdown, encoding="utf-8")

print(f"Generated hub page: {OUTPUT_PATH}")
print(f"Total articles: {len(all_articles)}")
print(f"Categories: {len(sorted_categories)}")
for cat, articles in sorted_categories:
    print(f"  {cat}: {len(articles)} articles")