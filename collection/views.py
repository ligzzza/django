from django.shortcuts import render, get_object_or_404
from collection.models import Category, Item


def index(request):
    try:
        # Получаем ID категории, а не название
        coins_category = Category.objects.get(name="Монеты")
        stamps_category = Category.objects.get(name="Марки")

        coins = Item.objects.filter(category=coins_category)[:5]
        stamps = Item.objects.filter(category=stamps_category)[:5]

        return render(request, 'index.html', {
            'coins': coins,
            'stamps': stamps,
            'coins_category_id': coins_category.id,
            'stamps_category_id': stamps_category.id
        })
    except Category.DoesNotExist:
        # Обработка случая, когда категории не найдены
        return render(request, 'index.html', {
            'error': 'Категории не найдены'
        })
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'collection/item_detail.html', {'item': item})