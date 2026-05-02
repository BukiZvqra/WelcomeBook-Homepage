# Design Tokens: TES Borovets

> Philosophy: **Scandinavian Alpine** — топло, естествено, generous whitespace, нисък визуален шум.
> Stack: Pure CSS custom properties (no Tailwind, no JS framework).

---

## Color Primitives

### Primary — Deep Alpine Blue

| Token | Value | Usage |
|---|---|---|
| `--color-primary-50` | `#F0F4F8` | Lightest tint, hover backgrounds |
| `--color-primary-100` | `#D9E2EC` | Light backgrounds |
| `--color-primary-200` | `#BCCCDC` | Borders on light bg |
| `--color-primary-300` | `#9FB3C8` | Disabled states |
| `--color-primary-400` | `#829AB1` | Secondary text on dark |
| `--color-primary-500` | `#486581` | Interactive icons |
| `--color-primary-600` | `#334E68` | Active nav |
| `--color-primary-700` | `#243B53` | Main brand color (headings, UI) |
| `--color-primary-800` | `#1B3A52` | ← **default `--primary`** |
| `--color-primary-900` | `#102A43` | Footer background, darkest surfaces |

### Accent — Warm Gold/Amber

| Token | Value | Usage |
|---|---|---|
| `--color-accent-50` | `#FFFAF0` | Lightest tint |
| `--color-accent-100` | `#FEEBC8` | Badge backgrounds |
| `--color-accent-200` | `#FBD38D` | Highlight backgrounds |
| `--color-accent-300` | `#F6AD55` | Footer headings |
| `--color-accent-400` | `#ED8936` | Hover accent |
| `--color-accent-500` | `#C9A961` | ← **default `--accent`**, CTAs, nav active |
| `--color-accent-600` | `#B7791F` | Eyebrow text, labels |
| `--color-accent-700` | `#975A16` | Dark accent |

### Neutral — Warm Whites (NOT cold grey)

| Token | Value | Usage |
|---|---|---|
| `--color-neutral-0` | `#FFFFFF` | Pure white (cards) |
| `--color-neutral-50` | `#FAFAF7` | ← **default `--surface`**, page background |
| `--color-neutral-100` | `#F4F4EF` | Alternate section backgrounds |
| `--color-neutral-200` | `#E8E8E1` | Borders, dividers |
| `--color-neutral-300` | `#D4D4CB` | Input borders |
| `--color-neutral-400` | `#A8A89E` | Placeholder text |
| `--color-neutral-500` | `#707068` | Secondary text |
| `--color-neutral-600` | `#4F4F47` | Muted body text |
| `--color-neutral-700` | `#2C2C2C` | ← **default `--text`**, body text |
| `--color-neutral-800` | `#1A1A1A` | Emphasized text |
| `--color-neutral-900` | `#0F0F0F` | Near-black |

### Semantic

| Token | Value |
|---|---|
| `--color-success` | `#2F855A` |
| `--color-warning` | `#C9A961` (same as accent) |
| `--color-error` | `#C53030` |
| `--color-info` | `#2C5282` |

---

## Semantic Layer (mapped to primitives)

```css
--color-bg-primary:       var(--color-neutral-50)   /* Page background */
--color-bg-secondary:     #fff                       /* Card backgrounds */
--color-bg-tertiary:      var(--color-neutral-100)   /* Wells, inputs */
--color-bg-inverse:       var(--color-primary-900)   /* Footer, dark sections */

--color-text-primary:     var(--color-neutral-700)   /* Body text */
--color-text-secondary:   var(--color-neutral-500)   /* Secondary text */
--color-text-tertiary:    var(--color-neutral-400)   /* Placeholder */
--color-text-inverse:     var(--color-neutral-50)    /* On dark bg */
--color-text-link:        var(--color-primary-700)   /* Links */

--color-border-default:   var(--color-neutral-200)   /* Dividers, card borders */
--color-border-subtle:    var(--color-neutral-100)   /* Very subtle separation */
--color-border-focus:     var(--color-accent-500)    /* Focus rings */

--color-accent-default:   var(--color-accent-500)    /* Primary CTAs */
--color-accent-hover:     var(--color-accent-600)    /* CTA hover */
```

---

## Typography

### Font Stack

```css
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
             'Helvetica Neue', Arial, sans-serif;
```

System fonts only — zero loading time, GDPR-clean, native Cyrillic support.

### Scale (rem-based)

| Token | Value | px equiv. | Usage |
|---|---|---|---|
| `--text-xs` | `0.75rem` | 12px | Captions, labels, fine print |
| `--text-sm` | `0.875rem` | 14px | Secondary text, table cells |
| `--text-base` | `1rem` | 16px | Body text (default) |
| `--text-lg` | `1.125rem` | 18px | Lead paragraphs |
| `--text-xl` | `1.25rem` | 20px | h4 / card titles |
| `--text-2xl` | `1.5rem` | 24px | h3 / section sub-headings |
| `--text-3xl` | `2rem` | 32px | h2 / section headings |
| `--text-4xl` | `2.75rem` | 44px | h1 / page headings |
| `--text-5xl` | `clamp(2.5rem, 6vw, 4.5rem)` | 40–72px | Hero headlines |

### Weights

