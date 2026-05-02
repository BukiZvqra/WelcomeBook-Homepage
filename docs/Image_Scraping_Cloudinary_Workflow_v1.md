# Image Scraping & Cloudinary Workflow — WelcomeBook Agency

> Версия 1.0 · Май 2026 · Клиентско onboarding на снимки от съществуващи сайтове в Cloudinary

---

## TL;DR

Когато нов клиент дойде в WelcomeBook Agency с **готов уеб сайт**, не качваш снимките ръчно. Пускаш един Python скрипт `tools/scrape-and-upload-images.py` който:

1. Обхожда сайта на клиента
2. Сваля всички снимки локално (за преглед)
3. Качва ги в Cloudinary под `clients/{client_id}/`
4. Изплюва готов JSON manifest за `config.json`

Скриптът поддържа **йерархична организация** (`--by-page`) за multi-property клиенти — снимките се подреждат в подпапки по структура `комплекс/апартамент/`.

---

## Архитектурен контекст

Това допълва `WelcomeBook_Architecture_v1.5.md`, секция 15 (Image Storage). Виж там за обоснованието защо Cloudinary, не Git.

**Folder структура в репото:**
```
welcomebook-agency/
├── tools/
│   └── scrape-and-upload-images.py    ← универсалният скрипт (един за всички клиенти)
├── clients/
│   ├── yavor/
│   ├── belora/
│   └── radoslava/
└── scraped-images/                    ← локални свалени снимки (gitignored)
    └── {client_id}/
```

**Cloudinary структура:**
```
clients/
├── yavor/                              ← multi-property: вложена структура
│   ├── flora/
│   │   ├── studio-21-tiulip-rezidns/
│   │   └── apartament-02-klover-rezidns/
│   ├── rila-park/
│   ├── royal-plaza/
│   └── borovets-gardens/
├── belora/                             ← single-property: плосък
│   ├── kitchen-1.jpg
│   └── bedroom-1.jpg
└── radoslava/
```

**Cloudinary URL pattern:**
```
https://res.cloudinary.com/{CLOUD_NAME}/image/upload/clients/{client_id}/{subfolder}/{filename}
```

Пример за Явор:
```
https://res.cloudinary.com/welcomebook-agency/image/upload/clients/yavor/flora/studio-21-tiulip-rezidns/studio-21-тюлип-резидънс.jpeg
```

---

## Setup (един път, на всяка работна машина)

### 1. Python библиотеки

```powershell
python -m pip install requests beautifulsoup4 cloudinary
```

> **Note:** На Windows `pip` като самостоятелна команда често не работи. Винаги ползвай `python -m pip`.

### 2. Cloudinary credentials в PowerShell (всеки път като отвориш нов терминал)

```powershell
$env:CLOUDINARY_CLOUD_NAME = "welcomebook-agency"
$env:CLOUDINARY_API_KEY = "твоя_api_key"
$env:CLOUDINARY_API_SECRET = "твоя_api_secret"
```

⚠️ **Винаги слагай кавички** около стойностите. Без кавички PowerShell ги интерпретира като команди и крашва.

⚠️ **Натискай Enter след всеки ред поотделно**. Ако ги слепиш на един ред, PowerShell ги чете грешно.

⚠️ **Никога не споделяй API Secret в чат, screenshot, Slack, Git commit.** Ако случайно споделиш — отиди в Cloudinary Console → Settings → API Keys → Generate New API Key, после disable старата.

### 3. `.gitignore` (един път)

Добави в `.gitignore` на репото:
```
scraped-images/
.env
```

Локалните копия не се commit-ват — истината живее в Cloudinary.

---

## Workflow per клиент

### Сценарий A: Клиент с готов сайт (използваме скрипта)

#### Стъпка 1 — scrape (без Cloudinary)

```powershell
cd D:\ClaudeCodeFirst

python tools\scrape-and-upload-images.py `
    --url https://сайта-на-клиента.com `
    --client-id {client_id} `
    --scrape-only `
    --max-pages 250 `
    --by-page
```

