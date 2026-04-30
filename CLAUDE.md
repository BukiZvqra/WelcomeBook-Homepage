# CLAUDE.md — WelcomeBook Agency

## Контекст
Monorepo за WelcomeBook Agency — агенция която build-ва уебсайтове + 
портали с AI чатбот за български Airbnb/Booking хостове.

## Архитектурен документ (single source of truth)
Пълната архитектура живее в `WelcomeBook_Architecture_v1_4.md` в Project 
Knowledge на свързания Claude.ai chat.

При нужда от секция → потребителят ще копира релевантната част в prompt-а.
НЕ предполагай съдържание от документа без да го имаш в context.

## Default model
DEFAULT: claude-sonnet-4-6 за изпълнение
OPUS only за: planning, complex bugs, architecture changes

## Build phase tracker
Текущ клиент: Yavor (ТЕС Боровец) — multiproperty, 1 уебсайт + 4 портала
Текуща фаза: Phase 1 — repo setup
Следваща фаза: Phase 2 — Eleventy install + config

## Принципи
1. Един монорепо за цялата агенция
2. Eleventy (11ty) за static sites
3. Markdown за knowledge (не БД до 40+ клиента)
4. Cloudinary за снимки — НИКОГА не push в Git
5. Netlify Functions за shared chatbot backend (един за всички клиенти)
6. Branch + Preview workflow — НИКОГА direct push в main за клиентски сайт
7. Build template само когато имаш ПЛАТЕН клиент за него

## Преди промяна
- Промени в shared template (засяга всички клиенти) → Plan mode (Shift+Tab)
- Промени в client config → direct edit ОК
- Setup на нов клиент → следвай Architecture секция 8
- При несигурност → питай потребителя, не предполагай

## Какво НЕ правиш
- Не build-ваш втори website template без платен клиент
- Не push-ваш оригинални снимки в Git (Cloudinary за images)
- Не правиш custom код за първия клиент — template-ът е thin
- Не build-ваш admin panel в първите 6 месеца
- Не пишеш Cypress/Jest тестове сега — manual test преди deploy
- Не пипаш старите папки (homepage/, homepage2/, portal/, Ai chatbot Demo Test/, 
  welcomebook-videos/) без explicit инструкция от потребителя

## Стари папки в repo-то (не пипай без инструкция)
- homepage/, homepage2/ — funnel сайтове на агенцията (welcomebook.agency)
- portal/ — стар portal master template (ще се мигрира към templates/portal-master/)
- Ai chatbot Demo Test/ — chatbot прототип (ще се мигрира към backend/)
- welcomebook-videos/ — маркетинг видеа
- tools/, workflows/ — съществуващи Claude Code workflows

## Нова структура (build-ваме сега)
- marketing-site/ — за бъдеща миграция на funnel-ите
- shared-apps/financial-tracker/ — за бъдеща интеграция
- shared-resources/ — message templates, signs pack, checklists, feedback forms
- templates/ — website + portal master templates
- backend/netlify/functions/ — shared chatbot endpoint
- clients/ — per-client data (yavor/ е първият)
