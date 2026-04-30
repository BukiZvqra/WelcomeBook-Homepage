# Client Design System

> Universal design rules за всички клиентски сайтове, build-нати от WelcomeBook Agency.
>
> **Какво е това:** Технически правила за typography, layout, photography, copy и accessibility, които **не зависят** от brand-а на конкретния клиент.
>
> **Какво НЕ е това:** Това НЕ е наш brand spec (Midnight Navy + Orange). Цветовете, лого, тон на гласа на всеки клиент са негови собствени.
>
> **Кой го следва:** Claude Code при build на website + portal templates. Ти, при ръчни корекции.

---

## 1. КЛЮЧОВ ПРИНЦИП

Всеки клиентски сайт има **свой бранд** (цветове, лого, име). Този документ описва **универсалните технически правила**, които правят всеки сайт:

- ✅ Бърз (performance-first)
- ✅ Достъпен (mobile + accessibility)
- ✅ Професионален (typography + layout consistency)
- ✅ GDPR-compliant (no Google Fonts, no third-party tracking)
- ✅ Български-friendly (Cyrillic typography, Bulgarian conventions)

Brand-ът на клиента сe прилага **върху** тези правила, не **вместо** тях.

---

## 2. TYPOGRAPHY — UNIVERSAL RULES

### 2.1 Font stack (no Google Fonts, no custom webfonts)

