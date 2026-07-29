import {
  countBodyWords,
  inspectThinSensitiveArticle,
  minimumSensitiveBodyWords
} from './thin-sensitive-page-rules.mjs';

const words = (count) =>
  Array.from({ length: count }, (_, index) => `woord${index + 1}`).join(' ');
const article = ({
  slug = 'voorbeeld',
  title = 'Voorbeeld',
  description = 'Een gewone vergelijking zonder gevoelig onderwerp.',
  draft = false,
  body = words(150)
} = {}) => `---
title: "${title}"
slug: ${slug}
description: "${description}"
draft: ${draft}
---
${body}
`;

const cases = [
  {
    name: '149-word nutrition page fails',
    input: article({
      slug: 'persoonlijke-voeding',
      title: 'Persoonlijke voeding vergeleken',
      body: words(149)
    }),
    expected: true
  },
  {
    name: '150-word nutrition page passes the thinness floor',
    input: article({
      slug: 'persoonlijke-voeding',
      title: 'Persoonlijke voeding vergeleken',
      body: words(150)
    }),
    expected: false
  },
  {
    name: 'draft sensitive page is outside the published floor',
    input: article({
      slug: 'reisverzekering-vergelijken',
      title: 'Reisverzekering vergelijken',
      draft: true,
      body: words(20)
    }),
    expected: false
  },
  {
    name: 'thin nonsensitive page is not mislabeled',
    input: article({
      slug: 'video-editor-vergelijken',
      title: 'Video editors vergelijken',
      body: words(20)
    }),
    expected: false
  },
  {
    name: 'frontmatter does not inflate body count',
    input: article({
      slug: 'juridisch-advies',
      title: `Juridisch advies ${words(200)}`,
      body: words(3)
    }),
    expected: true
  },
  {
    name: 'real-estate comparison is treated as consequential',
    input: article({
      slug: 'makelaars-vastgoed',
      title: 'Makelaars en vastgoed',
      body: words(40)
    }),
    expected: true
  },
  {
    name: 'savings comparison is treated as financial',
    input: article({
      slug: 'spaarrekeningen',
      title: 'Spaarrekeningen vergelijken',
      body: words(40)
    }),
    expected: true
  },
  {
    name: 'privacy comparison is treated as legal/privacy',
    input: article({
      slug: 'privacy-tools',
      title: 'Privacy tools vergelijken',
      body: words(40)
    }),
    expected: true
  },
  {
    name: 'markdown links preserve visible anchor words only',
    input: article({
      slug: 'voeding',
      title: 'Voeding',
      body: `[Bron met woorden](${words(250)}) ${words(145)}`
    }),
    expected: true
  },
  {
    name: 'body-only sensitive term does not relabel a generic comparison',
    input: `# Juridisch\n\n${words(20)}`,
    expected: false
  }
];

const failures = [];
for (const testCase of cases) {
  const actual = inspectThinSensitiveArticle(
    `${testCase.name}.md`,
    testCase.input
  ).finding;
  if (actual !== testCase.expected) {
    failures.push({
      name: testCase.name,
      expected: testCase.expected,
      actual
    });
  }
}

const exactCount = countBodyWords(words(minimumSensitiveBodyWords));
if (exactCount !== minimumSensitiveBodyWords) {
  failures.push({
    name: 'word counter boundary',
    expected: minimumSensitiveBodyWords,
    actual: exactCount
  });
}

console.log(
  JSON.stringify(
    {
      schema: 'dutch-ai-tools-thin-sensitive-page-tests-v0.1',
      cases: cases.length + 1,
      failures,
      passed: failures.length === 0
    },
    null,
    2
  )
);
process.exitCode = failures.length === 0 ? 0 : 1;
