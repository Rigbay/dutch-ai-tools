#!/usr/bin/env python3
"""Fix related fields for batch 15 articles to cross-link between new articles."""
import os

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

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

def read_file(path):
    with open(path) as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

count = 0
for slug, new_related in LINK_MAP.items():
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    content = read_file(path)
    
    # Find and replace the related block
    old_block = "related:\n- ai-beeldherkenning-2026\n- ai-stemgeneratie-2026\n- ai-tools-marketing-teams-2026"
    new_block = "related:\n" + "\n".join(f"- {s}" for s in new_related)
    
    if old_block in content:
        content = content.replace(old_block, new_block)
        write_file(path, content)
        print(f"  {slug}: updated related -> {new_related}")
        count += 1
    else:
        # Try to find any related block
        for line in content.split("\n"):
            if line.startswith("related:"):
                print(f"  {slug}: found related block but pattern mismatch: {line}")
                break

print(f"\nUpdated {count}/5 articles")