```css
font-family: 'Helvetica', 'Arial', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Защо system fonts:**
- ⚡ **Performance** — zero loading time (font-ът вече е на устройството на госта)
- 🇧🇬 **Cyrillic support** — Helvetica и Arial имат добра кирилица; Segoe UI е default за Windows; -apple-system за macOS/iOS
- 🔒 **GDPR** — Google Fonts изпраща IP към Google (нарушение в EU). System fonts = нула 3rd party.
- 📱 **Native feel** — изглежда естествено на всеки device

**Изключение:** Ако клиентът explicitly предостави свой font (paid license), приемаме го. Но **никога Google Fonts**.

### 2.2 Type scale (rem-based)

| Token | Size | Usage |
|---|---|---|
| `--text-xs` | 0.75rem (12px) | Captions, labels, fine print |
| `--text-sm` | 0.875rem (14px) | Secondary text, table cells |
| `--text-base` | 1rem (16px) | **Body text — default** |
| `--text-lg` | 1.125rem (18px) | Lead paragraphs |
| `--text-xl` | 1.5rem (24px) | Sub-headings, card titles |
| `--text-2xl` | 2rem (32px) | Section headings |
| `--text-3xl` | 2.5rem (40px) | Page headings |
| `--text-4xl` | 3.5rem (56px) | Hero headlines |

**Защо rem (не px):** User може да увеличи default font size в browser-а (accessibility) — rem респектира това, px не.

### 2.3 Type weights

- `400` — Regular body text
- `600` — Semi-bold for emphasis, sub-headings
- `700` — Bold for headlines
- `800` — Extra bold (rare, only top-level hero headlines)

**НЕ използвай:**
- `300` (Light) — нечетимо при малки sizes на retina screens
- `900` (Black) — твърде тежко, изглежда pretentious

### 2.4 Line height

- Headlines: `1.15` (tight)
- Body: `1.55` (comfortable reading)
- Captions: `1.4` (compact)

### 2.5 Type rules

✅ **DO:**
- Headlines на български **винаги normal-case** — никога ALL CAPS
- Body text **винаги ляво-подравнено** — не justify (justify прави неравномерни spaces в Cyrillic)
- Maximum line length: **65-75 characters** (включително spaces)
- Bulgarian text заема **~20% повече horizontal space** от English — design-вай за това

❌ **DON'T:**
- Никакви ALL CAPS на български (нечетимо: "АПАРТАМЕНТИ В БОРОВЕЦ" е грозно)
- Не разреждай character spacing на body text
- Не използвай italic за дълги passages (Bulgarian italic е лош на screen)
- Не миксвай serif + sans-serif на същата страница

---

## 3. LAYOUT & SPACING

### 3.1 Mobile-first principle

Всеки template започва от **mobile (320-380px width)**, после се разширява за tablet и desktop.

**Защо:**
- 60-70% от guests на rental sites резервират от телефон
- Mobile-first = по-малко CSS overhead на mobile (бързо)
- По-лесно е да scale up отколкото down

### 3.2 Spacing scale (rem-based)

| Token | Size | Usage |
|---|---|---|
| `--space-xs` | 0.25rem (4px) | Inline elements, tight |
| `--space-sm` | 0.5rem (8px) | Closely related elements |
| `--space-md` | 1rem (16px) | Default spacing |
| `--space-lg` | 1.5rem (24px) | Section internals (mobile padding) |
| `--space-xl` | 2rem (32px) | Card spacing |
| `--space-2xl` | 3rem (48px) | Section spacing (desktop padding) |
| `--space-3xl` | 4rem (64px) | Major page sections |
| `--space-4xl` | 6rem (96px) | Hero spacing |

### 3.3 Container widths

```css
--container-sm: 640px;    /* Narrow content (текстови страници) */
--container-md: 768px;    /* Standard articles */
--container-lg: 1024px;   /* Default (most pages) */
--container-xl: 1280px;   /* Wide content (galleries, dashboards) */
--container-2xl: 1536px;  /* Full-width hero (rare) */
```

**Default за повечето секции:** `--container-lg` (1024px max-width).

### 3.4 Layout principles

✅ **DO:**
- White space e sacred — поне **40-50%** от layout-а (генерозни padding/margin)
- Single accent color per surface (или primary, или semantic, не и двете)
- Cards имат subtle elevation (slight shadow или border, не двете)
- Generous tap targets на mobile (min 44×44px по Apple HIG)

❌ **DON'T:**
- Не претрупвай всичко на един екран
- Не използвай повече от 3 цвята в едно visual element (background + text + accent)
- Не миксвай различни border-radius на сходни компоненти
- Не правиш fixed pixel widths за text containers

---

## 4. PHOTOGRAPHY & IMAGERY

### 4.1 Photo style (за rental property сайтове)

| Категория | Правила |
|---|---|
| **Property photos** | Bright, naturally lit, wide angles. **No fish-eye, no over-saturation.** |
| **Hero images** | Lifestyle-oriented (как изглежда престоя), не clinical real estate shots |
| **Gallery** | Consistent crop ratios, последователен white balance, no random Instagram filters |
| **Owner/host photos** | Real photos с разрешение. Никакви stock photos на хора. |

### 4.2 Acceptable photo processing

✅ **OK:**
- Light/shadow adjustment (basic exposure)
- White balance correction
- Slight saturation bump (max +10%)
- Crop & alignment
- Cloudinary auto-format/auto-quality (вижда се само от browser-а)

❌ **NOT OK:**
- HDR-look (tone-mapped, fake)
- Vignettes (черни ъгли)
- Fake bokeh / blurred backgrounds
- AI-generated stock people (видими artifacts)
- Heavy Instagram-style filters

### 4.3 Source rules

✅ **OK source:**
- Photos taken by клиента (или собственика)
- Shots от Airbnb/Booking listings (с permission)
- AI-enhanced versions of original property photos (не AI-generated from scratch)
- Photos на местни забележителности (Wikimedia Commons, Unsplash, или с photographer permission)

❌ **НЕ OK:**
- Stock photos на хора с visible "stock" feel ("happy family in front of generic house")
- AI-generated property exteriors (legal risk + fake feeling)
- Pinterest-found images (copyright)
- Screenshots от competitors

### 4.4 Image storage & delivery

**Always Cloudinary** (`welcomebook-agency` cloud name). Никога снимки в Git.

URL pattern с auto-format/auto-quality:
```
https://res.cloudinary.com/welcomebook-agency/image/upload/f_auto,q_auto/clients/[client_id]/[file]
```

**Image dimensions guideline:**
- Hero: 1920×1080 source, displayed responsive
- Gallery: 1200×900 source
- Thumbnails: 400×300 source
- Cloudinary auto-resize-ва според device

---

## 5. ICONOGRAPHY

### 5.1 Style

**Lucide icons** (или Heroicons, Tabler Icons) — open source, consistent set.

**Stroke weight:** 1.5-2px

**Sizes:**
- Min: 16px
- Optimum: 20-24px
- Large: 32px (hero CTAs)

### 5.2 Color rules

✅ **DO:**
- Иконите винаги в **same color** as surrounding text (или brand accent за emphasis)
- Consistent stroke weight в всички иконы on the same surface

❌ **DON'T:**
- Не миксвай filled и outlined icons на същата surface
- Не използвай **face emoji** (😊 😅 🎉) като icons в official content (виж 8.4)
- Не използвай иконы с brand-specific цветове, ако сайтът е monochrome

> **Note:** Unicode symbols като ✓ ★ ✕ → не са face emoji — те са typography characters. Използването им като trust markers е OK (виж секция 8.4).

---

## 6. ACCESSIBILITY

### 6.1 Mandatory rules

✅ **Color contrast:** WCAG AA минимум за текст
- Body text: 4.5:1 contrast ratio
- Large text (18px+ bold или 24px+): 3:1
- UI elements (бутоните): 3:1

✅ **Tap targets на mobile:** минимум 44×44px (Apple HIG)

✅ **Alt text за всяка снимка:**
- Hero: `alt="Изглед от спалнята на [Property Name] към планината"`
- Gallery: `alt="Кухня с гранитен плот и модерни уреди"`
- Decorative: `alt=""` (празно — screen reader ще го пропусне)

✅ **Semantic HTML:**
- `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`
- `<h1>` един път на страница; `<h2>`-`<h3>` йерархично
- Linkове като `<a>`, бутоните като `<button>`

### 6.2 Mobile accessibility

- Min font size: 16px (under 16px iOS auto-zoom-ва форми)
- Bottom navigation/CTA min 60px height (thumb-friendly)
- Forms: explicit `<label>` (не само placeholder)

---

## 7. PERFORMANCE

### 7.1 Critical metrics

Всеки клиентски сайт трябва да има:

| Metric | Target |
|---|---|
| Lighthouse Performance | 85+ |
| Largest Contentful Paint | < 2.5s |
| First Input Delay | < 100ms |
| Cumulative Layout Shift | < 0.1 |

### 7.2 Performance rules

✅ **DO:**
- Cloudinary `f_auto,q_auto` за всички снимки
- Lazy loading за below-the-fold images: `<img loading="lazy">`
- Inline critical CSS (above-the-fold), defer the rest
- System fonts (zero font loading time)
- Async loading на 3rd party scripts (BNBForms widget)

❌ **DON'T:**
- Никакви Google Fonts
- Никакви jQuery (vanilla JS where possible)
- Не зареждай video файлове на mobile (използвай poster image)
- Не embed-вай YouTube iframes без `loading="lazy"`

---

## 8. COPYWRITING — UNIVERSAL RULES

> **Note:** Тук НЕ говорим за tone of voice (всеки клиент има свой). Говорим за **технически copy правила** валидни за всички български сайтове.

### 8.1 Bulgarian punctuation

✅ **DO:**
- **Visible content (на сайта):** използвай правилни Bulgarian кавички `„..."` (долна-горна) — стандартът на български език
- **HTML атрибути и code:** използвай английски `"..."` (HTML изисква това)
- Тирета винаги — (em-dash) с интервали ОТ ДВЕТЕ страни
- Многоточие винаги ... (3 точки), не …
- Запетая преди "но", "а", "обаче"

