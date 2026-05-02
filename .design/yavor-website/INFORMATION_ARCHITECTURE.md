# Information Architecture: TES Borovets Website

## Site Map

### BG (root — default language)

```
/ (Homepage)
├── /apartments/                       ← Всички 21 имота, filterable grid
│   ├── /complex/flora/                ← Flora Complex (15 имота)
│   │   └── /property/[slug]/          ← Отделна страница за всеки имот
│   ├── /complex/royal-plaza/          ← Royal Plaza & Iglika (1 имот)
│   │   └── /property/[slug]/
│   ├── /complex/rila-park/            ← Rila Park & Semiramida (3 имота)
│   │   └── /property/[slug]/
│   └── /complex/borovets-gardens/     ← Borovets Gardens (2 имота)
│       └── /property/[slug]/
├── /services/                         ← 6 услуги в clean grid
│   ├── /services/property-manager/
│   ├── /services/transfers/
│   ├── /services/ski/
│   ├── /services/team-building/
│   ├── /services/safari/
│   └── /services/hiking/
├── /about-borovets/                   ← Курортен контекст, зима + лято
├── /selling-emotions/                 ← Placeholder (не се build-ва в Phase 1)
└── /contact/                          ← Netlify Form + Viber + WhatsApp
```

### EN (mirror под /en/ prefix)

```
/en/ (EN Homepage)
├── /en/apartments/
│   ├── /en/complex/flora/
│   │   └── /en/property/[slug]/
│   ├── /en/complex/royal-plaza/
│   │   └── /en/property/[slug]/
│   ├── /en/complex/rila-park/
│   │   └── /en/property/[slug]/
│   └── /en/complex/borovets-gardens/
│       └── /en/property/[slug]/
├── /en/services/
│   ├── /en/services/property-manager/
│   ├── /en/services/transfers/
│   ├── /en/services/ski/
│   ├── /en/services/team-building/
│   ├── /en/services/safari/
│   └── /en/services/hiking/
├── /en/about-borovets/
└── /en/contact/
```

### Външни links (footer only, не са страници)

```
European Projects  → https://tes-borovets.com/european-projects  (стар сайт, external)
TripAdvisor        → client.tripadvisor_url
Facebook           → client.facebook_url
```

### Phase 2 (RU — структура е идентична)

```
/ru/ → пълен mirror на BG структурата
```

---

## Navigation Model

### Primary navigation (header, всички страници)

| # | BG label | EN label | Destination |
|---|---|---|---|
| 1 | Апартаменти | Apartments | `/apartments/` |
| 2 | Услуги | Services | `/services/` |
| 3 | За Боровец | About Borovets | `/about-borovets/` |
| 4 | Контакти | Contact | `/contact/` |
| — | BG \| EN | BG \| EN | lang switcher (utility) |

**Max items**: 4 + lang switcher. Dropdown-и не се използват.

### Secondary navigation (footer, групирана)

| Колона | Съдържание |
|---|---|
| **TES Borovets** | Лого + слоган + „от 2009" |
| **Комплекси** | Flora · Royal Plaza · Rila Park · Borovets Gardens |
| **Услуги** | Property Manager · Трансфери · Ски · Тимбилдинг · Сафари · Пешеходни турове |
| **Информация** | За Боровец · Контакти · Европроекти (external) · TripAdvisor · Facebook |

### Utility navigation

- **Lang switcher**: `BG | EN` — top-right в header, active language е подчертан. На mobile — вътре в hamburger menu-то.
- **Contact shortcuts**: Viber бутон + WhatsApp бутон в header (само десктоп и таблет). На mobile — вътре в hamburger menu-то.

### Mobile navigation

- **Hamburger бутон** вдясно в header (min 44×44px)
- **CSS-only reveal** чрез `:focus-within` на `.site-header` (вече имплементирано)
- **Съдържание на мобилното меню**:
  1. Апартаменти
  2. Услуги
  3. За Боровец
  4. Контакти
  5. — separator —
  6. Viber: +359 888 909 237
  7. WhatsApp: +359 888 909 237
  8. — separator —
  9. BG | EN

---

## Content Hierarchy

### Homepage `/`

