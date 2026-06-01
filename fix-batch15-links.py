#!/usr/bin/env python3
"""Fix related fields and add internal cross-links between new batch 15 articles."""
import re, os

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

# Map slug -> [related slugs that include at least 2 from the new batch + 1 existing relevant article]
LINK_MAP = {
    "beste-ai-e-commerce-dropshipping-tools-2026": [
        "beste-ai-interieur-ontwerp-tools-2026",
        "beste-ai-podcast-productie-tools-2026",
        "ai-tools-marketing-teams-2026"
    ],
    "beste-ai-3d-modellering-tools-2026": [
        "beste-ai-interieur-ontwerp-tools-2026",
        "beste-ai-research-academische-tools-2026",
        "ai-beeldherkenning-2026"
    ],
    "beste-ai-interieur-ontwerp-tools-2026": [
        "beste-ai-3d-modellering-tools-2026",
        "beste-ai-e-commerce-dropshipping-tools-2026",
        "ai-beeldherkenning-2026"
    ],
    "beste-ai-podcast-productie-tools-2026": [
        "beste-ai-research-academische-tools-2026",
        "beste-ai-3d-modellering-tools-2026",
        "ai-stemgeneratie-2026"
    ],
    "beste-ai-research-academische-tools-2026": [
        "beste-ai-podcast-productie-tools-2026",
        "beste-ai-e-commerce-dropshipping-tools-2026",
        "notion-vs-obsidian-vs-logseq-2026"
    ],
}

# Article titles for natural link text
TITLES = {
    "beste-ai-e-commerce-dropshipping-tools-2026": "AI Tools voor E-commerce & Dropshipping",
    "beste-ai-3d-modellering-tools-2026": "AI 3D Modellering & AR/VR Tools",
    "beste-ai-interieur-ontwerp-tools-2026": "AI Interieur & Woonontwerp Tools",
    "beste-ai-podcast-productie-tools-2026": "AI Podcast & Audio Productie Tools",
    "beste-ai-research-academische-tools-2026": "AI Tools voor Research & Academisch Werk",
}

# Contextual paragraphs to insert internal links into each article
# (slug -> list of (anchor_text_approx, replacement_with_link))
LINKS = {
    "beste-ai-e-commerce-dropshipping-tools-2026": [
        ("Interior AI", "[Interior AI (zie ook AI Interieur & Woonontwerp Tools)](/dutch-ai-tools/beste-ai-interieur-ontwerp-tools-2026/)"),
        ("podcast", "[podcast tools](/dutch-ai-tools/beste-ai-podcast-productie-tools-2026/)"),
    ],
    "beste-ai-3d-modellering-tools-2026": [
        ("interieur", "[interieur ontwerp](/dutch-ai-tools/beste-ai-interieur-ontwerp-tools-2026/)"),
        ("Onderzoek", "[Academisch onderzoek](/dutch-ai-tools/beste-ai-research-academische-tools-2026/)"),
    ],
    "beste-ai-interieur-ontwerp-tools-2026": [
        ("3D", "[3D-modellering](/dutch-ai-tools/beste-ai-3d-modellering-tools-2026/)"),
        ("e-commerce", "[e-commerce tools](/dutch-ai-tools/beste-ai-e-commerce-dropshipping-tools-2026/)"),
    ],
    "beste-ai-podcast-productie-tools-2026": [
        ("onderzoek", "[research tools](/dutch-ai-tools/beste-ai-research-academische-tools-2026/)"),
        ("3D", "[3D](/dutch-ai-tools/beste-ai-3d-modellering-tools-2026/)"),
    ],
    "beste-ai-research-academische-tools-2026": [
        ("podcast", "[podcastproductie](/dutch-ai-tools/beste-ai-podcast-productie-tools-2026/)"),
        ("e-commerce", "[e-commerce](/dutch-ai-tools/beste-ai-e-commerce-dropshipping-tools-2026/)"),
    ],
}

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def fix_related(slug, new_related):
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    content = read_file(path)
    # Replace related block
    old_related = "related:\n- ai-beeldherkenning-2026\n- ai-stemgeneratie-2026\n- ai-tools-marketing-teams-2026"
    new_related_yaml = "related:\n" + "\n".join(f"- {s}" for s in new_related)
    if old_related in content:
        content = content.replace(old_related, new_related_yaml)
        write_file(path, content)
        return True
    return False

def add_internal_links(slug, links):
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    content = read_file(path)
    count = 0
    for anchor, replacement in links:
        if anchor in content:
            content = content.replace(anchor, replacement)
            count += 1
    if count > 0:
        write_file(path, content)
    return count

print("=== Fixing related fields ===")
for slug, related in LINK_MAP.items():
    if fix_related(slug, related):
        print(f"  {slug}: related updated to {related}")
    else:
        print(f"  {slug}: NOT FOUND (maybe already updated)")

print("\n=== Adding internal links ===")
for slug, links in LINKS.items():
    count = add_internal_links(slug, links)
    print(f"  {slug}: {count} links added")

print("\nDone!")