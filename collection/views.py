from django.shortcuts import render
from .models import Category, Item
from django.db.models import Avg, Max

def index(request):
    try:
        # Получаем категории
        coins_category = Category.objects.get(name="Монеты")
        stamps_category = Category.objects.get(name="Марки")

        # Получаем последние 5 монет и марок
        latest_coins = Item.objects.filter(category=coins_category).order_by('-id')[:5]
        latest_stamps = Item.objects.filter(category=stamps_category).order_by('-id')[:5]

        # Статистика
        total_items = Item.objects.count()
        average_value = Item.objects.aggregate(Avg('estimated_value'))['estimated_value__avg'] or 0
        max_value = Item.objects.aggregate(Max('estimated_value'))['estimated_value__max'] or 0

        # Поиск
        query = request.GET.get('q', '')
        items = Item.objects.filter(title__icontains=query) if query else None

        return render(request, 'main/index.html', {
            'latest_coins': latest_coins,
            'latest_stamps': latest_stamps,
            'total_items': total_items,
            'average_value': average_value,
            'max_value': max_value,
            'query': query,
            'items': items,
            'coins_category_id': coins_category.id,
            'stamps_category_id': stamps_category.id
        })

    except Category.DoesNotExist:
        return render(request, 'main/index.html', {
            'error': 'Категории не найдены',
            'latest_coins': [],
            'latest_stamps': [],
            'total_items': 0,
            'average_value': 0,
            'max_value': 0
        })

def coins_view(request):
    coins_category = Category.objects.get(name="Монеты")
    coins = Item.objects.filter(category=coins_category).order_by('-id')
    return render(request, 'main/calendar_coins.html', {'coins': coins})

def stamps_view(request):
    stamps_category = Category.objects.get(name="Марки")
    stamps = Item.objects.filter(category=stamps_category).order_by('-id')
    return render(request, 'main/calendar_stamps.html', {'stamps': stamps})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'main/item_detail.html', {'item': item})