1. **Hero** — Seasonal alpine image + tagline „Боровец през всички сезони" + 2 CTA. *Первият и единственен елемент above the fold. Продава дестинацията.*
2. **Complexes grid** — 4 карти с bg-image, брой имоти, link към complex. *Отговаря на „какво точно предлагаш" веднага след hero.*
3. **Services preview** — 6 карти в grid, без описание. *Показва широчината на бизнеса без да отклонява от апартаментите.*
4. **About** — 3–4 изречения за Явор + „от 2009" + 17 години опит. *Trust signal преди контакт.*
5. **Borovets teaser** — Dark section, seasonal hooks (зима/лято), link към `/about-borovets/`. *Destination selling, не apartment selling.*
6. **Contact mini-section** — Форма + телефон + Viber. *Последен CTA преди footer.*

### Apartments listing `/apartments/`

1. **Page header** — H1 + брой имоти (21) + filter bar. *Веднага поставя потребителя в context на избора.*
2. **Filter bar** — по комплекс + по тип (двойна/студио/1-спален/2-спален). *Phase 1: static pills/tabs. Phase 2: JS filtering.*
3. **Properties grid** — sorted по Явор: двойна → студио → 1-спален → 2-спален. *Default sort отразява бизнес приоритет.*
4. **Complex section headers** — визуален разделител между комплекси ако filter = „All". *Помага на потребителя да асоциира имот с комплекс.*
5. **CTA banner** — „Не намирате подходящ имот? Свържете се с нас" → `/contact/`. *Catch-all за потребителите без match.*

### Complex page `/complex/[id]/`

1. **Hero** — Complex image с overlay + name + subtitle + брой имоти.
2. **About section** — 2–3 изречения за локацията + ключова info (разстояние от гондола, etc.).
3. **Properties grid** — всички имоти в комплекса, sorted по тип.
4. **Location/map** — embed или статична snimka (Phase 1: static image).
5. **Contact CTA** — „Резервирайте директно" → phone + Viber + form link.

### Property page `/property/[slug]/`

1. **Gallery** — Hero image + thumbnail strip (Phase 1: 1 hero + 3–4 thumbnails или само hero).
2. **Property details** — Тип · Комплекс · Капацитет · Площ (ако е налично).
3. **Description** — Paragraph с highlights на имота.
4. **Amenities list** — Icons + labels (Wi-Fi, кухня, паркинг, etc.).
5. **Contact CTA** — sticky на мобилен (Phase 2), static на desktop. Phone + Viber + WhatsApp.
6. **Similar properties** — 2–3 карти от същия комплекс.
7. **Breadcrumb** — Home → Апартаменти → [Complex name] → [Property name].

### Services landing `/services/`

1. **Page hero** — H1 + subtitle „Пълен комфорт от пристигане до заминаване".
2. **6 service cards** — Icon + name + 1-line description + link към individual page. Grid 2-col mobile / 3-col desktop.
3. **CTA** — „Имате въпрос?" → `/contact/`.

### Single service `/services/[id]/`

1. **Service hero** — Image или icon + H1 + subtitle.
2. **Description** — 2–3 параграфа: какво включва, за кого е, как работи.
3. **Process steps** — 3–4 стъпки (optional, само за property-manager).
4. **Pricing note** — „Свържете се за персонализирана оферта" (без цени в Phase 1).
5. **CTA** — `mailto:` или `/contact/` с pre-filled subject.
6. **Related services** — 2–3 карти.

### About Borovets `/about-borovets/`

1. **Hero** — Panorama снимка + „Защо Боровец?".
2. **Winter section** — Ски писти, Гондола, сезон (Декември–Март).
3. **Summer section** — MTB, hiking, природа (Юни–Септември).
4. **Getting there** — От София (75 км, ~1ч15), трансфер опция → `/services/transfers/`.
5. **Restaurants & amenities** — Кратък списък, без да е guide.
6. **Services cross-link** — „TES Borovets организира всичко" → `/services/`.

### Contact `/contact/`

1. **Page header** — H1 „Свържете се с нас".
2. **Netlify Form** — Вашето им / Email / Телефон (optional) / Съобщение / Honeypot. Submit → inline success message.
3. **Alternative contact methods** — Viber (BG: +359 888 909 237) · WhatsApp · Email · Phone EN · Phone RU — всеки с click-to-call/chat.
4. **Map** — статична embed или screenshot от Google Maps за Флора Комплекс.
5. **Response time note** — „Отговаряме в рамките на 24ч" (задава очаквания).

---

## User Flows

### Flow A: Турист търси апартамент за зимата

