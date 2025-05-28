from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'category', 'themes', 'title', 'description', 'country',
            'year', 'condition', 'estimated_value', 'photo'
        ]
        widgets = {
            'themes': forms.CheckboxSelectMultiple(),  # Мультивыбор для тем
            'condition': forms.Select(choices=Item.CONDITION_CHOICES),  # Выпадающий список для состояния
        }