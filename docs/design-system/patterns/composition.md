# Composition Patterns

## Overview

Composition patterns define how visual elements are arranged to create hierarchy, focus, and visual interest. The refined minimal aesthetic relies on **asymmetric compositions**, **generous whitespace**, and **typography-driven layouts**.

---

## Visual Hierarchy Principles

### Hierarchy Through Scale

```css
/* Level 1: Most important */
.hierarchy-primary {
  font-size: var(--text-h1);
  font-weight: 600;
  line-height: var(--leading-tight);
}

/* Level 2: Secondary */
.hierarchy-secondary {
  font-size: var(--text-h2);
  font-weight: 500;
  line-height: var(--leading-snug);
}

/* Level 3: Tertiary */
.hierarchy-tertiary {
  font-size: var(--text-h3);
  font-weight: 500;
  line-height: var(--leading-normal);
}

/* Level 4: Body */
.hierarchy-body {
  font-size: var(--text-body);
  font-weight: 400;
  line-height: var(--leading-relaxed);
}

/* Level 5: Supporting */
.hierarchy-supporting {
  font-size: var(--text-sm);
  font-weight: 400;
  color: var(--charcoal-50);
}
```

### Hierarchy Through Position

```css
/* Top-left = Primary importance */
.position-primary {
  position: absolute;
  top: var(--space-6);
  left: var(--space-6);
}

/* Top-right = Secondary importance */
.position-secondary {
  position: absolute;
  top: var(--space-6);
  right: var(--space-6);
}

/* Bottom = Supporting info */
.position-supporting {
  position: absolute;
  bottom: var(--space-6);
  left: var(--space-6);
  right: var(--space-6);
}
```

---

## Asymmetric Compositions

### Off-Center Hero

```css
.hero-off-center {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-12);
  align-items: center;
  padding: var(--section-padding-fluid) var(--container-padding-fluid);
}

.hero-off-center .content {
  grid-column: 1;
  grid-row: 1;
  text-align: left;
}

.hero-off-center .image {
  grid-column: 2;
  grid-row: 1;
  position: relative;
  /* Shift image down for asymmetry */
  top: var(--space-8);
}

@media (max-width: 768px) {
  .hero-off-center {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-off-center .content,
  .hero-off-center .image {
    grid-column: 1;
    grid-row: auto;
  }

  .hero-off-center .image {
    top: 0;
    order: -1;  /* Image first on mobile */
  }
}
```

---

### Golden Ratio Layout

```css
.layout-golden {
  display: grid;
  grid-template-columns: 1fr 1.618fr;  /* Golden ratio */
  gap: var(--space-12);
}

@media (max-width: 768px) {
  .layout-golden {
    grid-template-columns: 1fr;
  }
}
```

---

### Thirds Layout

```css
.layout-thirds {
  display: grid;
  grid-template-columns: 1fr 2fr;  /* 1:2 ratio */
  gap: var(--space-12);
}

@media (max-width: 768px) {
  .layout-thirds {
    grid-template-columns: 1fr;
  }
}
```

---

## Whitespace as Design Element

### Generous Breathing Room

```css
/* Section with extra spacing */
.section-spacious {
  padding: var(--space-32) var(--container-padding-fluid);
}

/* Content surrounded by whitespace */
.content-island {
  max-width: 600px;
  margin: var(--space-24) auto;
  padding: var(--space-12);
}

/* Vertical rhythm with spacing */
.vertical-rhythm > * + * {
  margin-top: var(--space-6);
}
```

### Whitespace Zones

```css
/* Top zone - breathing room */
.whitespace-top {
  padding-top: var(--space-20);
}

/* Bottom zone - breathing room */
.whitespace-bottom {
  padding-bottom: var(--space-20);
}

/* Surrounded by whitespace */
.whitespace-surrounded {
  padding: var(--space-12);
  margin: var(--space-12);
}
```

---

## Typography-Driven Layouts

### Editorial Style (Large Type)

```css
.editorial-layout {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--section-padding-fluid) var(--container-padding-fluid);
}

.editorial-layout h1 {
  font-size: clamp(var(--text-4xl), 10vw, var(--text-6xl));
  line-height: var(--leading-tight);
  margin-bottom: var(--space-6);
}

.editorial-layout h2 {
  font-size: clamp(var(--text-2xl), 5vw, var(--text-4xl));
  line-height: var(--leading-snug);
  margin-top: var(--space-12);
  margin-bottom: var(--space-4);
}
```

### Magazine Style (Pull Quotes)

```css
.pull-quote {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-style: italic;
  line-height: var(--leading-snug);
  color: var(--sage-600);
  padding: var(--space-12) var(--space-8);
  border-left: 4px solid var(--sage-400);
  margin: var(--space-12) 0;
}

@media (max-width: 768px) {
  .pull-quote {
    font-size: var(--text-2xl);
    padding: var(--space-8) var(--space-6);
  }
}
```

---

## Focal Points

### Single Focus

```css
/* Draw attention to one element */
.focal-point {
  position: relative;
}

.focal-point::before {
  content: '';
  position: absolute;
  inset: -20px;
  border: 2px solid var(--sage-300);
  border-radius: var(--radius-lg);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.focal-point:hover::before {
  opacity: 1;
}
```

