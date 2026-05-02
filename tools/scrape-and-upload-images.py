#!/usr/bin/env python3
"""
scrape-and-upload-images.py — WelcomeBook Agency tool

Какво прави:
  Обхожда съществуващ клиентски сайт, сваля всички снимки, качва ги в
  Cloudinary под clients/{client_id}/. Прави manifest.json с готов gallery
  array за config.json.

Употреба:
  # Само scrape (без Cloudinary creds):
  python3 tools/scrape-and-upload-images.py \\
      --url https://tes-borovets.com/bg/ \\
      --client-id yavor \\
      --scrape-only

  # Само upload на вече свалени снимки (с Cloudinary creds):
  python3 tools/scrape-and-upload-images.py \\
      --client-id yavor \\
      --upload-only

  # Двете заедно:
  python3 tools/scrape-and-upload-images.py \\
      --url https://tes-borovets.com/bg/ \\
      --client-id yavor

Env vars (за upload):
  CLOUDINARY_CLOUD_NAME
  CLOUDINARY_API_KEY
  CLOUDINARY_API_SECRET

Output:
  ./scraped-images/{client_id}/              — свалени снимки
  ./scraped-images/{client_id}/_manifest.json — mapping + готов gallery
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup


# ───────────────────────────────────────────────────────────────────
# Конфигурация
# ───────────────────────────────────────────────────────────────────

# По default пропускаме UI assets (logo-та, флагчета, иконки)
# защото те не са content. Override-ваш с --include-assets
DEFAULT_EXCLUDE_PATTERNS = [
    r"/assets/images/",       # logo, flags, icons
    r"/static/",
    r"\.svg($|\?)",            # SVG обикновено са icons
    r"favicon",
    r"sprite",
    r"placeholder",
    r"google\.com",            # Google Play badges
    r"apple\.com",             # App Store badges
    r"facebook\.com",
    r"instagram\.com",
]

# Връщаме само тези extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

USER_AGENT = "WelcomeBookAgency-ImageScraper/1.0"

REQUEST_TIMEOUT = 20
CRAWL_DELAY = 0.15  # бъди добър гражданин на интернет


# ───────────────────────────────────────────────────────────────────
# Crawler
# ───────────────────────────────────────────────────────────────────

class SiteCrawler:
    def __init__(self, start_url, max_pages=80, max_depth=3,
                 exclude_patterns=None, include_assets=False,
                 section_pattern=None, detail_pattern=None):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.include_assets = include_assets

        patterns = list(DEFAULT_EXCLUDE_PATTERNS)
        if include_assets:
            patterns = [p for p in patterns if "/assets/" not in p]
        if exclude_patterns:
            patterns.extend(exclude_patterns)
        self.exclude_re = [re.compile(p, re.IGNORECASE) for p in patterns]

        self.section_re = re.compile(section_pattern) if section_pattern else None
        self.detail_re = re.compile(detail_pattern) if detail_pattern else None

        self.visited_pages = set()
        self.found_images = {}  # url -> {"url": ..., "alt": ..., "found_on": [...]}
        self.page_parents = {}   # url -> parent_url (за hierarchy)

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def is_same_domain(self, url):
        return urlparse(url).netloc == self.domain

    def is_excluded(self, url):
        return any(rx.search(url) for rx in self.exclude_re)

    def has_image_extension(self, url):
        path = urlparse(url).path.lower()
        # image_cache на TES Боровец няма extension, проверяваме и това
        if "/image_cache/" in path or "/uploads/" in path or "/media/" in path:
            return True
        return any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS)

    def normalize_url(self, url):
        """Премахва v=2, ?cache= и подобни query strings."""
        parsed = urlparse(url)
        # Запазваме path; query string игнорираме за dedup
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def extract_images_from_page(self, soup, page_url):
        """Извлича всички image URL-и от страница (img src, data-src, srcset, og:image)."""
        results = []

        # <img src> и lazy-load варианти
        for img in soup.find_all("img"):
            for attr in ("src", "data-src", "data-lazy-src", "data-original"):
                src = img.get(attr)
                if src:
                    abs_url = urljoin(page_url, src)
                    alt = img.get("alt", "").strip()
                    results.append((abs_url, alt))
                    break

            # srcset — взимаме най-голямата версия
            srcset = img.get("srcset") or img.get("data-srcset")
            if srcset:
                # "url 480w, url 960w" — взимаме последния (най-голям)
                last = srcset.strip().split(",")[-1].strip().split()[0]
                abs_url = urljoin(page_url, last)
                alt = img.get("alt", "").strip()
                results.append((abs_url, alt))

        # <a href="...jpg"> — често галерии слагат пълни снимки тук
        for a in soup.find_all("a", href=True):
            href = a["href"]
            abs_url = urljoin(page_url, href)
            if self.has_image_extension(abs_url):
                results.append((abs_url, a.get_text(strip=True)))

        # og:image, twitter:image
        for meta in soup.find_all("meta"):
            prop = (meta.get("property") or meta.get("name") or "").lower()
            if prop in ("og:image", "twitter:image"):
                content = meta.get("content")
                if content:
                    abs_url = urljoin(page_url, content)
                    results.append((abs_url, "og:image"))

        # CSS background-image в style="..."
        for el in soup.find_all(style=True):
            matches = re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", el["style"])
            for m in matches:
                abs_url = urljoin(page_url, m)
                results.append((abs_url, "css-bg"))

        return results

    def find_internal_links(self, soup, page_url):
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()  # ← важно: trim whitespace от raw HTML
            if not href:
                continue
            abs_url = urljoin(page_url, href)
            abs_url = abs_url.split("#")[0].strip()  # премахваме anchor + trim
            if not self.is_same_domain(abs_url):
                continue
            if self.has_image_extension(abs_url):
                continue  # изображенията не са страници
            # Пропускаме file extensions които не са страници
            path = urlparse(abs_url).path.lower()
            if any(path.endswith(ext) for ext in (".pdf", ".zip", ".doc", ".xls")):
                continue
            links.append(abs_url)
        return links

    def crawl(self):
        queue = [(self.start_url, 0, None)]  # (url, depth, parent)
        page_count = 0

        while queue and page_count < self.max_pages:
            url, depth, parent = queue.pop(0)
            if url in self.visited_pages:
                continue
            if depth > self.max_depth:
                continue

            self.visited_pages.add(url)
            self.page_parents[url] = parent
            page_count += 1
            print(f"  [{page_count}/{self.max_pages}] depth={depth}  {url}")

            try:
                resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if resp.status_code != 200:
                    print(f"      → {resp.status_code}, прескачам")
                    continue
                if "text/html" not in resp.headers.get("content-type", ""):
                    continue
            except Exception as e:
                print(f"      → грешка: {e}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # Извличаме image URL-ите
            for img_url, alt in self.extract_images_from_page(soup, url):
                if not self.is_same_domain(img_url):
                    continue
                if self.is_excluded(img_url):
                    continue
                if not self.has_image_extension(img_url):
                    continue
                normalized = self.normalize_url(img_url)
                if normalized not in self.found_images:
                    self.found_images[normalized] = {
                        "url": img_url,  # оригинален URL с query
                        "alt": alt,
                        "found_on": [url],
                    }
                else:
                    if url not in self.found_images[normalized]["found_on"]:
                        self.found_images[normalized]["found_on"].append(url)

            # Намираме нови вътрешни линкове за обхождане
            for link in self.find_internal_links(soup, url):
                if link not in self.visited_pages:
                    queue.append((link, depth + 1, url))

            time.sleep(CRAWL_DELAY)

        return self.found_images


# ───────────────────────────────────────────────────────────────────
# Downloader
# ───────────────────────────────────────────────────────────────────

def slug_from_url(url, strip_re=None):
    """Взима последния path segment, премахва pattern-a (ако има)."""
    if not url:
        return ""
    path = urlparse(url).path.rstrip("/")
    last = path.split("/")[-1] or ""
    if strip_re:
        last = strip_re.sub("", last)
    # Slugify за безопасни имена
    last = re.sub(r"[^\w\-]+", "-", last).strip("-")
    return last or ""


def derive_subfolder(found_on, page_parents, section_re, detail_re):
    """
    Решава в коя подпапка отива снимката.

    - Ако е намерена на 'detail' страница (напр. _p143.html):
        → {parent_section_slug}/{detail_slug}/
    - Ако е намерена само на 'section' страница (напр. _c10):
        → {section_slug}/
    - Иначе:
        → '' (root, тоест без подпапка)
    """
    if not detail_re and not section_re:
        return ""

    # Първо приоритизираме detail pages
    if detail_re:
        for page_url in found_on:
            if detail_re.search(page_url):
                detail_slug = slug_from_url(page_url, detail_re)
                parent_url = page_parents.get(page_url)
                if parent_url and section_re and section_re.search(parent_url):
                    section_slug = slug_from_url(parent_url, section_re)
                    return f"{section_slug}/{detail_slug}"
                return detail_slug

    # Без detail — пробваме само section
    if section_re:
        for page_url in found_on:
            if section_re.search(page_url):
                return slug_from_url(page_url, section_re)

    return ""


def make_filename(image_url, alt, used_names):
    """Генерира хубаво име за файла. Гарантирано unique в рамките на set-а."""
    parsed = urlparse(image_url)
    original_name = unquote(parsed.path.split("/")[-1])

    # Ако оригиналното име е hash (например 0e9b854ebbca...), използваме alt
    is_hash = bool(re.match(r"^[a-f0-9]{20,}", original_name))

    if is_hash and alt:
        # Slugify alt текста
        slug = re.sub(r"[^\w\s-]", "", alt.lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")[:50]
        if slug:
            # Запазваме оригиналното extension
            ext_match = re.search(r"\.(jpe?g|png|webp|gif)$", original_name, re.IGNORECASE)
            ext = ext_match.group(0) if ext_match else ".jpg"
            base_name = f"{slug}{ext}"
        else:
            base_name = original_name or "image.jpg"
    else:
        base_name = original_name or "image.jpg"

    # Гарантираме extension
    if not re.search(r"\.(jpe?g|png|webp|gif)$", base_name, re.IGNORECASE):
        # image_cache отговорите често нямат extension в URL — погадаме .jpg
        base_name += ".jpg"

    # Уникалност
    if base_name in used_names:
        # Добавяме кратък hash от URL за да го направим unique
        url_hash = hashlib.md5(image_url.encode()).hexdigest()[:6]
        name_part, ext = base_name.rsplit(".", 1)
        base_name = f"{name_part}-{url_hash}.{ext}"

    used_names.add(base_name)
    return base_name


def download_images(found_images, output_dir, page_parents=None,
                    section_re=None, detail_re=None):
    """
    Сваля снимките локално. Ако са дадени patterns, организира в подпапки.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    # Използваме separate sets-ове за уникалност в рамките на всяка папка
    used_names_per_folder = {}
    manifest = []

    by_page = bool(page_parents and (section_re or detail_re))
    mode_label = "по структура на сайта" if by_page else "плосък"
    print(f"\n📥 Свалям {len(found_images)} снимки ({mode_label}) в {output_dir}/")

    for i, (norm_url, info) in enumerate(found_images.items(), 1):
        original_url = info["url"]
        alt = info["alt"]

        try:
            resp = session.get(original_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                print(f"  [{i}/{len(found_images)}] ❌ {resp.status_code}  {original_url}")
                continue
            content = resp.content
        except Exception as e:
            print(f"  [{i}/{len(found_images)}] ❌ {e}")
            continue

        # Detect-ваме реалното extension от Content-Type ако трябва
        content_type = resp.headers.get("content-type", "").lower()
        if "image" not in content_type:
            print(f"  [{i}/{len(found_images)}] ⚠️ не е image ({content_type})")
            continue

        # Реши подпапката
        subfolder = ""
        if by_page:
            subfolder = derive_subfolder(
                info["found_on"], page_parents, section_re, detail_re
            )

        # Уникалност в рамките на подпапката (не глобално)
        used_names = used_names_per_folder.setdefault(subfolder, set())
        filename = make_filename(original_url, alt, used_names)

        target_dir = output_dir / subfolder if subfolder else output_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / filename
        filepath.write_bytes(content)

        size_kb = len(content) / 1024
        rel_display = f"{subfolder}/{filename}" if subfolder else filename
        print(f"  [{i}/{len(found_images)}] ✅ {rel_display}  ({size_kb:.0f} KB)")

        manifest.append({
            "filename": filename,
            "subfolder": subfolder,
            "original_url": original_url,
            "alt": alt,
            "found_on": info["found_on"],
            "size_bytes": len(content),
            "cloudinary_url": None,  # ще се попълни при upload
        })

        time.sleep(CRAWL_DELAY)

    return manifest


# ───────────────────────────────────────────────────────────────────
# Cloudinary upload
# ───────────────────────────────────────────────────────────────────

def upload_to_cloudinary(manifest, client_id, output_dir):
    import cloudinary
    import cloudinary.uploader

    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        print("\n❌ Липсват Cloudinary env vars:")
        print("   CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET")
        print("\n   На Windows PowerShell:")
        print('   $env:CLOUDINARY_CLOUD_NAME = "..."')
        print('   $env:CLOUDINARY_API_KEY = "..."')
        print('   $env:CLOUDINARY_API_SECRET = "..."')
        return manifest

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )

    base_folder = f"clients/{client_id}"
    print(f"\n☁️  Качвам {len(manifest)} снимки в Cloudinary → {base_folder}/")

    for i, item in enumerate(manifest, 1):
        subfolder = item.get("subfolder", "")
        # Локалният път включва подпапката
        if subfolder:
            filepath = output_dir / subfolder / item["filename"]
            target_folder = f"{base_folder}/{subfolder}"
        else:
            filepath = output_dir / item["filename"]
            target_folder = base_folder

        if not filepath.exists():
            print(f"  [{i}/{len(manifest)}] ❌ файлът липсва: {filepath}")
            continue

        # public_id без extension — Cloudinary го добавя сам
        public_id_base = item["filename"].rsplit(".", 1)[0]

        try:
            result = cloudinary.uploader.upload(
                str(filepath),
                folder=target_folder,
                public_id=public_id_base,
                overwrite=False,         # не презаписвай ако вече съществува
                resource_type="image",
                use_filename=False,
                unique_filename=False,
            )
            item["cloudinary_url"] = result["secure_url"]
            item["cloudinary_public_id"] = result["public_id"]
            display = f"{subfolder}/{item['filename']}" if subfolder else item["filename"]
            print(f"  [{i}/{len(manifest)}] ✅ {display}")
        except Exception as e:
            print(f"  [{i}/{len(manifest)}] ❌ {item['filename']}: {e}")

    return manifest


