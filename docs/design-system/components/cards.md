# Card Components

## Overview

Cards are the primary content containers for products and articles. The current implementation uses a **generic card grid** pattern that needs to be refactored into varied, asymmetric layouts for the refined minimal aesthetic.

---

## Current Card System (Pre-Refactor)

### Product Card

**Issues**: All cards same size, centered content, generic grid placement.

```css
.product-card {
  background: var(--white);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  text-align: center;  /* CENTERED - needs left-align */
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 1px solid var(--gold-200);
  box-shadow: var(--shadow-subtle);
  position: relative;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-elevated);
  border-color: var(--sage-300);
}

.product-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-sage);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.product-card:hover::before {
  opacity: 1;
}
```

**HTML Structure**:
```html
<div class="product-card">
  <div class="product-image-wrapper">
    <img src="/assets/images/whipped-tallow-cream-lemon.png" alt="Whipped Tallow Balm - Lemon">
    <div class="product-overlay">
      <span class="shop-btn">Shop Now</span>
    </div>
  </div>
  <h3>Whipped Tallow Balm - Lemon</h3>
  <p class="product-benefits">uplifting, brightening, energizing</p>
</div>
```

**Problems**:
- Uses `div` with `onclick` instead of `<a>` tag (not keyboard accessible)
- All cards identical size (no variation)
- Centered text (should be left-aligned)
- Generic grid placement (no featured/standard/compact variants)

---

### Article Card

**Issues**: Same as product cards—generic, identical, centered.

```css
.article-card {
  background: var(--white);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all var(--transition-normal);
  border: 1px solid var(--gold-200);
  cursor: pointer;
  position: relative;
  box-shadow: var(--shadow-subtle);
}

.article-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 5px;
  background: var(--gradient-sage);
  border-radius: var(--radius-xl) 0 0 var(--radius-xl);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.article-card:hover::before {
  opacity: 1;
}
```

---

## Refactored Card System (Post-Redesign)

### Design Principles for New Cards

1. **Varied Sizes**: Featured, standard, compact variants
2. **Left-Aligned**: Text left-aligned, not centered
3. **Semantic HTML**: Use `<a>` tags, not `div` with `onclick`
4. **Asymmetric Layout**: Break the grid, varied positioning
5. **Image-First**: Let product photography be the hero

---

## Product Card Variants

### Featured Product Card (Large, Hero Treatment)

**Usage**: Hero spotlight, "Product of the Month", bestseller highlight.

```css
.product-card-featured {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  background: var(--cream-50);
  border-radius: var(--radius-2xl);
  padding: var(--space-12);
  text-align: left;
  border: 1px solid var(--gold-200);
  box-shadow: var(--shadow-medium);
}

@media (max-width: 768px) {
  .product-card-featured {
    grid-template-columns: 1fr;
    padding: var(--space-6);
  }
}

.product-card-featured .product-image {
  aspect-ratio: 1;
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--cream-200);
}

.product-card-featured .product-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.product-card-featured h3 {
  font-size: var(--text-3xl);
  margin-bottom: var(--space-3);
}

.product-card-featured .price {
  font-size: var(--text-xl);
  font-weight: 500;
  color: var(--sage-600);
  margin-bottom: var(--space-4);
}

.product-card-featured .description {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--charcoal-50);
  margin-bottom: var(--space-6);
}
```

**HTML**:
```html
<a href="https://etsy.com/..." class="product-card-featured">
  <div class="product-image">
    <img src="/assets/images/whipped-tallow-cream-lavender.png" alt="Whipped Tallow Balm - Lavender">
  </div>
  <div class="product-content">
    <span class="product-tag">This Week's Favorite</span>
    <h3>Whipped Tallow Balm - Lavender</h3>
    <p class="price">€21.00 · 60ml</p>
    <p class="description">Our calming lavender balm is perfect for evening routines. French lavender promotes relaxation and restful sleep.</p>
    <span class="button-primary">Shop on Etsy →</span>
  </div>
</a>
```

---

### Standard Product Card (Default)

**Usage**: Main product grid, standard product display.

```css
.product-card-standard {
  background: var(--white);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  text-align: left;
  border: 1px solid var(--gold-200);
  box-shadow: var(--shadow-subtle);
  transition:
    transform var(--transition-normal),
    box-shadow var(--transition-normal);
}

.product-card-standard:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-elevated);
  border-color: var(--sage-300);
}

.product-card-standard .product-image {
  aspect-ratio: 1;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--cream-200);
  margin-bottom: var(--space-4);
}

.product-card-standard h3 {
  font-size: var(--text-lg);
  font-weight: 500;
  margin-bottom: var(--space-2);
}

.product-card-standard .price {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--sage-600);
  margin-bottom: var(--space-3);
  display: block;
}

.product-card-standard .benefits {
  font-size: var(--text-sm);
  color: var(--charcoal-50);
}

.product-card-standard .cta {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  margin-top: var(--space-3);
  color: var(--sage-400);
  font-size: var(--text-sm);
  font-weight: 500;
}
```

**HTML**:
```html
<a href="https://etsy.com/..." class="product-card-standard">
  <div class="product-image">
    <img src="/assets/images/whipped-tallow-cream-lemon.png" alt="Whipped Tallow Balm - Lemon" loading="lazy">
  </div>
  <h3>Lemon</h3>
  <span class="price">€21.00 · 60ml</span>
  <p class="benefits">uplifting, brightening, energizing</p>
  <span class="cta">View on Etsy →</span>
</a>
```

---

### Compact Product Card (Small)

**Usage**: Related products, "You might also like", grid with many items.

