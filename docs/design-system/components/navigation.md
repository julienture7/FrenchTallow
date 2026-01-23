# Navigation Components

## Overview

Navigation elements include the header, language selector, and any future navigation patterns. The current implementation needs accessibility improvements and refinements.

---

## Site Header

### Current Implementation

```css
.site-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--gold-200);
  transition: all var(--transition-normal);
}

.site-header.scrolled {
  box-shadow: var(--shadow-subtle);
  background: rgba(255, 255, 255, 0.98);
}

.header-container {
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 1.1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

**Refinements Needed**:
- Reduce padding on scroll (condensed header)
- Add skip navigation link
- Improve mobile responsiveness

---

### Refactored Header

```css
.site-header {
  background: rgba(254, 253, 247, 0.95); /* Slightly warm white */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--gold-200);
  transition:
    padding var(--transition-normal),
    box-shadow var(--transition-normal),
    background var(--transition-normal);
}

.site-header.scrolled {
  box-shadow: var(--shadow-subtle);
  background: rgba(254, 253, 247, 0.98);
}

/* Condensed on scroll */
.site-header.scrolled .header-container {
  padding-top: var(--space-4);
  padding-bottom: var(--space-4);
}

.header-container {
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: var(--space-5) var(--space-6);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: padding var(--transition-normal);
}

/* Skip Navigation Link */
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  background: var(--sage-500);
  color: var(--white);
  padding: var(--space-2) var(--space-4);
  text-decoration: none;
  z-index: 1001;
  border-radius: var(--radius-md);
  transition: top var(--transition-quick);
}

.skip-link:focus {
  top: var(--space-4);
}
```

---

## Site Logo

### Current Implementation

```css
.site-logo {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--charcoal-200);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  transition: opacity var(--transition-quick);
}

.site-logo:hover {
  opacity: 0.8;
}

.site-logo img {
  height: 56px;
  width: auto;
}
```

### Refinements

```css
.site-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
  color: var(--charcoal-200);
  transition: opacity var(--transition-quick);
}

.site-logo:hover {
  opacity: 0.8;
}

.site-logo img {
  height: 48px;
  width: auto;
}

.site-logo .brand-text {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 600;
  display: flex;
  align-items: baseline;
  gap: 0.15rem;
}

.site-logo .brand-highlight {
  color: var(--sage-500);
}

.site-logo .tagline {
  font-family: var(--font-body);
  font-size: 0.65rem;
  font-weight: 400;
  color: var(--charcoal-50);
  text-transform: uppercase;
  letter-spacing: var(--tracking-widest);
  margin-left: var(--space-3);
  padding-left: var(--space-3);
  border-left: 1px solid var(--gold-200);
}
```

**Accessibility**: Ensure logo link has proper aria-label:
```html
<a href="/" class="site-logo" aria-label="FrenchTallowSoap - Home">
  <img src="/assets/images/logo.png" alt="FrenchTallowSoap">
  <span class="brand-text">
    <span>French</span><span class="brand-highlight">Tallow</span>Soap
  </span>
  <span class="tagline">Natural Skincare</span>
</a>
```

---

## Language Selector

### Current Implementation (NEEDS REFACTOR)

**Problems**:
- Lacks proper ARIA roles
- No keyboard navigation (arrow keys)
- No `aria-expanded` state
- Not a proper combobox/listbox pattern

```css
.lang-selector {
  position: relative;
}

.lang-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: var(--cream-100);
  border: 1px solid var(--gold-200);
  border-radius: var(--radius-full);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 500;
  transition: all var(--transition-quick);
}

.lang-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: var(--white);
  border: 1px solid var(--gold-200);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-elevated);
  padding: var(--space-3);
  display: none;
  min-width: 220px;
  max-height: 420px;
  overflow-y: auto;
  z-index: 100;
}

.lang-dropdown.active {
  display: block;
}
```

### Refactored Language Selector (Accessible)

```css
.lang-selector {
  position: relative;
}

.lang-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: var(--cream-100);
  border: 1px solid var(--gold-200);
  border-radius: var(--radius-full);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 500;
  transition:
    border-color var(--transition-quick),
    background var(--transition-quick),
    box-shadow var(--transition-quick);
}

.lang-btn:hover,
.lang-btn:focus {
  border-color: var(--sage-400);
  background: var(--white);
  box-shadow: var(--shadow-subtle);
}

.lang-btn svg {
  transition: transform var(--transition-quick);
}

.lang-selector[aria-expanded="true"] .lang-btn svg {
  transform: rotate(180deg);
}

.lang-dropdown {
  position: absolute;
  top: calc(100% + var(--space-3));
  right: 0;
  width: 100%;
  min-width: 240px;
  background: var(--white);
  border: 1px solid var(--gold-200);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-elevated);
  padding: var(--space-2);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition:
    opacity var(--transition-quick),
    transform var(--transition-quick),
    visibility var(--transition-quick);
  max-height: 400px;
  overflow-y: auto;
}

