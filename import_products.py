#!/usr/bin/env python
"""
===================================================
  QarStyle — Скрипт импорта товаров из CSV
===================================================
Запуск:
  .venv/bin/python import_products.py

Файлы:
  import_products/products.csv   — данные товаров
  import_products/images/        — все фотографии товаров

"""

import os
import sys
import csv
import shutil
import django

# Настройка Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qarstyle_project.settings')
django.setup()

from store.models import (
    Product, Category, Department, Size, Color,
    ProductVariant, ProductImage
)
from django.core.files import File

# ── Пути ──────────────────────────────────────────────────────────────────────
CSV_FILE   = os.path.join(BASE_DIR, 'import_products', 'products.csv')
IMAGES_DIR = os.path.join(BASE_DIR, 'import_products', 'images')
MEDIA_DIR  = os.path.join(BASE_DIR, 'media', 'products')
os.makedirs(MEDIA_DIR, exist_ok=True)

# ── Вспомогательные функции ───────────────────────────────────────────────────

def get_or_create_color(name: str, hex_code: str) -> Color:
    name = name.strip()
    hex_code = hex_code.strip()
    color, created = Color.objects.get_or_create(
        name=name,
        defaults={'hex_code': hex_code}
    )
    if created:
        print(f"  🎨 Создан цвет: {name} ({hex_code})")
    return color


def get_or_create_size(name: str) -> Size:
    name = name.strip().upper()
    size, created = Size.objects.get_or_create(name=name)
    if created:
        print(f"  📏 Создан размер: {name}")
    return size


def copy_image_to_media(filename: str) -> str | None:
    """Копирует файл из import_products/images/ в media/products/ и возвращает относительный путь."""
    src = os.path.join(IMAGES_DIR, filename.strip())
    if not os.path.exists(src):
        print(f"  ⚠️  Файл не найден: {filename} (пропускаем)")
        return None
    dst = os.path.join(MEDIA_DIR, filename.strip())
    shutil.copy2(src, dst)
    return f"products/{filename.strip()}"


# ── Основной импорт ───────────────────────────────────────────────────────────

def import_products():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Файл не найден: {CSV_FILE}")
        return

    created_count  = 0
    skipped_count  = 0

    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"\n📦 Найдено строк в CSV: {len(rows)}\n{'─'*50}")

    for row in rows:
        name = row['name'].strip()

        # ── Проверка дубликата ─────────────────────────────────────────────
        if Product.objects.filter(name=name).exists():
            print(f"⏭️  Уже существует: {name}")
            skipped_count += 1
            continue

        print(f"\n➕ Добавляю: {name}")

        # ── Отдел ─────────────────────────────────────────────────────────
        dept_slug = row['department'].strip().lower()
        try:
            department = Department.objects.get(slug=dept_slug)
        except Department.DoesNotExist:
            department, _ = Department.objects.get_or_create(
                slug=dept_slug, defaults={'name': dept_slug}
            )
            print(f"  🏬 Создан отдел: {dept_slug}")

        # ── Категория ──────────────────────────────────────────────────────
        cat_slug = row['category'].strip().lower()
        try:
            category = Category.objects.get(slug=cat_slug)
        except Category.DoesNotExist:
            # Если категории нет — создаём с понятным названием
            cat_names = {
                'jackets':      'Куртки',
                'aksessuary':   'Аксессуары',
                'bezrukavka':   'Безрукавка',
                'pants':        'Брюки',
                'sweaters':     'Свитеры',
                'tshirts':      'Футболки',
                'shoes':        'Обувь',
                'bags':         'Сумки',
            }
            human_name = cat_names.get(cat_slug, cat_slug.capitalize())
            category, _ = Category.objects.get_or_create(
                slug=cat_slug, defaults={'name': human_name}
            )
            print(f"  📂 Создана категория: {human_name}")

        # ── Главное изображение ────────────────────────────────────────────
        main_image_rel = None
        main_image_file = row.get('main_image', '').strip()
        if main_image_file:
            main_image_rel = copy_image_to_media(main_image_file)

        # ── Создание товара ────────────────────────────────────────────────
        product = Product(
            name        = name,
            department  = department,
            category    = category,
            price       = int(str(row['price']).replace(' ', '').replace(',', '')),
            description = row.get('description', '').strip(),
            available   = True,
            is_sale     = row.get('is_sale', 'no').strip().lower() in ('yes', 'да', '1', 'true'),
            is_resale   = row.get('is_resale', 'no').strip().lower() in ('yes', 'да', '1', 'true'),
        )
        if main_image_rel:
            product.image = main_image_rel
        product.save()
        print(f"  ✅ Товар сохранён (id={product.id})")

        # ── Цвета ──────────────────────────────────────────────────────────
        # Формат: "Blue:#1A3A6E|Black:#000000"
        color_objects = {}  # name -> Color instance
        colors_raw = row.get('colors', '').strip()
        if colors_raw:
            for part in colors_raw.split('|'):
                part = part.strip()
                if ':' in part:
                    cname, chex = part.split(':', 1)
                    color_obj = get_or_create_color(cname, chex)
                    color_objects[cname.strip()] = color_obj

        # ── Галерея (дополнительные фото) ──────────────────────────────────
        # Формат: "Blue:jacket_blue_1.jpg,jacket_blue_2.jpg|Black:jacket_black_1.jpg"
        gallery_raw = row.get('gallery_images', '').strip()
        if gallery_raw:
            for part in gallery_raw.split('|'):
                part = part.strip()
                if ':' in part:
                    cname, filenames = part.split(':', 1)
                    cname = cname.strip()
                    color_for_gallery = color_objects.get(cname)
                    for fname in filenames.split(','):
                        fname = fname.strip()
                        if fname:
                            rel = copy_image_to_media(fname)
                            if rel:
                                ProductImage.objects.create(
                                    product=product,
                                    color=color_for_gallery,
                                    image=rel
                                )
                                print(f"  🖼️  Галерея: {fname} [{cname}]")

        # ── Варианты (размеры × цвета) ─────────────────────────────────────
        # Формат: "XS:2|S:3|M:5"  (размер:количество)
        sizes_raw = row.get('sizes_stock', '').strip()
        if sizes_raw:
            # Берём первый цвет по умолчанию (или None если нет цветов)
            default_color = list(color_objects.values())[0] if color_objects else None
            for part in sizes_raw.split('|'):
                part = part.strip()
                if ':' in part:
                    sname, stock_str = part.split(':', 1)
                    size_obj = get_or_create_size(sname)
                    stock    = int(stock_str.strip()) if stock_str.strip().isdigit() else 0
                    ProductVariant.objects.create(
                        product=product,
                        size=size_obj,
                        color=default_color,
                        stock=stock
                    )
                    print(f"  📏 Вариант: {size_obj.name} / {default_color.name if default_color else '—'} / stock={stock}")

        created_count += 1

    # ── Итог ──────────────────────────────────────────────────────────────────
    print(f"\n{'═'*50}")
    print(f"✅ Добавлено товаров: {created_count}")
    print(f"⏭️  Пропущено (уже есть): {skipped_count}")
    print(f"{'═'*50}\n")


if __name__ == '__main__':
    import_products()
