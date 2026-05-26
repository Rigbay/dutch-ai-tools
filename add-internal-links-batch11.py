#!/usr/bin/env python3
"""Add internal 'Lees ook' links to all Dutch AI tools articles.
Picks 3 related articles per post, inserts before FAQ or at end.
Batch 11b — May 26 2026."""
import re, random
from pathlib import Path

ARTICLES_DIR = Path("/tmp/dutch-ai-tools/src/content/articles")
OUTPUT_FILE = Path("/tmp/dutch-ai-tools/internal-linking-report.md")

# Category → article slugs mapping
CATEGORY_MAP = {
    "business": [],
    "tools": [],
    "creative": [],
    "tech": [],
    "health": [],
    "education": [],
    "lifestyle": [],
    "industry": [],
    "finance": [],
    "other": [],
}

articles = {}
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
    
    # Check if already has Lees ook
    has_links = "Lees ook" in content
    
    articles[slug] = {
        "content": content,
        "category": cat,
        "title": title,
        "has_links": has_links,
    }

# For each article, pick 3 related articles from same or adjacent category
def get_related(slug, cat, n=3):
    """Pick n related articles, prioritizing same category, then random."""
    same = [s for s in CATEGORY_MAP.get(cat, []) if s != slug]
    other = [s for s in articles if s != slug and s not in same]
    
    chosen = same[:n]
    if len(chosen) < n:
        chosen.extend(other[:n - len(chosen)])
    
    return chosen[:n]

report_lines = []
report_lines.append("# Internal Linking Report — Dutch AI Tools")
report_lines.append(f"Date: 2026-05-26\n")

updated = 0
skipped = 0

for slug, data in articles.items():
    if data["has_links"]:
        skipped += 1
        continue
    
    related = get_related(slug, data["category"])
    if not related:
        continue
    
    # Build Lees ook section
    links_md = "\n\n---\n\n## Lees ook\n\n"
    for r_slug in related:
        r_data = articles.get(r_slug, {})
        r_title = r_data.get("title", r_slug)
        # Clean title
        r_title = r_title.replace("'", "").strip()
        links_md += f"- [{r_title}](/{r_slug}/)\n"
    
    content = data["content"]
    
    # Insert before FAQ or at end
    if "## Veelgestelde Vragen" in content or "## FAQ" in content:
        # Insert before FAQ
        parts = re.split(r'(## (?:Veelgestelde Vragen|FAQ))', content, maxsplit=1)
        if len(parts) >= 2:
            new_content = parts[0].rstrip() + links_md + "\n" + parts[1] + (parts[2] if len(parts) > 2 else "")
        else:
            new_content = content.rstrip() + links_md
    else:
        new_content = content.rstrip() + links_md
    
    # Write back
    f = ARTICLES_DIR / f"{slug}.md"
    f.write_text(new_content, encoding="utf-8")
    updated += 1
    
    report_lines.append(f"- **{data['title']}** ← {', '.join(articles[r]['title'][:40] for r in related)}")

report_lines.insert(2, f"- Updated: {updated}")
report_lines.insert(3, f"- Already had links: {skipped}")
report_lines.insert(4, f"- Total articles: {len(articles)}\n")

OUTPUT_FILE.write_text("\n".join(report_lines), encoding="utf-8")
print(f"Updated: {updated}")
print(f"Skipped (already had links): {skipped}")
print(f"Total: {len(articles)}")
print(f"Report: {OUTPUT_FILE}")