**Пример (от content.md към HTML output):**
```markdown
<!-- В content.md (visible content) -->
Гостите казват „чудесно място, ще се върнем!"

<!-- Eleventy render-ва в HTML с правилни кавички за visible text -->
<p>Гостите казват „чудесно място, ще се върнем!"</p>

<!-- HTML атрибутите винаги с английски кавички -->
<img src="kitchen.jpg" alt="Кухнята с гранитен плот">
```

❌ **DON'T:**
- Не миксвай `„..."` и `"..."` в visible content на едно място
- Не използвай `« »` (френски guillemets) за български текст
- Не използвай ! повече от 1 пъти в текст (изглежда desperate)
- Не използвай all-caps за emphasis ("ВАЖНО:" → използвай **"Важно:"**)

### 8.2 Numbers & specifics

Винаги **конкретни числа** > vague descriptions:
- ✅ "150 метра от Gondola lift"
- ❌ "близо до лифта"

### 8.3 Length guidelines per element

| Контекст | Макс дължина |
|---|---|
| Headline | 8 думи |
| Sub-headline | 15 думи |
| Hero paragraph | 35 думи |
| Section title | 6 думи |
| Card description | 50-80 думи |
| Testimonial | 30-60 думи |
| CTA button text | 2-4 думи |
| Form field label | 1-3 думи |
| Error message | 1 sentence |

