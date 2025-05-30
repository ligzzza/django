# Generated by Django 5.2 on 2025-05-02 21:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('collector', 'Коллекционер'), ('admin', 'Администратор')], max_length=50, verbose_name='Название роли')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название тематики')),
            ],
            options={
                'verbose_name': 'Тематика',
                'verbose_name_plural': 'Тематики',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection.role', verbose_name='Роль')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('country', models.CharField(max_length=100, verbose_name='Страна происхождения')),
                ('year', models.IntegerField(verbose_name='Год создания')),
                ('condition', models.CharField(choices=[('M', 'Идеальное'), ('NM', 'Почти идеальное'), ('VG', 'Очень хорошее'), ('G', 'Хорошее'), ('F', 'Удовлетворительное'), ('P', 'Плохое')], max_length=2, verbose_name='Состояние')),
                ('estimated_value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Оценочная стоимость')),
                ('photo', models.ImageField(upload_to='items/', verbose_name='Фотография')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection.category', verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
                ('themes', models.ManyToManyField(to='collection.theme', verbose_name='Тематики')),
            ],
            options={
                'verbose_name': 'Предмет коллекции',
                'verbose_name_plural': 'Предметы коллекции',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StorageCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Температура (°C)')),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Влажность (%)')),
                ('last_check_date', models.DateTimeField(verbose_name='Дата последней проверки')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='collection.item', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Условия хранения',
                'verbose_name_plural': 'Условия хранения',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена сделки')),
                ('transaction_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата сделки')),
                ('notes', models.TextField(blank=True, verbose_name='Примечания')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='buy_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection.item', verbose_name='Предмет')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sell_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'ordering': ['-transaction_date'],
            },
        ),
    ]
