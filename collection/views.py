from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .forms import ItemForm
from .models import Category, Item
from django.db.models import Avg, Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'GET':
        form = ItemForm(instance=item)
        context = {'form': form, 'title': 'Редактировать предмет'}
        return render(request, 'main/edit_form.html', context)

    elif request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('main/items_list')
    # Можно сделать страницу подтверждения, или сразу удалять
    return render(request, 'main/item_confirm_delete.html', {'item': item})