# WelcomeBook Agency — Архитектура v1.4

> Един монолитен Git репо · Един shared chatbot backend · N клиента · Custom домейн per клиент

---

## 1. ПЪЛНА FOLDER СТРУКТУРА

```
welcomebook-agency/                          ← Един Git репо за цялата агенция
│
├── .github/workflows/                       ← CI/CD автоматизация (после)
├── .env.example                             ← Шаблон, без реални ключове
├── .gitignore                               ← node_modules, .env, *.log, logs/
├── README.md
├── CLAUDE.md                                ← Глобални инструкции за Claude Code
├── package.json                             ← Eleventy + dependencies
├── eleventy.config.js                       ← Build конфигурация
│
├── marketing-site/                          ← welcomebook.agency (постоянен asset на агенцията)
│   ├── homepage/                            ← главна funnel
│   ├── funnelpricing/                       ← /funnelpricing страница
│   ├── netlify.toml
│   └── README.md
│
├── shared-apps/                             ← STATEFUL приложения, multi-tenant
│   └── financial-tracker/                   ← welcomebook-tracker.netlify.app
│       ├── frontend/                        ← Един deploy за всички клиенти
│       ├── supabase/                        ← БД + access control
│       ├── netlify.toml
│       └── README.md
│
├── shared-resources/                        ← MASTER COPIES на готови материали
│   ├── message-templates/                   ← 30 templates BG+EN, master copy
│   ├── signs-pack/                          ← printable PDFs (WiFi, правила, check-out)
│   ├── checklists/                          ← cleaning, maintenance
│   └── feedback-form/                       ← guest feedback templates
│
├── templates/                               ← MASTER ШАБЛОНИ (не се променят per клиент)
│   ├── website-boutique/                    ← Шаблон A: бутиков, 1 имот
│   │   ├── src/                             ← Eleventy templates (.njk)
│   │   ├── assets/                          ← CSS, JS
│   │   └── README.md                        ← Какви placeholder-и приема
│   ├── website-family/                      ← Шаблон B: семеен, 1-3 имота
│   ├── website-multiproperty/               ← Шаблон C: property manager, 4+ имота
│   └── portal-master/                       ← Един шаблон за всички портали
│       ├── src/
│       ├── assets/
│       │   └── chatbot-widget.js            ← Чатбот UI (изпраща към backend)
│       └── README.md
│
├── backend/                                 ← STATELESS SHARED SERVICE
│   └── netlify/functions/
│       ├── chatbot.js                       ← Един endpoint за всички чатботи
│       ├── lib/
│       │   ├── load-knowledge.js            ← Чете knowledge.md per client
│       │   ├── claude-client.js             ← Wrapper около Claude API
│       │   ├── system-prompt.js             ← Генерира system prompt
│       │   └── fallback.js                  ← Error handling, fallback messages
│       └── package.json
│
├── tools/                                   ← AUTOMATION SCRIPTS (за теб)
│   ├── new-client.sh                        ← Генерира папка за нов клиент
│   ├── deploy-client.sh                     ← Build & deploy на конкретен клиент
│   ├── update-knowledge.sh                  ← Бърз update на knowledge без deploy
│   ├── backup-supabase.sh                   ← Weekly export на Supabase данни
│   └── README.md
│
└── workflows/                               ← CLAUDE CODE WORKFLOWS
    ├── new-client-setup.md                  ← Промпт: setup нов клиент
    ├── update-knowledge.md                  ← Промпт: update knowledge
    ├── seo-optimization.md                  ← Промпт: SEO на Booking/Airbnb
    └── generate-offer.md                    ← Промпт: генериране на оферта
```

> **Note:** `logs/` папката не е в репото. Тя се създава локално когато сваляш логове от Netlify за анализ (виж секция 16). В `.gitignore` е добавена за да не се commit-не случайно.

> **Note:** `clients/` структурата е в секция 2 (отделно за яснота).

---

## 2. КЛИЕНТСКА СТРУКТУРА · clients/

```
clients/
│
├── _template/                           ← Темплейт за нов клиент (не deploy)
│   ├── client-info.md                   ← Базова инфо за клиента
│   ├── customizations/                  ← Override-и над shared-resources/
│   │   ├── messages/                    ← .gitkeep вътре, override-ва само променени
│   │   ├── signs/                       ← .gitkeep вътре, override-нати signs (рядко)
│   │   └── checklists/                  ← .gitkeep вътре, override-нати checklists (рядко)
│   ├── website/
│   │   ├── config.json
│   │   ├── content.md
│   │   └── README.md                    ← "Images live in Cloudinary, see config.json"
│   └── portals/property-1/
│       ├── config.json
│       ├── knowledge.md
│       └── README.md                    ← Same note за images
│
├── belora/                              ← Кристина Николаева
│   ├── client-info.md                   ← Метаданни: контакти, домейн, локация
│   ├── customizations/                  ← Override само промените (празно по default)
│   │   ├── messages/                    ← .gitkeep вътре, override-ва само променени
│   │   ├── signs/                       ← .gitkeep вътре
│   │   └── checklists/                  ← .gitkeep вътре
│   ├── website/
│   │   ├── config.json
│   │   ├── content.md
│   │   └── netlify.toml
│   └── portals/
│       └── property-1/
│           ├── config.json
│           ├── knowledge.md
│           └── netlify.toml
│
├── yavor/                               ← Явор Кичев — ТЕС Боровец
│   ├── client-info.md
│   ├── customizations/
│   │   ├── messages/                    ← .gitkeep
│   │   ├── signs/                       ← .gitkeep
│   │   └── checklists/                  ← .gitkeep
│   ├── website/                         ← един сайт: tes-borovets.com
│   │   ├── config.json
│   │   ├── content.md
│   │   └── netlify.toml
│   └── portals/                         ← 4 портала за 4-те комплекса
│       ├── flora-residence/
│       ├── royal-plaza/
│       ├── rila-park/
│       └── borovets-gardens/
│
└── radoslava/                           ← Радослава — Bird Villa
    ├── client-info.md
    ├── customizations/
    │   ├── messages/                    ← .gitkeep
    │   ├── signs/                       ← .gitkeep
    │   └── checklists/                  ← .gitkeep
    ├── website/                         ← Тя си има WordPress сайт
    │   └── README.md                    ← "Не се прави сайт — клиентът има свой"
    └── portals/property-1/
        └── ...
```

> **Note:** Всеки клиент **винаги** има `customizations/` директория със същата структура като в `_template/` — дори ако е празна. Това е consistent pattern. Празните директории остават в Git с `.gitkeep` файл вътре.

> **Note:** Снимките **никога не са в Git**. Реални снимки живеят в Cloudinary. URL-ите са в `config.json`. Виж секция 15.

---

## 3. THREE TYPES OF DEPLOYMENTS

Архитектурата има 3 различни вида deployments. Разбирането на разликата е критично, защото всеки тип има свои правила за update, backup и scaling.

### Type 1 · Static deployments (per клиент)
- **Какво:** Уебсайтове и портали — едни статични файлове за всеки клиент
- **Колко:** N сайта × M портала per клиент
- **Update:** Редактираш конфиг или съдържание → push → Netlify auto-deploy
- **Cost:** Нулев per deployment (Netlify free tier)
- **Примери:** `belora.bg`, `portal.belora.bg`, `tes-borovets.com`

### Type 2 · Stateless shared services (един за всички)
- **Какво:** Backend функции, които нямат собствено състояние — само обработват заявки
- **Колко:** Един deploy за всички клиенти
- **Update:** Промяна в `chatbot.js` → push → автоматично за всички клиенти
- **Cost:** Pay per request (Claude API), но един API ключ
- **Примери:** Chatbot Netlify Function

### Type 3 · Stateful shared apps (един deploy, access controlled)
- **Какво:** Приложения с БД и потребители — едно приложение, multi-tenant access
- **Колко:** Един deploy с user/tenant isolation през БД
- **Update:** Миграции на БД + frontend deploy. По-внимателно от Type 1 и 2.
- **Cost:** Хостинг на БД (Supabase) + frontend
- **Примери:** Финансов тракер (`welcomebook-tracker.netlify.app`)

> **PRO TIP:** Когато планираш нова feature, питай се: **"Това per клиент ли е, един за всички, или има shared state?"** Отговорът ти казва къде кодът трябва да живее в репото.

