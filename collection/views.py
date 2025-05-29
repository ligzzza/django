from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .forms import ItemForm
from .models import Category, Item
from django.db.models import Avg, Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

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

        favorite_ids = request.session.get('favorites', [])

        # Получаем предметы, которые в избранном (по id)
        favorite_items = Item.objects.filter(id__in=favorite_ids)

        # Поиск
        query = request.GET.get('q', '')
        items = Item.objects.filter(title__icontains=query) if query else Item.objects.all()

        return render(request, 'main/index.html', {
            'latest_coins': latest_coins,
            'latest_stamps': latest_stamps,
            'total_items': total_items,
            'average_value': average_value,
            'max_value': max_value,
            'query': query,
            'items': items,
            'coins_category_id': coins_category.id,
            'stamps_category_id': stamps_category.id,
            'favorite_ids': favorite_ids,
            'favorite_items': favorite_items,
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
    try:
        coins_category = Category.objects.get(name="Монеты")
        coins = Item.objects.filter(category=coins_category).order_by('-id')
    except Category.DoesNotExist:
        coins = []

    return render(request, 'main/calendar_coins.html', {'items': coins})

def stamps_view(request):
    try:
        stamps_category = Category.objects.get(name="Марки")
        stamps = Item.objects.filter(category=stamps_category).order_by('-id')
    except Category.DoesNotExist:
        stamps = []

    return render(request, 'main/calendar_stamps.html', {'items': stamps})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'main/item_detail.html', {'item': item})

def items_list(request):
    items = Item.objects.all()
    return render(request, 'main/items_list.html', {'items': items})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item   # или ваша модель

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные успешно добавлены!")  # сообщение для toast
            return redirect('item_create')  # перенаправление на ту же страницу
    else:
        form = ItemForm()
    return render(request, 'main/item_form.html', {'form': form, 'title': 'Создать новый элемент'})

def item_edit(request, pk):
    item = get_object_or_404(Item, id=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ItemForm(instance=item)
        return render(request, 'main/edit_form.html', {'form': form, 'item': item})


def item_delete(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        messages.error(request, "Предмет не найден.")
        return redirect(request.META.get('HTTP_REFERER', 'items_list'))

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Предмет успешно удалён.")
        return redirect(request.META.get('HTTP_REFERER', 'items_list'))

    return render(request, 'main/item_form.html', {'item': item})


def toggle_favorite(request, item_id):
    if request.method == "POST":
        favorites = request.session.get('favorites', [])
        if item_id in favorites:
            favorites.remove(item_id)
        else:
            favorites.append(item_id)
        request.session['favorites'] = favorites
        request.session.modified = True
    return redirect('index')



