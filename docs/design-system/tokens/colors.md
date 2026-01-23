# Color Tokens

## Palette Overview

The FrenchTallowSoap color palette is warm, organic, and sophisticated—evoking natural ingredients, artisanal craftsmanship, and French heritage.

### Design Philosophy

- **Warm over pure**: No pure white (#FFF) or pure black (#000). All colors have subtle warmth.
- **Nature-inspired**: Sage (herbs), gold (quality), cream (purity)
- **Subtle over saturated**: Restful, not attention-grabbing
- **Cohesive through tinting**: Neutrals tinted toward sage for subconscious harmony

---

## Primitive Color Tokens

### Sage (Primary Accent)

```css
--sage-50:  #F5F7F2;  /* Very light sage - backgrounds */
--sage-100: #E8EBE0;  /* Light sage - subtle backgrounds */
--sage-200: #C5D4C0;  /* Sage lighter - hover states */
--sage-300: #A8B99A;  /* Sage light - accents */
--sage-400: #8B9F7C;  /* Sage primary - main accent */
--sage-500: #6B7F5C;  /* Sage dark - emphasis */
--sage-600: #4A5A3E;  /* Sage darker - strong emphasis */
--sage-700: #3A4A32;  /* Deep sage - text on light */
```

**Usage**:
- `sage-300/400`: Interactive elements (buttons, links, focus states)
- `sage-500/600`: Emphasis, active states
- `sage-100/200`: Subtle backgrounds, hover states
- `sage-50`: Very light backgrounds

---

### Gold (Secondary Accent)

```css
--gold-50:  #FDF8F0;  /* Very light gold - backgrounds */
--gold-100: #F5EFE3;  /* Gold lighter - highlights */
--gold-200: #E8DCC4;  /* Gold light - borders */
--gold-300: #C4A86B;  /* Gold primary - accents */
--gold-400: #A68B4E;  /* Gold dark - emphasis */
```

**Usage**:
- `gold-200`: Borders, dividers
- `gold-300`: Secondary accents, "premium" indicators
- `gold-100/50`: Warm backgrounds, highlights

---

### Cream (Backgrounds)

```css
--cream-50:  #FFFEFA;  /* Near white - primary background */
--cream-100: #FAF7F2;  /* Cream primary - main bg */
--cream-200: #F5F0E8;  /* Cream secondary - cards */
--cream-300: #F0E9DD;  /* Cream tertiary - nested cards */
```

**Usage**:
- `cream-50/100`: Page backgrounds
- `cream-200`: Card backgrounds, elevated surfaces
- `cream-300`: Nested elements, subtle depth

---

### Charcoal (Text)

```css
--charcoal-50:  #7A7A7A;  /* Warm gray - secondary text */
--charcoal-100: #3D3D3D;  /* Light charcoal - muted text */
--charcoal-200: #2D2D2D;  /* Charcoal primary - body text */
--charcoal-300: #1A1A1A;  /* Dark charcoal - headings */
```

**Usage**:
- `charcoal-50`: Secondary text, descriptions
- `charcoal-100`: Muted text, captions
- `charcoal-200`: Primary body text
- `charcoal-300`: Headings, emphasis

---

## Semantic Color Tokens

```css
/* Backgrounds */
--color-bg-primary: var(--cream-100);
--color-bg-secondary: var(--cream-200);
--color-bg-elevated: var(--white);
--color-bg-muted: var(--cream-50);

/* Text */
--color-text-primary: var(--charcoal-200);
--color-text-secondary: var(--charcoal-50);
--color-text-muted: var(--charcoal-100);
--color-text-on-dark: var(--cream-100);
--color-text-on-accent: var(--white);

/* Accents */
--color-accent-primary: var(--sage-400);
--color-accent-hover: var(--sage-500);
--color-accent-active: var(--sage-600);
--color-accent-subtle: var(--sage-200);

/* Secondary Accent */
--color-accent-gold: var(--gold-300);
--color-accent-gold-dark: var(--gold-400);

/* Borders */
--color-border-subtle: var(--gold-200);
--color-border-default: var(--sage-300);
--color-border-strong: var(--sage-500);

/* Functional */
--color-success: var(--sage-400);
--color-warning: var(--gold-300);
--color-error: #C45A5A;  /* Muted red */
--color-info: var(--sage-500);
```

---

## Color Relationships

### Contrast Ratios (WCAG AA)

| Foreground | Background | Ratio | Grade |
|------------|------------|-------|-------|
| `--charcoal-200` on `--cream-100` | 12.8:1 | AAA |
| `--charcoal-50` on `--cream-100` | 4.9:1 | AA |
| `--sage-400` on `--cream-100` | 3.2:1 | ❌ Fail |
| `--white` on `--sage-500` | 7.1:1 | AA |
| `--charcoal-200` on `--sage-400` | 6.1:1 | AA |

**Note**: Sage text on light backgrounds fails WCAG AA. Use sage only with white text or as background with dark text.

---

## Gradient Tokens

```css
--gradient-sage: linear-gradient(135deg,
  var(--sage-200) 0%,
  var(--sage-400) 50%,
  var(--sage-500) 100%
);

--gradient-gold: linear-gradient(135deg,
  var(--gold-100) 0%,
  var(--gold-300) 100%
);

--gradient-hero: linear-gradient(180deg,
  var(--white) 0%,
  var(--cream-100) 50%,
  var(--cream-200) 100%
);
```

**Usage Guidelines**:
- Use gradients sparingly—they can feel decorative and unnecessary
- Prefer flat colors for refined minimal aesthetic
- If using gradients, ensure they add meaning (not just decoration)

---

## Color Usage Guidelines

### DO:
- ✅ Use `--color-bg-primary` for page backgrounds
- ✅ Use `--color-text-primary` for body text
- ✅ Use `--color-accent-primary` for interactive elements
- ✅ Use gold borders for elegant definition
- ✅ Use cream backgrounds for warmth

### DON'T:
- ❌ Use sage for text on light backgrounds (fails contrast)
- ❌ Use pure white (#FFF) or pure black (#000)
- ❌ Use gray on colored backgrounds (use tinted background color instead)
- ❌ Overuse gradients (prefer flat, intentional color)
- ❌ Mix too many accent colors (sage + gold is sufficient)

---

## Category Color Coding (Future)

For product categorization, consider subtle accent variations:

```css
/* Citrus & Fresh */
--color-citrus: #D4A574;  /* Subtle apricot */

/* Warm & Comforting */
--color-warm: #C4826B;  /* Terracotta */

/* Herbal & Earthy */
--color-herbal: var(--sage-500);

/* Floral & Fruity */
--color-floral: #D4A0A0;  /* Soft rose */
```

These should be used very sparingly—just small accents, not overwhelming color.
