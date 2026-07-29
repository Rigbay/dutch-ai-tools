export const minimumSensitiveBodyWords = 150;

export const sensitiveTopicRules = [
  {
    id: 'health-nutrition',
    pattern:
      /\b(?:voeding|dieet|maaltijdplanning|gezondheid|medische?|mindfulness|meditatie)\b/giu
  },
  {
    id: 'financial-savings-insurance',
    pattern:
      /\b(?:spaarrekeningen?|spaargeld|deposito|reisverzekering|verzekeringen?|rente|budgetteren|beleggen|investeren)\b/giu
  },
  {
    id: 'legal-privacy',
    pattern:
      /\b(?:juridisch|juridische|legal[\s-]?tech|advocaten?|notarissen?|contractanalyse|compliance|privacy|avg)\b/giu
  },
  {
    id: 'real-estate-financial-legal',
    pattern:
      /\b(?:makelaars?|vastgoed|woningwaardering|huizenprijzen|waardebepaling)\b/giu
  }
];

const splitArticle = (text) => {
  const match = text.match(/^---\s*\r?\n([\s\S]*?)\r?\n---\s*(?:\r?\n)?/);
  if (!match) {
    return { yaml: '', body: text };
  }

  return {
    yaml: match[1],
    body: text.slice(match[0].length)
  };
};

const field = (yaml, name) => {
  const match = yaml.match(
    new RegExp(`^${name}:\\s*['"]?([^\\r\\n'"]+)`, 'mi')
  );
  return match?.[1]?.trim() || null;
};

const isDraft = (yaml) => /^draft:\s*true\s*$/mi.test(yaml);

export const countBodyWords = (body) => {
  const plainText = body
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`[^`]*`/g, ' ')
    .replace(/!\[[^\]]*]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]+)]\([^)]*\)/g, '$1')
    .replace(/<[^>]+>/g, ' ')
    .replace(/https?:\/\/\S+/g, ' ');

  return plainText.match(/[\p{L}\p{N}]+(?:['’.-][\p{L}\p{N}]+)*/gu)?.length || 0;
};

export const inspectThinSensitiveArticle = (file, text) => {
  const { yaml, body } = splitArticle(text);
  const slug = field(yaml, 'slug') || file.replace(/\.md$/i, '');
  const title = field(yaml, 'title') || '';
  const description = field(yaml, 'description') || '';
  const topicText = `${slug} ${title} ${description}`;
  const sensitiveRuleIds = [];

  for (const rule of sensitiveTopicRules) {
    if (rule.pattern.test(topicText)) {
      sensitiveRuleIds.push(rule.id);
    }
    rule.pattern.lastIndex = 0;
  }

  const wordCount = countBodyWords(body);
  const draft = isDraft(yaml);

  return {
    file,
    slug,
    title,
    draft,
    wordCount,
    sensitiveRuleIds,
    finding:
      !draft &&
      sensitiveRuleIds.length > 0 &&
      wordCount < minimumSensitiveBodyWords
  };
};
