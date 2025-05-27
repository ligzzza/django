from django.urls import path
from collection import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/coins/', views.coins_view, name='calendar_coins'),
    path('calendar/stamps/', views.stamps_view, name='calendar_stamps'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/', views.items_list, name='items_list'),
    path('items/add/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
]