#!/usr/bin/env python3
"""Add 'Lees ook' cross-linking sections to all Dutch AI Tools articles missing them.
Finds related articles by category, inserts before FAQ or at end.
June 3 2026 cron batch — targets remaining ~138 uncovered articles."""
import re, sys
from pathlib import Path

ARTICLES_DIR = Path("/workspace/kieskeuken/dutch-ai-tools/src/content/articles")
OUTPUT_FILE = Path("/workspace/kieskeuken/dutch-ai-tools/internal-linking/report-cron-20260603.md")

CATEGORY_MAP = {}
articles = {}

# Load all articles
for f in sorted(ARTICLES_DIR.glob("*.md")):
    content = f.read_text(encoding="utf-8")
    slug = f.stem
    
    # Extract category
    cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
    cat = cat_match.group(1) if cat_match else "other"
    if cat not in CATEGORY_MAP:
        CATEGORY_MAP[cat] = []
    CATEGORY_MAP[cat].append(slug)
    
    # Extract title
    title_match = re.search(r"^title:\s*'?(.+?)'?\s*$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else slug
    title = title.replace("'", "").strip()
    
    # Check if already has internal links section
    has_links = "Lees ook" in content or "Verder lezen" in content or "Lees verder" in content
    
    # Check for "Gerelateerde artikelen" at bottom
    has_gerelateerd = "Gerelateerde artikelen" in content
    
    articles[slug] = {
        "content": content,
        "category": cat,
        "title": title,
        "has_links": has_links,
        "has_gerelateerd": has_gerelateerd,
    }

def get_related(slug, cat, n=3):
    """Pick n related articles, prioritizing same category, then adjacent categories."""
    same = [s for s in CATEGORY_MAP.get(cat, []) if s != slug]
    other = [s for s in articles if s != slug and s not in same]
    
    chosen = same[:n]
    if len(chosen) < n:
        other_pool = [s for s in other if s not in chosen]
        # Prefer articles that already have links (richer content)
        linked_other = sorted(other_pool, key=lambda s: (0 if articles[s].get("has_links") else 1, s))
        chosen.extend(linked_other[:n - len(chosen)])
    
    return chosen[:n]

report_lines = []
updated = 0
skipped_no_need = 0
skipped_error = 0

for slug, data in articles.items():
    if data["has_links"] or data["has_gerelateerd"]:
        skipped_no_need += 1
        continue
    
    related = get_related(slug, data["category"])
    if not related:
        skipped_error += 1
        continue
    
    # Build links section
    links_md = "\n\n---\n\n## Verder lezen\n\n"
    for r_slug in related:
        r_title = articles.get(r_slug, {}).get("title", r_slug)
        links_md += f"- [{r_title}](/{r_slug}/)\n"
    
    content = data["content"]
    
    # Insert before FAQ/Vragen section or at end
    faq_pattern = r'(## (?:Veelgestelde Vragen|FAQ|Veelgestelde vragen))'
    if re.search(faq_pattern, content):
        parts = re.split(faq_pattern, content, maxsplit=1)
        if len(parts) >= 2:
            new_content = parts[0].rstrip() + links_md + "\n" + parts[1] + (parts[2] if len(parts) > 2 else "")
        else:
            new_content = content.rstrip() + links_md
    else:
        new_content = content.rstrip() + links_md
    
    fpath = ARTICLES_DIR / f"{slug}.md"
    fpath.write_text(new_content, encoding="utf-8")
    
    report_lines.append(f"- [{slug}] now links to: {', '.join(related)}")
    updated += 1

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(
    f"# Internal Linking Cron Report — 2026-06-03\n\n"
    f"Articles updated with 'Verder lezen' sections: **{updated}**\n"
    f"Already had links (skipped): **{skipped_no_need}**\n"
    f"No related found (skipped): **{skipped_error}**\n\n"
    + "\n".join(report_lines),
    encoding="utf-8"
)

print(f"Updated: {updated}")
print(f"Skipped (already linked): {skipped_no_need}")
print(f"Skipped (no related): {skipped_error}")
print(f"Total articles: {len(articles)}")