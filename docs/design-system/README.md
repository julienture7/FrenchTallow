# FrenchTallowSoap Design System

**Version**: 1.0
**Last Updated**: 2025-01-19
**Status**: Foundation + Extraction Phase

## Overview

This design system captures the reusable components, design tokens, and patterns for the FrenchTallowSoap website. It serves as the single source of truth for design decisions and enables systematic consistency across the interface.

### Design Principles

1. **Refined Restraint** - Every element must earn its place. Let typography and whitespace do the heavy lifting.
2. **Trust Through Transparency** - Clear product information, authentic imagery, straightforward navigation.
3. **Warm Minimalism** - Minimal but never cold. Use warm neutrals, subtle textures, gentle transitions.
4. **Left-Aligned Sophistication** - Avoid center-alignment. Left-align with asymmetric compositions.
5. **Typography as Voice** - Distinctive, well-paired fonts with careful attention to scale, weight, spacing.

## Architecture

```
design-system/
├── README.md              # This file - system overview
├── tokens/                # Design tokens (colors, typography, spacing)
│   ├── colors.md         # Color palette with usage guidelines
│   ├── typography.md     # Type scale, font families, line heights
│   ├── spacing.md        # Spacing scale and rhythm
│   ├── shadows.md        # Shadow system
│   └── transitions.md    # Animation timing and easing
├── components/            # Reusable UI components
│   ├── buttons.md        # Button variants and states
│   ├── cards.md          # Product and article cards
│   ├── navigation.md     # Header, language selector
│   └── badges.md         # Trust badges, tags
└── patterns/              # Layout and composition patterns
    ├── layouts.md        # Grid systems, container patterns
    └── composition.md    # Asymmetric layouts, visual hierarchy
```

## Usage

This design system is **documentative**—it captures and formalizes existing patterns. The CSS implementation remains inline in `public/index.html` for optimal performance (minimal HTTP requests).

When making design changes:
1. Consult this documentation for established patterns
2. Update the documentation when introducing new patterns
3. Ensure changes align with the design principles

## Token Hierarchy

Design tokens are organized into three levels:

1. **Primitive Tokens** - Base values (e.g., `--color-sage-500: #8B9F7C`)
2. **Semantic Tokens** - Purpose-specific values (e.g., `--color-primary: var(--color-sage-500)`)
3. **Component Tokens** - Component-specific overrides (e.g., `--button-bg: var(--color-primary)`)

## Component Status

| Component | Status | Notes |
|-----------|--------|-------|
| Button | ✅ Documented | Primary, secondary, ghost variants |
| Product Card | 🔄 Needs Refactor | Currently generic grid, needs variation |
| Article Card | 🔄 Needs Refactor | Needs featured/standard variants |
| Language Selector | ✅ Documented | Dropdown pattern, i18n considerations |
| Trust Badge | 🔄 Needs Refactor | Should be semantic HTML |
| Filter Pill | ⚠️ Deprecated | Will be replaced with discovery pattern |

## Roadmap

### Phase 1: Foundation (Current)
- ✅ Design principles established
- ✅ Design context documented
- ✅ Component inventory completed
- 🔄 Token extraction in progress
- ⏳ Component documentation

### Phase 2: Refinement
- ⏳ Refactor components based on critique findings
- ⏳ Add component variants (featured, standard, compact)
- ⏳ Implement asymmetric layouts
- ⏳ Add refined typography system

### Phase 3: Polish
- ⏳ Add micro-interactions
- ⏳ Implement animation system
- ⏳ Complete accessibility enhancements
- ⏳ Performance optimization

## Contributing

When modifying the design system:

1. **Document changes** - Update relevant documentation files
2. **Maintain consistency** - Follow established patterns
3. **Test thoroughly** - Check all component variants and states
4. **Consider accessibility** - WCAG 2.1 Level AA compliance
5. **Validate i18n** - Ensure patterns work for 24 languages

---

*This design system is a living document. It evolves with the product and should be updated as patterns emerge and improve.*
