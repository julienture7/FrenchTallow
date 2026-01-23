# Typography Tokens

## Font Families

### Current Implementation

```css
/* Display / Headings */
--font-display: 'Cormorant Garamond', Georgia, serif;

/* Body / UI */
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Monospace (code, data) */
--font-mono: 'SF Mono', 'Roboto Mono', 'Menlo', monospace;
```

### Post-Redesign (Refined Minimal)

```css
/* Display / Headings */
--font-display: 'Cormorant Garamond', Georgia, serif;

/* Body / UI - REPLACING INTER */
--font-body: 'Karla', 'Inter', sans-serif;  /* Or: Fraunces, Instrument Sans */

/* Monospace */
--font-mono: 'SF Mono', 'Roboto Mono', 'Menlo', monospace;
```

**Rationale**: Inter is functional but overused and generic. Karla adds warmth and character while maintaining readability.

---

## Type Scale

### Modular Scale: Major Third (1.250)

```css
--text-xs:   0.640rem;  /* 10.24px - tiny labels */
--text-sm:   0.800rem;  /* 12.8px - small text */
--text-base: 1.000rem;  /* 16px - body text */
--text-lg:   1.250rem;  /* 20px - lead text */
--text-xl:   1.563rem;  /* 25px - subheading */
--text-2xl:  1.953rem;  /* 31.25px - heading */
--text-3xl:  2.441rem;  /* 39.06px - section heading */
--text-4xl:  3.052rem;  /* 48.83px - hero subheading */
--text-5xl:  3.815rem;  /* 61.04px - hero heading */
--text-6xl:  4.768rem;  /* 76.29px - display */
```

### Fluid Typography (Responsive)

```css
--text-h1: clamp(2.75rem, 6vw, 4.5rem);    /* 44px - 72px */
--text-h2: clamp(2rem, 3.5vw, 2.75rem);    /* 32px - 44px */
--text-h3: clamp(1.25rem, 2.25vw, 1.6rem); /* 20px - 25.6px */
--text-body: clamp(1rem, 1vw + 0.5rem, 1.125rem); /* 16px - 18px */
```

---

## Font Weights

