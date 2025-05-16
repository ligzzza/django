import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from collection.models import Role, User, Category, Theme, Item, StorageCondition, Transaction
from django.utils import timezone
import random
from decimal import Decimal


# Удаляем транзакции, связанные с пользователями
Transaction.objects.all().delete()

# Удаляем предметы, связанные с пользователями
Item.objects.all().delete()

# Теперь удаляем пользователей
User.objects.all().delete()

# После этого можно удалить роли и остальные таблицы
Role.objects.all().delete()
Category.objects.all().delete()
Theme.objects.all().delete()
StorageCondition.objects.all().delete()

# Создание ролей
roles = []
role_names = ['collector', 'admin']
for name in role_names:
    role, created = Role.objects.get_or_create(name=name)
    roles.append(role)

# Создаем категории 'монета' и 'марка'
coins_category, _ = Category.objects.get_or_create(name='монета')
stamps_category, _ = Category.objects.get_or_create(name='марка')

categories = [coins_category, stamps_category]

# Создание тематик
themes = []
theme_names = [f"Тема {i+1}" for i in range(10)]
for name in theme_names:
    theme, created = Theme.objects.get_or_create(name=name)
    themes.append(theme)

# Создание пользователей
users = []
for i in range(10):
    username = f"user{i+1}"
    email = f"user{i+1}@example.com"
    role = random.choice(roles)
    user = User.objects.create_user(
        username=username,
        email=email,
        password='password123',
        role=role
    )
    users.append(user)

import datetime

# Создаем предметы, все связанные с 'монета' или 'марка'
for i in range(10):
    user = random.choice(users)
    category = random.choice(categories)  # выбираем 'монета' или 'марка'
    title = f"Предмет {i+1}"
    description = f"Описание предмета {i+1}"
    country = f"Страна {i+1}"
    year = 2000 + i
    condition = random.choice([choice[0] for choice in Item.CONDITION_CHOICES])
    estimated_value = Decimal(f"{random.uniform(100, 1000):.2f}")
    photo_path = 'prog/1992_g_30_k_standarty_prostaja_bumaga_chistye_ne_gashenye_4_51.jpg'  # убедитесь, что файл существует

    item = Item.objects.create(
        user=user,
        category=category,
        title=title,
        description=description,
        country=country,
        year=year,
        condition=condition,
        estimated_value=estimated_value,
        photo=photo_path
    )
    # Привязка тем (можете оставить или рандом)
    item.themes.set([random.choice(themes)])
    item.save()

# Создаем условия хранения
for item in Item.objects.all():
    StorageCondition.objects.create(
        item=item,
        temperature=Decimal(f"{random.uniform(15, 25):.2f}"),
        humidity=Decimal(f"{random.uniform(30, 70):.2f}"),
        last_check_date=timezone.now() - datetime.timedelta(days=random.randint(0, 365))
    )

# Создаем транзакции
for i in range(10):
    item = random.choice(Item.objects.all())
    buyer = random.choice(users)
    seller = random.choice([u for u in users if u != buyer])
    price = Decimal(f"{random.uniform(50, 2000):.2f}")
    Transaction.objects.create(
        item=item,
        buyer=buyer,
        seller=seller,
        price=price,
        transaction_date=timezone.now() - datetime.timedelta(days=random.randint(0, 365)),
        notes=f"Примечание к сделке {i+1}"
    )