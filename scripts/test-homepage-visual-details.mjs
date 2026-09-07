import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');

const homepage = read('src/pages/index.astro');
const header = read('src/components/Header.astro');
const icon = read('src/components/TaskRouteIcon.astro');

const checks = [
  {
    name: 'arbitrary route abbreviations are absent',
    pass: !/\b(?:TXT|SRC|DEV)\b/.test(homepage),
  },
  {
    name: 'all three task icons are declared and rendered',
    pass:
      ["'writing'", "'research'", "'building'"].every((name) => homepage.includes(`icon: ${name}`))
      && homepage.includes('<TaskRouteIcon name={route.icon} />'),
  },
  {
    name: 'task routes retain writing/research and send automation directly to its comparison',
    pass: [
      "title: 'Schrijven & analyseren'",
      "href: '/beste-ai-chatbots-2026/'",
      "title: 'Research met bronnen'",
      "href: '/categorie/productiviteit/'",
      "title: 'Werk automatiseren'",
      "href: '/beste-ai-automation-tools-2026/'",
    ].every((expected) => homepage.includes(expected)),
  },
  {
    name: 'development remains available in the category grid',
    pass: /const coreCategories = \[[^\]]*'development'/.test(homepage)
      && homepage.includes('href: `/categorie/${category}/`'),
  },
  {
    name: 'decorative task icons are hidden from assistive technology',
    pass:
      icon.includes('aria-hidden="true"')
      && icon.includes('focusable="false"')
      && homepage.includes('class="tool-orb" aria-hidden="true"'),
  },
  {
    name: 'the phone tagline hides instead of truncating',
    pass:
      /class="[^"]*\bhidden\b[^"]*\bsm:block\b[^"]*"[^>]*>Kies wijzer\. Werk slimmer\.<\/span>/.test(header)
      && !/class="[^"]*\btruncate\b[^"]*"[^>]*>Kies wijzer\. Werk slimmer\.<\/span>/.test(header),
  },
];

for (const check of checks) {
  console.log(`${check.pass ? 'PASS' : 'FAIL'} ${check.name}`);
}

const failures = checks.filter((check) => !check.pass);
if (failures.length) {
  process.exitCode = 1;
} else {
  console.log(`\n${checks.length}/${checks.length} homepage visual-detail checks passed.`);
}
