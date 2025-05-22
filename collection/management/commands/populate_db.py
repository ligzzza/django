import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile

# Правильные импорты ваших моделей
from collection.models import (
    Role,
    User,
    Category,
    Theme,
    Item,
    StorageCondition
)

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Populates the database with sample data for rare coins and stamps'

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")

        # Очистка старых данных
        self._clean_data()

        # Создание ролей
        self._create_roles()

        # Создание пользователей
        admin_user = self._create_admin()
        collectors = self._create_collectors(5)

        # Создание категорий
        categories = self._create_categories()

        # Создание тематик
        themes = self._create_themes()

        # Создание предметов коллекции
        self._create_items(collectors, categories, themes, 20)

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))

    def _clean_data(self):
        """Очистка старых данных"""
        StorageCondition.objects.all().delete()
        Item.objects.all().delete()
        Theme.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()
        self.stdout.write("Cleaned existing data")

    def _create_roles(self):
        """Создание ролей"""
        Role.objects.create(name='admin')
        Role.objects.create(name='collector')
        self.stdout.write("Created roles")

    def _create_admin(self):
        """Создание администратора"""
        admin_role = Role.objects.get(name='admin')
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role=admin_role
        )
        self.stdout.write(f"Created admin user: {admin.username}")
        return admin

    def _create_collectors(self, count):
        """Создание коллекционеров"""
        collector_role = Role.objects.get(name='collector')
        collectors = []

        for i in range(count):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password='collector123',
                role=collector_role
            )
            collectors.append(user)
            self.stdout.write(f"Created collector: {user.username}")

        return collectors

    def _create_categories(self):
        """Создание категорий"""
        categories = [
            "Монеты",
            "Марки",
        ]

        created = []
        for name in categories:
            category = Category.objects.create(name=name)
            created.append(category)
            self.stdout.write(f"Created category: {category.name}")

        return created

    def _create_themes(self):
        """Создание тематик"""
        themes = [
            "Исторические личности",
            "Животные",
            "Космос",
            "Спорт",
            "Архитектура",
            "Военная тематика",
            "Юбилейные даты",
            "Флора",
            "Транспорт",
            "Искусство"
        ]

        created = []
        for name in themes:
            theme = Theme.objects.create(name=name)
            created.append(theme)
            self.stdout.write(f"Created theme: {theme.name}")

        return created

    def _create_items(self, collectors, categories, themes, count):
        """Создание предметов коллекции"""
        coin_descriptions = [
            "Редкая монета в отличном состоянии",
            "Коллекционная монета с исторической ценностью",
            "Монета с ограниченным тиражом",
            "Инвестиционная монета из драгоценного металла",
            "Памятная монета к знаменательному событию"
        ]

        stamp_descriptions = [
            "Редкий экземпляр почтовой марки",
            "Марка с типографским браком, повышающим ценность",
            "Коллекционная марка в идеальном состоянии",
            "Марка из ограниченной серии",
            "Историческая марка с высокой ценностью"
        ]

        countries = ["Россия", "СССР", "США", "Германия", "Франция", "Великобритания", "Китай", "Япония"]

        for i in range(count):
            # Выбираем случайные параметры
            collector = random.choice(collectors)
            category = random.choice(categories)

            if category.name == "Монеты":
                title = self._generate_coin_title()
                description = random.choice(coin_descriptions)
            else:
                title = self._generate_stamp_title()
                description = random.choice(stamp_descriptions)

            item = Item.objects.create(
                user=collector,
                category=category,
                title=title,
                description=description,
                country=random.choice(countries),
                year=random.randint(1800, 2023),
                condition=random.choice(['M', 'NM', 'VG', 'G', 'F']),
                estimated_value=random.uniform(100, 100000),
                photo=self._get_random_image(category.name.lower())
            )

            # Добавляем тематики
            item.themes.set(random.sample(list(themes), random.randint(1, 3)))

            # Создаем условия хранения
            self._create_storage_conditions(item)

            self.stdout.write(f"Created item: {item.title}")

    def _generate_coin_title(self):
        """Генерация названия монеты"""
        metals = ["золотая", "серебряная", "медная", "никелевая", "бронзовая"]
        types = ["рубль", "копейка", "доллар", "евро", "фунт", "динар"]
        adjectives = ["юбилейная", "памятная", "редкая", "историческая", "коллекционная"]

        return f"{random.choice(adjectives)} {random.choice(metals)} {random.choice(types)}"

    def _generate_stamp_title(self):
        """Генерация названия марки"""
        themes = ["космос", "животные", "спорт", "архитектура", "история"]
        adjectives = ["редкая", "коллекционная", "ограниченная", "памятная"]

        return f"{random.choice(adjectives)} марка на тему '{random.choice(themes)}'"

    def _get_random_image(self, item_type):
        """Получение случайного изображения (заглушка)"""
        # В реальном проекте здесь должна быть логика загрузки реальных изображений
        # Для примера используем пустое изображение
        from django.core.files.images import ImageFile
        from io import BytesIO
        from PIL import Image

        # Создаем пустое изображение
        image = Image.new('RGB', (800, 600), color=(73, 109, 137))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')

        return ImageFile(image_io, name=f"{item_type}_{fake.uuid4()}.jpg")

    def _create_storage_conditions(self, item):
        """Создание условий хранения для предмета"""
        StorageCondition.objects.create(
            item=item,
            temperature=random.uniform(18.0, 22.0),
            humidity=random.uniform(40.0, 60.0),
            last_check_date=now() - timedelta(days=random.randint(1, 30))
        )
        self.stdout.write(f"Created storage conditions for {item.title}")