### 8.4 Emoji & Unicode symbols policy

**Важно разграничение:** "emoji" и "Unicode symbols" не са едно и също.

**Unicode symbols** (typography characters):
- ✓ ✕ ★ ☆ → ← ↑ ↓ ▲ ▼ ●
- Тези са OK за trust markers, рейтинги, индикатори
- Не са "emoji" в съвременния смисъл — те са typography

**Face/object emoji** (graphical):
- 😊 😅 🎉 🚀 🔥 💯 — graphical pictographs
- Тези са по-стилистично рискови

✅ **OK използване (Unicode symbols):**
- Trust markers: ✓ "WiFi включен", ✕ "Не се пуши"
- Star ratings: ★★★★★ в testimonials
- Section markers: → "Виж повече"

✅ **OK с предпазливост (graphical emoji):**
- 1-2 в hero на marketing site — ако е в стил
- Никога в legal documents
- Никога в email subject lines (изглежда spam)

❌ **NEVER:**
- Face emoji в body text за emphasis
- Emoji повече от 1-2 в един параграф
- Emoji в form labels или error messages
- Emoji в CTA buttons ("Запази 🎉" — looks unprofessional)

**Принцип:** Emoji-те са като сол. 0 = безвкусно. 5 = развалено.

---

## 9. FORMS — UNIVERSAL RULES

### 9.1 Field design

✅ **DO:**
- Explicit `<label>` над всеки field (не само placeholder)
- Min height 48px (mobile-friendly)
- Visible focus state (border color change или outline)
- Inline validation **след blur** (не докато пишат)
- Required fields маркирани със `*`

❌ **DON'T:**
- Placeholder-only labels (изчезва when user пише)
- Floating labels (ad-hoc, unreliable accessibility)
- Auto-submit на change events
- Reset buttons (frustrating UX)

### 9.2 Booking forms (BNBForms widget specific)

Когато embed-ваш BNBForms widget:
- Container min-height: 600px (за да не jump-ва layout-ът докато widget зарежда)
- Background: surface color (обикновено white или light)
- Spacing: `--space-2xl` отгоре и отдолу
- Mobile: full-width, no horizontal padding ограничения

---

## 10. PAGE TEMPLATES & CONTENT STRUCTURE

> **Защо е тук:** Без structured rules за what content goes where, всяка build сесия ще импровизира. Това гарантира, че всеки клиентски сайт има consistent UX.

### 10.1 Multi-property website (Yavor pattern)

Темплейтът поддържа **множество страници**. Eleventy автоматично генерира URL-и от файловата структура.

**Структура на страниците:**

