from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Название роли"),
                            choices=[('collector', 'Коллекционер'), ('admin', 'Администратор')])

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _("Роль")
        verbose_name_plural = _("Роли")

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Убедимся, что роль 'admin' существует, или создадим её
        admin_role, created = Role.objects.get_or_create(name='admin')
        extra_fields.setdefault('role', admin_role)  # Указываем роль для суперпользователя

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название категории"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название тематики"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Тематика")
        verbose_name_plural = _("Тематики")


class Item(models.Model):
    CONDITION_CHOICES = [
        ('M', _('Идеальное')),
        ('NM', _('Почти идеальное')),
        ('VG', _('Очень хорошее')),
        ('G', _('Хорошее')),
        ('F', _('Удовлетворительное')),
        ('P', _('Плохое')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Владелец"))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_("Категория"))
    themes = models.ManyToManyField(Theme, verbose_name=_("Тематики"))
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))
    country = models.CharField(max_length=100, verbose_name=_("Страна происхождения"))
    year = models.IntegerField(verbose_name=_("Год создания"))
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, verbose_name=_("Состояние"))
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Оценочная стоимость"))
    photo = models.ImageField(upload_to='items/', verbose_name=_("Фотография"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата добавления"))

    def __str__(self):
        return f"{self.title} ({self.year})"

    @property
    def condition_display(self):
        return dict(self.CONDITION_CHOICES).get(self.condition, '')

    class Meta:
        verbose_name = _("Предмет коллекции")
        verbose_name_plural = _("Предметы коллекции")
        ordering = ['-created_at']


class StorageCondition(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name=_("Предмет"))
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Температура (°C)"))
    humidity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Влажность (%)"))
    last_check_date = models.DateTimeField(verbose_name=_("Дата последней проверки"))

    def __str__(self):
        return f"Условия хранения для {self.item.title}"

    class Meta:
        verbose_name = _("Условия хранения")
        verbose_name_plural = _("Условия хранения")


