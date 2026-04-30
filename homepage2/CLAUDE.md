# CLAUDE.md — WelcomeBook Agency (Project-Local)

> Този файл важи САМО за този проект. Global правилата в `D:\ClaudeCodeFirst\CLAUDE.md` също се прилагат.

---

## 1. БИЗНЕСЪТ

**WelcomeBook Agency** — дигитална агенция за български Airbnb/Booking домакини.

**Ключов диференциатор:** фиксирана setup такса + месечен абонамент. **Никакъв процент** от приходите на домакина.

**Стратегически shift:** Welcome Book вече **НЕ Е** статичен PDF. Това е **интерактивен уеб welcome book + AI чатбот**. PDF остава само като физически premium upsell.

## 2. ПЛАТФОРМЕНА АРХИТЕКТУРА

### Guest-facing
- Уеб welcome book + AI Чатбот
- QR код
- **Public booking зона** (за потенциални гости)
- **Private post-booking зона** (WiFi, check-in кодове, чатбот — само за резервирали)

### Host-facing
- Client portal с Supabase Auth login
- Dashboard с 9-картен grid: Financial Tracker, Welcome Book, Checklists, Messages & Templates, Social Posts, Listing Optimization, Signs & Labels, Guest Feedback, Settings

**Subdomain модел:** `welcomebook.bg` → `krasi.welcomebook.bg`. Custom domain = upsell.

## 3. ПАКЕТИ И ЦЕНИ (EUR — ФИНАЛИЗИРАНИ)

| Пакет | Setup | Абонамент |
|-------|-------|-----------|
| **СТАРТ** | €149 / €249 / €349 | €29 / €55 / €79 / месец |
| **PROFESSIONAL** ⭐ | €229 / €399 / €499 | €55 / €99 / €149 / месец |
| **PREMIUM** | €349 / €549 / €749+ | €99 / €179 / €279+ / месец |

### Правила за ценообразуване

- **Никога BGN** в клиентски материали
- Динамични цени според приходи и брой имоти
- A la carte: може без конкретна услуга при редуцирана цена
- Спре ли абонаментът — спират всички услуги (нищо не остава при клиента)

### PROFESSIONAL задължителни компоненти

- AI Чатбот (основен selling point)
- Сайт с директни резервации (0% комисионна)
- Хостинг + поддръжка + минорни промени

### Алокация

| Услуга | СТАРТ | PROF | PREMIUM |
|--------|-------|------|---------|
| Message templates | ✅ | ❌ | — |
| AI Чатбот | ❌ | ✅ | ✅ |
| AI снимки | 3/setup | 3/месец | 10/месец |
| AI видео | ❌ | ❌ | 3/месец |
| Review Optimization | ❌ | ❌ | ❌ (изключено) |
| Cleaning Checklist | ❌ | ❌ | ❌ (изключено) |

## 4. SALES ФУНЕЛ

FB реклами → Безплатна консултация → Обаждане (бележки в Notion) → Анализ → Antigravity прави PPTX → Viber follow-up (1-2 дни) → Второ обаждане с презентация → Затваряне

**Колеги:**
- **Неда** — първични sales разговори
- **Antigravity** — PPTX от Notion офертите
- **Google Ads специалист** — външен

## 5. WORKFLOW ЗА ОФЕРТИ (ЗАДЪЛЖИТЕЛЕН)

1. Прочети CRM: `https://docs.google.com/document/d/1GVBJAxXVBELsWsBMiDDtKSa3yg16BjBs6JjAqjKXYy0/edit`
2. Fetch pricing page от Notion: `33adc142-082d-81be-8fed-f8fd7ba7d51e`
3. Изгради офертата в чата за review
4. Създай Notion child page под CRM записа
5. Antigravity конвертира в PPTX

### Задължителни секции

**"📎 ОБЯВИ И ОНЛАЙН ПРИСЪСТВИЕ"** (първо):
- Airbnb/Booking линкове, сайт, IG, FB, Google Maps

