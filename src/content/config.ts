import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const toolSchema = z.object({
  name: z.string(),
  verdict: z.string(),
  priceRange: z.string(),
  bestFor: z.string(),
  rating: z.number().min(1).max(5),
  affiliateLink: z.string().min(1)
});

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string().min(80).max(180),
    category: z.enum(['productiviteit', 'marketing', 'creatie', 'development', 'business']),
    rating: z.number().min(1).max(5),
    priceRange: z.string(),
    pros: z.array(z.string()).min(2),
    cons: z.array(z.string()).min(2),
    affiliateLinks: z.array(z.string().min(1)).min(1),
    date: z.coerce.date(),
    modelYear: z.number(),
    featuredTool: z.string(),
    readingTime: z.string(),
    tools: z.array(toolSchema).min(5),
    related: z.array(z.string()).min(2).max(3),
    draft: z.boolean().default(false),
    faq: z.array(z.object({
      q: z.string(),
      a: z.string()
    })).min(3)
  })
});

export const collections = { articles };
