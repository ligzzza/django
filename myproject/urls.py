from django.urls import path
from collection import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/coins/', views.coins_view, name='calendar_coins'),
    path('calendar/stamps/', views.stamps_view, name='calendar_stamps'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]