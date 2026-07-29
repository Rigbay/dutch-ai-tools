import { spawnSync } from 'node:child_process';
import {
  mkdtempSync,
  mkdirSync,
  rmSync,
  writeFileSync
} from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { extractInternalArticleLinks } from './model-freshness-links.mjs';

const cases = [
  { input: '[A](/draft-slug/)', expected: ['draft-slug'] },
  { input: '[A](/draft-slug)', expected: ['draft-slug'] },
  { input: '[A](/draft-slug/?ref=one)', expected: ['draft-slug'] },
  { input: '[A](/draft-slug#section)', expected: ['draft-slug'] },
  { input: '[A](https://example.com/draft-slug/)', expected: [] },
  {
    input: '[A](/first/) and [B](/second?ref=two)',
    expected: ['first', 'second']
  }
];

const failures = cases.flatMap(({ input, expected }) => {
  const actual = extractInternalArticleLinks(input).map(({ slug }) => slug);
  return JSON.stringify(actual) === JSON.stringify(expected)
    ? []
    : [{ input, expected, actual }];
});

const fixtureRoot = mkdtempSync(join(tmpdir(), 'dat-freshness-links-'));
const articlesDir = join(fixtureRoot, 'articles');
mkdirSync(articlesDir);

writeFileSync(
  join(articlesDir, 'draft-slug.md'),
  `---
title: Draft
slug: draft-slug
draft: true
---
Hidden.
`
);
writeFileSync(
  join(articlesDir, 'published.md'),
  `---
title: Published
slug: published
draft: false
---
[Slash](/draft-slug/)
[No slash](/draft-slug)
`
);
writeFileSync(
  join(articlesDir, 'placeholder.md'),
  `---
title: Placeholder
slug: placeholder
draft: false
tools:
  - name: 'Tool1'
  - name: "AI Tool G"
---
Unsafe placeholder inventory.
`
);

const auditPath = join(
  dirname(fileURLToPath(import.meta.url)),
  'audit-model-freshness.mjs'
);
const integration = spawnSync(process.execPath, [auditPath], {
  encoding: 'utf8',
  env: {
    ...process.env,
    MODEL_FRESHNESS_ARTICLES_DIR: articlesDir
  }
});

let integrationResult = null;
try {
  integrationResult = JSON.parse(integration.stdout);
} catch {
  failures.push({
    input: 'integration fixture',
    expected: 'valid JSON audit output',
    actual: integration.stdout || integration.stderr
  });
}

const integrationLinks =
  integrationResult?.findings?.linksToDrafts?.map(({ target }) => target) || [];
const integrationPlaceholders =
  integrationResult?.findings?.placeholderFindings?.flatMap(({ entries }) => entries) || [];
if (
  integration.status !== 1 ||
  JSON.stringify(integrationLinks) !==
    JSON.stringify(['draft-slug', 'draft-slug']) ||
  JSON.stringify(integrationPlaceholders) !==
    JSON.stringify(['Tool1', 'AI Tool G'])
) {
  failures.push({
    input: 'published links and placeholder-name integration fixture',
    expected: {
      exitStatus: 1,
      links: ['draft-slug', 'draft-slug'],
      placeholders: ['Tool1', 'AI Tool G']
    },
    actual: {
      exitStatus: integration.status,
      links: integrationLinks,
      placeholders: integrationPlaceholders
    }
  });
}

rmSync(fixtureRoot, { recursive: true, force: true });

console.log(
  JSON.stringify(
    {
      schema: 'dutch-ai-tools-model-freshness-link-tests-v1',
      cases: cases.length,
      integrationCases: 3,
      failures,
      passed: failures.length === 0
    },
    null,
    2
  )
);

process.exitCode = failures.length === 0 ? 0 : 1;
