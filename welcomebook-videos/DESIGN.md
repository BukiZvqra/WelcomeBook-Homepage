# DESIGN.md — WelcomeBook Visual Identity

## Style Prompt

Velvet Standard с топъл балкански привкус. Тъмно морско синьо с богато злато — премиум и доверен, но не студен. Агенцията е professional done-for-you услуга за Airbnb хостове. Визията трябва да казва: "Ние сме надеждни, ние знаем занаята, ти можеш да се отпуснеш." Широко разредени ALL CAPS labels, serif headlines с тежест, generous negative space. Нищо не трябва да се чувства суетно или хаотично.

## Colors

| Role       | Hex       | Usage                              |
|------------|-----------|-------------------------------------|
| Background | `#0a1628` | Главен фон — дълбоко морско синьо   |
| Foreground | `#F5F0E8` | Основен текст — топло бяло/крем     |
| Accent     | `#C9A84C` | Злато — лога, числа, линии, акценти |
| Secondary  | `#8FA5C2` | Описания, taglines — мек синьо-сив  |
| Border     | `rgba(201,168,76,0.25)` | Фини рамки на карти    |

## Typography

- **Headlines:** Playfair Display, 700. Serif с характер — доверие и стил.
- **Labels / UI:** Inter, 400, letter-spacing: 0.2em, UPPERCASE. Чисто и прецизно.
- **Body / Desc:** Inter, 300. Леко и четимо.
- **Numbers:** Inter, 700, `font-variant-numeric: tabular-nums`. Числата да са акцент.

## Motion Rules

- Eases: `power3.out` за headlines, `expo.out` за lines/elements, `power2.out` за body text
- Entrances: y offset 20–60px, opacity 0→1, duration 0.5–0.9s
- Stagger cards: 0.25s между всяка карта
- Ambient: breathing glow (scale 1→1.15), ghost text drift (slow, none ease)
- Crossfades between scenes: 0.5–0.7s overlap, incoming scene fades from opacity 0
- Final scene: fade to opacity 0 over 0.8s

## What NOT to Do

1. Не използвай gradient text (background-clip: text) — евтино изглежда
2. Не използвай чисто `#000` или `#fff` — тинтирай към #0a1628 / #F5F0E8
3. Не използвай повече от 2 font families (Playfair + Inter)
4. Не слагай exit animations освен на последната сцена
5. Не използвай cyan-on-dark или purple-to-blue neon gradients