```css
.product-card-compact {
  background: var(--white);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
  text-align: left;
  border: 1px solid var(--gold-200);
  transition:
    transform var(--transition-quick),
    box-shadow var(--transition-quick);
}

.product-card-compact:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-soft);
}

.product-card-compact .product-image {
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--cream-200);
  margin-bottom: var(--space-2);
}

.product-card-compact h3 {
  font-size: var(--text-sm);
  font-weight: 500;
  margin-bottom: var(--space-1);
}

.product-card-compact .price {
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--sage-600);
}
```

---

## Article Card Variants

### Featured Article Card (Horizontal)

**Usage**: Hero article, featured story, spotlight content.

```css
.article-card-featured {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--space-6);
  background: var(--white);
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--gold-200);
  box-shadow: var(--shadow-medium);
}

@media (max-width: 768px) {
  .article-card-featured {
    grid-template-columns: 1fr;
  }
}

.article-card-featured .article-image {
  aspect-ratio: 4/3;
  background: var(--cream-200);
}

.article-card-featured .article-content {
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.article-card-featured .article-meta {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.article-card-featured h3 {
  font-size: var(--text-2xl);
  font-weight: 500;
  line-height: var(--leading-snug);
  margin-bottom: var(--space-3);
}

.article-card-featured .excerpt {
  font-size: var(--text-base);
  color: var(--charcoal-50);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-4);
}
```

**HTML**:
```html
<a href="/articles/..." class="article-card-featured">
  <div class="article-image">
    <img src="/images/article-hero.jpg" alt="Article feature image">
  </div>
  <div class="article-content">
    <div class="article-meta">
      <span class="tag">Herbal Remedies</span>
      <span class="reading-time">8 min read</span>
    </div>
    <h3>The Ancient Art of Tallow: A Complete Guide</h3>
    <p class="excerpt">Discover why traditional tallow balms are making a comeback in modern skincare...</p>
    <span class="cta">Read full story →</span>
  </div>
</a>
```

---

### Standard Article Card (Vertical)

**Usage**: Article grid, blog listing.

```css
.article-card-standard {
  background: var(--white);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  border: 1px solid var(--gold-200);
  box-shadow: var(--shadow-subtle);
  transition:
    transform var(--transition-normal),
    box-shadow var(--transition-normal);
  text-align: left;
}

.article-card-standard:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-elevated);
  border-color: var(--sage-300);
}

.article-card-standard .article-meta {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin-bottom: var(--space-3);
}

.article-card-standard h3 {
  font-size: var(--text-xl);
  font-weight: 500;
  line-height: var(--leading-snug);
  margin-bottom: var(--space-3);
}

.article-card-standard .excerpt {
  font-size: var(--text-sm);
  color: var(--charcoal-50);
  line-height: var(--leading-relaxed);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: var(--space-4);
}

.article-card-standard .article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-4);
  border-top: 1px solid var(--cream-200);
}
```

---

### Minimal Article Card (Compact)

**Usage**: Sidebar, "More articles", compact listings.

```css
.article-card-minimal {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--gold-200);
  transition:
    background var(--transition-quick),
    border-color var(--transition-quick);
}

.article-card-minimal:hover {
  background: var(--cream-50);
  border-color: var(--sage-300);
}

.article-card-minimal .article-image {
  width: 80px;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  background: var(--cream-200);
  flex-shrink: 0;
}

.article-card-minimal .article-content {
  flex: 1;
  min-width: 0;
}

.article-card-minimal h3 {
  font-size: var(--text-base);
  font-weight: 500;
  line-height: var(--leading-snug);
  margin-bottom: var(--space-2);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card-minimal .meta {
  font-size: var(--text-xs);
  color: var(--charcoal-50);
}
```

---

## Card Accessibility

### Semantic HTML

**❌ WRONG** - div with onclick:
```html
<div class="product-card" onclick="window.open('/product')">
  ...
</div>
```

**✅ CORRECT** - proper link:
```html
<a href="/product" class="product-card">
  ...
</a>
```

### Focus States

All cards must have visible focus indication:

```css
.product-card:focus-visible,
.article-card:focus-visible {
  outline: 2px solid var(--sage-500);
  outline-offset: 2px;
}
```

### ARIA Labels

For cards with complex content:

```html
<article class="article-card" aria-labelledby="article-title-1">
  <h3 id="article-title-1">Article Title</h3>
  ...
</article>
```

---

## Card Grid Patterns (Post-Refactor)

### Asymmetric Grid (BREAK THE TEMPLATE)

```css
.products-grid-asymmetric {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6);
}

/* Featured product spans 6 columns */
.products-grid-asymmetric .product-card-featured {
  grid-column: span 6;
}

/* Standard products span 3 columns */
.products-grid-asymmetric .product-card-standard {
  grid-column: span 3;
}

@media (max-width: 1024px) {
  .products-grid-asymmetric .product-card-featured,
  .products-grid-asymmetric .product-card-standard {
    grid-column: span 6;
  }
}

@media (max-width: 768px) {
  .products-grid-asymmetric .product-card-featured,
  .products-grid-asymmetric .product-card-standard {
    grid-column: span 12;
  }
}
```

### Masonry Layout (Varied Heights)

```css
.products-grid-masonry {
  column-count: 3;
  column-gap: var(--space-6);
}

.product-card {
  break-inside: avoid;
  margin-bottom: var(--space-6);
}
```

---

## Migration Path

### Phase 1: Refactor HTML Structure
- Convert `div` with `onclick` to `<a>` tags
- Add semantic heading structure
- Add proper alt text

### Phase 2: Implement New Variants
- Create featured, standard, compact variants
- Add left-aligned content structure
- Implement varied card sizes

### Phase 3: Break the Grid
- Implement asymmetric layouts
- Add zigzag compositions
- Featured spot treatments

### Phase 4: Polish
- Refine hover states
- Add micro-interactions
- Ensure accessibility
