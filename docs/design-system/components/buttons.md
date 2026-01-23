# Button Components

## Overview

Buttons are the primary interactive elements in the interface. All buttons must be keyboard accessible, have clear hover/focus states, and follow consistent styling patterns.

---

## Button Variants

### Primary Button

The main call-to-action button. Use for the most important action on a page.

```css
.button-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--padding-btn-md);
  background: var(--gradient-sage);
  color: var(--white);
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: 500;
  letter-spacing: 0.03em;
  text-decoration: none;
  cursor: pointer;
  transition:
    transform var(--transition-quick),
    box-shadow var(--transition-quick);
}

.button-primary:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-soft);
}

.button-primary:active {
  transform: translateY(0);
}

.button-primary:focus-visible {
  outline: 2px solid var(--sage-500);
  outline-offset: 2px;
}
```

**Usage**: "Shop Now", "Explore Collection", "Find Your Scent"

---

### Secondary Button

Less prominent action. Used alongside primary button or for secondary actions.

```css
.button-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--padding-btn-md);
  background: var(--white);
  color: var(--charcoal-200);
  border: 1px solid var(--gold-200);
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition:
    border-color var(--transition-quick),
    background var(--transition-quick),
    transform var(--transition-quick);
}

.button-secondary:hover {
  border-color: var(--sage-400);
  background: var(--cream-50);
}

.button-secondary:active {
  transform: scale(0.98);
}
```

**Usage**: "Learn More", "View All Products", "Read Article"

---

### Ghost Button

Minimal button for tertiary actions.

```css
.button-ghost {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--padding-btn-sm) var(--padding-btn-md);
  background: transparent;
  color: var(--sage-400);
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  position: relative;
  transition:
    color var(--transition-color),
    gap var(--transition-quick);
}

.button-ghost::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background: currentColor;
  transition: width var(--transition-normal);
}

.button-ghost:hover {
  color: var(--sage-600);
  gap: var(--space-3);
}

.button-ghost:hover::after {
  width: 100%;
}
```

**Usage**: "Cancel", "Close", "Back to top", tertiary links

---

### Text Link

For inline actions and navigation.

```css
.link {
  display: inline;
  color: var(--sage-400);
  text-decoration: none;
  font-weight: 500;
  position: relative;
  cursor: pointer;
  transition: color var(--transition-color);
}

.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background: currentColor;
  transition: width var(--transition-normal);
}

.link:hover {
  color: var(--sage-600);
}

.link:hover::after {
  width: 100%;
}

.link:focus-visible {
  outline: 2px solid var(--sage-500);
  outline-offset: 2px;
  border-radius: 2px;
}
```

**Usage**: Inline links, navigation, "Read more"

---

## Button Sizes

### Small

```css
.button-sm {
  padding: var(--padding-btn-sm);
  font-size: var(--text-sm);
}
```

**Usage**: Compact areas, inline with text

### Medium (Default)

```css
.button-md {
  padding: var(--padding-btn-md);
  font-size: var(--text-base);
}
```

**Usage**: Standard buttons, most common size

### Large

```css
.button-lg {
  padding: var(--padding-btn-lg);
  font-size: var(--text-lg);
}
```

**Usage**: Hero CTAs, prominent actions

---

## Button States

### Disabled

```css
.button:disabled,
.button-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
```

### Loading

```css
.button-loading {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.button-loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
```

### Active (Pressed)

```css
.button:active {
  transform: scale(0.98);
}
```

---

## Button with Icon

```css
.button-with-icon {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.button-with-icon svg {
  width: 16px;
  height: 16px;
}

/* Icon only button */
.button-icon-only {
  padding: var(--space-3);
  aspect-ratio: 1;
}

.button-icon-only svg {
  width: 20px;
  height: 20px;
}
```

---

## Button Groups

Related buttons grouped together:

```css
.button-group {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.button-group-vertical {
  flex-direction: column;
  align-items: stretch;
}

.button-group .button {
  flex: 1;
}
```

---

## Accessibility

### Minimum Touch Targets

All buttons must meet **44x44px minimum** for touch targets:

```css
/* Ensure button is at least 44px tall */
.button {
  min-height: 44px;
  min-width: 44px;
}
```

### Focus States

Always provide visible focus indication:

```css
.button:focus-visible {
  outline: 2px solid var(--sage-500);
  outline-offset: 2px;
}
```

### ARIA Attributes

```html
<!-- Standard button -->
<button class="button-primary">Submit</button>

<!-- Icon button with label -->
<button class="button-icon-only" aria-label="Close menu">
  <svg>...</svg>
</button>

<!-- Button as link -->
<a href="/products" class="button-primary" role="button">
  Shop Now
</a>
```

---

## Usage Examples

### Hero CTA

```html
<button class="button-primary button-lg">
  Explore Our Collection
</button>
```

### Card Action

```html
<a href="/products/lemon" class="button-secondary button-sm">
  View Details
</a>
```

### Navigation Link

```html
<a href="/about" class="link">
  Our Story
</a>
```

### Icon Button

```html
<button class="button-ghost button-icon-only" aria-label="Search">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="11" cy="11" r="8"/>
    <path d="M21 21l-4.35-4.35"/>
  </svg>
</button>
```

### Button with Arrow

```html
<a href="/products" class="button-primary">
  Shop Now
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M5 12h14M12 5l7 7-7 7"/>
  </svg>
</a>
```

---

## HTML Implementation

For the inline CSS implementation (single file approach), include these button styles in the main stylesheet and use the class names shown above.