```
homepage (/)
├── Hero section
├── Featured Properties
├── About
├── Why Us
├── Testimonials
├── Contact CTA
└── Footer

complex-listing (/complex/[id]/)
├── Complex hero
├── Properties grid
├── Map / Location
└── Footer

single-property (/property/[id]/)
├── Photo gallery
├── Details (title, capacity, price)
├── Description
├── Amenities
├── Booking widget
├── Reviews
├── Similar properties
└── Footer

about (/about/)
contact (/contact/)
book (/book/)  ← BNBForms widget page
```

### 10.2 Homepage content structure

| Section | Content | Length |
|---------|---------|--------|
| **Hero** | Title (max 8 думи) + Subtitle (max 15 думи) + CTA butтon + Hero image | 1 screen height |
| **Featured Properties** | 3-6 property cards (image + title + capacity + price + CTA) | Grid: 1 col mobile, 2-3 cols desktop |
| **About** | 1-2 параграфа за бизнеса + 1 photo на собственика/локация | Max 100 думи |
| **Why Us** | 3-4 benefit points (icon + title + 1-sentence description) | 4 cards в grid |
| **Testimonials** | 3-5 quotes (text + name + property name) | Carousel или grid |
| **Contact CTA** | 1 line + button + phone/email | Simple band |
| **Footer** | Copyright, legal links, social, contact | Standard |

**Hero rules:**
- Винаги hero image (не gradient само)
- CTA button text: action-oriented ("Виж имотите", "Резервирай сега", не "Кликни тук")
- Subtitle обяснява value prop, не повтаря title
- Title и subtitle не са на същия език смесено

### 10.3 Complex listing page structure

| Section | Content | Length |
|---------|---------|--------|
| **Complex Hero** | Complex name + 1-line description + Hero image | 0.6 screen height |
| **Filter bar** (optional) | Sort by price/capacity/dates | Sticky on scroll |
| **Properties grid** | Cards (photo + name + capacity + amenities preview + price + CTA) | 1 col mobile, 3 cols desktop |
| **Location info** | Map embed + address + nearby attractions | Below grid |
| **Booking CTA** | "Не виждаш точното? Питай ни" + form | Bottom band |
| **Footer** | Standard | Standard |

### 10.4 Single property page structure

| Section | Content | Notes |
|---------|---------|-------|
| **Photo gallery** | 8-12 photos, lightbox-able, thumbnail strip | Hero photo first, gallery navigable |
| **Details bar** | Title, max guests, bedrooms, bathrooms, price/night | Sticky on scroll? |
| **Description** | 3-5 paragraphs, 200-400 думи total | Markdown-rendered |
| **Amenities** | Grid of icons + labels (8-15 items) | 2 cols mobile, 4 cols desktop |
| **Booking widget** | BNBForms embed | Full width, min 600px height |
| **Map & Location** | Embed + nearby info (lifts, restaurants, ski runs) | Smaller than complex listing |
| **Reviews** | 5-10 guest reviews if available | Optional if new property |
| **Similar properties** | 3 related properties | Below reviews |
| **Footer** | Standard | Standard |

### 10.5 About page structure

Прости 4 секции:
1. **Hero** — title + 1 line tagline
2. **Story** — 2-3 параграфа за бизнеса (как започна, мисия, опит)
3. **Team/Owner** — photo + bio (1 paragraph) на собственика
4. **Stats / Achievements** (optional) — "Над 5000 гости от 2009", "4.8 средна оценка"

### 10.6 Contact page structure

1. **Hero** — title + subtitle
2. **Contact methods** — phone, email, address (clickable)
3. **Map** — Google Maps или OpenStreetMap embed
4. **Contact form** — name, email, message (3 полета максимум)
5. **Office hours** — кога отговаряме

### 10.7 Boutique single-property pattern (бъдеща опция)

За клиенти с **един имот** (Belora-style guest house):

