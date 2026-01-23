# Badge & Tag Components

## Overview

Badges and tags are small UI elements that convey status, category, or metadata. They should be used sparingly and purposefully.

---

## Trust Badges

### Current Implementation

**Problem**: Trust badges are `div` elements without semantic meaning.

```html
<div class="trust-badge">
  <div class="trust-badge-icon">
    <svg>...</svg>
  </div>
  <span>Made in France</span>
</div>
```

**Refactor Needed**: Convert to semantic HTML.

---

### Refactored Trust Badges

```css
.trust-badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-5);
  justify-content: center;
}

.trust-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-5);
  background: var(--white);
  border: 1px solid var(--gold-200);
  border-radius: var(--radius-lg);
  min-width: 130px;
  text-align: center;
  transition:
    transform var(--transition-normal),
    box-shadow var(--transition-normal),
    border-color var(--transition-normal);
}

.trust-badge:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-soft);
  border-color: var(--sage-300);
}

.trust-badge-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--sage-400);
}

.trust-badge-icon svg {
  width: 26px;
  height: 26px;
}

.trust-badge-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--charcoal-200);
  line-height: var(--leading-normal);
}
```

### Semantic HTML Structure

**Option 1: Using DL (Description List)**

```html
<dl class="trust-badges">
  <div class="trust-badge">
    <dt class="trust-badge-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
    </dt>
    <dd class="trust-badge-label">Made in France</dd>
  </div>

  <div class="trust-badge">
    <dt class="trust-badge-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M12 2L15 8L22 9L17 14L18 21L12 18L6 21L7 14L2 9L9 8L12 2Z"/>
      </svg>
    </dt>
    <dd class="trust-badge-label">Premium Quality</dd>
  </div>

  <!-- more badges -->
</dl>
```

**Option 2: Using Figure**

```html
<figure class="trust-badge">
  <div class="trust-badge-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  </div>
  <figcaption class="trust-badge-label">Made in France</figcaption>
</figure>
```

---

## Article Tags

### Category Tags

```css
.article-tag {
  display: inline-block;
  font-size: var(--text-xs);
  font-weight: 500;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-full);
  background: var(--cream-100);
  color: var(--sage-600);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  text-decoration: none;
  transition:
    background var(--transition-quick),
    color var(--transition-quick);
}

.article-tag:hover {
  background: var(--sage-100);
  color: var(--sage-700);
}

/* Product tag variant */
.article-tag.product {
  background: var(--gradient-gold);
  color: var(--charcoal-200);
}
```

**Usage**:
```html
<div class="article-meta">
  <span class="article-tag">Herbal Remedies</span>
  <span class="article-tag product">Lavender Balm</span>
  <span class="reading-time">8 min read</span>
</div>
```

---

## Reading Time Badge

```css
.reading-time {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  color: var(--charcoal-50);
  background: var(--cream-200);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-full);
}

.reading-time::before {
  content: '📖';
  font-size: 10px;
}
```

**Usage**:
```html
<span class="reading-time">8 min</span>
```

---

## Status Badges

### Out of Stock

```css
.badge-out-of-stock {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: var(--cream-300);
  color: var(--charcoal-50);
  font-size: var(--text-xs);
  font-weight: 500;
  border-radius: var(--radius-full);
}
```

### New Arrival

```css
.badge-new {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: var(--sage-400);
  color: var(--white);
  font-size: var(--text-xs);
  font-weight: 500;
  border-radius: var(--radius-full);
}
```

### Bestseller

```css
.badge-bestseller {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: var(--gold-300);
  color: var(--charcoal-200);
  font-size: var(--text-xs);
  font-weight: 500;
  border-radius: var(--radius-full);
}
```

---

## Notification Badges

### Notification Dot

```css
.notification-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  background: var(--sage-500);
  border-radius: 50%;
  border: 2px solid var(--white);
}
```

### Notification Count

```css
.notification-count {
  position: absolute;
  top: -8px;
  right: -8px;
  min-width: 18px;
  height: 18px;
  background: var(--sage-500);
  color: var(--white);
  font-size: 10px;
  font-weight: 600;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}
```

---

## Featured Badge

```css
.badge-featured {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  background: var(--gradient-sage);
  color: var(--white);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-soft);
}

.badge-featured svg {
  width: 12px;
  height: 12px;
}
```

**Usage**:
```html
<span class="badge-featured">
  <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
    <path d="M8 1L10 5.5L15 6L11.5 9.5L12.5 14.5L8 12L3.5 14.5L4.5 9.5L1 6L6 5.5L8 1Z"/>
  </svg>
  Featured
</span>
```

---

## Accessibility for Badges

### Hide Decorative Icons

```html
<span class="badge-featured">
  <svg aria-hidden="true" viewBox="0 0 16 16" fill="currentColor">
    <path d="M8 1L10 5.5L15 6L11.5 9.5L12.5 14.5L8 12L3.5 14.5L4.5 9.5L1 6L6 5.5L8 1Z"/>
  </svg>
  <span>Featured</span>
</span>
```

### Screen Reader Text

For badges that rely on visual icons:

```html
<div class="trust-badge">
  <div class="trust-badge-icon">
    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <text x="12" y="14" text-anchor="middle" font-size="8" fill="currentColor" stroke="none">FR</text>
    </svg>
  </div>
  <span class="trust-badge-label">Made in France</span>
</div>
```

Or use `aria-label` for context:
```html
<div class="trust-badge" role="note" aria-label="Made in France - certified French origin">
  ...
</div>
```

---

## Badge Sizes

### Small

```css
.badge-sm {
  padding: var(--space-1) var(--space-2);
  font-size: var(--text-xs);
}
```

### Medium (Default)

```css
.badge-md {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-xs);
}
```

### Large

```css
.badge-lg {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
}
```

---

## Badge Placement

### On Card

```css
.card-with-badge {
  position: relative;
}

.card-badge {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  z-index: 1;
}
```

### On Image

```css
.image-with-badge {
  position: relative;
  overflow: hidden;
}

.image-badge {
  position: absolute;
  bottom: var(--space-3);
  left: var(--space-3);
  z-index: 1;
}
```

---

## Color Variants (Use Sparingly)

For product category color coding:

```css
.badge-citrus {
  background: var(--color-citrus);
  color: var(--white);
}

.badge-warm {
  background: var(--color-warm);
  color: var(--white);
}

.badge-herbal {
  background: var(--color-herbal);
  color: var(--white);
}

.badge-floral {
  background: var(--color-floral);
  color: var(--white);
}
```

**Guideline**: Use category colors very sparingly. Too many colors create visual noise.
