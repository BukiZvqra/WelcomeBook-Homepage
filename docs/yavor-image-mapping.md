# Yavor — Image Mapping: Cloudinary → Нов сайт

> Версия 1.0 · Май 2026 · Фаза 2 анализ  
> Базиран на: `scraped-images/yavor/_manifest.json` (619 снимки) + `_config-snippet.json`

---

## Инвентар (какво имаме в Cloudinary)

| Cloudinary папка | Съдържа | Брой снимки | Забележка |
|---|---|---|---|
| `clients/yavor/` (root) | Снимки от homepage на стария сайт | ~15 | Микс от service thumbnails + property thumbnails |
| `clients/yavor/borovets/` | Дестинационни снимки на Боровец | ~17 | От `/bg/borovets_c1` |
| `clients/yavor/apartamenti-v-komplex-flora/` | Flora — category ниво + 12 per-property папки | ~220 | 12 папки × ~18 снимки + 12 category thumbs |
| `clients/yavor/apartamenti-v-kompleksi-rila-park-i-semiramida/` | Rila Park — 2 per-property папки | ~46 | само 2 от 3 имота имат папки |
| `clients/yavor/apartamenti-v-kompleksi-roial-plaza-i-iglika/` | Royal Plaza — само category ниво | ~18 | Няма per-property sub-folder |
| `clients/yavor/apartamenten-kompleks-borovets-gardns/` | Borovets Gardens — 2 per-property папки | ~38 | Пълно покритие |
| `clients/yavor/vili-i-apartamenti-v-raiona/` | Вили в района (извън 4-те комплекса) | ~26 | ⚠️ Не съществува в новия сайт |
| `clients/yavor/uslugi/` | Услуги — category + 3 per-service папки | ~60 | Само hiking, team-building, safari имат папки |
| **ОБЩО** | | **~619** | |

### Важна бележка: Cloudinary пътищата са с ДЪЛГИ имена

Папките са кръстени по URL-ите на стария сайт, **не** по краткия `flora/`, `rila-park/` формат от workflows документацията. Реалните `public_id`-та изглеждат така:
```
clients/yavor/apartamenti-v-komplex-flora/studio-21-tiulip-rezidns/студио-21-тюлип-резидънс
```
Не `clients/yavor/flora/studio-21/...`.

---

## Секция 1: WEBSITE — страница по страница

### 1.1 Homepage `/` и `/en/`

| Секция в новия сайт | Файл | Кои снимки от Cloudinary | Брой | Статус |
|---|---|---|---|---|
| Hero background image | `src/index.njk` + `src/en/index.njk` | Нито едно от горните не е изрична "hero" снимка. Най-добър кандидат: `borovets/e50ab250...jpeg` (194KB — най-голямата в папката) | 1 | ⚠️ Partial — нужно е одобрение от Явор |
| Complexes grid (4 карти) — понастоящем CSS gradients | `index.njk` → complex cards | По 1 thumbnail от всеки комплекс: `apartamenti-v-komplex-flora/_main[0]`, `apartamenti-v-kompleksi-rila-park-i-semiramida/_main[0]`, `apartamenti-v-kompleksi-roial-plaza-i-iglika/_main[0]`, `apartamenten-kompleks-borovets-gardns/_main[0]` | 4 | ✅ Mapped 1:1 |
| Services preview (6 карти) | `index.njk` → service cards | `усluги/тиймбилдинг.png`, `uslugi/пешеходни-турове.jpeg`, `uslugi/джип-сафари-боровец.jpeg`, `апартаменти-под-наем.jpeg`, `ски-услуги.jpeg`, `трансфери-и-самолетни-билети.jpeg` (root) | 6 | ⚠️ Partial — 3 услуги (property-manager, transfers, ski) нямат dedicated service detail images |

---

### 1.2 Apartments listing `/apartments/` и `/en/apartments/`