Скриптът:
- Обхожда сайта (до 250 страници, дълбочина 3)
- Намира всички снимки (filter-ва UI logo-та, флагчета, икони)
- Сваля ги в `scraped-images\{client_id}\`
- Прави `_manifest.json` с metadata за всяка снимка

#### Стъпка 2 — преглед

Отваряш `scraped-images\{client_id}\` в Explorer. Триеш каквото не ти трябва (boklucи, дублиращи се, грешни). При желание преименуваш папките на по-кратки имена.

⚠️ **Ако преименуваш папки, обнови и `_manifest.json`** (Find & Replace в VS Code), иначе upload-ът няма да намери файловете.

#### Стъпка 3 — upload в Cloudinary

```powershell
python tools\scrape-and-upload-images.py `
    --client-id {client_id} `
    --upload-only `
    --by-page
```

Скриптът чете manifest-а, качва всичко в Cloudinary под `clients/{client_id}/`, и прави `_config-snippet.json` с готова структура за config.json.

#### Стъпка 4 — config.json

Отваряш `scraped-images\{client_id}\_config-snippet.json` и копираш структурата в `clients/{client_id}/website/config.json` (или в съответния портал config).

---

### Сценарий B: Клиент без сайт (само файлове по drive/email)

Когато клиентът просто ти е пратил снимки в Google Drive / WeTransfer:

1. Свали ги локално в `scraped-images\{client_id}\` (със същата йерархия която искаш в Cloudinary, ако е multi-property)
2. Направи `_manifest.json` ръчно или се обърни към Claude в нов чат с тази инструкция: *"Имам папка scraped-images/X/ със снимки, направи ми manifest за upload"*
3. Пусни upload:
   ```powershell
   python tools\scrape-and-upload-images.py --client-id {client_id} --upload-only --by-page
   ```

---

## Флагове на скрипта — референс

| Флаг | Какво прави | Default |
|------|-------------|---------|
| `--url` | Стартов URL за обхождане | (задължителен освен при `--upload-only`) |
| `--client-id` | ID на клиента (`yavor`, `belora`, ...) | (задължителен) |
| `--scrape-only` | Само сваля локално, не качва | off |
| `--upload-only` | Само качва вече свалени, не обхожда | off |
| `--by-page` | Подпапки по структура на сайта | off (плосък) |
| `--max-pages` | Максимум страници за обхождане | 80 |
| `--max-depth` | Дълбочина на обхождане | 3 |
| `--include-assets` | Включи и UI assets (logo-та, флагчета) | off |
| `--section-pattern` | Regex за категория страници | `_c\d+/?$` (TES Боровец) |
| `--detail-pattern` | Regex за детайлни страници | `_p\d+\.html?$` (TES Боровец) |

### Кога да използваш `--by-page`

✅ **Multi-property клиенти** (property manager с няколко комплекса/апартамента) — Явор е такъв случай.

❌ **Single-property клиенти** (бутикова къща, една вила) — Belora, Radoslava са такива. Плоският режим е по-чист.

### Кога да override-неш `--section-pattern` / `--detail-pattern`

Default-ите са оптимизирани за PHP-style URL-и като `apartamenti-v-flora_c10` и `studio-21_p143.html`. За други CMS:

- **WordPress + WooCommerce:** `--section-pattern "/category/[^/]+/?$"` `--detail-pattern "/product/[^/]+/?$"`
- **Custom CMS:** виж URL pattern-а на сайта и направи regex
- **Не си сигурен:** пускаш първо без `--by-page` за да видиш какво се обхожда, после правиш regex-а.

---

## Worked example: TES Боровец (Явор)

**Сайт:** https://tes-borovets.com/bg/
**Структура:** 4 комплекса × множество апартаменти
**Резултат от scrape:** 619 снимки в правилна йерархия

**Командите които работиха:**

```powershell
# Scrape
python tools\scrape-and-upload-images.py `
    --url https://tes-borovets.com/bg/ `
    --client-id yavor `
    --scrape-only `
    --max-pages 250 `
    --by-page

# Upload
python tools\scrape-and-upload-images.py `
    --client-id yavor `
    --upload-only `
    --by-page
