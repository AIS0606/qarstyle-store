import uuid
import glob
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product, Category, Department

class Command(BaseCommand):
    help = 'Imports demo products from Napapijri using local placeholder image'

    def handle(self, *args, **options):
        self.stdout.write('Starting import...')
        
        mens_dept, _ = Department.objects.get_or_create(slug='mens', defaults={'name': 'Мужчины'})
        jackets_cat, _ = Category.objects.get_or_create(slug='jackets', defaults={'name': 'Куртки'})

        mock_data = [
            ("Rainforest Next Summer Anorak Jacket", 175.00),
            ("Traveler Jacket", 245.00),
            ("Amiata Short Jacket", 175.00),
            ("Rainforest Dune Anorak", 220.00),
            ("Rivalto Field Jacket", 220.00),
        ]

        # Find the placeholder image generated earlier
        img_paths = glob.glob('/Users/ais/.gemini/antigravity/brain/0c220d32-5ddb-4342-8fe5-d5ca70fe29d9/demo_jacket_1_*.png')
        if not img_paths:
            self.stdout.write(self.style.ERROR('Error: Local placeholder image not found. Please ensure it exists.'))
            return
            
        with open(img_paths[0], 'rb') as f:
            img_data = f.read()

        added = 0
        for name, price_gbp in mock_data:
            if Product.objects.filter(name=name).exists():
                self.stdout.write(f'Product "{name}" already exists, skipping.')
                continue

            price_kzt = int(price_gbp * 560)
            
            try:
                product = Product(
                    department=mens_dept,
                    category=jackets_cat,
                    name=name,
                    description=f"Оригинальная куртка {name} от Napapijri. Импортирована временно для демонстрации.",
                    price=Decimal(price_kzt),
                    available=True
                )
                
                slug = f"napa-{uuid.uuid4().hex[:6]}"
                product.image.save(f"{slug}.png", ContentFile(img_data), save=False)
                product.save()
                
                added += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully added {name} ({price_kzt} KZT)'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to add {name}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Done! Added {added} products.'))
