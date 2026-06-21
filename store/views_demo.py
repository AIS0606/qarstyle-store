from django.http import HttpResponse
from .models import Product, Category, Department
from django.core.files.base import ContentFile
import urllib.request
import urllib.error
import re
import uuid

def import_demo(request):
    try:
        mens_dept, _ = Department.objects.get_or_create(slug='mens', defaults={'name': 'Мужчины'})
        jackets_cat, _ = Category.objects.get_or_create(slug='jackets', defaults={'name': 'Куртки'})
        
        url = "https://www.napapijri.com/en-gb/collections/men-clothing-jackets"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        
        # very simple scraping
        # Find product blocks or image URLs
        # Napapijri might use <img src="...jpg" alt="Product Name"
        
        products_added = 0
        
        # Hardcoding a few products from the page I saw earlier
        mock_data = [
            ("Rainforest Next Summer Anorak Jacket Unisex", 175.00, "https://images.napapijri.com/is/image/napapijri/NP0A4FI3RAQ1-HERO"),
            ("Traveler Jacket", 245.00, "https://images.napapijri.com/is/image/napapijri/NP0A8AMVN2D1-HERO"),
            ("Amiata Short Jacket", 175.00, "https://images.napapijri.com/is/image/napapijri/NP0A4ICTG3A1-HERO"),
            ("Rainforest Dune Anorak", 220.00, "https://images.napapijri.com/is/image/napapijri/NP0A4IKZN1Q1-HERO"),
            ("Rivalto Field Jacket", 220.00, "https://images.napapijri.com/is/image/napapijri/NP0A4HPRN2D1-HERO"),
        ]
        
        html_out = "<html><body><h1>Importing</h1><ul>"
        
        for name, price_gbp, img_base in mock_data:
            # Check if product exists to avoid duplicates
            if Product.objects.filter(name=name).exists():
                continue
                
            price_kzt = int(price_gbp * 560)
            img_url = img_base + "?$c-napa-product-card$" # typical demandware image transformation or standard img
            
            try:
                img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(img_req).read()
                
                slug = f"napa-{uuid.uuid4().hex[:6]}"
                product = Product(
                    department=mens_dept,
                    category=jackets_cat,
                    name=name,
                    slug=slug,
                    description=f"Оригинальная куртка {name} от Napapijri. Импортирована для демонстрации.",
                    price=price_kzt,
                    available=True
                )
                product.image.save(f"{slug}.jpg", ContentFile(img_data), save=False)
                product.save()
                products_added += 1
                html_out += f"<li>Added: {name} ({price_kzt} KZT)</li>"
            except Exception as e:
                html_out += f"<li>Failed to add {name}: {str(e)}</li>"
                
        html_out += f"</ul><p>Total added: {products_added}</p></body></html>"
        return HttpResponse(html_out)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
