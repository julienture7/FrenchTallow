import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SITE_URL = 'https://frenchtallow.com';
const articlesDir = path.join(__dirname, '..', 'articles');
const publicDir = path.join(__dirname, '..', 'public');
const sitemapPath = path.join(publicDir, 'sitemap.xml');

// Supported languages
const languages = ['bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv'];

async function generateSitemap() {
  const urls = [];

  // Homepage
  urls.push({ loc: `${SITE_URL}/`, changefreq: 'daily', priority: '1.0' });

  // Language homepages
  for (const lang of languages) {
    urls.push({ loc: `${SITE_URL}/${lang}/`, changefreq: 'daily', priority: '0.9' });
  }

  // Read all article JSON files
  const articleFiles = fs.readdirSync(articlesDir).filter(f => f.endsWith('.json'));

  for (const file of articleFiles) {
    const filePath = path.join(articlesDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    const article = JSON.parse(content);

    urls.push({
      loc: `${SITE_URL}/articles/${article.slug}/`,
      changefreq: 'weekly',
      priority: '0.8'
    });
  }

  // Generate XML
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(url => `  <url>
    <loc>${url.loc}</loc>
    <changefreq>${url.changefreq}</changefreq>
    <priority>${url.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  // Ensure public directory exists
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }

  // Write sitemap.xml
  fs.writeFileSync(sitemapPath, xml, 'utf-8');

  console.log(`✅ Generated sitemap.xml with ${urls.length} URLs`);
}

generateSitemap().catch(console.error);
