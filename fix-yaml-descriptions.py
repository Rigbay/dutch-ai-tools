#!/usr/bin/env python3
"""Fix YAML description fields that have broken double quotes."""

import os, sys, re

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find description: "..."
    lines = content.split('\n')
    fixed = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('description: "') and not line.endswith('"'):
            # Multi-line quoted string
            desc_lines = [line]
            j = i + 1
            while j < len(lines) and not lines[j].rstrip().endswith('"'):
                desc_lines.append(lines[j])
                j += 1
            if j < len(lines):
                desc_lines.append(lines[j])
                i = j
            # Reformat as >-
            desc_text = '\n'.join(desc_lines)
            desc_text = desc_text.replace('description: "', '').replace('"', '').strip()
            # Clean up line breaks
            desc_text = ' '.join(desc_text.split())
            if len(desc_text) > 180:
                desc_text = desc_text[:177] + '...'
            fixed.append('description: >-')
            fixed.append(f'  {desc_text}')
        else:
            fixed.append(line)
        i += 1
    
    new_content = '\n'.join(fixed)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith('.md'):
            path = os.path.join(ARTICLES_DIR, fname)
            if fix_file(path):
                print(f"Fixed: {fname}")
                count += 1
    print(f"\nFixed {count} files.")

if __name__ == '__main__':
    main()