---

## 4. КАК РАБОТИ — 3 СЦЕНАРИЯ

### 🟢 Сценарий A: Нов клиент с 1 имот (Belora)

```
clients/belora/
├── website/         → deploy към belora.bg              (един уебсайт)
└── portals/
    └── property-1/  → deploy към portal.belora.bg       (един портал с чатбот)
```

### 🟡 Сценарий B: Клиент с няколко имота, един бранд (Явор — ТЕС Боровец)

```
clients/yavor/
├── website/                       → tes-borovets.com           (един сайт за всичките 4 комплекса)
└── portals/
    ├── flora-residence/           → flora.tes-borovets.com    (или portal1.tes-borovets.com)
    ├── royal-plaza/               → royal.tes-borovets.com
    ├── rila-park/                 → rila.tes-borovets.com
    └── borovets-gardens/          → gardens.tes-borovets.com
```

### 🔵 Сценарий C: Клиент с готов сайт (Радослава — WordPress)

```
clients/radoslava/
├── website/         → README обяснява "не се deploy-ва, клиентът има свой WP"
└── portals/
    └── property-1/  → portal.thebirdvilla.com  (само портал, без сайт)
```

---

## 5. SHARED RESOURCES PATTERN — КАК СПЕСТЯВА ЧАСОВЕ

Имаш 30 message templates (BG+EN), signs pack (WiFi/правила/check-out), checklists, feedback forms. Те са общи за повечето клиенти. Без shared structure всеки клиент копира 30 файла → дублиране → bug-fix става 50 промени.

### Master + Override pattern

**Master copies живеят в `shared-resources/`:**
```
shared-resources/
├── message-templates/
│   ├── 01-booking-confirmation.md
│   ├── 02-checkin-instructions.md
│   ├── ... (30 общо)
│   └── README.md
├── signs-pack/
│   ├── wifi-sign.html
│   ├── house-rules.html
│   └── checkout-sign.html
├── checklists/
│   ├── cleaning-checklist.md
│   └── maintenance-checklist.md
└── feedback-form/
    └── guest-feedback.html
```

**Per-client override-и живеят в `clients/[name]/customizations/`:**
```
clients/belora/customizations/
└── messages/
    └── 01-booking-confirmation.md   ← override само ако Belora иска нещо различно
```

### Resolution logic

При build на портала или сайта:
1. Скриптът проверява `clients/belora/customizations/messages/01-...`
2. Ако съществува → използва клиентската версия
3. Ако не → използва `shared-resources/message-templates/01-...`

**Резултат:** Bug-fix в master template = автоматично за всички 50 клиента, които не override-ват. Override-ите са explicit.

> **PRO TIP:** Override-вай само когато клиентът ИЗРИЧНО иска различен текст. По default, наследяване от shared-resources/. 95% от клиентите никога не override-ват нищо.

---

## 6. BUILD SYSTEM · ELEVENTY (11ty)

> **Това е блокираща информация — без нея не можеш да започнеш.** Тук решаваме *как* config.json + content.md + Cloudinary URLs се превръщат в работещ статичен сайт.

### Защо Eleventy

| Критерий | Eleventy | Astro | Custom Node.js |
|----------|----------|-------|----------------|
| Кратко learning curve | ✅ | 🟡 | ❌ |
| Config-driven (JSON → HTML) | ✅ | ✅ | Manual |
| Build speed (50+ клиента) | ✅ | ✅ | Зависи |
| Markdown support out-of-box | ✅ | ✅ | Manual |
| Claude Code знае го добре | ✅ | ✅ | N/A |
| Zero JS runtime в готовия сайт | ✅ | ✅ (default) | ✅ |
| Maintenance след 1 година | ✅ | ✅ | ⚠️ |

**Решение: Eleventy.** Лек, добре документиран, perfect fit за config-driven static sites. Astro е алтернатива ако в бъдеще искаш React/Vue components в сайтовете — но за сегашните нужди Eleventy е правилния избор.

### Как работи build процесът

```
Input:
  templates/website-family/src/index.njk      ← Master Eleventy template
  clients/belora/website/config.json          ← {"business_name":"Belora", ...}
  clients/belora/website/content.md           ← Текстове на сайта
  Cloudinary URLs (от config.json)            ← Снимките

      ↓ npx eleventy --config=eleventy.config.js --input=...

Output:
  _site/belora/                               ← Build artifact, deploy към Netlify
    ├── index.html
    ├── about/index.html
    ├── contact/index.html
    └── assets/css/main.css
```

### `eleventy.config.js` (опростен пример)

```javascript
module.exports = function(eleventyConfig) {
  // Зарежда client config from CLI arg
  const clientId = process.env.CLIENT_ID;
  const clientConfig = require(`./clients/${clientId}/website/config.json`);

  // Прави config глобално достъпен в templates
  eleventyConfig.addGlobalData("client", clientConfig);

  // Шаблон за изграждане на Cloudinary URL
  eleventyConfig.addShortcode("img", function(filename) {
    const cloudName = process.env.CLOUDINARY_CLOUD_NAME;
    return `https://res.cloudinary.com/${cloudName}/image/upload/clients/${clientId}/${filename}`;
  });

  return {
    dir: {
      input: `templates/website-${clientConfig.template}/src`,
      output: `_site/${clientId}`
    }
  };
};
```

### Пример template в Eleventy (`.njk`)

```nunjucks
<!DOCTYPE html>
<html lang="{{ client.language[0] }}">
<head>
  <title>{{ client.business_name }}</title>
  <style>--primary: {{ client.primary_color }};</style>
</head>
<body>
  <h1>{{ client.business_name }}</h1>
  <img src="{% img client.hero_image %}" alt="{{ client.business_name }}">

  <section class="gallery">
  {% for image in client.gallery %}
    <img src="{% img image %}" alt="">
  {% endfor %}
  </section>
</body>
</html>
```

При build с `CLIENT_ID=belora`, шаблонът се "пълни" с данните от Belora's config.json и излиза готов HTML със снимки от Cloudinary.

### Build команда

```bash
# Build за един клиент
CLIENT_ID=belora npx eleventy

# Watch mode за development
CLIENT_ID=belora npx eleventy --serve