```
1. Google "apartments Borovets ski" / „апартаменти Боровец зима"
   → lands on Homepage или /complex/flora/ (SEO entry)

2. Homepage → Hero section
   CTA "Виж апартаментите" → /apartments/

3. /apartments/ → Filter по тип: "Студио" ИЛИ scroll по grid
   → click на property card
   → /property/studio-flora-03/

4. /property/studio-flora-03/ → Gallery + Details + Amenities
   ↳ satisfied → Contact CTA: Viber / WhatsApp / phone
   ↳ not sure → "Similar properties" → друг имот
   ↳ wants different complex → breadcrumb → /apartments/

5. Contact: Viber click → директна комуникация с Явор
   ИЛИ: fills Netlify Form → email до Явор
```

**Drop-off risk**: /apartments/ → property. Ако grid е объркан или sort е лош, потребителят се губи.
**Mitigation**: Clear complex section headers + Явор's explicit sort order.

---

### Flow B: Property owner търси property management

```
1. Google "property manager Borovets" / „управление на апартамент Боровец"
   → lands on /services/property-manager/ (SEO entry)
   ИЛИ: Homepage → Services section → click "Property Manager"

2. /services/property-manager/ → Description + Process steps
   → builds trust: "от 2009", "21 имота под управление"

3. CTA → /contact/ с pre-filled subject "Property management inquiry"
   ИЛИ: директен Viber/WhatsApp от страницата

4. Контакт с Явор → оферта
```

**Key insight**: Тези потребители не идват от Homepage. Direct SEO landing на service page е primary entry.

---

### Flow C: Existing guest изследва Боровец

```
1. Email от Явор / директна препратка
   → lands on /about-borovets/

2. /about-borovets/ → Winter / Summer sections
   → discovery: "MTB trails? — не знаех"
   → discovery: "трансфер от София"

3. Click "Трансфери" cross-link → /services/transfers/
   ИЛИ: click "Ски услуги" → /services/ski/

4. /services/ski/ → CTA → contact за booking на ски услуга

5. Optional: Homepage → Complexes → разглежда останалите комплекси
   → upgrade от студио към 1-спален за следващия престой
```

---

## Naming Conventions

| Концепция | BG label | EN label | Бележка |
|---|---|---|---|
| Имот / Апартамент | **Апартамент** | **Apartment** | Не „unit" или „room". |
| Резервация | **Резервация** | **Booking** | Не „запазване". |
| Свържете се | **Свържете се** | **Get in touch** | Не „Contact us" (по-топло). |
| Домакин | **Домакин** | **Host** | Явор = домакин, не „manager". |
| Сезон | **Ски сезон / Летен сезон** | **Ski season / Summer season** | Не „зима/лято" в headings. |
| Комплекс | **Комплекс** | **Complex** | Flora Complex, не „Flora Resort". |
| Тип имот | **Двойна стая / Студио / 1-спален / 2-спален** | **Double room / Studio / 1-bedroom / 2-bedroom** | Явор's explicit sort order. |
| Трансфер | **Трансфер** | **Transfer** | Не „транспорт" или „shuttle". |

---

## Component Reuse Map

| Component | Присъства на | Вариации |
|---|---|---|
| `base.njk` layout | Всички страници | — |
| `header.njk` | Всички страници | — |
| `footer.njk` | Всички страници | — |
| `.hero` section | Homepage, Complex, Service, About, Contact | Различни images и overlay opacity |
| `.complex-card` | Homepage complexes grid, /apartments/ | Homepage: 4 карти; /apartments/: с повече detail |
| Property card (extend from `property-card.njk`) | /apartments/, /complex/[id]/, /property/[id]/ similar | — |
| `.service-card` | Homepage preview (compact), /services/ (full) | Homepage: без description; /services/: с 1-line description |
| `.contact-card` | Homepage contact mini, /contact/ | /contact/: full form + cards |
| Breadcrumb | /complex/[id]/, /property/[id]/, /services/[id]/ | Не на homepage |
| Lang switcher | Всички страници | Desktop: header top-right; Mobile: вътре в nav |

---

## Content Growth Plan

| Секция | Расте ли? | Accommodated how |
|---|---|---|
| Имоти (properties) | Да — Явор може да добавя нови | Eleventy pagination от `properties.json` data file. Add property = add JSON entry. |
| Комплекси | Не скоро (4 са фиксирани) | Static .njk pages per complex. Phase 2 portal expansion. |
| Услуги | Ниско (6 са core) | Static .njk pages per service. Нов = нов файл. |
| Езици | RU в Phase 2 | `/ru/` directory mirror — zero architectural промени. |
| Photos | Да — Явор добавя снимки | Cloudinary folder structure `clients/yavor/[complex]/[property]/`. No Git changes. |
| Blog / News | Не в Phase 1 | — |

