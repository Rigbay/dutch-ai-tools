#!/usr/bin/env python3
"""Add 'Verder lezen' internal linking sections to 4 new articles.
Picks 3-4 related existing articles per new article."""

import os, re

ARTICLES_DIR = "src/content/articles"

NEW_SLUGS = [
    "beste-ai-tools-retail-winkels-2026",
    "beste-ai-tools-persoonlijke-financien-2026",
    "beste-ai-tools-logistiek-transport-2026",
    "beste-ai-tools-vastgoed-makelaardij-2026",
]

# Related links per new article (slug -> [(title, slug), ...])
RELATED_LINKS = {
    "beste-ai-tools-retail-winkels-2026": [
        ("AI Tools voor E-commerce", "ai-voor-ecommerce-2026"),
        ("Beste AI Marketing Tools", "beste-ai-marketing-tools-2026"),
        ("AI Tools voor Sales", "beste-ai-sales-tools-2026"),
        ("AI Tools voor Content Creators", "beste-ai-tools-content-creators-2026"),
    ],
    "beste-ai-tools-persoonlijke-financien-2026": [
        ("Beste AI Financiële & Boekhouding Tools", "beste-ai-financiele-boekhouding-tools-2026"),
        ("AI Tools voor ZZP'ers", "beste-ai-tools-zzpers-2026"),
        ("Beste AI Tools voor Administratie", "beste-ai-tools-administratie-2026"),
        ("AI Tools voor Beleggers", "beste-ai-tools-beleggers-investeerders-2026"),
    ],
    "beste-ai-tools-logistiek-transport-2026": [
        ("Beste AI Automation Tools", "beste-ai-automation-tools-2026"),
        ("AI Tools voor API Development", "beste-ai-tools-api-development-testing-2026"),
        ("Beste AI Cloud Optimalisatie Tools", "beste-ai-tools-cloud-optimalisatie-2026"),
        ("AI Tools voor MKB & Startende Ondernemers", "ai-tools-mkb-starten-2026"),
    ],
    "beste-ai-tools-vastgoed-makelaardij-2026": [
        ("Beste AI Tools voor Architecten", "beste-ai-tools-architecten-bouwkunde-2026"),
        ("Beste AI Tools voor de Bouw", "beste-ai-tools-bouw-2026"),
        ("AI Tools voor Energiebeheer", "beste-ai-tools-energiebeheer-2026"),
        ("EU AI Act Compliance Tools", "eu-ai-act-compliance-tools-2026"),
    ],
}

def add_verder_lezen(path, links):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if already has Verder lezen section
    if "## Verder lezen" in content:
        print(f"  Already has Verder lezen section, skipping")
        return False
    
    # Build the section
    section = "\n\n## Verder lezen\n\n"
    section += "Wil je meer vergelijken? Lees ook:\n\n"
    for title, slug in links:
        section += f"- [{title}](/{slug}/)\n"
    
    # Append before EOF
    new_content = content.rstrip() + section
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    count = 0
    for slug in NEW_SLUGS:
        path = os.path.join(ARTICLES_DIR, f"{slug}.md")
        if not os.path.exists(path):
            print(f"NOT FOUND: {path}")
            continue
        links = RELATED_LINKS.get(slug, [])
        if add_verder_lezen(path, links):
            count += 1
            print(f"  Added 'Verder lezen' to {slug}")
    print(f"Done. Updated {count} articles.")

if __name__ == "__main__":
    main()