# Build за всички клиенти (за CI)
for client in clients/*/; do
  CLIENT_ID=$(basename $client) npx eleventy
done
```

> **PRO TIP:** Не започвай с custom build script. Eleventy решава 95% от case-овете out-of-the-box. Кастомизация идва само когато имаш специфичен use case.

---

## 7. КОНФИГУРАЦИОННИ ФАЙЛОВЕ — КАК ИЗГЛЕЖДАТ

### `clients/belora/client-info.md`
```markdown
# Belora — Кристина Николаева

- **Контакт:** Кристина Николаева, +359 88X XXX XXX
- **Email:** kristina@example.com
- **Брой имоти:** 1
- **Локация:** с. Геша, общ. Дряново
- **Домейн:** belora.bg (купен от клиента, насочен към Netlify)
- **Активен сезон:** Април-Октомври + Нова година
- **Notes:** Pet-friendly, нов хост (от 2025), без ревюта в момента
```

> **Note:** Файлът е за теб (operator metadata), не се чете от build процеса. Тиер, цена, договор — те живеят в offer документи (Master Playbook), не в архитектурен файл.

### `clients/belora/website/config.json` (пълен пример)
```json
{
  "client_id": "belora",
  "domain": "belora.bg",
  "template": "family",
  "language": ["bg", "en"],
  "primary_color": "#8B6F47",
  "accent_color": "#D4A574",
  "owner_name": "Кристина Николаева",
  "business_name": "Guest House Belora",
  "contact_phone": "+359 88X XXX XXX",
  "contact_email": "info@belora.bg",
  "hero_image": "kitchen-1.jpg",
  "gallery": [
    "kitchen-1.jpg",
    "bedroom-1.jpg",
    "bedroom-2.jpg",
    "bathroom-1.jpg",
    "exterior-1.jpg"
  ]
}
```

> **Note:** Снимките се reference-ват по име на файл. Eleventy build процесът добавя Cloudinary prefix автоматично през `{% img %}` shortcode. Не пишеш пълни URL-и в config.json.

### `clients/belora/portals/property-1/config.json`
```json
{
  "client_id": "belora-1",
  "domain": "portal.belora.bg",
  "property_name": "Guest House Belora",
  "language": ["bg", "en"],
  "primary_language": "bg",
  "fallback_contact": "+359 88X XXX XXX",
  "chatbot": {
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 800,
    "temperature": 0.3,
    "timeout_seconds": 10,
    "tone": "warm-professional",
    "restrictions": [
      "Не отговаряй на политически въпроси",
      "При искане за refund/cancellation, насочи към домакина",
      "Не давай мнения за други имоти/конкуренти"
    ]
  }
}
```

### `clients/belora/portals/property-1/knowledge.md`
```markdown
# Guest House Belora — Knowledge Base

## За имота
- 6 гости, 2 спални, 7 легла, 1 баня
- Pet-friendly (до 2 кучета)
- Безплатен паркинг
- Кафе машина в кухнята

## WiFi
- Network: BeloraGuest
- Password: dryanovo2025

## Check-in / Check-out
- Check-in: 14:00 - 22:00
- Check-out: до 11:00
- Адрес: с. Геша, общ. Дряново
- Ключ: в сейфа на входната врата, код 4471

## Правила
- Pet-friendly: до 2 кучета
- Без пушене вътре
- Тих час: 22:00 - 08:00
- Без партита

## Препоръки за района
- **Дряновски манастир** — 5 мин с кола, отворен 08:00-18:00
- **Бачо Киро пещера** — 10 мин с кола, входна такса €5
- **Дряновски водопади** — 15 мин с кола + 30 мин ходене
- **Ресторант "Балкан"** — традиционна кухня, 3 мин пеша

## Контакт при спешност
Кристина: +359 88X XXX XXX (само при спешност, между 08:00-22:00)
```

---

## 8. SETUP WORKFLOW ЗА НОВ КЛИЕНТ (под 30 минути)

### Стъпка 1: Генерираш папка (2 мин)
```bash
./tools/new-client.sh belora
```
Скриптът:
- Копира `clients/_template/` като `clients/belora/`
- Подменя `{{CLIENT_ID}}` навсякъде с `belora`
- Създава първи property портал

### Стъпка 2: Попълваш `client-info.md` (3 мин)
Името, контактите, домейна, локацията.

### Стъпка 3: Попълваш `knowledge.md` (15-20 мин)
Тук е реалната работа — събираш WiFi-я, правилата, препоръките от обаждането с клиента.

### Стъпка 4: Качваш снимки в Cloudinary (3 мин)
```bash
# Качваш в Cloudinary под clients/belora/ folder
# Cloudinary автоматично дава URL pattern:
# https://res.cloudinary.com/[YOUR_CLOUD_NAME]/image/upload/clients/belora/kitchen-1.jpg
```
В `config.json` слагаш само имена на файлове (без пълен URL). Eleventy add-ва prefix-а.

### Стъпка 5: Deploy preview (5 мин)
```bash
git checkout -b client/belora
./tools/deploy-client.sh belora --preview
```
Скриптът:
- Build-ва уебсайта от темплейта + config.json + content.md (с Eleventy)
- Build-ва портала от portal-master + config.json + knowledge.md
- Създава Netlify Deploy Preview (URL: `deploy-preview-N--belora.netlify.app`)
- НЕ deploy-ва в production още

### Стъпка 6: Тестване в preview (5 мин)
- Отваряш preview URL на телефон
- Питаш чатбота 5 въпроса (WiFi, check-in, ресторант, кучета, манастир)
- Тестваш fallback (изключи WiFi → виждаш ли graceful error?)
- Ако всичко работи → одобряваш PR → merge в main → production deploy

> **PRO TIP:** Никога не пускай клиент в production без преминаване през preview. Едно "ще проверя бързо после" = 1 разочарован клиент = 5 нови потенциални.

---

## 8.5. NETLIFY DEPLOY CONFIGURATION — КАК CLIENT_ID СЕ МАПВА КЪМ NETLIFY SITES

> **Кога четеш това:** Преди build на втория клиент. За първия клиент правиш всичко ръчно през Netlify UI за да научиш workflow-а.

### Един клиент = 1-N Netlify sites

Според броя deployable сайтове на клиента:

| Клиент | Уебсайт | Портал(и) | Total Netlify sites |
|--------|---------|-----------|---------------------|
| **Belora** (1 имот) | belora.bg | portal.belora.bg | 2 |
| **Yavor** (4 имота) | tes-borovets.com | flora/royal/rila/gardens.tes-borovets.com | 5 |
| **Radoslava** (WP сайт) | — (има свой) | portal.thebirdvilla.com | 1 |

### Mapping в client-info.md

Всеки клиент пази Netlify site ID-тата си в `client-info.md`. Site ID-то е unique identifier за всеки Netlify site (получаваш го при създаване на сайта в Netlify UI или CLI).

```markdown
# Belora — Кристина Николаева

- **Контакт:** Кристина Николаева, +359 88X XXX XXX
- **Локация:** с. Геша, общ. Дряново
- **Домейн:** belora.bg
- **Активен сезон:** Април-Октомври + Нова година

## Netlify sites

- **website:**
  - site_id: `abc123-def456-...`
  - production_url: `https://belora.bg`
  - custom_domain: `belora.bg` (DNS → Netlify)
- **portal-property-1:**
  - site_id: `ghi789-jkl012-...`
  - production_url: `https://portal.belora.bg`
  - custom_domain: `portal.belora.bg` (DNS → Netlify)
```

### Как `deploy-client.sh` решава кой site ID да използва

Скриптът чете `client-info.md` (или отделен `netlify-mapping.json` за по-чисто parsing) и извиква Netlify CLI с правилния site ID:

```bash
#!/bin/bash
# tools/deploy-client.sh (опростен pseudocode)
CLIENT_ID=$1
PREVIEW_FLAG=$2  # --preview или празно

# Зарежда mapping
NETLIFY_MAPPING="clients/$CLIENT_ID/netlify-mapping.json"

# Build website
CLIENT_ID=$CLIENT_ID npx eleventy --input=templates/website-${TEMPLATE}/src \
  --output=_site/$CLIENT_ID/website

# Deploy website
WEBSITE_SITE_ID=$(jq -r '.website.site_id' $NETLIFY_MAPPING)
if [ "$PREVIEW_FLAG" = "--preview" ]; then
  netlify deploy --site=$WEBSITE_SITE_ID --dir=_site/$CLIENT_ID/website
else
  netlify deploy --site=$WEBSITE_SITE_ID --dir=_site/$CLIENT_ID/website --prod
fi

# Build & deploy всеки portal
for portal in clients/$CLIENT_ID/portals/*/; do
  PORTAL_ID=$(basename $portal)
  PORTAL_SITE_ID=$(jq -r ".portals.\"$PORTAL_ID\".site_id" $NETLIFY_MAPPING)
  # ... build + deploy logic