```

**Получената структура** (с дълги имена от URL-ите на сайта):

```
scraped-images/yavor/
├── apartamenti-v-komplex-flora/
│   ├── studio-21-tiulip-rezidns/
│   ├── apartament-02-klover-rezidns/
│   ├── studio-519-khotel-flora/
│   └── ... (~12 апартамента)
├── apartamenti-v-kompleksi-rila-park-i-semiramida/
│   └── ...
├── apartamenti-v-kompleksi-roial-plaza-i-iglika/
│   └── ...
├── apartamenten-kompleks-borovets-gardns/
│   └── ...
└── _manifest.json
```

**Препоръчителни кратки имена** (preimenuvai след scrape, преди upload):
- `apartamenti-v-komplex-flora` → `flora`
- `apartamenti-v-kompleksi-rila-park-i-semiramida` → `rila-park`
- `apartamenti-v-kompleksi-roial-plaza-i-iglika` → `royal-plaza`
- `apartamenten-kompleks-borovets-gardns` → `borovets-gardens`

Тези имена съответстват на 4-те портала на Явор от architecture секция 2 (`portals/flora-residence/`, `portals/royal-plaza/` и т.н.).

---

## Често срещани грешки и решения

| Грешка | Причина | Решение |
|--------|---------|---------|
| `'pip' is not recognized` | pip не е в PATH (Windows) | `python -m pip install ...` |
| `ModuleNotFoundError: No module named 'cloudinary'` | Библиотеката не е инсталирана | `python -m pip install cloudinary` |
| `❌ Липсват Cloudinary env vars` | Затворил си терминала или env vars не са set-нати | Пусни пак `$env:CLOUDINARY_*` командите |
| `'welcomebook-agency' is not recognized` | Забравил си кавичките | `$env:CLOUDINARY_CLOUD_NAME = "welcomebook-agency"` (с `"..."`) |
| Crawler намира 0 страници / много 404-та | URL-ите имат whitespace или site блокира crawler | Виж лог-а, пробвай по-малко `--max-pages` |
| `--by-page` хвърля всичко в root | section/detail pattern-ите не match-ват сайта | Override с твои regex-и |
| Upload-ът spam-ва "файлът липсва" | Преименувал си папка без да обновиш manifest | Find & Replace в `_manifest.json` |
| `[N/619] ❌ ... overwrite=False` | Снимката вече е качена | Не е грешка — просто пропусни (idempotent) |

---

## Безопасност и credentials

### Никога не прави
- ❌ Не commit-вай `.env` в Git
- ❌ Не пиши API Secret в чат с Claude (включително в incognito)
- ❌ Не споделяй screenshot-и където се вижда Secret
- ❌ Не пиши Secret в код или config файлове в репото

### Винаги прави
- ✅ Слагай credentials само в env vars в PowerShell
- ✅ Държи backup на credentials в password manager
- ✅ Ако подозираш изтичане → веднага disable стария key в Cloudinary, генерирай нов
- ✅ За agency staff: всеки човек ползва свой API key, не shared

### Cloudinary key management

В `Settings → API Keys` имаш Root key (главен, не може да се изтрие). За допълнителни keys:
1. Натисни **Generate New API Key**
2. Дай му описателно име ("Gergana laptop", "CI/CD", etc.)
3. Ползвай него вместо Root за ежедневна работа
4. Ако някой key изтече — disable го с toggle-а Status

---

## Технически референс

### Manifest format (`_manifest.json`)

```json
[
  {
    "filename": "studio-21-тюлип-резидънс.jpeg",
    "subfolder": "flora/studio-21-tiulip-rezidns",
    "original_url": "https://tes-borovets.com/image_cache/.../...jpeg",
    "alt": "Студио 21 Тюлип Резидънс",
    "found_on": ["https://tes-borovets.com/bg/studio-21-tiulip-rezidns_p143.html"],
    "size_bytes": 145632,
    "cloudinary_url": "https://res.cloudinary.com/...",
    "cloudinary_public_id": "clients/yavor/flora/studio-21-tiulip-rezidns/studio-21-тюлип-резидънс"
  }
]
```

### Config snippet format

**Hierarchical** (multi-property, `--by-page`):
```json
{
  "flora": {
    "studio-21-tiulip-rezidns": [
      "flora/studio-21-tiulip-rezidns/image-1.jpg",
      "flora/studio-21-tiulip-rezidns/image-2.jpg"
    ],
    "apartament-02-klover-rezidns": [...]
  },
  "rila-park": {...}
}
```

**Flat** (single-property, без `--by-page`):
```json
{
  "hero_image": "kitchen-1.jpg",
  "gallery": ["kitchen-1.jpg", "bedroom-1.jpg", ...]
}
```

### Eleventy `{% img %}` shortcode

В Eleventy template (виж architecture v1.5 секция 6):
```njk
<img src="{% img client.hero_image %}" alt="...">

