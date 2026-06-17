#!/usr/bin/env python3
import os, yaml, re

articles_dir = "/workspace/dutch-ai-tools/src/content/articles"
fixed_count = 0

for fname in os.listdir(articles_dir):
    if not fname.endswith(".md"):
        continue
    
    path = os.path.join(articles_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if frontmatter is properly closed
    if not content.startswith('---\n'):
        print(f"⚠ {fname}: Doesn't start with ---")
        continue
    
    # Count --- delimiters
    parts = content.split('---')
    if len(parts) < 3:
        print(f"✗ {fname}: Missing closing --- (has {len(parts)-1} delimiters)")
        # Add closing --- and minimal body
        if content.strip().endswith('---'):
            # Already ends with --- but split didn't catch it
            continue
        # Find where frontmatter ends (first line after opening --- that's not a YAML key)
        lines = content.split('\n')
        in_frontmatter = True
        body_start = None
        for i, line in enumerate(lines):
            if i == 0 and line == '---':
                continue
            if in_frontmatter:
                if line.strip() == '':
                    continue
                if ':' in line and not line.startswith(' '):
                    # YAML key
                    continue
                else:
                    # Not a YAML key, this is body
                    body_start = i
                    break
        if body_start is None:
            # No body found, add closing --- and placeholder
            new_content = content.rstrip() + '\n---\n\n*Artikel inhoud volgt.*'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {fname}: Added closing --- and placeholder body")
            fixed_count += 1
        else:
            # Insert closing --- before body
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                if i == body_start - 1:
                    new_lines.append('---')
            new_content = '\n'.join(new_lines)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {fname}: Inserted closing --- before body")
            fixed_count += 1
    else:
        # Has both opening and closing ---
        if parts[2].strip() == '':
            # Body is empty after frontmatter
            new_content = content.rstrip() + '\n\n*Artikel inhoud volgt.*'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {fname}: Added placeholder body")
            fixed_count += 1
        else:
            # Has content, check if it's just whitespace
            body = parts[2].strip()
            if not body:
                new_content = content.rstrip() + '\n\n*Artikel inhoud volgt.*'
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ {fname}: Added placeholder body to empty content")
                fixed_count += 1
            else:
                # Has content, validate YAML
                try:
                    yaml.safe_load(parts[1])
                    # print(f"✓ {fname}: OK")
                except yaml.YAMLError as e:
                    print(f"✗ {fname}: YAML error: {e}")

print(f"\nFixed {fixed_count} articles")