done
```

> **PRO TIP:** За първия клиент **не пиши скрипта**. Прави всеки deploy ръчно през `netlify deploy --site=<site_id>` командата. След втория клиент имаш достатъчно опит за да автоматизираш разумно.

### Netlify-mapping.json (по-чист alternative)

Вместо да се опитваме да parse-ваме markdown, по-чистият подход е отделен JSON файл per клиент:

```json
{
  "client_id": "belora",
  "website": {
    "site_id": "abc123-def456-...",
    "site_name": "belora-website",
    "custom_domain": "belora.bg",
    "production_url": "https://belora.bg"
  },
  "portals": {
    "property-1": {
      "site_id": "ghi789-jkl012-...",
      "site_name": "belora-portal-1",
      "custom_domain": "portal.belora.bg",
      "production_url": "https://portal.belora.bg"
    }
  }
}
```

Файлът живее в `clients/belora/netlify-mapping.json`. Лесен за parsing, по-малко risk от грешка.

### Custom domains setup — DNS, какво прави клиентът

Клиентът купува домейна (например `belora.bg` от Namecheap или от български регистратор). След това има 2 стъпки за да го свърже с Netlify:

**Стъпка 1: Добавяш custom domain в Netlify (твоя страна)**

```bash
netlify domains:add belora.bg --site=<WEBSITE_SITE_ID>
netlify domains:add portal.belora.bg --site=<PORTAL_SITE_ID>
```

Или през Netlify UI: Site settings → Domain management → Add custom domain.

Netlify ти дава DNS records, които клиентът трябва да добави.

**Стъпка 2: Клиентът добавя DNS records (на регистратора му)**

Стандартен setup за apex domain (`belora.bg`):

| Type | Host | Value |
|------|------|-------|
| `A` | `@` | `75.2.60.5` (Netlify load balancer) |
| `CNAME` | `www` | `<site-name>.netlify.app` |

За subdomain (`portal.belora.bg`):

| Type | Host | Value |
|------|------|-------|
| `CNAME` | `portal` | `<portal-site-name>.netlify.app` |

> **PRO TIP:** Изпрати на клиента screenshot на DNS settings от Netlify, не само текст. Намери български клиент → Намери Namecheap/Superhosting/Cloudflare скрийншот → пращаш точно как изглежда. Спестяваш 30 минути telephone support.

**Стъпка 3: SSL автоматично**

След като DNS се пропагира (5 мин - 2 часа), Netlify автоматично provisions Let's Encrypt SSL сертификат. Без ръчни стъпки.

> **PRO TIP:** Винаги проверявай че HTTPS работи преди да обявиш сайта за готов на клиента. Netlify дава green checkmark в Domain management когато SSL е активен.

### Как се управлява всичко това (workflow)

```
1. Клиент купува домейн (belora.bg)                       ← клиентът прави
2. Ти създаваш 2 Netlify sites през CLI или UI            ← ти правиш
3. Записваш site_id-тата в netlify-mapping.json           ← ти правиш
4. Добавяш custom domains в Netlify                       ← ти правиш
5. Изпращаш DNS instructions на клиента                   ← ти правиш
6. Клиентът добавя DNS records при регистратора           ← клиентът прави
7. Изчакваш propagation (5 мин - 2 часа)                  ← природа
8. Verify HTTPS работи                                    ← ти проверяваш
9. Build & deploy през ./tools/deploy-client.sh           ← ти правиш
10. Тестваш в preview, merge, production                  ← ти правиш
```

> **PRO TIP:** Стъпки 2-5 в първия клиент те отнемат час. След втория клиент → 15 минути. След петия → автоматизираш в `tools/setup-netlify-sites.sh`.

---

## 9. STAGING vs PRODUCTION — КАК ТЕСТВАШ ПРЕДИ ДА СЪСИПЕШ

### Принципи
- **Никога не push-ваш direct в `main`** за клиентски сайт
- **Винаги работиш в feature branch** (`client/belora`, `fix/yavor-wifi`)
- **PR → Deploy Preview URL** (Netlify прави автоматично)
- **Тестваш в preview → merge → production**

### Workflow в детайли

```
1. Започваш промяна:
   git checkout -b fix/belora-wifi-update

2. Редактираш knowledge.md, push-ваш:
   git add ... && git commit -m "Belora: update WiFi password"
   git push origin fix/belora-wifi-update

3. GitHub създава PR автоматично (или ръчно през UI)

4. Netlify създава Deploy Preview URL:
   deploy-preview-12--belora.netlify.app

5. Отваряш preview, тестваш — питаш чатбота новата парола

6. Ако работи → одобряваш PR → merge в main

7. Netlify автоматично deploy-ва main → production (portal.belora.bg)
```

### Защо това правило не се пренебрегва

- **Direct push в main = direct production** — ако грешиш WiFi паролата с typo, гостът на Belora получава грешен код
- **Preview URL е безплатен** — Netlify го прави автоматично, не ти струва нищо
- **Code review** — дори ти сам, преглеждането на PR преди merge хваща 50% от грешките

> **PRO TIP:** Slack/Viber канал със сам себе си — пращаш preview URL → отваряш на телефон. Това разделя "пишене на код" от "тестване на резултат" което е критично за качество.

---

## 10. CHATBOT KNOWLEDGE LOADING — КАК ЧАТБОТЪТ "ВИЖДА" KNOWLEDGE.MD

> **Това е блокираща информация — без нея чатботът не може да работи.**

### High-level flow

```
Гост: "Какъв е WiFi-ят?"
   ↓
Portal frontend → POST /api/chatbot { client_id: "belora-1", message: "..." }
   ↓
chatbot.js Netlify Function:
   1. Чете client_id
   2. Зарежда knowledge.md от файлова система
   3. Зарежда config.json (chatbot settings + restrictions)
   4. Изгражда system prompt
   5. Изпраща към Claude API:
      - system: [generated system prompt + knowledge.md]
      - messages: [{ role: "user", content: "Какъв е WiFi-ят?" }]
   6. Връща response.content[0].text към frontend
```

### Pseudocode на `chatbot.js`

```javascript
const Anthropic = require('@anthropic-ai/sdk');
const { loadKnowledge, loadConfig, buildSystemPrompt, fallback } = require('./lib');
const { withTimeout } = require('./lib/timeout');

exports.handler = async (event) => {
  // Frontend изпраща: client_id, messages array (conversation history)
  const { client_id, messages } = JSON.parse(event.body);

  // Validate: messages трябва да е array с поне един user message
  if (!Array.isArray(messages) || messages.length === 0) {
    return { statusCode: 400, body: JSON.stringify({ error: 'messages array required' }) };
  }

  try {
    const config = loadConfig(client_id);
    const knowledge = loadKnowledge(client_id);
    const systemPrompt = buildSystemPrompt(config, knowledge);
    const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

    // Capping: ограничи history до последните 20 messages (10 turns)
    // за да не експлодира token usage при дълги разговори
    const cappedMessages = messages.slice(-20);

    const response = await withTimeout(
      client.messages.create({
        model: config.chatbot.model,
        max_tokens: config.chatbot.max_tokens,
        temperature: config.chatbot.temperature,
        system: systemPrompt,
        messages: cappedMessages   // ← пълна conversation history
      }),
      config.chatbot.timeout_seconds * 1000
    );

    return {
      statusCode: 200,
      body: JSON.stringify({ reply: response.content[0].text })
    };

  } catch (err) {
    logError(client_id, err);
    return {
      statusCode: 200,
      body: JSON.stringify({ reply: fallback(client_id) })
    };
  }
};
```

### Pseudocode на `lib/timeout.js` (споделен helper)

```javascript
// Един timeout helper, използван навсякъде
function withTimeout(promise, ms) {
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('TIMEOUT')), ms)
  );
  return Promise.race([promise, timeoutPromise]);
}

module.exports = { withTimeout };
```

### Pseudocode на `lib/system-prompt.js`

```javascript
function buildSystemPrompt(config, knowledge) {
  const tone = config.chatbot.tone || 'warm-professional';
  const restrictions = config.chatbot.restrictions || [];

  return `Ти си AI асистент за ${config.property_name}.

ПРАВИЛА:
- Говори на ${config.primary_language} по подразбиране, EN ако гост пише на английски.
- Тон: ${tone}.
- Отговаряй САМО на въпроси, на които можеш да намериш отговор в KNOWLEDGE по-долу.
- Ако не знаеш отговора → "Препоръчвам да се свържете с домакина: ${config.fallback_contact}"
- ${restrictions.map(r => `- ${r}`).join('\n')}

KNOWLEDGE:
${knowledge}

Отговаряй кратко, ясно, дружелюбно. Без emoji освен ако гостът използва.`;
}
```

### Token limits — какво да следиш

- Claude Haiku 4.5 context window: 200k tokens
- Average knowledge.md: ~1,000-2,000 tokens (за 1 имот)
- System prompt overhead: ~200 tokens
- User message: ~50-200 tokens
- **Total per заявка:** ~1,500-2,500 tokens (далеч под лимита)

> **PRO TIP:** Ако knowledge.md мине над 5,000 tokens — split-вай по теми (knowledge-rules.md, knowledge-area.md) и в `system-prompt.js` зареждай само релевантния файл базиран на user message keywords. Това е оптимизация за post-MVP — за сега 1 файл стига.

---

## 11. CONVERSATION STATE · КАК СЕ ПАЗИ ИСТОРИЯТА НА РАЗГОВОРА

> **Decisive решение, не опция:** Frontend пази conversation history. Backend е stateless. Всяка заявка изпраща пълния messages array.

### Защо frontend pази history (не backend / не БД)

| Подход | Pros | Cons | Решение |
|--------|------|------|---------|
| **Frontend in-memory** | Прост, privacy-friendly, без БД | History умира при browser refresh | ✅ ДА |
| **Backend session DB** | Преживява refresh | Сложност, БД cost, privacy concerns | ❌ Не (post-MVP) |
| **No history (stateless per Q&A)** | Най-просто | Чатботът не разбира follow-up въпроси | ❌ Не |

**Aргументи за frontend approach:**

1. **Privacy** — guest данни никога не се пазят на наш сървър след сесия. Важно за GDPR.
2. **Простота** — без БД setup, миграции, schema. Работещ chatbot за минути.
3. **Cost** — Claude prompt caching прави повтарящ се context почти безплатен (90% намаление). System prompt + knowledge.md се cache-ват автоматично от Anthropic при repeated заявки.
4. **Use case fit** — guest сесии са кратки (5-30 мин). Browser refresh е rare. Загубата на history при refresh е acceptable trade-off.

### Frontend pseudocode (в `templates/portal-master/assets/chatbot-widget.js`)

```javascript
// State live в memory на browser сесия
const conversationState = {
  messages: [],                    // array of {role, content}
  client_id: 'belora-1'            // от config.json при load
};

