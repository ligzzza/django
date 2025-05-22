from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'created_at')
    list_filter = ('role', 'is_staff', 'is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )
    readonly_fields = ('last_login', 'created_at')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)

# Добавьте в admin.py после существующего кода

from .models import Category, Theme, Item, StorageCondition


class StorageConditionInline(admin.TabularInline):
    model = StorageCondition
    extra = 0
    verbose_name = _("Условия хранения")
    verbose_name_plural = _("Условия хранения")
    readonly_fields = ('last_check_date',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'year', 'condition_display', 'estimated_value', 'created_at')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'country')
    filter_horizontal = ('themes',)
    inlines = [StorageConditionInline]
    date_hierarchy = 'created_at'
    list_display_links = ('title',)
    raw_id_fields = ('user', 'category')
    readonly_fields = ('created_at',)

    @admin.display(description=_('Состояние'))
    def condition_display(self, obj):
        return obj.get_condition_display()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_display_links = ('name',)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_display_links = ('name',)