| Token | Value |
|---|---|
| `--font-normal` | `400` |
| `--font-medium` | `500` |
| `--font-semibold` | `600` |
| `--font-bold` | `700` |

### Line Heights

| Token | Value | Usage |
|---|---|---|
| `--leading-tight` | `1.15` | Headlines |
| `--leading-snug` | `1.35` | Sub-headings |
| `--leading-normal` | `1.55` | Body text |
| `--leading-relaxed` | `1.7` | Long-form, captions |

### Letter Spacing

| Token | Value | Usage |
|---|---|---|
| `--tracking-tight` | `-0.02em` | Hero headlines |
| `--tracking-normal` | `0` | Body |
| `--tracking-wide` | `0.05em` | Eyebrow / ALL-CAPS labels |

---

## Spacing (4px base, rem values)

| Token | Value | px equiv. | Usage |
|---|---|---|---|
| `--space-1` | `0.25rem` | 4px | Inline tight spacing |
| `--space-2` | `0.5rem` | 8px | Closely related elements |
| `--space-3` | `0.75rem` | 12px | Component internal padding |
| `--space-4` | `1rem` | 16px | Default paragraph spacing |
| `--space-5` | `1.5rem` | 24px | Section internals (mobile padding) |
| `--space-6` | `2rem` | 32px | Card spacing |
| `--space-7` | `3rem` | 48px | Section spacing (desktop) |
| `--space-8` | `4rem` | 64px | Major sections |
| `--space-9` | `6rem` | 96px | Hero padding |
| `--space-10` | `8rem` | 128px | Extreme whitespace |

---

## Containers

| Token | Value | Usage |
|---|---|---|
| `--container-sm` | `640px` | Narrow content (text pages) |
| `--container-md` | `768px` | Standard articles |
| `--container-lg` | `1024px` | Default (most pages) |
| `--container-xl` | `1280px` | Wide content |

---

## Border Radius

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | `4px` | Small elements (badges, tags) |
| `--radius-md` | `8px` | Cards, inputs, buttons (default) |
| `--radius-lg` | `12px` | Large cards |
| `--radius-xl` | `16px` | Hero sections, modals |
| `--radius-full` | `9999px` | Pills, avatars |

---

## Shadows (subtle, Scandinavian — large blur, low opacity)

| Token | Value | Usage |
|---|---|---|
| `--shadow-sm` | `0 1px 2px 0 rgba(36,59,83,0.05)` | Subtle elevation |
| `--shadow-md` | `0 4px 6px -1px rgba(36,59,83,0.08), 0 2px 4px -1px rgba(36,59,83,0.04)` | Cards (default) |
| `--shadow-lg` | `0 10px 15px -3px rgba(36,59,83,0.10), 0 4px 6px -2px rgba(36,59,83,0.05)` | Hover state elevation |
| `--shadow-xl` | `0 20px 25px -5px rgba(36,59,83,0.10), 0 10px 10px -5px rgba(36,59,83,0.04)` | Modals, overlays |

---

## Motion

| Token | Value | Usage |
|---|---|---|
| `--duration-fast` | `150ms` | Hover effects, micro-interactions |
| `--duration-base` | `250ms` | State transitions (default) |
| `--duration-slow` | `400ms` | Reveals, page transitions |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Natural deceleration |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Balanced transitions |

---

## Breakpoints

| Token | Value | Context |
|---|---|---|
| `--bp-sm` | `375px` | Mobile (base) |
| `--bp-md` | `768px` | Tablet |
| `--bp-lg` | `1024px` | Desktop |
| `--bp-xl` | `1280px` | Wide desktop |

---

## Backward-Compatible Aliases

The CSS also defines legacy aliases so existing template code continues to work:

```css
--primary: var(--color-primary-800)     /* #1B3A52 */
--accent:  var(--color-accent-500)      /* #C9A961 */
--surface: var(--color-neutral-50)      /* #FAFAF7 */
--text:    var(--color-neutral-700)     /* #2C2C2C */
--sky:     #E8EEF2
--border:  var(--color-neutral-200)     /* #E8E8E1 */
--shadow:  var(--shadow-md)

/* Legacy spacing */
--space-sm:  var(--space-2)   /* 0.5rem */
--space-md:  var(--space-4)   /* 1rem   */
--space-lg:  var(--space-5)   /* 1.5rem */
--space-xl:  var(--space-6)   /* 2rem   */
--space-2xl: var(--space-7)   /* 3rem   */
--space-3xl: var(--space-8)   /* 4rem   */
--space-4xl: var(--space-9)   /* 6rem   */

/* Legacy container */
--container: var(--container-lg)   /* 1024px */

/* Legacy radius */
--radius: var(--radius-md)   /* 8px */
```

---

## Dark Mode

Phase 1: Not implemented. The color palette has warm neutrals that invert naturally.

Phase 2 approach: `[data-theme="dark"]` overrides on `:root`. Dark bg = `--color-primary-900`, surfaces = `--color-primary-800`, text = `--color-primary-100`. Accent remains `--color-accent-400` (slightly lighter for dark bg contrast).

---

*Generated:* 2026-05-01  
*Client:* Yavor Кичев / TES Borovets  
*Philosophy:* Scandinavian Alpine