.lang-dropdown.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.lang-option {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--text-sm);
  transition:
    background var(--transition-quick),
    padding-left var(--transition-quick);
}

.lang-option:hover,
.lang-option:focus {
  background: var(--cream-100);
  padding-left: var(--space-5);
  outline: none;
}

.lang-option.selected {
  background: var(--sage-400);
  color: var(--white);
}

.lang-option.selected:hover,
.lang-option.selected:focus {
  background: var(--sage-500);
}
```

### Accessible HTML Structure

```html
<div class="lang-selector">
  <button
    class="lang-btn"
    id="languageButton"
    aria-haspopup="listbox"
    aria-expanded="false"
    aria-labelledby="languageButton"
  >
    <span id="currentLang">English</span>
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
      <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
  </button>
  <ul
    class="lang-dropdown"
    id="languageList"
    role="listbox"
    aria-labelledby="languageButton"
  >
    <li role="option">
      <button class="lang-option selected" data-lang="en" aria-selected="true">
        English
      </button>
    </li>
    <li role="option">
      <button class="lang-option" data-lang="fr" aria-selected="false">
        Français
      </button>
    </li>
    <!-- ... more languages ... -->
  </ul>
</div>
```

### Keyboard Navigation JavaScript

```javascript
// Keyboard navigation for language selector
const langSelector = document.querySelector('.lang-selector');
const langBtn = langSelector.querySelector('.lang-btn');
const langDropdown = langSelector.querySelector('.lang-dropdown');
const langOptions = langDropdown.querySelectorAll('.lang-option');

// Toggle dropdown
langBtn.addEventListener('click', () => {
  const isExpanded = langBtn.getAttribute('aria-expanded') === 'true';
  langBtn.setAttribute('aria-expanded', !isExpanded);
  langDropdown.classList.toggle('active', !isExpanded);
  if (!isExpanded) {
    langOptions[0].focus();
  }
});

// Keyboard navigation
langOptions.forEach((option, index) => {
  option.addEventListener('keydown', (e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        const next = langOptions[index + 1] || langOptions[0];
        next.focus();
        break;
      case 'ArrowUp':
        e.preventDefault();
        const prev = langOptions[index - 1] || langOptions[langOptions.length - 1];
        prev.focus();
        break;
      case 'Escape':
        langDropdown.classList.remove('active');
        langBtn.setAttribute('aria-expanded', 'false');
        langBtn.focus();
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        option.click();
        break;
    }
  });
});

// Close when clicking outside
document.addEventListener('click', (e) => {
  if (!langSelector.contains(e.target)) {
    langDropdown.classList.remove('active');
    langBtn.setAttribute('aria-expanded', 'false');
  }
});
```

---

## Mobile Navigation (Future Enhancement)

### Hamburger Menu

```css
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: var(--space-2);
    background: transparent;
    border: none;
    cursor: pointer;
  }

  .mobile-menu-btn span {
    width: 24px;
    height: 2px;
    background: var(--charcoal-200);
    border-radius: 2px;
    transition: all var(--transition-normal);
  }

  .mobile-menu-btn[aria-expanded="true"] span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }

  .mobile-menu-btn[aria-expanded="true"] span:nth-child(2) {
    opacity: 0;
  }

  .mobile-menu-btn[aria-expanded="true"] span:nth-child(3) {
    transform: rotate(-45deg) translate(5px, -5px);
  }

  .mobile-nav {
    position: fixed;
    inset: 0;
    background: var(--cream-50);
    padding: var(--space-6);
    transform: translateX(100%);
    transition: transform var(--transition-normal);
    z-index: 999;
  }

  .mobile-nav.active {
    transform: translateX(0);
  }
}
```

---

## Breadcrumbs (Future)

```css
.breadcrumbs {
  display: flex;
  gap: var(--space-2);
  padding: var(--space-4) 0;
  font-size: var(--text-sm);
}

.breadcrumb-item {
  color: var(--charcoal-50);
}

.breadcrumb-item:not(:last-child)::after {
  content: '/';
  margin-left: var(--space-2);
  color: var(--gold-300);
}

.breadcrumb-item a {
  color: var(--sage-400);
  text-decoration: none;
}

.breadcrumb-item a:hover {
  color: var(--sage-600);
}

.breadcrumb-item[aria-current="page"] {
  color: var(--charcoal-200);
  font-weight: 500;
}
```

---

## Accessibility Checklist

- [x] Skip navigation link
- [ ] Language selector proper ARIA pattern (combobox/listbox)
- [ ] Keyboard navigation for all menus
- [ ] Focus visible states on all interactive elements
- [ ] aria-current for current page
- [ ] aria-label for logo link
- [ ] aria-expanded for dropdown toggles
- [ ] Escape key closes dropdowns
- [ ] Click outside closes dropdowns
- [ ] Focus management after menu close
