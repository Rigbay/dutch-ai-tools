/** ArticleLayout owns the page h1. Keep body heading text and slugs intact. */
export default function remarkArticleHeadings() {
  return function transform(tree) {
    function visit(node) {
      // A few legacy articles use standalone HTML headings to pin old anchors.
      // Convert the plain-text form so Astro includes it in rendered headings.
      // Leave complex HTML untouched rather than guessing at its semantics.
      if (node.type === 'html') {
        const heading = /^<h([1-6])\s+id="([^"]+)">([^<&]*)<\/h\1>$/.exec(node.value.trim());
        if (heading) {
          node.type = 'heading';
          node.depth = Number(heading[1]);
          node.data = { hProperties: { id: heading[2] } };
          node.children = [{ type: 'text', value: heading[3] }];
          delete node.value;
        }
      }
      if (node.type === 'heading' && node.depth === 1) node.depth = 2;
      if (node.type === 'table') {
        node.data = { ...node.data, hProperties: {
          ...node.data?.hProperties,
          tabIndex: 0,
          ariaLabel: 'Vergelijkingstabel, horizontaal scrollbaar',
        } };
      }
      if (Array.isArray(node.children)) {
        node.children = node.children.filter(child => child.type !== 'heading' || child.children.length > 0);
        node.children.forEach(visit);
      }
    }
    visit(tree);
  };
}
