import re

with open('store/admin_views.py', 'r') as f:
    content = f.read()

# We want to replace everything from "def admin_blocks_list(request):" to "def admin_settings(request):"
start_str = "def admin_blocks_list(request):"
end_str = "def admin_settings(request):"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_views = """def admin_blocks_list(request):
    from .models import Block
    blocks = Block.objects.all().order_by('order')
    return render(request, 'admin/blocks_list.html', {'blocks': blocks, 'types': Block.TYPE_CHOICES})

@staff_member_required
def api_block_get(request, block_id):
    from .models import Block
    block = get_object_or_404(Block, id=block_id)
    data = {
        'id': block.id,
        'type': block.type,
        'is_active': block.is_active,
        'title': block.title,
        'subtitle': block.subtitle,
        'button_text': block.button_text,
        'button_link': block.button_link,
        'title_secondary': block.title_secondary,
        'subtitle_secondary': block.subtitle_secondary,
        'button_text_secondary': block.button_text_secondary,
        'button_link_secondary': block.button_link_secondary,
        'image_main_url': block.image_main.url if block.image_main else None,
        'image_secondary_url': block.image_secondary.url if block.image_secondary else None,
        'items': [{
            'id': item.id,
            'title': item.title,
            'subtitle': item.subtitle,
            'link': item.link,
            'order': item.order,
            'image_url': item.image.url if item.image else None
        } for item in block.items.all().order_by('order')]
    }
    return JsonResponse({'status': 'ok', 'block': data})

@staff_member_required
def api_block_save(request, block_id):
    from .models import Block
    block = get_object_or_404(Block, id=block_id)
    if request.method == 'POST':
        block.type = request.POST.get('type', block.type)
        block.title = request.POST.get('title', '')
        block.subtitle = request.POST.get('subtitle', '')
        block.button_text = request.POST.get('button_text', '')
        block.button_link = request.POST.get('button_link', '')
        block.title_secondary = request.POST.get('title_secondary', '')
        block.subtitle_secondary = request.POST.get('subtitle_secondary', '')
        block.button_text_secondary = request.POST.get('button_text_secondary', '')
        block.button_link_secondary = request.POST.get('button_link_secondary', '')
        
        is_active_val = request.POST.get('is_active')
        if is_active_val is not None:
            block.is_active = is_active_val == 'true'
            
        if 'image_main' in request.FILES:
            block.image_main = request.FILES['image_main']
        if 'image_secondary' in request.FILES:
            block.image_secondary = request.FILES['image_secondary']
            
        block.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_block_add(request):
    from .models import Block
    if request.method == 'POST':
        type = request.POST.get('type', 'hero')
        order = int(request.POST.get('order', Block.objects.count() + 1))
        # Shift blocks down if inserting
        Block.objects.filter(order__gte=order).update(order=models.F('order') + 1)
        
        block = Block.objects.create(type=type, order=order, is_active=True, title="Новый блок")
        return JsonResponse({'status': 'ok', 'block_id': block.id})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_block_delete(request, block_id):
    from .models import Block
    if request.method == 'POST':
        block = get_object_or_404(Block, id=block_id)
        block.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
@csrf_exempt
def api_block_reorder(request):
    from .models import Block
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        order_list = data.get('order', [])
        for index, block_id in enumerate(order_list):
            Block.objects.filter(id=block_id).update(order=index)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_blockitem_add(request, block_id):
    from .models import Block, BlockItem
    if request.method == 'POST':
        block = get_object_or_404(Block, id=block_id)
        last_order = block.items.count()
        item = BlockItem.objects.create(block=block, title="Новая карточка", order=last_order+1)
        return JsonResponse({'status': 'ok', 'item_id': item.id})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_blockitem_save(request, item_id):
    from .models import BlockItem
    item = get_object_or_404(BlockItem, id=item_id)
    if request.method == 'POST':
        item.title = request.POST.get('title', '')
        item.subtitle = request.POST.get('subtitle', '')
        item.link = request.POST.get('link', '')
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_blockitem_delete(request, item_id):
    from .models import BlockItem
    if request.method == 'POST':
        item = get_object_or_404(BlockItem, id=item_id)
        item.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
@csrf_exempt
def api_blockitem_reorder(request, block_id):
    from .models import BlockItem
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        order_list = data.get('order', [])
        for index, item_id in enumerate(order_list):
            BlockItem.objects.filter(id=item_id, block_id=block_id).update(order=index)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
"""
    
    # We want to replace everything including the decorators before admin_blocks_list
    # The start_str might not include @staff_member_required.
    # Let's just use slicing
    
    before = content[:start_idx]
    after = content[end_idx:]
    
    with open('store/admin_views.py', 'w') as f:
        f.write(before + new_views + after)
    print("Replaced admin_views block section")
