import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';
import remarkArticleHeadings from './src/lib/remarkArticleHeadings.mjs';

export default defineConfig({
  site: 'https://dutchaitools.nl',
  devToolbar: { enabled: false },
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date()
    }),
    tailwind({
      applyBaseStyles: false
    })
  ],
  markdown: {
    remarkPlugins: [remarkArticleHeadings],
    shikiConfig: {
      theme: 'github-light'
    }
  },
  trailingSlash: 'always'
});