| Секция | Файл | Снимки | Брой | Статус |
|---|---|---|---|---|
| Property cards (thumbnail per property) | `property-card.njk` + `apartments.njk` | По 1 от `_main` листа на всеки комплекс: Flora 12, Rila Park 2, Royal Plaza 1, Borovets Gardens 2 | 17 | ⚠️ Partial — 1 имот без thumbnail (виж §1.4) |
| Filter bar | `apartments.njk` | Без снимки | — | — |

---

### 1.3 Flora Complex `/complex/flora/` + property pages

| Страница | Cloudinary subfolder | Real name (стар сайт) | New site slug (очакван) | Снимки | Статус |
|---|---|---|---|---|---|
| Complex hero | `apartamenti-v-komplex-flora/_main[0]` | — | — | 1 | ✅ |
| `/property/studio-flora-XX/` | `studio-21-tiulip-rezidns/` | Студио 21 Тюлип Резидънс | studio-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/studio-flora-XX/` | `studio-13-tiulip-rezidns/` | Студио 13 Тюлип Резидънс | studio-flora-?? | 16 | ⚠️ Mapping нужен |
| `/property/studio-flora-XX/` | `studio-519-khotel-flora/` | Студио 519 Хотел Флора | studio-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/studio-flora-XX/` | `studio-19-klover-rezidns/` | Студио 19 Кловер Резидънс | studio-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/studio-flora-XX/` | `studio-14-klover-rezidns/` | Студио 14 Кловер Резидънс | studio-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/onebr-flora-XX/` | `apartament-02-klover-rezidns/` | Апартамент 02 Кловер Резидънс | onebr-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/onebr-flora-XX/` | `apartament-10-mailili-rezidns/` | Апартамент 10 Майлили Резидънс | onebr-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/onebr-flora-XX/` | `apartament-05-klover-rezidns/` | Апартамент 05 Кловер Резидънс | onebr-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/twobr-flora-XX/` | `apartament-601-khotel-flora/` | Апартамент 601 Хотел Флора | twobr-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/twobr-flora-XX/` | `apartament-208-khotel-flora/` | Апартамент 208 Хотел Флора | twobr-flora-?? | 26 | ⚠️ Mapping нужен |
| `/property/double-flora-XX/` | `apartament-28-violet-rezidns/` | Апартамент 28 Виолет Резидънс | double-flora-?? | 18 | ⚠️ Mapping нужен |
| `/property/double-flora-XX/` | `apartament-13-klover-rezidns/` | Апартамент 13 Кловер Резидънс | double-flora-?? | 18 | ⚠️ Mapping нужен |

> **Критична забележка:** Стар сайт → нов сайт mapping-ът е блокиран. Старите имена са реални (Студио 21 Тюлип Резидънс), новите са placeholder (Студио Flora 01). **Явор трябва да потвърди кое реално апартаментно наименование отива към кой нов slug.** Алтернативно: вместо generic "Flora 01/02" — запазваме реалните имена в `properties.json`.
>
> Типовете съвпадат по брой: 5 studios, 3 one-bedrooms, 2 two-bedrooms в стария сайт = 5+3+2 в новия. Но кое е кое изисква потвърждение.

---

### 1.4 Rila Park `/complex/rila-park/` + property pages

| Страница | Cloudinary subfolder | Real name | New site slug | Снимки | Статус |
|---|---|---|---|---|---|
| Complex hero | `apartamenti-v-kompleksi-rila-park-i-semiramida/_main[0]` | — | — | 1 | ✅ |
| `/property/studio-rila-park-01/` | `studio-503-rila-park/` | Студио 503 Рила Парк | studio-rila-park-01 | 26 | ✅ Mapped 1:1 |
| `/property/twobr-rila-park-01/` | `apartament-44-rila-park/` | Апартамент 44 Рила Парк | twobr-rila-park-01 | 18 | ✅ Mapped 1:1 |
| `/property/onebr-rila-park-01/` | — | *(не открито в стария сайт)* | onebr-rila-park-01 | 0 | ❌ Missing — нови снимки нужни |

