import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './articles' }),
  schema: z.object({
    title: z.string(),
    body: z.string(),
    product: z.string(),
    product_name: z.string(),
    product_link: z.string(),
    product_image: z.string(),
    language: z.string(),
    language_name: z.string(),
    angle: z.string(),
    slug: z.string(),
    generated_at: z.string(),
    season: z.string(),
    variation_seed: z.string().optional(),
    useless_detail: z.string().optional(),
    random_tangent: z.string().optional()
  })
});

export const collections = { articles };
