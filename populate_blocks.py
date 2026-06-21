import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qarstyle_project.settings')
django.setup()

from store.models import Block, BlockItem

# Hero Block
Block.objects.create(
    type='hero',
    order=1,
    title='Желаю вам пышного* лета!',
    subtitle='Коллекция QarStyle',
    button_text='МАГАЗИН ДЛЯ МУЖЧИН',
    button_link='/catalog/?department=mens',
    button_text_secondary='МАГАЗИН ЖЕНСКОЙ ОДЕЖДЫ',
    button_link_secondary='/catalog/?department=womens',
    is_active=True
)

# Pills
b2 = Block.objects.create(
    type='category_pills',
    order=2,
    is_active=True
)
BlockItem.objects.create(block=b2, title='Новинка для мужчин', link='/catalog/?department=mens', order=1)
BlockItem.objects.create(block=b2, title='Новинка для женщин', link='/catalog/?department=womens', order=2)
BlockItem.objects.create(block=b2, title='Новое для детей', link='/catalog/?department=kids', order=3)

# Two Column
Block.objects.create(
    type='two_column',
    order=3,
    title='Верхняя одежда для него',
    button_text='МАГАЗИН ДЛЯ МУЖЧИН',
    button_link='/catalog/?department=mens',
    title_secondary='Верхняя одежда для нее',
    button_text_secondary='МАГАЗИН ЖЕНСКОЙ ОДЕЖДЫ',
    button_link_secondary='/catalog/?department=womens',
    is_active=True
)

# Banner CTA
Block.objects.create(
    type='banner_cta',
    order=4,
    title='Открыто для всех.',
    subtitle='Представляем коллекцию Circular Collection — полный набор снаряжения для активного отдыха, созданный из переработанных материалов, который прослужит долго и подойдет человеку для любого приключения.',
    button_text='Купить коллекцию',
    button_link='/catalog/',
    is_active=True
)

# Product Grid
Block.objects.create(
    type='product_grid',
    order=5,
    title='ДЕМИСЕЗОННЫЕ КУРТКИ',
    button_text='В каталог →',
    button_link='/catalog/',
    is_active=True
)

print("Blocks populated successfully!")