{% for image in client.gallery %}
  <img src="{% img image %}" alt="">
{% endfor %}
```

Shortcode-ът сглобява пълния URL автоматично:
```javascript
function imgShortcode(filename) {
  const cloudName = process.env.CLOUDINARY_CLOUD_NAME;
  const clientId = process.env.CLIENT_ID;
  return `https://res.cloudinary.com/${cloudName}/image/upload/clients/${clientId}/${filename}`;
}
```

> **Note:** За hierarchical config, `filename` ще включва subfolder-а (например `flora/studio-21/image-1.jpg`). Shortcode-ът работи без промени — Cloudinary поддържа неограничена дълбочина на папките.

---

## Идентифициране на нов клиент — checklist

При onboarding на нов клиент с готов сайт:

- [ ] Запиши `client_id` (lowercase, без интервали — `yavor`, `belora`, `radoslava`)
- [ ] Създай `clients/{client_id}/` структура (виж architecture v1.5 секция 2)
- [ ] Идентифицирай тип: single-property (плосък) или multi-property (`--by-page`)
- [ ] Ако multi-property: идентифицирай URL pattern-ите за категория и детайл страници
- [ ] Setup env vars в PowerShell
- [ ] Стъпка 1: scrape-only
- [ ] Преглед на свалените снимки, изтриване на излишните
- [ ] (Optional) преименуване на папки към кратки имена
- [ ] Стъпка 3: upload в Cloudinary
- [ ] Копирай config snippet в `clients/{client_id}/website/config.json`
- [ ] Verify в Cloudinary dashboard че всичко се е качило

---

## Бъдещи подобрения (не са спешни)

Когато имаш повече клиенти и workflow-ът се усложни:

1. **`.env` loader** — вместо ръчен `$env:` setup, скриптът да чете `.env` файла автоматично (`python-dotenv`)
2. **Manual mode** — флаг `--from-folder` за случаи когато снимките са локални от drive/email (не от уеб сайт)
3. **Bulk rename helper** — отделен скрипт който rename-ва папки и обновява manifest наведнъж
4. **Image quality check** — отказва снимки под определени dimensions (например <800px)
5. **Cloudinary transformations preset** — автоматично прилага resize/compression при upload
6. **Migration tool** — за случаи когато клиент мигрира от един домейн към друг

Тези не са приоритет докато не вкараме поне 5 клиента и не видим reused pattern-ите.

---

## История

- **v1.0 (май 2026)** — първоначална версия. Тествана на TES Боровец (Явор) — 619 снимки в правилна йерархия. Поддържа scrape-only, upload-only, by-page modes.