async function sendMessage(userText) {
  // Append user message
  conversationState.messages.push({
    role: 'user',
    content: userText
  });

  // Render user message в UI
  renderMessage('user', userText);

  // Show typing indicator
  showTyping();

  try {
    // POST към backend с пълната history
    const response = await fetch('/api/chatbot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        client_id: conversationState.client_id,
        messages: conversationState.messages   // ← пълен array
      })
    });

    const { reply } = await response.json();

    // Append assistant reply към state
    conversationState.messages.push({
      role: 'assistant',
      content: reply
    });

    // Render в UI
    hideTyping();
    renderMessage('assistant', reply);

  } catch (err) {
    hideTyping();
    renderMessage('assistant', 'Извинявам се, временно не мога да отговоря.');
  }
}
```

### Token budget over time

Conversation растe с всеки turn. Без cap, при 50 turns:
- 50 messages × ~150 tokens average = ~7,500 tokens
- + system prompt (1,500-2,500) = ~10,000 tokens total
- Cost per request: расте линейно

**Решение: cap до последните 20 messages (10 turns)** — backend `chatbot.js` прави `messages.slice(-20)` (виж секция 10).

Защо 20 е разумен cap:
- Покрива 95% от реални guest разговори
- Държи token usage predictable
- При нужда от дълъг контекст, чатботът пита "Можем ли да започнем отначало?"

### Какво се случва при browser refresh

Conversation се изгубва. Гостът започва от нула. **Това е acceptable** защото:
- 95% от guest интеракции са еднократни сесии
- Чатботът има knowledge.md → новият разговор не започва "от нищо"
- Гостът не очаква history (не е chat app, а помощник)

### Когато ще преминем към backend session DB (post-MVP)

Знаци, че е време:
- Гост feedback: "Защо забравяш предишния ни разговор?"
- Multi-device use case (гост started on phone, continues on tablet)
- 50+ клиента — стойностно е да даваме "history" като premium feature

Тогава: добавяш Supabase session table, frontend изпраща `session_id` вместо messages array, backend зарежда history от БД.

> **PRO TIP:** Не започвай със session DB. Frontend approach е достатъчен за първите 12 месеца. Add complexity само когато имаш реален guest pain point — не на хипотеза.

---

## 12. ПРОМЯНА НА CHATBOT ПОВЕДЕНИЕТО · ТОН, ЕЗИК, ОГРАНИЧЕНИЯ

Клиентите ще искат специфики: "чатботът да е по-формален", "да отказва политически въпроси", "да не препоръчва конкуренти". Това се прави **БЕЗ да се пипа кода** — само през `config.json`.

### Tone presets (в `chatbot.tone`)

| Стойност | Кога | Пример |
|----------|------|--------|
| `warm-professional` | Default за повечето клиенти | "Здравейте! Радвам се да помогна..." |
| `formal` | Бутикови имоти, бизнес гости | "Уважаеми гости, бих искал да отбележа..." |
| `casual` | Млади хостове, hostel-стил | "Хей! WiFi-ът е..." |
| `boutique-elegant` | Premium имоти €200+/нощ | "Добре дошли в нашия дом..." |

### Restrictions array

Списък от инструкции, които винаги се добавят в system prompt:

```json
"restrictions": [
  "Не отговаряй на политически или религиозни въпроси",
  "При въпрос за refund/cancellation, насочи към домакина",
  "Не давай мнения за други имоти или конкуренти",
  "Не препоръчвай Booking/Airbnb — само директни резервации",
  "Ако гост пита за алкохол → препоръчай местни винарни"
]
```

### Когато клиентът иска промяна

1. Редактираш `config.json` (например добавяш restriction)
2. Branch → push → preview
3. Тестваш с няколко въпроса
4. Merge → production

**Време:** 2-3 минути. **Без code change.** Това е силата на config-driven архитектура.

---

## 13. MULTI-LANGUAGE STRATEGY · РЕШЕНИЕ

> **Decisive решение, не опция:** Един knowledge.md с всичко на BG. Чатботът автоматично превежда при заявка на друг език.

### Защо този подход (не другите)

| Подход | Pros | Cons | Решение |
|--------|------|------|---------|
| **2 файла** (knowledge-bg.md, knowledge-en.md) | Контрол на превода | 2x maintenance, sync риск | ❌ Не |
| **Един файл, smesен** (BG + EN заедно) | Един source | Confusing за Claude, рядко работи добре | ❌ Не |
| **Един BG файл, Claude превежда** | Един source, по-малко работа | Зависи от качеството на превода | ✅ ДА |

### Как работи

В `config.json`:
```json
"language": ["bg", "en"],
"primary_language": "bg"
```

В `system-prompt.js`:
```
ПРАВИЛА:
- Говори на български по подразбиране.
- Ако гостът пише на английски → отговори на английски, превеждайки info от KNOWLEDGE по-долу.
- KNOWLEDGE е на български. Превеждай го качествено когато трябва.
```

Claude Haiku 4.5 е много добър в превод BG↔EN. За руски/немски също работи — добавяш в `language` array.

### Кога правиш ръчен превод (override)

Ако клиентът иска специфичен превод (например "Дряновски манастир" винаги да се превежда като "Dryanovo Monastery", не "Dryanovsky"):

В `clients/belora/portals/property-1/config.json`:
```json
"translation_overrides": {
  "Дряновски манастир": "Dryanovo Monastery",
  "Бачо Киро": "Bacho Kiro Cave"
}
```

`system-prompt.js` подава тези overrides в prompt-а: "Когато превеждаш на английски, винаги използвай тези преводи..."

> **PRO TIP:** За първите 5-10 клиента не пиши translation_overrides. Тествай как Claude превежда сам — в 95% от случаите е достатъчно добре. Override-ваш само когато има конкретно недоволство.

---

## 14. UPDATE WORKFLOW (когато клиентът иска промяна)

### Сценарий A: Промяна на WiFi или check-in часове
```bash
git checkout -b fix/belora-wifi
# Редактираш knowledge.md
git add clients/belora/portals/property-1/knowledge.md
git commit -m "Belora: update WiFi password"
git push origin fix/belora-wifi
# Преглеждаш Deploy Preview → merge → production
```
Готово за 2-3 минути. Чатботът използва новата инфо при следваща заявка.

### Сценарий B: Нова страница на сайта
- Branch → редактираш `content.md` → push → preview → merge → production
- Готово за 5-10 минути

### Сценарий C: Промяна в shared template (засяга всички клиенти)
- ⚠️ **По-внимателно** — това засяга всички 50 клиента
- Branch → промяна в `templates/portal-master/`
- Тествай **поне 3 различни клиента** в preview
- Code review (дори ти сам) преди merge
- Bonus: notification до клиентите ако промяната е visible

---

## 15. IMAGE STORAGE — ЗАЩО CLOUDINARY, НЕ GIT

### Проблем
30-50 снимки × 2-5MB × 50 клиента = **3-12 GB** в Git репото. Git не е направен за binary файлове — клонирането на репото става бавно, push/pull-ът виси, GitHub започва да жалва.

### Решение: Cloudinary

**Структура в Cloudinary:**
```
[YOUR_CLOUD_NAME]/                          ← твоят Cloudinary акаунт
└── clients/                                ← всички клиентски снимки тук
    ├── belora/
    │   ├── kitchen-1.jpg
    │   ├── bedroom-1.jpg
    │   └── ... (30 снимки)
    ├── yavor/
    │   ├── flora-exterior-1.jpg
    │   └── ...
    └── radoslava/