# ───────────────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scrape клиентски сайт + качи снимки в Cloudinary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--url", help="Start URL за обхождане")
    parser.add_argument("--client-id", required=True,
                        help="Идентификатор на клиента (yavor, belora, и т.н.)")
    parser.add_argument("--output-dir", default="./scraped-images",
                        help="Локална папка за свалени снимки (default: ./scraped-images)")
    parser.add_argument("--max-pages", type=int, default=80,
                        help="Максимум брой страници за обхождане (default: 80)")
    parser.add_argument("--max-depth", type=int, default=3,
                        help="Максимална дълбочина на обхождане (default: 3)")
    parser.add_argument("--include-assets", action="store_true",
                        help="Включи и UI assets (logo-та, флагчета). По default ги пропускаме.")
    parser.add_argument("--scrape-only", action="store_true",
                        help="Само сваля снимките локално, не качва в Cloudinary")
    parser.add_argument("--upload-only", action="store_true",
                        help="Само качва вече свалени снимки. URL не е нужен.")
    parser.add_argument("--by-page", action="store_true",
                        help="Организирай снимките в подпапки по структура на сайта "
                             "(section/detail). За TES Боровец = комплекс/апартамент.")
    parser.add_argument("--section-pattern", default=r"_c\d+/?$",
                        help="Regex за 'section' страници (default: '_c\\d+/?$' — TES Боровец)")
    parser.add_argument("--detail-pattern", default=r"_p\d+\.html?$",
                        help="Regex за 'detail' страници (default: '_p\\d+\\.html?$' — TES Боровец)")
    args = parser.parse_args()

    if args.upload_only and args.scrape_only:
        sys.exit("❌ --scrape-only и --upload-only взаимно се изключват")

    if not args.upload_only and not args.url:
        sys.exit("❌ --url е задължителен (освен ако не е --upload-only)")

    output_dir = Path(args.output_dir) / args.client_id
    manifest_path = output_dir / "_manifest.json"

    # Compile patterns ако e by-page mode
    section_re = re.compile(args.section_pattern) if args.by_page else None
    detail_re = re.compile(args.detail_pattern) if args.by_page else None

    # ── SCRAPE FAZA ────────────────────────────────────────────────
    if not args.upload_only:
        print(f"🌐 Обхождам {args.url}")
        print(f"   client_id = {args.client_id}")
        print(f"   max_pages = {args.max_pages}, max_depth = {args.max_depth}")
        if args.by_page:
            print(f"   организация = по структура на сайта (--by-page)")
            print(f"     section pattern = {args.section_pattern}")
            print(f"     detail pattern  = {args.detail_pattern}")
        print()

        crawler = SiteCrawler(
            start_url=args.url,
            max_pages=args.max_pages,
            max_depth=args.max_depth,
            include_assets=args.include_assets,
            section_pattern=args.section_pattern if args.by_page else None,
            detail_pattern=args.detail_pattern if args.by_page else None,
        )
        found = crawler.crawl()

        print(f"\n📊 Намерени уникални снимки: {len(found)}")
        print(f"   Обходени страници: {len(crawler.visited_pages)}")

        manifest = download_images(
            found, output_dir,
            page_parents=crawler.page_parents if args.by_page else None,
            section_re=section_re,
            detail_re=detail_re,
        )

        # Записваме manifest веднага след scrape (за да не загубим работа при срив)
        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Manifest запазен: {manifest_path}")
    else:
        # Upload-only — четем съществуващия manifest
        if not manifest_path.exists():
            sys.exit(f"❌ Не намирам {manifest_path}. Първо пусни --scrape-only.")
        with manifest_path.open(encoding="utf-8") as f:
            manifest = json.load(f)
        print(f"📂 Прочетен manifest с {len(manifest)} снимки")

    # ── UPLOAD FAZA ────────────────────────────────────────────────
    if not args.scrape_only:
        manifest = upload_to_cloudinary(manifest, args.client_id, output_dir)
        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Manifest обновен с Cloudinary URLs: {manifest_path}")

        # Generate config snippet — flat или hierarchical
        uploaded = [m for m in manifest if m.get("cloudinary_url")]
        if uploaded:
            has_subfolders = any(m.get("subfolder") for m in uploaded)

            if has_subfolders:
                # Hierarchical: { section: { detail: [filenames] } }
                hierarchy = {}
                for m in uploaded:
                    sub = m.get("subfolder", "")
                    parts = sub.split("/", 1) if sub else ("_general", "")
                    section = parts[0] if parts and parts[0] else "_general"
                    detail = parts[1] if len(parts) > 1 and parts[1] else "_main"
                    hierarchy.setdefault(section, {}).setdefault(detail, []).append(
                        f"{sub}/{m['filename']}" if sub else m["filename"]
                    )
                snippet = hierarchy
            else:
                # Flat (стария формат)
                filenames = [m["filename"] for m in uploaded]
                snippet = {
                    "hero_image": filenames[0],
                    "gallery": filenames,
                }

            snippet_path = output_dir / "_config-snippet.json"
            with snippet_path.open("w", encoding="utf-8") as f:
                json.dump(snippet, f, indent=2, ensure_ascii=False)
            print(f"📋 Готов config.json snippet: {snippet_path}")

    print("\n✅ Готово.")


if __name__ == "__main__":
    main()
