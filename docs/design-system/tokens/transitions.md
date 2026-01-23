# Transition & Animation Tokens

## Timing Functions

### Easing Curves

```css
/* Linear */
--ease-linear: linear;

/* Standard */
--ease-in: ease-in;
--ease-out: ease-out;
--ease-in-out: ease-in-out;

/* Custom - Natural Motion */
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);      /* Natural deceleration */
--ease-out-quint: cubic-bezier(0.2, 1, 0.4, 1);      /* Very smooth deceleration */
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);      /* Exponential deceleration */

/* Custom - Bounce (AVOID) */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Dated, tacky */
```

### Recommended Easing

| Interaction | Easing | Rationale |
|-------------|--------|-----------|
| Hover/focus | `--ease-out-quart` | Natural, smooth |
| Enter/exit | `--ease-out-quint` | Very polished |
| Scroll parallax | `--ease-out-expo` | Sophisticated |
| Color change | `ease-in-out` | Balanced |
| **AVOID** | `--ease-bounce` | Feels dated/tacky |

---

## Duration Tokens

```css
/* Instant */
--duration-instant: 0ms;

/* Fast (micro-interactions) */
--duration-fast: 150ms;      /* 0.15s - Hover states, focus */

/* Normal (state changes) */
--duration-normal: 250ms;    /* 0.25s - Dropdowns, toggles */

/* Slow (page transitions) */
--duration-slow: 400ms;      /* 0.4s - Modal enter, page transition */

/* Very slow (major animations) */
--duration-slower: 600ms;    /* 0.6s - Hero animations */
```

### Usage by Interaction

| Interaction | Duration | Token |
|-------------|----------|-------|
| Button hover | 150ms | `--duration-fast` |
| Link underline | 150ms | `--duration-fast` |
| Dropdown toggle | 200ms | Between fast/normal |
| Card hover elevation | 250ms | `--duration-normal` |
| Filter change crossfade | 300ms | `--duration-normal` |
| Modal enter/exit | 400ms | `--duration-slow` |
| Page load staggered | 150-600ms | Staggered `--duration-fast` to `--duration-slower` |

---

## Composite Transition Tokens

```css
/* Quick micro-interactions */
--transition-quick: var(--duration-fast) var(--ease-out-quart);

/* Standard state changes */
--transition-normal: var(--duration-normal) var(--ease-out-quart);

/* Slow transitions */
--transition-slow: var(--duration-slow) var(--ease-out-quint);

/* Color-only transition */
--transition-color: var(--duration-normal) ease-in-out;
```

---

## Animation Properties

### What to Animate

```css
/* ✅ GOOD - Performant properties */
transform: translateX(), translateY(), scale(), rotate();
opacity: 0, 0.5, 1;
filter: blur(), brightness();

/* ❌ BAD - Causes layout thrashing */
width, height, padding, margin;
top, left, right, bottom;
border-radius;
```

### Rule of Thumb

**Only animate `transform` and `opacity` for 60fps performance.**

---

## Transition Patterns

### Hover Elevation

```css
.card {
  transition:
    transform var(--transition-normal),
    box-shadow var(--transition-normal);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-elevated);
}
```

### Focus Ring

```css
.button:focus-visible {
  outline: 2px solid var(--sage-400);
  outline-offset: 2px;
  transition: outline var(--transition-quick);
}
```

### Color Shift

```css
.link {
  color: var(--sage-400);
  transition: color var(--transition-color);
}

.link:hover {
  color: var(--sage-600);
}
```

### Fade In/Out

```css
.fade-enter {
  opacity: 0;
  transform: translateY(10px);
}

.fade-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity var(--transition-normal),
    transform var(--transition-normal);
}
```

---

## Staggered Animations

For sequential element reveals:

```css
/* Item 1 */
.item-1 {
  animation-delay: 0ms;
}

/* Item 2 */
.item-2 {
  animation-delay: 100ms;
}

/* Item 3 */
.item-3 {
  animation-delay: 200ms;
}

/* ...and so on */
```

### Formula: Stagger Delay

```
Base delay: 0ms
Increment: 100ms (var(--duration-fast) * 0.66)
Max delay: 600ms (6 items)
```

---

## Reduced Motion

**CRITICAL**: Always respect `prefers-reduced-motion`.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Alternative: Disable Non-Essential Motion

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable decorative animations */
  .floating-element {
    animation: none;
  }

  /* Keep essential transitions instant */
  .menu-toggle {
    transition-duration: 0.01ms;
  }
}
```

---

## Loading States

### Spinner

```css
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 0.9s linear infinite;
}
```

### Pulse (Skeleton Loading)

```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton {
  animation: pulse 1.5s ease-in-out infinite;
}
```

### Shimmer (Alternative to Pulse)

```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    var(--cream-100) 0%,
    var(--cream-200) 50%,
    var(--cream-100) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
```

---

## Page Load Sequence

### Recommended Stagger

```css
/* 0ms: Background fade in */
body {
  animation: fadeIn var(--transition-slow);
}

/* 200ms: Logo slides down */
.logo {
  animation: slideDown 400ms var(--ease-out-quart) 200ms backwards;
}

/* 400ms: Hero heading fades up */
.hero h1 {
  animation: fadeUp 400ms var(--ease-out-quart) 400ms backwards;
}

/* 600ms: Hero subheading fades up */
.hero p {
  animation: fadeUp 400ms var(--ease-out-quart) 600ms backwards;
}

/* 800ms: CTA button fades in */
.hero .cta {
  animation: fadeIn 400ms var(--ease-out-quart) 800ms backwards;
}

/* 1000ms+: Product cards cascade in */
.product-card:nth-child(1) { animation-delay: 1000ms; }
.product-card:nth-child(2) { animation-delay: 1100ms; }
.product-card:nth-child(3) { animation-delay: 1200ms; }
/* ... continue for all cards */
```

### Keyframes

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Interaction Feedback

### Button Press

```css
.button:active {
  transform: scale(0.98);
  transition: transform var(--transition-quick);
}
```

### Link Hover Expansion

```css
.link {
  position: relative;
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

.link:hover::after {
  width: 100%;
}
```

### Card Reveal (On Hover)

```css
.card .hidden-content {
  opacity: 0;
  transform: translateY(10px);
  transition:
    opacity var(--transition-normal),
    transform var(--transition-normal);
}

.card:hover .hidden-content {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Performance Tips

1. **Use `will-change` sparingly**: Only for elements with known, frequent animation
   ```css
   .animated-card {
     will-change: transform, opacity;
   }
   ```

2. **Remove `will-change` after animation**: Prevent unnecessary compositing
   ```css
   .animated-card.animation-ended {
     will-change: auto;
   }
   ```

3. **Use `transform: translateZ(0)`**: For GPU acceleration when needed
   ```css
   .hardware-accelerated {
     transform: translateZ(0);
   }
   ```

4. **Throttle scroll handlers**: Don't fire on every pixel
   ```javascript
   // Use requestAnimationFrame or throttle
   ```

---

## Accessibility

### Essential vs Decorative Motion

- **Essential**: State changes, focus indicators, loading feedback
- **Decorative**: Floating elements, particle effects, background animations

### Guidelines

- Essential motion: Keep even with `prefers-reduced-motion` (make instant)
- Decorative motion: Remove with `prefers-reduced-motion`

### "Pause" Control

For auto-playing animations longer than 5 seconds:

```css
.animation-paused {
  animation-play-state: paused;
}
```

Provide a pause button for user control.
