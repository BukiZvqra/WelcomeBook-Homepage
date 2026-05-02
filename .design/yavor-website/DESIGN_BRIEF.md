# Design Brief: TES Borovets — Yavor Website

## Problem

Туристите (BG + EN) намират tes-borovets.com, виждат претрупан сайт без ясна структура и не разбират лесно какво предлага Явор, в кои комплекси са апартаментите, нито как да резервират. 17 години опит и 21 имота са невидими зад визуален шум. Резултат: изгубено доверие преди първи контакт.

## Solution

Чист, топъл, Scandinavian-inspired сайт, позициониращ Боровец като сезонна дестинация (зима + лято) и Явор като доверен local expert с 17 години опит. Funnel: **вижте курорта → доверете се на домакина → намерете апартамент → свържете се директно.** Без booking engine в Phase 1 — директен контакт чрез форма, Viber и WhatsApp.

## Experience Principles

1. **Дестинация first, апартаменти second** — Боровец е истинската продажба. Апартаментите следват, след като гостът е „купил" курорта.
2. **Доверие чрез конкретност** — „150м от Гондола", „от 2009", „21 имота в 4 комплекса" > generic „beautiful mountain apartments". Числата са credibility.
3. **Едно действие на екран** — всяка секция има един primary CTA. Гостът не избира между 4 бутона на едно място.

## Aesthetic Direction

- **Philosophy**: Scandinavian Alpine — топло, естествено, generous whitespace, нисък визуален шум. Чисто, но не студено.
- **Tone**: Warm, trustworthy, professional без да е corporate. Гласът е „личен подход от опитен домакин", не „luxury resort brand". Близо до Airbnb Superhost вибата.
- **Reference points**: Nordic ski resorts (Hemsedal.com, SkiStar.com) за структура и whitespace; добри Airbnb listings за specificity; Visit Bulgaria тип сайтове за сезонни снимки.
- **Anti-references**: Booking.com clutter; Flash-era български туристически сайтове; студен Apple-style minimalism; stock-photo feel с усмихнати непознати.

## Existing Patterns

Шаблонът има изграден design system. Всичко ново **разширява**, не замества.

- **Colors**: `--primary: #1B3A52` (deep alpine blue) · `--accent: #C9A961` (warm gold) · `--surface: #FAFAF7` (warm off-white) · `--sky: #E8EEF2` (soft blue-grey) · `--text: #2C2C2C`
- **Typography**: System sans-serif (Helvetica / -apple-system / Segoe UI), rem scale `--text-xs` (0.75rem) → `--text-4xl` (3.5rem), headings weight 700–800
- **Spacing**: `--space-sm` (0.5rem) → `--space-4xl` (6rem)
- **Borders**: `--radius: 8px` · `--border: #dde3e8` · `--shadow: 0 2px 10px rgba(27,58,82,0.10)`
- **Components**: `.btn` / `.btn-primary` / `.btn-outline`, `.complex-card`, `.service-card`, `.contact-card`, `.site-header`, `.hero`, `.site-footer`

## Component Inventory

| Component | Status | Notes |
|---|---|---|
| `site-header` | Modify | + Viber бутон (BG аудитория) + WhatsApp бутон (international) + BG/EN lang switcher |
| `.hero` (static) | Exists | Seasonal alpine image, dark overlay, 2 CTA. Phase 2 → crossfade upgrade |
| `.complexes-grid` / `.complex-card` | Exists | 4 карти на homepage, линкват към `/complex/{id}/` |
| `/apartments/` page | New | Listing на всички апартаменти по тип (двойна → студио → 1-спален → 2-спален) |
| `/complex/{id}/` pages (×4) | New | Flora + Royal Plaza + Rila Park + Borovets Gardens |
| `/services/` page | New | 6 услуги в clean grid, без dropdown |
| `/about-borovets/` page | New | Курортен контекст, сезони, защо Боровец |
| `/contact/` page + Netlify Form | New | Form + Viber + WhatsApp + click-to-call |
| Language switcher BG/EN | New | i18n-ready, RU slot reserved за Phase 2 |
| `.service-card` (preview) | Exists | На homepage — линк към `/services/` |
| `site-footer` | Exists | 4 колони, compliant |

