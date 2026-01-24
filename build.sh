#!/bin/bash
set -e

echo "Installing dependencies..."
pip install requests aiohttp

echo "Generating articles (4 products, all languages)..."
python blog.py daily

echo "Generating sitemap..."
node scripts/generate-sitemap.js

echo "Building site..."
npm run build

echo "Build complete!"