**Properties data model** (планирано за `clients/yavor/website/properties.json`):

```json
{
  "slug": "studio-flora-01",
  "complex": "flora",
  "type": "studio",
  "capacity": 2,
  "size_sqm": 28,
  "amenities": ["wifi", "kitchen", "balcony"],
  "images": ["studio-flora-01-main.jpg", "studio-flora-01-kitchen.jpg"],
  "description_bg": "...",
  "description_en": "..."
}
```

Eleventy generates `/property/[slug]/` via pagination over this file.

---

## URL Strategy

### Rules

- **BG root**: `/` — никога `/bg/`. Български е default.
- **EN prefix**: `/en/` — всички EN страници са mirror под `/en/`.
- **RU Phase 2**: `/ru/` — идентична структура.
- **Slug формат**: lowercase, hyphenated, само ASCII. `studio-flora-01`, не `студио-флора-01`.
- **Consistency**: slug-ът е еднакъв между езиците. `/apartments/` = `/en/apartments/`.

### Patterns

| Тип страница | BG URL | EN URL |
|---|---|---|
| Homepage | `/` | `/en/` |
| Apartments listing | `/apartments/` | `/en/apartments/` |
| Complex | `/complex/flora/` | `/en/complex/flora/` |
| Property | `/property/studio-flora-01/` | `/en/property/studio-flora-01/` |
| Services landing | `/services/` | `/en/services/` |
| Single service | `/services/ski/` | `/en/services/ski/` |
| About | `/about-borovets/` | `/en/about-borovets/` |
| Contact | `/contact/` | `/en/contact/` |

### Dynamic segments

- `/property/[slug]/` — slug идва от `properties.json` · Eleventy pagination
- `/complex/[id]/` — static files (4 комплекса, не се очаква growth)
- `/services/[id]/` — static files (6 услуги)

### Query parameters

Phase 1: Без JS query params. Filtering на `/apartments/` е static (CSS показва/скрива по data attribute) ИЛИ separate pages per filter.

Phase 2: `?type=studio&complex=flora` за BNBForms integration.

### Breadcrumb schema

```
Homepage:            (нняма breadcrumb)
/apartments/:         Home > Апартаменти
/complex/flora/:      Home > Апартаменти > Flora Complex
/property/[slug]/:    Home > Апартаменти > Flora Complex > [Property Name]
/services/:           Home > Услуги
/services/ski/:       Home > Услуги > Ски услуги
/about-borovets/:     Home > За Боровец
/contact/:            Home > Контакти
```

---

## Eleventy i18n Architecture

### Препоръчан подход: Directory-based (без external plugin)

```
src/
├── _data/
│   └── i18n/
│       ├── bg.json          ← BG strings: nav, buttons, labels
│       └── en.json          ← EN strings: same keys, EN values
├── _includes/ + _layouts/   ← shared, language-aware чрез {{ lang }}
├── index.njk                ← lang: bg (frontmatter)
├── apartments.njk
├── complex/ ...
├── property/ ...            ← Eleventy pagination, generates /property/[slug]/
├── services/ ...
├── about-borovets.njk
├── contact.njk
└── en/
    ├── en.json              ← { "lang": "en" } → sets lang data for whole dir
    ├── index.njk
    ├── apartments.njk
    ├── complex/ ...
    ├── property/ ...
    ├── services/ ...
    ├── about-borovets.njk
    └── contact.njk
```

**Lang switcher logic** в template:

```njk
{% if lang === "en" %}
  <a href="{{ page.url | replace('/en/', '/') }}">BG</a>
  <span class="active">EN</span>
{% else %}
  <span class="active">BG</span>
  <a href="/en{{ page.url }}">EN</a>
{% endif %}
```

**Translation usage** в template:

```njk
{# Зарежда BG или EN strings в зависимост от lang frontmatter #}
{% set t = i18n[lang] %}
<a href="/apartments/">{{ t.nav_apartments }}</a>
```

**Phase 2 RU**: Добавяш `src/ru/` директория + `i18n/ru.json`. Zero промени в base layout или config.

---

*Drafted:* 2026-05-01  
*Client:* Yavor Кичев / Tour Express Service Ltd.  
*Follows:* DESIGN_BRIEF.md  
*Next:* DESIGN_TOKENS (Phase 4)
