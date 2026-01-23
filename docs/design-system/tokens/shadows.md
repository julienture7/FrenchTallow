# Shadow Tokens

## Shadow System

Shadows create depth and elevation. The FrenchTallowSoap aesthetic uses **subtle, warm shadows**—never harsh or dramatic.

### Color Temperature

All shadows use **warm charcoal** (`rgba(45, 45, 45, X)`) rather than pure black for a softer, more organic feel.

---

## Shadow Scale

```css
/* No shadow */
--shadow-none: none;

/* Subtle - Barely noticeable depth */
--shadow-subtle: 0 2px 12px rgba(45, 45, 45, 0.06);

/* Soft - Gentle elevation */
--shadow-soft: 0 4px 20px rgba(45, 45, 45, 0.08);

/* Medium - Clear elevation */
--shadow-medium: 0 8px 32px rgba(45, 45, 45, 0.10);

/* Elevated - Strong depth */
--shadow-elevated: 0 16px 48px rgba(45, 45, 45, 0.12);

/* Floating - Maximum depth */
--shadow-floating: 0 24px 64px rgba(45, 45, 45, 0.15);
```

---

## Usage by Component

### Cards

```css
/* Default card state */
.card {
  box-shadow: var(--shadow-subtle);
}

/* Hover state */
.card:hover {
  box-shadow: var(--shadow-elevated);
}

/* Active/pressed state */
.card:active {
  box-shadow: var(--shadow-medium);
}
```

### Buttons

```css
/* Default button - no shadow */
.button {
  box-shadow: var(--shadow-none);
}

/* Primary button - subtle shadow */
.button-primary {
  box-shadow: var(--shadow-subtle);
}

/* Button hover */
.button:hover {
  box-shadow: var(--shadow-soft);
}
```

### Header

```css
/* Default header - no shadow */
.site-header {
  box-shadow: var(--shadow-none);
}

/* Scrolled header - subtle shadow */
.site-header.scrolled {
  box-shadow: var(--shadow-subtle);
}
```

### Dropdowns/Modals

```css
/* Dropdown menu */
.dropdown {
  box-shadow: var(--shadow-elevated);
}

/* Modal overlay */
.modal-overlay {
  box-shadow: var(--shadow-floating);
}

/* Modal content */
.modal-content {
  box-shadow: var(--shadow-floating);
}
```

### Tooltip/Popover

```css
.tooltip {
  box-shadow: var(--shadow-medium);
}
```

---

## Shadow Compositions

### Inner Shadow (Inset)

```css
--shadow-inset-sm: inset 0 1px 4px rgba(45, 45, 45, 0.08);
--shadow-inset-md: inset 0 2px 8px rgba(45, 45, 45, 0.10);
```

**Usage**: Pressed states, inset elements, form inputs.

```css
.button:active {
  box-shadow: var(--shadow-inset-sm);
}

.input:focus {
  box-shadow: var(--shadow-inset-md), 0 0 0 2px var(--sage-400);
}
```

### Colored Shadows (Warm Accents)

For special emphasis, use subtle colored shadows:

```css
/* Sage glow */
--shadow-glow-sage: 0 4px 20px rgba(139, 159, 124, 0.15);

/* Gold glow */
--shadow-glow-gold: 0 4px 20px rgba(196, 168, 107, 0.12);
```

**Usage sparingly**: Special featured items, premium products.

---

## Hover Shadow Animation

```css
.card {
  box-shadow: var(--shadow-subtle);
  transition: box-shadow var(--transition-normal);
}

.card:hover {
  box-shadow: var(--shadow-elevated);
}
```

---

## Layered Shadows (Complex Depth)

For multiple elevation levels:

```css
/* Close + distant shadow for realism */
--shadow-layered:
  0 2px 8px rgba(45, 45, 45, 0.06),
  0 16px 48px rgba(45, 45, 45, 0.08);
```

**Usage**: Featured elements, hero cards.

---

## Dark Mode Considerations

This site is **light mode only** (per design decisions), but if dark mode is added:

```css
/* Dark mode shadows would be lighter */
@media (prefers-color-scheme: dark) {
  --shadow-subtle: 0 2px 12px rgba(0, 0, 0, 0.4);
  --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.5);
  /* ... etc */
}
```

---

## Performance

Shadows can impact performance. Optimize by:

1. **Avoid animating box-shadow**: Use `opacity` on a pseudo-element instead
   ```css
   /* ❌ BAD - Animating box-shadow */
   .card { transition: box-shadow 0.3s; }

   /* ✅ GOOD - Animating opacity */
   .card::after {
     content: '';
     position: absolute;
     inset: 0;
     box-shadow: var(--shadow-elevated);
     opacity: 0;
     transition: opacity 0.3s;
   }
   .card:hover::after { opacity: 1; }
   ```

2. **Use simple shadows**: Fewer shadow layers = better performance
   ```css
   /* ✅ Better - Single shadow */
   box-shadow: 0 4px 20px rgba(45, 45, 45, 0.08);

   /* ❌ Worse - Multiple layers */
   box-shadow:
     0 2px 4px rgba(45, 45, 45, 0.04),
     0 4px 8px rgba(45, 45, 45, 0.06),
     0 8px 16px rgba(45, 45, 45, 0.08);
   ```

3. **Limit shadow animation scope**: Only animate shadows on visible elements

---

## Usage Guidelines

### DO:
- ✅ Use shadows for elevation and depth
- ✅ Match shadow intensity to elevation level
- ✅ Use warm shadows (not pure black)
- ✅ Keep shadows subtle for refined minimal aesthetic
- ✅ Animate shadow changes smoothly

### DON'T:
- ❌ Use harsh black shadows
- ❌ Overuse strong shadows—elevated sparingly
- ❌ Animate box-shadow on scroll (performance issue)
- ❌ Use shadows as borders (use actual borders)
- ❌ Mix shadow styles inconsistently

---

## Shadow Alternatives

### Border (Alternative to Shadow)

For subtle definition without shadow:

```css
.card {
  border: 1px solid var(--gold-200);
  box-shadow: var(--shadow-subtle);
}
```

### Offset Border (Elevation Without Shadow)

```css
.card {
  border: 1px solid var(--gold-200);
  border-bottom-width: 2px;
}
```

### Background Variation (Depth Without Shadow)

```css
.card-elevated {
  background: var(--cream-50);
  border: 1px solid var(--gold-200);
}
```
