import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qarstyle_project.settings')
django.setup()
from django.template.loader import render_to_string
from store.models import Product, Category, Department, Size, Color

# Fake request and context
categories = Category.objects.all()
print("Categories count:", categories.count())
for c in categories:
    print(c.name)