## Key Interactions

**Header:**
- Viber бутон → `viber://chat?number=+359888909237` (само mobile)
- WhatsApp бутон → `https://wa.me/359888909237`
- Lang switcher → `/en/` prefix route (static pages) или query param; RU slot е hidden/disabled в Phase 1
- Mobile hamburger → CSS-only `:focus-within` nav reveal (вече имплементирано)

**Hero:**
- Primary CTA „Виж апартаментите" → `/apartments/`
- Secondary CTA „Свържи се с нас" → `/contact/`

**Complexes:**
- Всяка карта „Виж апартаменти" → `/complex/{id}/`

**Contact форма (Netlify Forms):**
- Fields: Вашето им / Email / Телефон (optional) / Съобщение / Honeypot (hidden spam)
- On submit → Netlify handles, success message на страницата (no redirect)
- Click-to-call: `tel:+359888909237` и `tel:+359887887810`

## Responsive Behavior

| Зона | Mobile (<768px) | Tablet (768px+) | Desktop (1024px+) |
|---|---|---|---|
| Header | Logo + hamburger + WhatsApp icon | Full nav + contact buttons | Full nav + contact buttons |
| Hero | 100vh, gradient overlay, stacked CTAs | 90vh, side-by-side CTAs | 90vh |
| Complexes grid | 1 col | 2 col | 2 col (по-широки карти) |
| Services grid | 2 col | 3 col | 3 col |
| Contact grid | 1 col | 3 col | 3 col |
| Footer | 1 col | 2 col | 4 col |
| Viber бутон | Видим в header и contact | Видим | Видим |

Компоненти, които **сменят поведение** (не само размер) на mobile:
- `.main-nav` → скрита, разкрива се с `:focus-within`
- `.hero` → height 100vh (не 90vh) за по-драматичен ефект
- Viber бутон в header → само иконка без текст на <480px

## Accessibility Requirements

- **Contrast**: `--primary` (#1B3A52) на бяло = 14.7:1 (AAA) ✓ · `--accent` (#C9A961) на `--primary` = 6.6:1 (AA) ✓
- **Touch targets**: min 44×44px на всички интерактивни елементи (вече в CSS)
- **Semantic HTML**: `<header>`, `<nav aria-label="главна навигация">`, `<main>`, `<footer>`, правилна heading йерархия (h1 → h2 → h3)
- **Form**: `<label>` за всеки input, `required` attributes, видими error states
- **Images**: описателен `alt` за всяка снимка на комплекс/hero
- **Focus**: видим `:focus-visible` outline на всички interactive елементи

## Language Strategy

- **Phase 1**: BG (primary) + EN — статични .njk файлове, `/en/` prefix за EN версия
- **Phase 2**: RU — добавя се трети prefix `/ru/` без architectural промени
- **i18n-ready**: config.json вече има `language_phase_2: ["ru"]`, шаблонът се пише с преводими strings в config
- **Не се ползва JS i18n framework** — статични Eleventy pages са достатъчни за 3 езика при 20+ страни

## Out of Scope (Phase 1)

- BNBForms booking widget (`bnbforms_enabled: false` в config)
- RU езикова версия
- AI чатбот
- Royal Plaza, Rila Park, Borovets Gardens портали (само Flora)
- CSS crossfade hero (Phase 2 upgrade)
- Booking calendar / availability check
- Страницата „Продажба на емоции" (placeholder, не се build-ва)
- Admin panel

---

*Drafted:* 2026-05-01  
*Client:* Yavor Кичев / Tour Express Service Ltd.  
*Phase:* 1 (site + contact form + Flora portal)  
*Deadline:* Декември 2026 (преди ски сезон)
