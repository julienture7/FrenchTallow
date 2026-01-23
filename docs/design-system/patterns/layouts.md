# Layout Patterns

## Overview

Layout patterns define the structural framework for content organization. This site uses **responsive grid systems** with **fluid containers** and **asymmetric compositions**.

---

## Container System

### Max-Width Containers

```css
.container {
  width: 100%;
  max-width: var(--container-xl);  /* 1440px */
  margin: 0 auto;
  padding: 0 var(--container-padding-fluid);
}

.container-sm {
  max-width: var(--container-sm);  /* 640px */
}

.container-md {
  max-width: var(--container-md);  /* 960px */
}

.container-lg {
  max-width: var(--container-lg);  /* 1140px */
}
```

**Usage**:
```html
<!-- Standard page container -->
<div class="container">
  <!-- content -->
</div>

<!-- Narrow content (article) -->
<div class="container container-md">
  <!-- article content -->
</div>
```

---

## Grid Systems

### Product Grid (Current - Post-Refactor)

**Current Problem**: All products in identical auto-fill grid.

```css
/* CURRENT - Generic, monotonous */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: var(--space-6);
}
```

**Refactor Needed**: Varied sizes, asymmetric layout.

---

### Product Grid (Refactored - Asymmetric)

```css
/* REFACTORED - Varied, asymmetric */
.products-grid-asymmetric {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6);
}

/* Featured product - 6 columns (half width) */
.product-card-featured {
  grid-column: span 6;
  grid-row: span 2;
}

/* Standard products - 3 columns (quarter width) */
.product-card-standard {
  grid-column: span 3;
}

/* Compact products - 2 columns (sixth width) */
.product-card-compact {
  grid-column: span 2;
}

@media (max-width: 1024px) {
  .product-card-featured { grid-column: span 6; }
  .product-card-standard { grid-column: span 3; }
  .product-card-compact { grid-column: span 3; }
}

@media (max-width: 768px) {
  .products-grid-asymmetric {
    grid-template-columns: repeat(6, 1fr);
  }

  .product-card-featured { grid-column: span 6; }
  .product-card-standard { grid-column: span 3; }
  .product-card-compact { grid-column: span 2; }
}

@media (max-width: 480px) {
  .products-grid-asymmetric {
    grid-template-columns: 1fr;
  }

  .product-card-featured,
  .product-card-standard,
  .product-card-compact {
    grid-column: span 1;
  }
}
```

---

### Article Grid

```css
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
}

/* Featured article spans 2 columns */
.article-card-featured {
  grid-column: span 2;
}

@media (max-width: 768px) {
  .article-card-featured {
    grid-column: span 1;
  }
}
```

---

## Section Spacing

### Vertical Rhythm

```css
.section {
  padding: var(--section-padding-fluid) 0;
}

.section-tight {
  padding: var(--section-padding-sm) 0;
}

.section-spacious {
  padding: var(--section-padding-lg) 0;
}
```

**Values**:
```css
--section-padding-sm: var(--space-12);   /* 48px */
--section-padding-md: var(--space-20);   /* 80px */
--section-padding-lg: var(--space-24);   /* 96px */
--section-padding-fluid: clamp(var(--space-12), 8vw, var(--space-24)); /* 48px - 96px */
```

---

## Section Layout Patterns

### Centered Section (Classic)

```css
.section-centered {
  max-width: var(--container-md);
  margin: 0 auto;
  padding: var(--section-padding-fluid) var(--container-padding-fluid);
  text-align: center;
}
```

**Usage**: Hero, about text, simple content sections.

---

### Two-Column Section

```css
.section-two-column {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-12);
  padding: var(--section-padding-fluid) var(--container-padding-fluid);
}

@media (max-width: 768px) {
  .section-two-column {
    grid-template-columns: 1fr;
    gap: var(--space-8);
  }
}
```

**Usage**: Product spotlight (image left, text right).

---

### Asymmetric Section (Refined Minimal)

```css
.section-asymmetric {
  display: grid;
  grid-template-columns: 1.5fr 1fr;  /* Left column wider */
  gap: var(--space-12);
  padding: var(--section-padding-fluid) var(--container-padding-fluid);
}

@media (max-width: 768px) {
  .section-asymmetric {
    grid-template-columns: 1fr;
  }
}
```

**Usage**: Hero with text left, image right (refined minimal approach).

---

### Zigzag Section

Alternating image/text positions:

```css
.zigzag-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-12);
  padding: var(--section-padding-fluid) var(--container-padding-fluid);
}

.zigzag-section.reverse {
  direction: rtl;  /* Image left, text right */
}

.zigzag-section.reverse > * {
  direction: ltr;  /* Reset text direction */
}

@media (max-width: 768px) {
  .zigzag-section,
  .zigzag-section.reverse {
    grid-template-columns: 1fr;
    direction: ltr;
  }
}
```

**Usage**: Alternating product features, story sections.

---

## Hero Layout Patterns