### Spotlight Effect

```css
/* Dim surrounding elements */
.spotlight-container {
  position: relative;
}

.spotlight-container > * {
  opacity: 0.4;
  transition: opacity var(--transition-normal);
}

.spotlight-container > *.spotlight {
  opacity: 1;
}

.spotlight-container > *:hover {
  opacity: 1;
}
```

---

## Rule of Thirds Grid

```css
.grid-thirds-overlay {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: var(--space-2);
}

.grid-thirds-overlay::after {
  /* Overlay showing rule of thirds */
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(to right, var(--sage-200) 1px, transparent 1px),
    linear-gradient(to bottom, var(--sage-200) 1px, transparent 1px);
  background-size: 33.33% 33.33%;
  opacity: 0.3;
  pointer-events: none;
}
```

---

## Layering & Depth

### Layered Cards

```css
.layered-cards {
  position: relative;
  height: 400px;
}

.layered-cards .card {
  position: absolute;
  transition:
    transform var(--transition-normal),
    box-shadow var(--transition-normal),
    z-index var(--transition-normal);
}

.layered-cards .card:nth-child(1) {
  transform: translateY(0) translateX(0);
  z-index: 3;
}

.layered-cards .card:nth-child(2) {
  transform: translateY(20px) translateX(20px);
  z-index: 2;
}

.layered-cards .card:nth-child(3) {
  transform: translateY(40px) translateX(40px);
  z-index: 1;
}

.layered-cards:hover .card {
  transform: translateY(0) translateX(0);
}
```

### Parallax Layers

```css
.parallax-container {
  position: relative;
  height: 600px;
  overflow: hidden;
}

.parallax-bg {
  position: absolute;
  inset: -20%;
  background: url(/images/texture.jpg) center/cover;
  transform: translateY(var(--parallax-offset, 0));
  transition: transform 0.1s linear;
}

.parallax-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* JavaScript needed for scroll-linked parallax */
```

---

## Contrast & Balance

### High Contrast Layout

```css
.layout-high-contrast {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.layout-high-contrast .dark {
  background: var(--charcoal-200);
  color: var(--cream-100);
  padding: var(--space-12);
}

.layout-high-contrast .light {
  background: var(--cream-100);
  color: var(--charcoal-200);
  padding: var(--space-12);
}
```

### Balanced Diagonal

```css
.diagonal-split {
  position: relative;
  height: 500px;
  overflow: hidden;
}

.diagonal-split::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--sage-400) 0%, var(--sage-600) 100%);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 70%);
}

.diagonal-split .content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## Motion in Composition

### Fade-In Sequence

```css
.fade-in-sequence > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp var(--transition-slow) var(--ease-out-quint) forwards;
}

.fade-in-sequence > *:nth-child(1) { animation-delay: 0ms; }
.fade-in-sequence > *:nth-child(2) { animation-delay: 100ms; }
.fade-in-sequence > *:nth-child(3) { animation-delay: 200ms; }
.fade-in-sequence > *:nth-child(4) { animation-delay: 300ms; }

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Responsive Compositions

### Mobile Stack, Desktop Side-by-Side

```css
.composition-responsive {
  display: grid;
  gap: var(--space-8);
}

/* Mobile: stacked */
@media (max-width: 768px) {
  .composition-responsive {
    grid-template-columns: 1fr;
  }
}

/* Desktop: side-by-side */
@media (min-width: 769px) {
  .composition-responsive {
    grid-template-columns: 1fr 1fr;
  }
}
```

### Expandable Cards

```css
.expandable-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-6);
}

.expandable-card {
  grid-column: span 1;
  transition: grid-column var(--transition-slow);
}

.expandable-card.expanded {
  grid-column: span 2;
}

@media (max-width: 768px) {
  .expandable-card.expanded {
    grid-column: span 1;
  }
}
```

---

## Anti-Patterns to Avoid

### ❌ Perfect Symmetry

```css
/* AVOID: Everything centered and aligned */
.bad-symmetry {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### ❌ Equal Grid Distribution

```css
/* AVOID: All elements same size */
.bad-equal-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* Too uniform */
}
```

### ❌ No Breathing Room

```css
/* AVOID: Elements packed too tightly */
.bad-cramped {
  padding: var(--space-4);  /* Not enough space */
  gap: var(--space-2);
}
```

### ✅ Good Alternatives

```css
/* Good: Varied sizes, asymmetric, generous space */
.good-composition {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;  /* Varied */
  gap: var(--space-12);  /* Generous */
  padding: var(--section-padding-fluid);
}
```

---

## Checklist for Refined Minimal Compositions

- [ ] Left-align content by default
- [ ] Use varied sizes (not all equal)
- [ ] Asymmetric layouts (not perfectly centered)
- [ ] Generous whitespace (breathing room)
- [ ] Typography as primary visual element
- [ ] Limited color usage (restraint)
- [ ] Purposeful positioning (not random)
- [ ] Clear visual hierarchy
- [ ] Balanced but not symmetrical
- [ ] Intentional white space (not leftover space)
