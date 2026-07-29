const markdownLinkPattern = /\]\(\/([^)\s?#]+)(?:[?#][^)]*)?\)/g;

export const extractInternalArticleLinks = (text) =>
  [...text.matchAll(markdownLinkPattern)].map((match) => ({
    slug: match[1].replace(/\/+$/, ''),
    index: match.index
  }));