> **Rila Park 1-bedroom няма снимки.** Старият сайт, изглежда, не е имал детайлна страница за 1-спален Rila Park (или скрипт-ът не го е намерил). Явор трябва да провери и да качи снимки.

---

### 1.5 Royal Plaza `/complex/royal-plaza/` + property page

| Страница | Cloudinary subfolder | Real name | New site slug | Снимки | Статус |
|---|---|---|---|---|---|
| Complex hero + `/property/studio-royal-plaza-01/` | `apartamenti-v-kompleksi-roial-plaza-i-iglika/_main` (целия масив) | Студио 402 Роял Плаза + ~17 снимки | studio-royal-plaza-01 | 18 | ⚠️ Partial — всичко на category ниво, няма отделна per-property папка |

> Royal Plaza в стария сайт нямаше отделна детайлна страница по property. Всичките ~18 снимки са от listing страницата и покриват едно студио.

---

### 1.6 Borovets Gardens `/complex/borovets-gardens/` + property pages

| Страница | Cloudinary subfolder | Real name | New site slug | Снимки | Статус |
|---|---|---|---|---|---|
| Complex hero | `apartamenten-kompleks-borovets-gardns/_main[0]` | — | — | 1 | ✅ |
| `/property/studio-borovets-gardens-01/` | `studio-b35-borovets-gardns/` | Студио Б35 Боровец Гардънс | studio-borovets-gardens-01 | 18 | ✅ Mapped 1:1 |
| `/property/studio-borovets-gardens-02/` | `studio-b36-borovets-gardns/` | Студио Б36 Боровец Гардънс | studio-borovets-gardens-02 | 18 | ✅ Mapped 1:1 |

---

### 1.7 Services pages

| Страница | Cloudinary subfolder | Снимки | Брой | Статус |
|---|---|---|---|---|
| `/services/` landing (grid thumbnails) | `uslugi/тиймбилдинг.png`, `uslugi/пешеходни-турове.jpeg`, `uslugi/джип-сафари-боровец.jpeg` + root thumbnails | 6 max | ⚠️ Partial — само 3/6 услуги имат dedicated thumbnail |
| `/services/hiking/` | `uslugi/peshekhodni-turove/` | 26 | ✅ Mapped 1:1 |
| `/services/team-building/` | `uslugi/tiimbilding/` | 4 | ✅ Mapped 1:1 |
| `/services/safari/` | `uslugi/dzhip-safari-borovets/` | ~10 | ✅ Mapped 1:1 |
| `/services/property-manager/` | `клиенти/yavor/професионален-домоуправител.jpeg` (root, 1 thumbnail) | 1 | ❌ Missing — само 1 thumbnail, нужни са поне 3-4 снимки |
| `/services/transfers/` | `clients/yavor/трансфери-и-самолетни-билети.jpeg` (root, 1 thumbnail) | 1 | ❌ Missing — само 1 thumbnail |
| `/services/ski/` | `clients/yavor/ски-услуги.jpeg` (root, 1 thumbnail) | 1 | ❌ Missing — само 1 thumbnail |

---

### 1.8 About Borovets `/about-borovets/`

| Секция | Cloudinary subfolder | Снимки | Брой | Статус |
|---|---|---|---|---|
| Hero + Winter section + Summer section + Gallery | `borovets/` (17 снимки) | всичките | 17 | ✅ Mapped 1:1 |

> Папката е пълна с destination снимки от стария сайт. Достатъчно за Hero + 2 seasonal sections + general gallery.

---

### 1.9 Contact `/contact/`

Без снимки — само Netlify форма. **Статус: N/A**

---

## Секция 2: PORTALS — per-portal mapping

