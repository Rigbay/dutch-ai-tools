import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import remarkArticleHeadings from '../src/lib/remarkArticleHeadings.mjs';
import { createMarkdownProcessor } from '@astrojs/markdown-remark';

const read = path => fs.readFileSync(fileURLToPath(new URL(`../${path}`, import.meta.url)), 'utf8');
const homepage = read('src/pages/index.astro');
const layout = read('src/layouts/ArticleLayout.astro');
const base = read('src/layouts/BaseLayout.astro');

// Preserve the accepted task destinations while allowing the design to evolve.
for (const destination of ['/beste-ai-chatbots-2026/', '/categorie/productiviteit/', '/beste-ai-automation-tools-2026/']) {
  assert.ok(homepage.includes(`href: '${destination}'`), `Missing task destination: ${destination}`);
}
assert.match(homepage, /coreCategories = \[[^\]]*'development'/);
assert.ok(homepage.includes('href: `/categorie/${category}/`'));
assert.ok(layout.includes('href={`#${heading.slug}`}'), 'Reading links must use rendered heading IDs');
assert.ok(base.includes('href="#main-content"') && base.includes('id="main-content"'), 'Skip link must have a destination');

// The heading normalization changes semantics only, including nested Markdown,
// and leaves text/link nodes and already-correct heading levels unchanged.
const tree = {type:'root',children:[
  {type:'heading',depth:1,children:[{type:'text',value:'A & B'}]},
  {type:'heading',depth:2,children:[{type:'link',url:'#source',children:[{type:'text',value:'Sources'}]}]},
  {type:'blockquote',children:[{type:'heading',depth:1,children:[{type:'text',value:'Nested'}]}]},
]};
const expected = structuredClone(tree);
expected.children[0].depth = 2;
expected.children[2].children[0].depth = 2;
remarkArticleHeadings()(tree);
assert.deepEqual(tree, expected);
const legacy = {type:'root',children:[
  {type:'html',value:'<h2 id="tool-voor-tool">Tool voor tool: de echte afweging</h2>'},
  {type:'heading',depth:1,children:[]},
  {type:'html',value:'<h2 id="complex"><em>Preserve HTML</em></h2>'},
]};
remarkArticleHeadings()(legacy);
assert.equal(legacy.children.length, 2);
assert.equal(legacy.children[0].data.hProperties.id, 'tool-voor-tool');
assert.equal(legacy.children[0].children[0].value, 'Tool voor tool: de echte afweging');
assert.equal(legacy.children[1].value, '<h2 id="complex"><em>Preserve HTML</em></h2>');
const markdown = await createMarkdownProcessor({ remarkPlugins: [remarkArticleHeadings] });
const rendered = await markdown.render('# Article body\n\n<h2 id="tool-voor-tool">Tool voor tool</h2>\n\n#\n');
assert.deepEqual(rendered.metadata.headings.map(({depth,slug}) => ({depth,slug})), [
  {depth:2,slug:'article-body'}, {depth:2,slug:'tool-voor-tool'},
]);
console.log('Task routes, category access, reading anchors, skip navigation and heading normalization passed.');
