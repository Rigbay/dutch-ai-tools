import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const toolSchema = z.object({
  name: z.string(),
  verdict: z.string(),
  priceRange: z.string(),
  bestFor: z.string(),
  rating: z.number().min(1).max(5).optional(),
  affiliateLink: z.string().min(1)
});

const comparisonSchema = z.object({
    presentation: z.literal('comparison').optional(),
    metaTitle: z.string().optional(),
    title: z.string(),
    slug: z.string(),
    description: z.string().min(80).max(180),
    category: z.enum(['productiviteit', 'marketing', 'creatie', 'development', 'business', 'technologie', 'huis-tuin', 'persoonlijk']),
    rating: z.number().min(1).max(5).optional(),
    priceRange: z.string(),
    pros: z.array(z.string()).min(2),
    cons: z.array(z.string()).min(2),
    affiliateLinks: z.array(z.string().min(1)).min(1),
    date: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    modelYear: z.number(),
    featuredTool: z.string(),
    readingTime: z.string(),
    tools: z.array(toolSchema).min(3),
    related: z.array(z.string()).min(1).max(3),
    draft: z.boolean().default(false),
    faq: z.array(z.object({
      q: z.string(),
      a: z.string()
    })).min(3)
});

// Guides carry no product ratings, prices or provider cards. Comparisons retain
// their existing requirements (including at least three tools).
const guideSchema = comparisonSchema.omit({
  presentation: true, rating: true, priceRange: true, pros: true, cons: true,
  affiliateLinks: true, featuredTool: true, readingTime: true, tools: true
}).extend({
  presentation: z.literal('guide'),
  rating: z.never().optional(),
  priceRange: z.never().optional(),
  featuredTool: z.never().optional(),
  readingTime: z.never().optional(),
  affiliateLinks: z.array(z.string()).max(0).default([]),
  tools: z.array(toolSchema).max(0).default([])
});

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.union([guideSchema, comparisonSchema])
});

export const collections = { articles };
