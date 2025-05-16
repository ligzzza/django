from django.shortcuts import render
from django.db.models import Count, Avg
from .models import Item, Transaction, Category, Theme

def index(request):
    # Получение поискового запроса
    query = request.GET.get('q', '')

    # Фильтр по поисковому запросу (по названию или описанию)
    items_qs = Item.objects.all()
    if query:
        items_qs = items_qs.filter(title__icontains=query) | items_qs.filter(description__icontains=query)

    # Последние добавленные предметы
    latest_items = items_qs.order_by('-created_at')[:5]

    # Выборка последних монет/марок (используем правильное имя поля 'name')
    coins_category = Category.objects.filter(name__icontains='монет').first()
    stamps_category = Category.objects.filter(name__icontains='марк').first()

    latest_coins = Item.objects.filter(category=coins_category).order_by('-created_at')[:5] if coins_category else []
    latest_stamps = Item.objects.filter(category=stamps_category).order_by('-created_at')[:5] if stamps_category else []

    # Статистика
    total_items = Item.objects.count()
    # Средняя стоимость по всем предметам
    avg_value = Item.objects.aggregate(Avg('estimated_value'))['estimated_value__avg'] or 0

    context = {
        'query': query,
        'latest_items': latest_items,
        'latest_coins': latest_coins,
        'latest_stamps': latest_stamps,
        'total_items': total_items,
        'average_value': avg_value,
    }
    fhbvhd
    return render(request, 'main/index.html', context)