**"КАКВО ИЗГРАЖДАМЕ"**:
- Точен брой сайтове (обикн. 1)
- Брой Welcome Book портали (1 на имот/комплекс)
- Как работи AI Чатботът (1 чатбот на всички имоти)

### Забранено в оферти

- ❌ Review Optimization System
- ❌ Cleaning Checklist
- ❌ AI видео в Professional
- ❌ "Next Steps" секция с phone prompt
- ❌ BGN цени
- ❌ Измислени услуги извън pricing page
- ❌ Social media като bundle — винаги отделен line item

## 6. NOTION IDs

| Какво | ID |
|-------|-----|
| Main workspace | `2e6dc142-082d-8049-bf63-d08eaa320c29` |
| CRM database | `89ce3884-5b06-4794-ae7f-f9bd934218c7` |
| Main CRM parent | `33adc142-082d-814f-aaf4-fec1bc255406` |
| **Pricing reference** | `33adc142-082d-81be-8fed-f8fd7ba7d51e` |
| Offer template | `33bdc142-082d-818a-aa4b-c903cd643a60` |

### Notion правила

- Offer pages = **child pages** под CRM записа
- Нови CRM записи = `data_source_id`, не `page_id`
- Bulgarian search queries работят
- `update_content` fails silently → verify с `notion-fetch`
- `replace_content` с `allow_deleting_content: True` = надежден rewrite

## 7. ТЕХНИЧЕСКИ СТАК

### Client Portal
- Next.js + Supabase + Tailwind
- Live: `welcomebook-portal-8ee1.vercel.app`
- GitHub: `BukiZvqra/welcomebook-portal`
- Git: `kostadinpavlov17b@gmail.com`

### Financial Tracker
- Vanilla HTML/JS + Supabase
- Live: `welcomebook-tracker.netlify.app`

### Main Website
- `welcomebook.agency` (Netlify)
- FB Pixel: `1679192339343771`
- Meta Ad Account: `1275835870399890`

### Local Dev
- Path: `D:\ClaudeCodeFirst\homepage2\`
- Stable backup: `index_v1.html`
- Active: `index_v2.html`, `index.html`

### Брандинг
- Navy: `#0A0F1E`
- Amber: `#E8820C`
- Gradient край: `#F59E0B`
- Typography: Montserrat / Poppins

## 8. PPTX WORKFLOW

1. `python unpack.py`
2. Edit slide XML директно
3. `python pack.py --original`

Sources annotations от AI tools → `notesSlides` XML, не slide XML.

## 9. РЕКЛАМНИ КРЕАТИВИ — CINEMATIC FLAT LAY

- Overhead Hasselblad-style
- Warm linen background
- Golden hour side lighting
- Amber + deep navy `#0A0F1E`
- Montserrat ExtraBold
- Български текст вграден в изображението

### Nano Banana промпти

- **ВИНАГИ 1:1** (1080x1080px)
- Добавяй: `"square format 1:1 aspect ratio, 1080x1080px, Instagram/Facebook ad dimensions"`

## 10. ROADMAP

**Следващ приоритет:** Demo welcome book за реален имот (Краси / Balkanska Panorama)

**Скоро:** Google/FB OAuth (след custom domain), Direct booking Phase 1–3, Freemium upsell с locked cards

**По-нататък:** Client portal Phase 2–3, Dynamic Supabase-driven template, Access restriction за Financial Tracker

## 11. КЛЮЧОВИ УРОЦИ

- ❌ Оферти без клиентски контекст → много корекции за излишни услуги
- ❌ Никога не измисляй услуги или цени → pricing page първо
- ❌ Не създавай Notion страници преди реални данни
- ✅ Professional selling point = **AI Чатбот**, НЕ message templates
- ✅ Financial Tracker = ключов diff (няма публичен Airbnb API)
- ✅ Booking.com URL-и = JS-blocked → PDF export workaround

## 12. ЕЖЕСЕСИОННИ ЗАДАЧИ

При клиентска работа:
1. ✅ Прочети CRM Google Doc
2. ✅ Fetch pricing page
3. ✅ Провери Notion CRM
4. ❌ НЕ започвай оферта без контекст
