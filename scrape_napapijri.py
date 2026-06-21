import os
import sys

# Set up Django
sys.path.append('/Users/ais/Desktop/Новая папка')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qarstyle_project.settings')
import django
django.setup()

from store.models import Product, Category, Department
from django.core.files.base import ContentFile
import requests
from bs4 import BeautifulSoup
import uuid
from decimal import Decimal

# Ensure Department and Category exist
mens_dept, _ = Department.objects.get_or_create(slug='mens', defaults={'name': 'Мужчины'})
jackets_cat, _ = Category.objects.get_or_create(slug='jackets', defaults={'name': 'Куртки', 'department': mens_dept})
mens_dept.categories.add(jackets_cat)

url = "https://www.napapijri.com/en-gb/collections/men-clothing-jackets"
print(f"Fetching {url}...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')

count = 0
# The products are usually in <li> or <div> with class product-grid-item or similar, let's just find <a> tags wrapping images
# Many shopify/demandware sites use 'product-tile' or similar.
for tile in soup.find_all(class_=lambda x: x and 'product' in x.lower() and ('tile' in x.lower() or 'card' in x.lower() or 'item' in x.lower())):
    if count >= 12:
        break
    try:
        # Get title
        title_elem = tile.find(class_=lambda x: x and 'title' in x.lower() or 'name' in x.lower())
        if not title_elem:
            # try to find it in the link
            a_tags = tile.find_all('a')
            for a in a_tags:
                if a.text and len(a.text.strip()) > 5:
                    title_elem = a
                    break
        
        if not title_elem:
            continue
            
        title = title_elem.text.strip()
        if not title:
            continue
            
        # Get image
        img_elem = tile.find('img')
        if not img_elem:
            continue
        
        img_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('srcset')
        if not img_url:
            continue
            
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = 'https://www.napapijri.com' + img_url
            
        # Get price
        price_elem = tile.find(class_=lambda x: x and 'price' in x.lower())
        price_val = 150.00
        if price_elem:
            text = price_elem.text.strip()
            # Extract digits
            digits = ''.join(c for c in text if c.isdigit() or c == '.')
            if digits:
                try:
                    price_val = float(digits)
                except:
                    pass
                    
        # Convert to KZT approx (1 GBP = 560 KZT)
        price_kzt = int(price_val * 560)
        
        print(f"Found: {title} | {price_kzt} KZT | {img_url[:50]}...")
        
        # Download image
        img_resp = requests.get(img_url, headers=headers)
        if img_resp.status_code == 200:
            # Create product
            slug = f"napapijri-{uuid.uuid4().hex[:8]}"
            product = Product(
                category=jackets_cat,
                name=title,
                slug=slug,
                description="Оригинальная куртка Napapijri, импортирована для демонстрации.",
                price=Decimal(price_kzt),
                available=True
            )
            # Save image
            file_name = f"{slug}.jpg"
            product.image.save(file_name, ContentFile(img_resp.content), save=False)
            product.save()
            count += 1
            print(f"-> Saved product {product.id}")
            
    except Exception as e:
        print(f"Error processing tile: {e}")

print(f"Successfully imported {count} products!")