| Портал | Cloudinary source | Брой | Статус |
|---|---|---|---|
| `portals/flora-residence/` | `apartamenti-v-komplex-flora/` (всички per-property папки) | ~220 | ✅ — но нужно Явор–slug mapping (виж §1.3) |
| `portals/rila-park/` | `apartamenti-v-kompleksi-rila-park-i-semiramida/` | ~46 | ⚠️ Partial — onebr-rila-park няма снимки |
| `portals/royal-plaza/` | `apartamenti-v-kompleksi-roial-plaza-i-iglika/` | 18 | ⚠️ Partial — всичко на category ниво |
| `portals/borovets-gardens/` | `apartamenten-kompleks-borovets-gardns/` | ~38 | ✅ Mapped 1:1 |

---

## Секция 3: UNUSED в Cloudinary

| Cloudinary папка | Брой | Защо е unused |
|---|---|---|
| `vili-i-apartamenti-v-raiona/` | ~26 | 🗑️ Unused — "Вили и апартаменти в района" НЕ съществува в новия сайт. Вилата в с. Широки дол и другите имоти извън 4-те комплекса не са включени. Оставят се като резерв за Phase 2 ако Явор реши да ги добави. |
| Root `уеб-камери.jpeg` | 1 | 🗑️ Unused — "Уеб камери" е услуга на стария сайт, не е включена в 6-те услуги на новия. |
| Root `планински-турове.jpeg` | 1 | 🗑️ Unused — дублирана от `uslugi/пешеходни-турове.jpeg` (различна снимка, по-малка). |
| Root property thumbnails: `апартамент-404-хотел-флора`, `студио-18-тюлип-резидънс`, `студио-02-виолет-резидънс`, `студио-05-тюлип-резидънс`, `апартамент-11-майлили-резидънс`, `апартамент-03-тюлип-резидънс`, `двойна-стая-18-майлили-резидънс`, `студио-409-хотел-флора`, `студио-703-хотел-флора` | 9 | 🗑️ Unused (с уговорка) — homepage thumbnails от стария сайт. Повечето имоти ИМАТ per-property папка с пълна галерия. Тези са малки cover thumbs, които може да ползваме само ако нямаме по-добра алтернатива. |
| `borovets/ogimage.jpeg` | 1 | 🗑️ Unused — стар og:image на стария сайт, ниска резолюция (8KB). |

---

## Резюме: Какво действие е нужно

### ✅ Готово за директно ползване (след Фаза 3 — имплементация)
- Borovets Gardens: 2 от 2 имота — пълни галерии
- About Borovets page: 17 снимки готови
- Hiking service: 26 снимки готови
- Team-building service: 4 снимки готови
- Safari service: ~10 снимки готови

### ⚠️ Нужно потвърждение от Явор
1. **Flora mapping** — 12 реални стари имена → 12 нови placeholder slug-а. Явор да потвърди кое е кое, **или** да одобрим преименуване на `properties.json` entries по реалните имена (Студио Тюлип 21, Апартамент Кловер 02 и т.н.).
2. **Hero image** — коя снимка от `borovets/` да е homepage hero.
3. **Royal Plaza detail images** — само category снимки, нужно е потвърждение дали са достатъчни.

### ❌ Нужни нови снимки от Явор
1. `onebr-rila-park-01` — 1-спален Rila Park. Старият сайт не е имал такава страница (или не е scraped-ната). Нужни са поне 5-8 снимки.
2. `property-manager` service — само 1 thumbnail (9KB). Нужни 3-4 качествени снимки.
3. `transfers` service — само 1 thumbnail. Нужни 2-3 снимки.
4. `ski` service — само 1 thumbnail. Нужни 2-3 снимки.

---

## Следващи стъпки след одобрение

**Фаза 3 ще:**
1. Добави `images` поле към всеки entry в `properties.json` с реалните Cloudinary пътища
2. Актуализира `config.json` за сайта с heroImage per complex
3. Обнови `.njk` templates да рендерират реални снимки вместо CSS gradients
4. Маркира портал knowledge files с правилните image paths

---

*Drafted: 2026-05-02 · Status: ЧАКА ОДОБРЕНИЕ ОТ KOSTA*