```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Usage by Element

| Element | Font Family | Weight | Size | Line Height |
|---------|-------------|--------|------|-------------|
| H1 | Cormorant Garamond | 500-600 | `--text-h1` | 1.1-1.2 |
| H2 | Cormorant Garamond | 500 | `--text-h2` | 1.2-1.3 |
| H3 | Cormorant Garamond | 500 | `--text-h3` | 1.3-1.4 |
| Body | Karla/Inter | 400 | `--text-body` | 1.65-1.75 |
| Small | Karla/Inter | 400-500 | `--text-sm` | 1.5-1.6 |
| Button | Karla/Inter | 500 | `--text-base` | 1.3-1.4 |
| Caption | Karla/Inter | 400 | `--text-xs` | 1.4-1.5 |

---

## Line Heights

```css
--leading-tight: 1.1;    /* Headings */
--leading-snug: 1.25;   /* Display text */
--leading-normal: 1.5;   /* UI text */
--leading-relaxed: 1.65; /* Body text */
--leading-loose: 1.75;   /* Long-form reading */
```

### Usage Guidelines

- **Tight (1.1-1.2)**: Large display headings only
- **Normal (1.5)**: UI elements, buttons, labels
- **Relaxed (1.65)**: Body paragraphs, descriptions
- **Loose (1.75+)**: Long-form content, articles

---

## Letter Spacing

```css
--tracking-tighter: -0.05em;  /* Large display text */
--tracking-tight: -0.025em;   /* Headings */
--tracking-normal: 0;         /* Body text */
--tracking-wide: 0.03em;      /* Small text, uppercase */
--tracking-wider: 0.06em;     /* Buttons, labels */
--tracking-widest: 0.12em;    /* Tagline, tiny labels */
```

### Usage

| Element | Letter Spacing |
|---------|----------------|
| H1 | `--tracking-tight` |
| H2-H3 | `--tracking-tight` or normal |
| Uppercase text | `--tracking-wide` or `--tracking-wider` |
| Body text | `--tracking-normal` |
| Tiny labels (0.65rem) | `--tracking-widest` |

---

## Text Colors

```css
/* Semantic text colors */
--color-text-heading: var(--charcoal-300);    /* #1A1A1A */
--color-text-body: var(--charcoal-200);       /* #2D2D2D */
--color-text-secondary: var(--charcoal-50);   /* #7A7A7A */
--color-text-muted: var(--charcoal-100);      /* #3D3D3D */
--color-text-accent: var(--sage-500);         /* #6B7F5C */
--color-text-link: var(--sage-400);           /* #8B9F7C */
--color-text-link-hover: var(--sage-600);     /* #4A5A3E */
--color-text-inverted: var(--white);          /* For dark backgrounds */
```

---

## Typography Hierarchy

### Hero Section
```
H1: --text-h1 / Cormorant Garamond / 500-600 / --tracking-tight
Subheading: --text-xl / Cormorant Garamond / 400 / --leading-relaxed
```

### Section Headings
```
H2: --text-h2 / Cormorant Garamond / 500 / --tracking-tight
Optional Subhead: --text-base / Karla / 400 / --color-text-secondary
```

### Product Cards
```
Product Name: --text-lg / Cormorant Garamond / 500
Price: --text-base / Karla / 500
Benefits: --text-sm / Karla / 400 / --color-text-secondary
```

### Article Cards
```
Article Title: --text-xl / Cormorant Garamond / 500 / --leading-snug
Excerpt: --text-sm / Karla / 400 / --leading-relaxed / 3-line clamp
Meta: --text-xs / Karla / 500 / uppercase / --tracking-wide
```

### Buttons
```
Primary Button: --text-base / Karla / 500 / --tracking-wide
Secondary Button: --text-base / Karla / 500 / --tracking-normal
```

---

## Text Alignment Guidelines (Post-Redesign)

### Current State (Too Centered)
- Hero: centered
- Section headers: centered
- Product cards: centered
- Article cards: centered

### Refined Minimal Approach
```
✅ Left-align: Headings, body text, card content
✅ Center-align: Only for specific emphasis or narrow content
✅ Asymmetric: Mix of left-aligned elements with varied positions
```

**Rule**: Default to left-alignment. Center only when intentional.

---

## Font Loading Strategy

### Current
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

### Optimized (Post-Redesign)
```html
<!-- Preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload Critical Fonts -->
<link rel="preload" href="https://fonts.gstatic.com/s/cormorantgaramond/v10/co3YmX5slCNuHLi8bLeY9MK7whWMhyjYrEtAhKC4Zj8" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="https://fonts.gstatic.com/s/karla/v30/qkBbXvYC6trAT7RbLtyG5Q.woff2" as="font" type="font/woff2" crossorigin>

<!-- Load -->
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Karla:wght@300;400;500;600&display=swap" rel="stylesheet">
```

### Fallback Stack
```css
/* Cormorant Garamond */
font-family: 'Cormorant Garamond', Georgia, 'Times New Roman', serif;

/* Karla (or Inter) */
font-family: 'Karla', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

---

## Multilingual Typography

### Character Support

The fonts support extended Latin scripts. For 24-language support:

| Language Family | Font Support | Fallback |
|----------------|--------------|----------|
| Latin (EN, FR, ES, DE, IT, PT, NL) | Cormorant Garamond + Karla | System fonts |
| Greek (EL) | Cormorant Garamond + Karla | System fonts |
| Cyrillic (UK, BG, RU, SR) | Cormorant Garamond + Karla | System fonts |
| Nordic (SV, NO, DA, FI) | Cormorant Garamond + Karla | System fonts |
| Eastern European (PL, CS, RO, SK, SL, HR) | Cormorant Garamond + Karla | System fonts |
| Baltic (LT, LV, ET) | Cormorant Garamond + Karla | System fonts |
| Hungarian (HU) | Cormorant Garamond + Karla | System fonts |

### Language-Specific Considerations

- **Longer words** (German, Finnish): Ensure line-length accommodates
- **Accents** (French, Portuguese): Verify line-height doesn't clip
- **Non-Latin scripts** (future): Consider script-specific fonts

---

## Accessibility

### Minimum Font Sizes
- Body text: 16px (1rem) minimum
- Small text: 14px (0.875rem) minimum
- Tiny labels: 12px (0.75rem) absolute minimum

### Contrast Requirements
- Body text on light bg: 4.5:1 minimum (AA)
- Large text (18px+): 3:1 minimum (AA)
- Enhanced contrast: 7:1 (AAA)

### Font Adjustments
Respect user's browser font size settings (use `rem`, not `px` for body).