```

**Реален URL pattern на Cloudinary:**
```
https://res.cloudinary.com/[CLOUD_NAME]/image/upload/clients/[client_id]/[filename]
```

Например за Belora:
```
https://res.cloudinary.com/welcomebook-agency/image/upload/clients/belora/kitchen-1.jpg
```

### Как се използва в config.json

В `config.json` пишеш само **имена на файлове**:
```json
{
  "hero_image": "kitchen-1.jpg",
  "gallery": ["kitchen-1.jpg", "bedroom-1.jpg"]
}
```

Eleventy `{% img %}` shortcode (виж секция 6) изгражда пълния URL автоматично.

### Environment variable

В `.env`:
```
CLOUDINARY_CLOUD_NAME=welcomebook-agency
CLOUDINARY_API_KEY=...        ← само за upload script-ове, не за runtime
CLOUDINARY_API_SECRET=...     ← същото
```

В Netlify env vars (за production deploy): същите.

### Alternatives (ако Cloudinary не е приемлив)

| Услуга | Free tier | Кога я избираш |
|--------|-----------|----------------|
| **Cloudinary** | 25 GB storage + 25 GB bandwidth | Default — auto optimization, най-лесно |
| **ImageKit** | 20 GB storage + 20 GB bandwidth | Ако искаш повече transformation control |
| **Netlify Large Media** | 5 GB free | Само ако искаш всичко на Netlify |
| **Supabase Storage** | 1 GB free | Ако вече използваш Supabase за friction-less integration |

### Какво НЕ правиш

- ❌ Push оригинални снимки в Git
- ❌ Държиш ги локално без backup (Cloudinary вече е backup)
- ❌ Държиш всичко в едно Cloudinary folder без per-client изолация

> **PRO TIP:** Когато клиент остави агенцията, делетваш само неговата Cloudinary папка + папка в `clients/`. Няма "забравени" файлове.

---

## 16. CHATBOT RESILIENCE — КАКВО СТАВА КОГАТО НЕЩО СЕ СЧУПИ

### Сценарии за грешки

| Грешка | Причина | Какво правим |
|--------|---------|--------------|
| **Anthropic API down** | Outage от страна на Anthropic | Fallback message + log |
| **Rate limit hit** | Прекалено много заявки в кратък период | Graceful degradation + log |
| **Network timeout (10s+)** | Лоша връзка на госта или server delay | Fallback message |
| **Invalid knowledge.md** | Грешен формат след update | Default knowledge + alert към теб |
| **Missing config.json** | Сгрешен deploy | 503 страница + alert |

### Fallback Message Pattern

В `backend/netlify/functions/lib/fallback.js`:
```javascript
function getFallbackMessage(client_id, lang = 'bg') {
  const config = loadClientConfig(client_id);
  const phone = config.fallback_contact;

  if (lang === 'bg') {
    return `Извинявам се, временно не мога да отговоря.
    Моля свържете се с домакина: ${phone}`;
  }
  return `Sorry, I'm temporarily unable to respond.
    Please contact the host: ${phone}`;
}
```

### Timeout Strategy

Използваме централизирания `withTimeout` helper от `lib/timeout.js` (виж секция 10):

```javascript
// chatbot.js — actual usage
const { withTimeout } = require('./lib/timeout');

try {
  return await withTimeout(
    claude.messages.create({...}),
    config.chatbot.timeout_seconds * 1000
  );
} catch (err) {
  logError(client_id, err);
  return getFallbackMessage(client_id);
}
```

> **Pro tip:** Един helper, една имплементация. Никога не дублирай Promise.race + setTimeout логика — bug fix трябва да става на едно място.

### Logging

**Note:** `logs/` папката е gitignored. Тя се създава локално когато сваляш логове от Netlify за анализ. Не съществува в репото като source-controlled директория.

```
logs/                                    ← локално, gitignored
├── chatbot/
│   ├── 2026-04-29-belora.jsonl         ← Per client, per day
│   └── 2026-04-29-yavor.jsonl
└── errors/
    └── 2026-04-29-errors.jsonl          ← Всички грешки на едно място