```
homepage (/)
├── Hero (с booking widget veno)
├── About the property
├── Photo gallery
├── Amenities
├── Location & nearby
├── Reviews
├── Booking widget (BNBForms)
└── Footer
```

Всичко на една страница — single-page application style. По-подходящо за boutique experience.

### 10.8 Content rules across all pages

✅ **DO:**
- Всяка страница има уникален `<title>` (за SEO)
- Всяка страница има meta description (155-160 chars)
- Open Graph tags за social sharing
- Breadcrumbs на dee pages (/complex/flora/property/studio-21)

❌ **DON'T:**
- Не дублирай съдържание между страници
- Не правиш страница без clear purpose ("Welcome page" е useless)
- Не embed-вай video/audio автоматично (lazy load only)

---

## 11. WHAT THIS DOCUMENT DOES NOT COVER

Този документ **не описва**:

- ❌ Цветова палитра на конкретния клиент → виж `clients/[id]/website/config.json`
- ❌ Лого, тон, tagline на агенцията → виж WelcomeBook brand assets (отделен документ)
- ❌ Architecture (Eleventy, Cloudinary, BNBForms) → виж `docs/architecture-v1.6.md`
- ❌ Site-specific content за всеки клиент → виж `clients/[id]/website/content.md`
- ❌ AI чатбот knowledge → виж `clients/[id]/portals/[name]/knowledge.md`

---

## 12. КОГА СЕ ОБНОВЯВА ТОЗИ ДОКУМЕНТ

**Не често.** Това са universal rules, които не зависят от конкретен клиент.

Тригери за update:
- Откриване на accessibility issue в реален build
- Нов industry standard (например WCAG 3.0)
- Performance regression която изисква нова optimization rule
- Нов type scale след 5+ клиента (ако забележиш pattern)

**Versioning:**
- `v1.0` — Първоначална версия (2026-04-30)
- `v1.x` — Minor patches (typo fixes, малки additions)
- `v2.0` — Major refresh (нова type scale, нова philosophy)

---

## 13. CHANGELOG

### v1.1 — 2026-04-30 (peer review patches)

**3 fixes от code review:**

1. **Bulgarian quotes corrected** (секция 8.1) — старият документ casваше "правилни Bulgarian кавички" `"..."`, което всъщност е английски стандарт. Поправено: `„..."` (low-high) за visible content, `"..."` за HTML атрибути. Пример добавен.

2. **Emoji vs Unicode symbols clarification** (секция 8.4) — beforehand размива дали ✓ ★ са OK или не. Сега ясно разграничено: Unicode symbols (✓ ★ ✕ →) са typography characters, OK за trust markers. Face emoji (😊 🎉) са graphical pictographs, ограничено използване.

3. **NEW Section 10: Page Templates & Content Structure** — преди това липсваше structured guidance за what content goes where. Сега documented:
   - Multi-property template (homepage + complex listing + single property + about + contact + book)
   - Content section breakdowns с дължини
   - Boutique single-property pattern (за бъдещи Belora-style клиенти)
   - SEO/Open Graph rules

**Архитектурно следствие:** Section 10 ще се реферира при всеки бъдещ build — Claude Code не трябва да импровизира page structure повече.

### v1.0 — 2026-04-30
Initial design system, fokused exclusively на universal rules за клиентски сайтове. Извлечени са правилата от WelcomeBook Brand Spec, които НЕ са brand-specific (typography, layout, photography, copy conventions, accessibility).

**Key decisions documented:**
- System fonts only (no Google Fonts, GDPR + performance)
- rem-based scales (typography + spacing)
- Mobile-first principle
- Cloudinary for ALL images (no Git)
- WCAG AA accessibility minimum
- Bulgarian punctuation conventions
- Limited emoji policy

---

> **Maintained by:** Костадин Павлов  
> **Single source of truth:** Този файл в `D:\ClaudeCodeFirst\docs\client-design-system.md` + Project Knowledge на claude.ai  
> **Last updated:** 2026-04-30