### Centered Hero (Current)

**Problem**: Too centered, lacks sophistication.

```css
.hero-centered {
  padding: clamp(var(--space-12), 8vw, var(--space-28)) var(--container-padding-fluid);
  text-align: center;
  background: var(--gradient-hero);
}
```

---

### Left-Aligned Hero (Refined Minimal)

```css
.hero-left-aligned {
  padding: clamp(var(--space-12), 8vw, var(--space-28)) var(--container-padding-fluid);
  background: var(--gradient-hero);
  position: relative;
  overflow: hidden;
}

.hero-content {
  max-width: 600px;
  text-align: left;
}

.hero-image {
  position: absolute;
  right: -5%;
  top: 50%;
  transform: translateY(-50%);
  width: 50%;
  max-width: 600px;
  opacity: 0.9;
}

@media (max-width: 1024px) {
  .hero-left-aligned {
    text-align: center;
  }

  .hero-content {
    max-width: 100%;
    margin: 0 auto;
  }

  .hero-image {
    position: relative;
    right: auto;
    top: auto;
    transform: none;
    width: 100%;
    max-width: 400px;
    margin: var(--space-8) auto 0;
  }
}
```

**HTML**:
```html
<section class="hero-left-aligned">
  <div class="hero-content">
    <span class="badge-featured">Made in France</span>
    <h1>Skincare Your Skin<br>Recognizes</h1>
    <p class="hero-description">
      Handcrafted whipped tallow balms from grass-fed beef suet.
      Pure, natural skincare that nourishes and protects.
    </p>
    <a href="#products" class="button-primary button-lg">
      Explore Our Collection
    </a>
  </div>
  <img class="hero-image" src="/assets/images/hero-product.png" alt="Featured Product">
</section>
```

---

## Navigation Layouts

### Sticky Header

```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
}
```

### Condensed on Scroll

```css
.site-header {
  transition:
    padding var(--transition-normal),
    box-shadow var(--transition-normal);
}

.site-header.scrolled {
  padding-top: var(--space-4);
  padding-bottom: var(--space-4);
  box-shadow: var(--shadow-subtle);
}
```

---

## Card Grid Patterns

### Masonry Layout (Pinterest-style)

```css
.grid-masonry {
  column-count: 3;
  column-gap: var(--space-6);
}

@media (max-width: 1024px) {
  .grid-masonry {
    column-count: 2;
  }
}

@media (max-width: 640px) {
  .grid-masonry {
    column-count: 1;
  }
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: var(--space-6);
}
```

### Flex Grid (Wrapping)

```css
.grid-flex {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
}

.flex-item {
  flex: 1 1 calc(33.333% - var(--space-6));  /* 3 columns with gap */
  min-width: 250px;
}

@media (max-width: 768px) {
  .flex-item {
    flex: 1 1 calc(50% - var(--space-6));  /* 2 columns */
  }
}

@media (max-width: 480px) {
  .flex-item {
    flex: 1 1 100%;  /* 1 column */
  }
}
```

---

## Overlay Layouts

### Full-Width Overlay

```css
.overlay-section {
  position: relative;
  height: 80vh;
  min-height: 400px;
  background: url(/images/hero.jpg) center/cover no-repeat;
}

.overlay-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(45, 45, 45, 0.3),
    rgba(45, 45, 45, 0.7)
  );
}

.overlay-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: var(--white);
  padding: var(--space-6);
}
```

---

## Split Layouts

### Split Screen (50/50)

```css
.split-screen {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}

.split-screen-left,
.split-screen-right {
  padding: var(--space-12);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.split-screen-left {
  background: var(--cream-100);
}

.split-screen-right {
  background: var(--white);
}

@media (max-width: 768px) {
  .split-screen {
    grid-template-columns: 1fr;
  }
}
```

---

## Responsive Breakpoints

### Mobile-First Approach

```css
/* Mobile (default) */
.component {
  /* Mobile styles */
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .component {
    /* Tablet styles */
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .component {
    /* Desktop styles */
  }
}

/* Wide (1440px+) */
@media (min-width: 1440px) {
  .component {
    /* Wide styles */
  }
}
```

### Container Queries (Future)

```css
.product-card {
  container-type: inline-size;
}

/* Compact when container is narrow */
@container (max-width: 300px) {
  .product-card {
    /* Compact card styles */
  }
}

/* Standard when container is wider */
@container (min-width: 300px) {
  .product-card {
    /* Standard card styles */
  }
}
```

---

## Layout Utilities

### Alignment

```css
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }

.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }
```

### Gap Utilities

```css
.gap-sm { gap: var(--space-4); }
.gap-md { gap: var(--space-6); }
.gap-lg { gap: var(--space-8); }
.gap-xl { gap: var(--space-12); }
```

### Padding Utilities

```css
.p-sm { padding: var(--space-4); }
.p-md { padding: var(--space-6); }
.p-lg { padding: var(--space-8); }
.p-xl { padding: var(--space-12); }
```
