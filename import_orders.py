#!/usr/bin/env python
"""
===================================================
  QarStyle — Скрипт импорта клиентов и заказов
===================================================
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Настройка Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qarstyle_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Order, OrderItem, Product

# ── Тестовые данные клиентов ──────────────────────────────────────────────────
CLIENTS = [
    {'username': 'client1', 'email': 'client1@example.com', 'first_name': 'Айнур', 'last_name': 'Сарбаев'},
    {'username': 'client2', 'email': 'client2@example.com', 'first_name': 'Фариза', 'last_name': 'Оралова'},
    {'username': 'client3', 'email': 'client3@example.com', 'first_name': 'Марат', 'last_name': 'Жакупов'},
    {'username': 'client4', 'email': 'client4@example.com', 'first_name': 'Дарья', 'last_name': 'Кульбаева'},
    {'username': 'client5', 'email': 'client5@example.com', 'first_name': 'Рамиль', 'last_name': 'Исаев'},
]

def create_clients():
    """Создание клиентов"""
    print("\n📝 Создание клиентов...")
    created_count = 0
    
    for client_data in CLIENTS:
        user, created = User.objects.get_or_create(
            username=client_data['username'],
            defaults={
                'email': client_data['email'],
                'first_name': client_data['first_name'],
                'last_name': client_data['last_name'],
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  ✅ Создан клиент: {client_data['first_name']} {client_data['last_name']}")
            created_count += 1
        else:
            print(f"  ℹ️  Клиент уже существует: {user.get_full_name()}")
    
    return created_count

def create_orders():
    """Создание заказов"""
    print("\n📦 Создание заказов...")
    
    users = User.objects.filter(username__startswith='client')
    products = Product.objects.all()
    
    if not users.exists():
        print("  ⚠️  Клиентов не найдено. Сначала создайте клиентов.")
        return 0
    
    if not products.exists():
        print("  ⚠️  Товаров не найдено. Сначала импортируйте товары.")
        return 0
    
    orders_created = 0
    statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    payment_methods = ['card', 'cash', 'kaspi']
    
    # Создание 10-15 заказов
    for i in range(12):
        user = random.choice(list(users))
        product = random.choice(list(products))
        quantity = random.randint(1, 3)
        
        # Случайная дата в последние 2 месяца
        days_ago = random.randint(1, 60)
        created_date = datetime.now() - timedelta(days=days_ago)
        
        order = Order.objects.create(
            user=user,
            payment_method=random.choice(payment_methods),
            created_at=created_date,
            updated_at=created_date,
            total_price=product.price * quantity,
        )
        
        # Добавление товара в заказ
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        
        print(f"  ✅ Заказ #{order.id}: {user.get_full_name()} - {product.name} (x{quantity})")
        orders_created += 1
    
    return orders_created

def main():
    print("\n" + "="*50)
    print("  QarStyle — Импорт клиентов и заказов")
    print("="*50)
    
    # Создание клиентов
    clients_created = create_clients()
    
    # Создание заказов
    orders_created = create_orders()
    
    print("\n" + "="*50)
    print(f"✅ Клиентов создано: {clients_created}")
    print(f"✅ Заказов создано: {orders_created}")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
