# Spacing Tokens

## Spacing Scale

### Base Unit: 4px

```css
--space-0:   0;        /* 0px */
--space-1:   0.25rem;  /* 4px */
--space-2:   0.5rem;   /* 8px */
--space-3:   0.75rem;  /* 12px */
--space-4:   1rem;     /* 16px */
--space-5:   1.25rem;  /* 20px */
--space-6:   1.5rem;   /* 24px */
--space-8:   2rem;     /* 32px */
--space-10:  2.5rem;   /* 40px */
--space-12:  3rem;     /* 48px */
--space-16:  4rem;     /* 64px */
--space-20:  5rem;     /* 80px */
--space-24:  6rem;     /* 96px */
--space-32:  8rem;     /* 128px */
```

### Semantic Spacing

```css
/* Tight spacing */
--space-tight: var(--space-2);    /* 8px */
--space-snug: var(--space-3);     /* 12px */

/* Normal spacing */
--space-sm: var(--space-4);        /* 16px */
--space-md: var(--space-6);        /* 24px */
--space-lg: var(--space-8);        /* 32px */

/* Generous spacing */
--space-xl: var(--space-12);       /* 48px */
--space-2xl: var(--space-16);      /* 64px */
--space-3xl: var(--space-20);      /* 80px */
--space-4xl: var(--space-24);      /* 96px */
```

---

## Component Spacing

### Padding

```css
/* Buttons */
--padding-btn-sm: var(--space-2) var(--space-4);   /* 8px 16px */
--padding-btn-md: var(--space-3) var(--space-6);   /* 12px 24px */
--padding-btn-lg: var(--space-4) var(--space-8);   /* 16px 32px */

/* Cards */
--padding-card-sm: var(--space-4);      /* 16px */
--padding-card-md: var(--space-6);      /* 24px */
--padding-card-lg: var(--space-8);      /* 32px */

/* Sections */
--padding-section-sm: var(--space-12);  /* 48px vertical */
--padding-section-md: var(--space-20);  /* 80px vertical */
--padding-section-lg: var(--space-24);  /* 96px vertical */
```

### Gap (Flex/Grid)

```css
--gap-tight: var(--space-3);    /* 12px */
--gap-sm: var(--space-4);        /* 16px */
--gap-md: var(--space-6);        /* 24px */
--gap-lg: var(--space-8);        /* 32px */
--gap-xl: var(--space-12);       /* 48px */
```

---

## Container Spacing

```css
/* Max-width containers */
--container-sm: 640px;   /* Narrow content */
--container-md: 960px;   /* Article content */
--container-lg: 1140px;  /* Standard page */
--container-xl: 1440px;  /* Wide layout */

/* Container padding (horizontal) */
--container-padding-sm: var(--space-4);   /* 16px */
--container-padding-md: var(--space-6);   /* 24px */
--container-padding-lg: var(--space-8);   /* 32px */
```

---

## Fluid Spacing

For responsive spacing that scales with viewport:

```css
/* Fluid gap: 16px at mobile, 32px at desktop */
--gap-fluid: clamp(var(--space-4), 4vw, var(--space-8));

/* Fluid section padding: 48px at mobile, 96px at desktop */
--section-padding-fluid: clamp(var(--space-12), 8vw, var(--space-24));

/* Fluid container padding: 16px at mobile, 32px at desktop */
--container-padding-fluid: clamp(var(--space-4), 4vw, var(--space-8));
```

---

## Rhythm & Visual Hierarchy

### Vertical Rhythm

Establish consistent vertical spacing using multiples of the base unit (4px):

```
Line height: 24px (1.5rem)
Spacing between paragraphs: 16px (1rem) = 2/3 of line height
Section spacing: 48px (3rem) = 2x line height
```

### Spacing Hierarchy

| Context | Spacing | Token |
|---------|---------|-------|
| Inline elements | 4-8px | `--space-1` to `--space-2` |
| Related items | 12-16px | `--space-3` to `--space-4` |
| Unrelated items | 24-32px | `--space-6` to `--space-8` |
| Sections | 48-96px | `--space-12` to `--space-24` |

---

## Responsive Spacing

### Mobile-First Approach

```css
/* Mobile (default) */
.component { padding: var(--space-4); }

/* Tablet (768px+) */
@media (min-width: 768px) {
  .component { padding: var(--space-6); }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .component { padding: var(--space-8); }
}
```

### Fluid Mobile to Desktop

```css
.component {
  padding: clamp(
    var(--space-4),  /* 16px at minimum */
    5vw,             /* Scales with viewport */
    var(--space-8)   /* 32px at maximum */
  );
}
```

---

## Usage Guidelines

### DO:
- ✅ Use spacing scale tokens consistently
- ✅ Use semantic tokens (`--space-md`) over literal values
- ✅ Use fluid spacing for responsive behavior
- ✅ Maintain visual rhythm with consistent spacing
- ✅ Use generous spacing for refined minimal aesthetic

### DON'T:
- ❌ Use arbitrary values (7px, 13px, 23px)
- ❌ Use spacing as a substitute for borders
- ❌ Overuse tight spacing—let content breathe
- ❌ Mix inconsistent spacing across similar components
- ❌ Use the same spacing everywhere—create rhythm through variation

---

## Spacing by Component

### Header
```
Logo-image gap: 8px (--space-2)
Header padding: 18px 32px (tight horizontal)
Header-scrolled padding: 14px 32px (condensed)
```

### Hero
```
Hero padding: 48px 16px mobile, 112px 32px desktop
Badge bottom margin: 32px
H1 bottom margin: 24px
Description bottom margin: 40px
Trust badges top margin: 48px
```

### Product Cards
```
Card padding: 22px (current) → 24px (--space-6) (refined)
Image bottom margin: 16px
H3 bottom margin: 8px
```

### Article Cards
```
Card padding: 28px (--space-7) → 32px (--space-8)
Meta bottom margin: 16px
H3 bottom margin: 14px
Excerpt to footer: 20px
```

### Footer
```
Footer padding: 64px 32px 32px
Section bottom margin: 48px
H4 bottom margin: 20px
```

---

## Negative Margin (For Overlap Effects)

Use sparingly for intentional overlap:

```css
--negative-sm: calc(-1 * var(--space-4));   /* -16px */
--negative-md: calc(-1 * var(--space-6));   /* -24px */
--negative-lg: calc(-1 * var(--space-8));   /* -32px */
```

**Usage**: Pulling elements up for overlap effects (e.g., image overlapping header, card overlapping section).

---

## Scroll Margin

For anchor link offset (sticky header compensation):

```css
html {
  scroll-margin-top: 80px; /* Account for sticky header */
}

/* Or per-section */
section {
  scroll-margin-top: 80px;
}
```