```

Netlify Functions автоматично логват console.log output — ти го exporтираш през CLI:
```bash
netlify logs:function chatbot --since 7d > logs/chatbot/this-week.jsonl
```

Всяка заявка → запис: `{ timestamp, client_id, question, response, latency_ms, error? }`

> **PRO TIP:** След 1 месец гледаш `logs/chatbot/` и виждаш кои въпроси чатботът е отговорил зле или не е отговорил → подобряваш `knowledge.md`. Това е cycle-а на подобрение.

---

## 17. BACKUP & DISASTER RECOVERY

Клиентите плащат monthly subscription защото се грижим за operational reliability. Това трябва да се отразява в архитектурата.

### Какво е бекъп-нато автоматично

| Asset | Бекъп от | Колко често | Recovery time |
|-------|----------|-------------|---------------|
| **Code** | GitHub | При всеки commit | < 5 мин |
| **Client images** | Cloudinary | При upload | < 1 мин |
| **Deployments** | Netlify | При всеки deploy | < 5 мин (rollback) |
| **Supabase data** | Manual script | Седмично | 1-2 часа |
| **API keys** | Password manager | Manual | < 30 мин |

### Manual бекъп — какво трябва да правиш

**Седмично (петък вечер, 5 минути):**
```bash
./tools/backup-supabase.sh
# Експортира financial-tracker данни → локално + S3
```

**Месечно (1-во число, 15 минути):**
- Verify, че Cloudinary still е активен
- Verify, че GitHub access не е expire-нал
- Verify, че Anthropic API key still е valid
- Update password manager ако нещо е променено

### Recovery Scenarios — какво правиш ако

**(a) GitHub акаунт suspended**
- Имаш local clone на репото (винаги)
- Push към alternative provider (GitLab, Bitbucket)
- Update Netlify на новия repo source
- **Recovery time:** 2-3 часа

**(b) Anthropic API rate limit**
- Fallback вече е активен (виж секция 16)
- Свържи се с Anthropic за upgrade на лимит
- Проверявай `logs/errors/` за affected клиенти
- **Recovery time:** 1-24 часа (зависи от Anthropic)

**(c) Netlify outage**
- Outage обикновено е < 1 час
- Fallback страница на различен провайдер за критичен случай (post-MVP)
- **Recovery time:** Чакане на Netlify (1-3 часа typical)

**(d) Клиентски домейн expire**
- Ти не си отговорен за това (клиентът купи домейна)
- Имей `client-info.md` reminder за renewal date
- Уведоми клиента 30 дни преди expire
- **Recovery time:** Зависи от клиента

### 2FA & Recovery Codes

Задължително 2FA на:
- Anthropic Console
- GitHub
- Netlify
- Supabase
- Cloudinary
- Domain registrars (Namecheap)

Recovery codes → **password manager** (1Password, Bitwarden). НЕ в .txt файл, НЕ в Notion.

> **PRO TIP:** Тествай recovery scenario веднъж месечно. "Какво правя ако GitHub-а се счупи СЕГА?" — ако не знаеш отговора за 60 секунди, документирай го.

---

## 18. КЛЮЧОВИ АРХИТЕКТУРНИ РЕШЕНИЯ — ОБЯСНЕНИЯ

### ❓ Защо един Git репо, не 50?
- **Bug-fix се прави на 1 място** — ако намериш грешка в портал шаблона, оправяш я веднъж и всички 50 портала се обновяват
- **Versioning е централизирано** — никога не се чудиш "коя версия има клиент X"
- **Backup е автоматичен** — GitHub автоматично пази всичко
- **Cost** — €0 (GitHub Free за private репота)

### ❓ Защо един backend, не 50?
- **Един API ключ, един бил** — не 50 OpenAI акаунта
- **Bug-fix централизирано** — оправяш чатбота за всички наведнъж
- **Скейл** — Netlify Functions free tier = 125,000 заявки/месец = достатъчно за 100+ клиента

### ❓ Защо markdown, не БД (за knowledge)?
- **Безплатно** — БД струва месечно
- **Versioning през Git** — виждаш кога си променил какво
- **Ти го редактираш по-бързо от admin панел** — в първите 6 месеца
- **Migration към БД след 40+ клиента** — когато стане смислено да дадеш admin панел на клиентите

### ❓ Защо custom домейн, не subdomain на welcomebook.agency?
- **Клиентите искат свой бранд** — `belora.bg` е по-професионално от `belora.welcomebook.agency`
- **Psychological ownership** — клиентът чувства, че сайтът е негов
- **SEO** — Google обича собствени домейни
- **Reality check** — Netlify free tier поддържа неограничено custom домейни

### ❓ Защо 3 уеб шаблона, не 1?
- **Property manager сайт е друго от бутик къща** — multi-property hub vs single hero image
- **Предотвратява custom искания** — "Имам шаблона за теб" вместо "от нулата"
- **80% от клиентите** падат в един от трите → drastically less work
- **20% custom** → плащат custom add-on

### ❓ Защо shared-resources/, не дублиране?
- **30 message templates × 50 клиента = 1,500 файла** — невъзможно за поддръжка
- **Override pattern** — клиент override-ва само промените, останалото наследява
- **Bug-fix в master template = автоматично за всички**

### ❓ Защо Eleventy, не custom build script?
- **Mature ecosystem** — 50,000+ projects на GitHub
- **Claude Code знае го отлично** — лесно да генерира templates
- **Config-driven естество** — perfect fit за наш use case
- **Zero JS runtime** — готовите сайтове са pure HTML/CSS

---

## 19. ЧЕРВЕНИ ФЛАГОВЕ — КАПАНИ ЗА ИЗБЯГВАНЕ

### 🔐 Security
- ❌ API ключ в код / .txt / Git — НИКОГА. Винаги в Netlify env vars.
- ❌ GitHub репо публично — задължително Private (безплатно е).
- ❌ Един API ключ за production + dev — направи 2 различни.
- ❌ Споделяне на access tokens в Slack/Viber — използвай password manager.

### 🛠️ Workflow
- ❌ **Build-ваш нов уебсайт шаблон без платен клиент за него.** **НИКОГА.** Build-ваш нов уебсайт шаблон **САМО** когато имаш ПЛАТЕН клиент, който го изисква. **Един шаблон, доказан с реален клиент > три шаблона на хипотеза.**
- ❌ Custom код за първия клиент — не. Темплейтът е thin, остана го thin.
- ❌ Admin панел за клиентите — не в първите 6 месеца. Спестяваш 50 часа.
- ❌ Cypress/Jest тестове сега — over-engineering. Манул тест преди deploy.
- ❌ Direct push в main за клиентски сайт — винаги feature branch + preview.

### 📦 Operations
- ❌ Push на оригинални снимки в Git — Cloudinary за images.
- ❌ Knowledge.md без fallback contact — гост получава Error 500.
- ❌ Чатбот без timeout — лошо UX при API outage.
- ❌ Без backup на Supabase — седмичен export е минимум.

---

## 20. COST STRUCTURE — ЗАЩО АРХИТЕКТУРАТА Е ЕВТИНА ЗА ПОДДРЪЖКА

Архитектурата е оптимизирана за **минимални оперативни разходи** — това освобождава margin за бизнес решения, които живеят в offer документи.

| Resource | Cost/мес | Бележка |
|----------|----------|---------|
| **Claude Haiku 4.5 API** | €1-3 / 10 клиента | ~100-300 заявки/клиент/мес. ~€0.001 за заявка. |
| **Netlify хостинг** | €0 | Free tier до 100 GB bandwidth, 125k function calls. |
| **Netlify Deploy Previews** | €0 | Безплатни, неограничени. |
| **GitHub Private** | €0 | Unlimited private repos за 1 user. |
| **Cloudinary** | €0 | Free tier 25GB storage + 25GB bandwidth/мес. |
| **Supabase** | €0 (start) → ~€25 (Pro) | Free до 500MB DB, 1GB storage. Pro когато стартираш. |
| **Domain registration** | €0 (клиентът плаща) | Клиентът купува свой домейн (€10-30/год). |
| **Password manager (1Password)** | ~€3 | За тебе, личен абонамент. |
| **Sentry / Logtail (post-MVP)** | €0 | Free tier за monitoring. |
| **Общо за 10 клиента** | **€10-30 / мес** | Реални monthly разходи на твоя страна. |

### Защо това е важно архитектурно

- **Низкият оперативен cost** позволява да предлагаш конкурентни цени
- **Free tier-ите** ти дават време да докажеш модела преди да плащаш повече
- **Скейл-абилно** — overall cost grows linear, не exponential
- **Predictable** — няма "сюрприз" сметки от unbounded scaling

### Кога architecture cost ще се промени

- **40+ клиента** → Netlify Pro (~€20/мес) за повече function calls
- **Supabase data > 500MB** → Supabase Pro (~€25/мес)
- **20+ заявки/секунда (peak)** → Dedicated server вместо Netlify Functions
- **100+ клиента** → Cloudinary Plus (~€90/мес) за повече bandwidth

> **PRO TIP:** Cost структурата тук е архитектурна. Цени за клиенти, маржин analysis, и pricing tiers живеят в offer документите (Master Playbook v3.0+).

---

## 21. MIGRATION FROM EXISTING SETUP (Personal Reference)

> ⚠️ **Disclaimer:** Тази секция е специфична за стартова миграция от моята лична текуща ситуация. Generic архитектурата е описана в секции 1-19 и не зависи от тази миграция.

### Какво имаш сега (`ClaudeCodeFirst/`)
```
ClaudeCodeFirst/
├── homepage/, homepage2/      ← маркетингови сайтове на агенцията
├── portal/                    ← welcomebook portal master template
├── Ai chatbot Demo Test/      ← chatbot прототип
├── welcomebook-videos/        ← маркетинг видеа
├── tools/, workflows/         ← Claude Code workflows
└── CLAUDE.md
```

### Стъпки за миграция (1-2 часа)

1. **Преименувай** `ClaudeCodeFirst/` → `welcomebook-agency/`
2. **Премести** `homepage/` и `homepage2/` в `marketing-site/` (отделно от клиентската структура — те са твоите funnels, не клиентски)
3. **Премести** `portal/` → `templates/portal-master/`
4. **Премести** `Ai chatbot Demo Test/` → използваш кода в `backend/netlify/functions/chatbot.js`
5. **Запази** `welcomebook-videos/`, `tools/`, `workflows/` — те си остават
6. **Създай** `templates/website-boutique/`, `website-family/`, `website-multiproperty/` — НО **САМО един** реално (за първия клиент). Останалите два празни placeholder-и.
7. **Създай** `clients/_template/` като скелет
8. **Създай** `shared-resources/` и попълни от съществуващите 30 message templates, signs pack, checklists
9. **Setup Eleventy** — `npm install @11ty/eleventy`, копирай `eleventy.config.js` от секция 6
10. **Setup Cloudinary акаунт** — създай `clients/` папка вътре, упload первите снимки
11. **Създай** `clients/yavor/` (твоят първи реален клиент) — попълваш данни, deploy-ваш

### Какво да НЕ правиш сега
- Не мигрирай старите HTML файлове в `homepage2/` — те са твоят funnel сайт, не клиентски
- Не пиши `tools/new-client.sh` още — направи първо Явор ръчно, разбери workflow-а, после автоматизирай
- **Не build-вай 3-те website темплейта** — започни с 1 (например `multiproperty` за Явор), добави следващ КОГАТО подпишеш клиент, който го изисква

---

## 22. ПЪРВИ ПРАКТИЧЕСКИ СТЪПКИ (тази седмица)

1. **Създай новата структура** като празни папки (30 мин)
2. **Setup Eleventy** в репото (`npm init`, `npm install @11ty/eleventy`) (15 мин)
3. **Премести Явор от plan-овете в реална папка** `clients/yavor/` (1 час)
4. **Build-ни един website шаблон в Eleventy** (`templates/website-multiproperty/` за Явор) (3-4 часа)
5. **Build-ни portal-master шаблон с chatbot widget** (4-5 часа)
6. **Build-ни `backend/netlify/functions/chatbot.js`** с fallback и timeout (3-4 часа)
7. **Setup Cloudinary акаунт** + качи Yavor's images (30 мин)
8. **Deploy-ни първия портал на Явор** (1 час)
9. **Тестваш с реален гост** (когато започне сезонът)

**Общо: ~17-20 часа работа за първия завършен клиент.** След това всеки следващ клиент е 4-6 часа.

---

## 23. КОГА ДА ПРОМЕНИМ АРХИТЕКТУРАТА

Тази структура издържа до **30-50 клиента** без преструктуриране. Знакове, че време да се променя:

- **40+ клиента** → migrate knowledge.md към Supabase БД (даваш admin панел на клиентите)
- **100+ заявки/час** → migrate chatbot.js от Netlify Functions към dedicated сървър
- **20+ custom website клиента** → wear out от поддръжка → въведи "no custom websites" политика, или вдигни цената
- **Започваш да наемаш хора** → въвеждаш `roles.md` в всеки клиент (кой работи по кого)
- **Клиент изисква нов website темплейт** → build-ваш 4-я (или 2-я) — но **САМО** когато имаш платена сделка за него

---

## 24. ВЪПРОСИ ЗА БЪДЕЩЕ

- **Клиентски admin панел** — кога ще искаш клиентите сами да редактират knowledge?
- **Multi-language website** — какво ако руски турист иска русифициран портал?
- **Booking widget на сайта** — кой провайдър (BNB Forms? Smoobu? Hostex?)
- **Анализ на чатбот логове** — кога да започнем да виждаме какво питат гостите за да подобряваме knowledge?
- **Mobile app per клиент** — има ли смисъл при 30+ клиента?

Тези не са спешни. Решават се след 5-10 завършени клиента.

---

## Companion PDF Reference

`WelcomeBook_Architecture_Reference_v1.pdf` визуализира секции 1-6 в print-ready формат с brand colors (#0A0F1E + #E8820C). PDF v1.0 е outdated спрямо този markdown. Следващата редакция на PDF (v1.3) трябва да отразява промените:
- Three Types of Deployments (секция 3)
- Shared Resources Pattern (секция 5)
- Build System · Eleventy (секция 6, нова в v1.2)
- Chatbot Knowledge Loading (секция 10, нова в v1.2)
- Conversation State (секция 11, нова в v1.3)
- Tone presets и Multi-language strategy (секции 12-13)
- Image Storage с правилни Cloudinary URLs (секция 15)
- Chatbot Resilience (секция 16)
- Cost Structure (преработена от "финансов модел" към чисти разходи)

---

## Changelog

### v1.3 → v1.4 (трети peer review patch)

**3 fixes от трети round code review:**

1. **Typo fix в pseudocode** — "за да не expлодира token usage" → "за да не експлодира token usage" (mixed латиница/кирилица в коментар на chatbot.js).
2. **`.gitkeep` бележки в `_template/` структурата** — добавени за consistency с реалните клиенти (Belora, Yavor, Radoslava). Преди само реалните клиенти имаха .gitkeep notes, сега и template-ът ги има.
3. **НОВА СЕКЦИЯ 8.5: Netlify Deploy Configuration** — explicit как `client_id` се мапва към Netlify site IDs, custom domains setup (DNS records, SSL), `netlify-mapping.json` файл per клиент, deploy-client.sh pseudocode, 10-стъпков workflow за нов клиент. БЛОКЕР, който е критичен за втория клиент.

**Архитектурно следствие:** С новата секция 8.5, документът сега покрива целия life cycle на нов клиент — от Netlify site creation до DNS propagation до production deploy. Няма повече implicit knowledge.

### v1.2 → v1.3 (втори peer review fixes)

**7 fixes от втори round code review:**

1. **Latinic остатък в секция 5** — "KAK СПЕСТЯВА ЧАСОВЕ" → "КАК СПЕСТЯВА ЧАСОВЕ". Същата грешка в секция 10 — "KAK ЧАТБОТЪТ" → "КАК ЧАТБОТЪТ".
2. **Zero-width characters премахнати** — "експор​тираш" → "експортираш" (3 общи случая, изчистени с Unicode regex).
3. **`timeoutPromise` consistency** — създаден централизиран `lib/timeout.js` с `withTimeout` helper. И двете секции (10 и 16) сега използват същата имплементация. Махната дублирана inline логика.
4. **НОВА СЕКЦИЯ 11: Conversation State** — decisive решение за как се пази history. Frontend pази messages array, backend е stateless. Включва: pseudocode на chatbot-widget.js, token budget management, capping до 20 messages, кога да migrate-ваме към session DB (post-MVP).
5. **`customizations/` consistency между _template/ и реални клиенти** — Belora, Yavor, Radoslava сега имат пълна структура (`messages/`, `signs/`, `checklists/`) с `.gitkeep` placeholders, точно като в `_template/`.
6. **`tier: "professional"` placeholder премахнат** — нито от `client-info.md`, нито от `config.json`. Не се използва в build процеса. Добавена бележка че operator metadata живее в client-info.md, цени/тиери в offer документи.
7. **Typo fix** — "Pro когато staraш" → "Pro когато стартираш".

**Архитектурно следствие:** Conversation history решението (frontend, не backend) е decisive за следващите 12 месеца. Това освобождава от Supabase complexity за чатбота — Supabase остава САМО за финансовия тракер.

### v1.1 → v1.2 (peer review fixes)

**11 fixes от code review:**

1. **Encoding cleanup** — премахнати zero-width characters в "Migрации" → "Миграции", "margин" → "маржин" (на 3 места)
2. **Latinic → Cyrillic консистентност** — "CHERVENI FLAGOVE → KAPANI ZA IZBYAGVANE" → "ЧЕРВЕНИ ФЛАГОВЕ — КАПАНИ ЗА ИЗБЯГВАНЕ"; "KAK ТЕСТВАШ" → "КАК ТЕСТВАШ" (на 2 места)
3. **Typo fix** — "Phycological ownership" → "Psychological ownership"
4. **Cloudinary URL pattern поправен** — от грешен `cloudinary.com/welcomebook/belora/` към реалния `res.cloudinary.com/[CLOUD_NAME]/image/upload/clients/[client_id]/[file]`
5. **`customizations/` consistency** — всички клиенти (`_template/`, `belora/`, `yavor/`, `radoslava/`) сега имат същата подструктура с `messages/`, `signs/`, `checklists/` (празни с .gitkeep ако не се override-ват)
6. **`hero_image` и `gallery` добавени в основния config.json пример** — преди бяха документирани само в Image Storage секцията (documentation drift)
7. **`images/` папки премахнати от клиентската структура** — снимките са САМО в Cloudinary, в Git само README обяснява това
8. **`logs/` папка премахната от main folder структура** — добавена като "Note" с обяснение че е gitignored
9. **НОВА СЕКЦИЯ 6: Build System · Eleventy** — explicit избор на Eleventy с pseudocode, build команди, защо не custom script (БЛОКЕР, който беше пропуснат в v1.1)
10. **НОВА СЕКЦИЯ 10: Chatbot Knowledge Loading** — explicit pseudocode на chatbot.js + system-prompt.js, как knowledge.md става Claude API call, token limits (БЛОКЕР, който беше пропуснат в v1.1)
11. **НОВА СЕКЦИЯ 11: Промяна на chatbot поведение** + **НОВА СЕКЦИЯ 12: Multi-language strategy** — config-driven tone/restrictions, decisive решение за multi-language (един BG knowledge.md, Claude превежда автоматично), не "опция"

### v1.0 → v1.1 (10 changes)

1. Махнати конкретни цени от архитектурен документ
2. Добавени `marketing-site/` и `shared-apps/` peer директории + Three Types of Deployments
3. Добавена `shared-resources/` + Override Pattern
4. Добавена секция Staging vs Production
5. Добавена секция Image Storage
6. Добавена секция Chatbot Resilience
7. Добавена секция Backup & Disaster Recovery
8. Засилено правило "Build template when paid client"
9. Migration секцията преименувана + disclaimer
10. PDF Reference синхронизация бележка
