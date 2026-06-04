#!/usr/bin/env python3
"""Add '## Lees ook' cross-linking to Dutch AI Tools articles that lack it.
Matches existing patterns: '## Lees ook' or '## Verder lezen' with 3-5 links.
"""
import re
from pathlib import Path

ARTICLES_DIR = Path("/workspace/kieskeuken/dutch-ai-tools/src/content/articles")
REPORT_FILE = Path("/workspace/kieskeuken/dutch-ai-tools/internal-linking/cron-2026-06-04.md")

# Build article index
articles = {}
categories = {}

for f in sorted(ARTICLES_DIR.glob("*.md")):
    content = f.read_text(encoding="utf-8")
    slug = f.stem

    # Extract category
    cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
    cat = cat_match.group(1).lower() if cat_match else "other"

    # Extract title
    title_match = re.search(r"^title:\s*'(.+?)'", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else slug

    has_lees_ook = bool(re.search(r'^## (Lees ook|Verder lezen)', content, re.MULTILINE))

    if cat not in categories:
        categories[cat] = []
    categories[cat].append(slug)

    articles[slug] = {
        "content": content,
        "category": cat,
        "title": title,
        "has_links": has_lees_ook,
    }

print(f"Total articles: {len(articles)}")
print(f"Categories: {len(categories)}")
for cat, slugs in sorted(categories.items()):
    print(f"  {cat}: {len(slugs)} articles")

def get_related(slug, cat, n=5):
    """Pick n related articles from same category first, then other categories."""
    same = [s for s in categories.get(cat, []) if s != slug]
    result = same[:n]
    if len(result) < n:
        other_all = [s for s in articles if s != slug and s not in result]
        result.extend(other_all[:n - len(result)])
    return result[:n]


updated = 0
skipped = 0
errors = []
report = []

for slug, data in sorted(articles.items()):
    if data["has_links"]:
        skipped += 1
        continue

    related = get_related(slug, data["category"])
    if not related:
        errors.append(f"{slug}: no related articles found")
        continue

    # Build links section (matching existing "Lees ook" style, most common)
    links_md = "\n\n---\n\n## Lees ook\n\n"
    for r_slug in related:
        r_title = articles.get(r_slug, {}).get("title", r_slug)
        links_md += f"- [{r_title}](/{r_slug}/)\n"

    content = data["content"]
    # Insert before end of file
    content = content.rstrip() + links_md

    fpath = ARTICLES_DIR / f"{slug}.md"
    fpath.write_text(content, encoding="utf-8")
    updated += 1

    titles = [articles.get(s, {}).get("title", s) for s in related]
    report.append(f"- {data['title']}: linked to {', '.join(titles[:3])}...")
    print(f"  ✓ {slug}: +{len(related)} links ({data['category']}) — {data['title'][:50]}")

print(f"\n=== SUMMARY ===")
print(f"Updated: {updated}")
print(f"Skipped (already had links): {skipped}")
print(f"Errors: {len(errors)}")

REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(REPORT_FILE, "w", encoding="utf-8") as rf:
    rf.write("# Dutch AI Tools Cross-linking Cron Report — 2026-06-04\n\n")
    rf.write(f"Updated: {updated} articles\n")
    rf.write(f"Skipped (already linked): {skipped}\n\n")
    for line in report:
        rf.write(line + "\n")
    for err in errors:
        rf.write(f"  ERROR: {err}\n")

print(f"Report written to {REPORT_FILE}")
