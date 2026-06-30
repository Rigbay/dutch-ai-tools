#!/usr/bin/env python3
import os, yaml, sys
from pathlib import Path

ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

def check_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split YAML frontmatter
    if not content.startswith('---\n'):
        return False, "No frontmatter start"
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return False, "No frontmatter end"
    yaml_str = parts[1]
    try:
        data = yaml.safe_load(yaml_str)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)

if __name__ == "__main__":
    errors = []
    for md_file in ARTICLES_DIR.glob("*.md"):
        ok, msg = check_yaml(md_file)
        if not ok:
            errors.append((md_file.name, msg))
    print(f"Checked {len(list(ARTICLES_DIR.glob('*.md')))} articles")
    if errors:
        print(f"\nFound {len(errors)} YAML errors:")
        for fname, msg in errors[:10]:
            print(f"  {fname}: {msg}")
        if len(errors) > 10:
            print(f"  ... and {len(errors)-10} more")
    else:
        print("All articles have valid YAML frontmatter")