import yaml
import os

articles_dir = "/workspace/dutch-ai-tools/src/content/articles"
for fname in os.listdir(articles_dir):
    if fname.endswith(".md"):
        path = os.path.join(articles_dir, fname)
        with open(path, 'r') as f:
            content = f.read()
        if content.startswith('---\n'):
            try:
                # Extract YAML frontmatter
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_text = parts[1]
                    data = yaml.safe_load(yaml_text)
                    print(f"✓ {fname}: OK")
                else:
                    print(f"✗ {fname}: No frontmatter")
            except yaml.YAMLError as e:
                print(f"✗ {fname}: YAML error: {e}")
            except Exception as e:
                print(f"✗ {fname}: Error: {e}")