
from django.contrib import admin
from django.urls import path
from collection import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    # path('calendar/coins/', views.calendar_coins, name='calendar_coins'),
    # path('calendar/stamps/', views.calendar_stamps, name='calendar_stamps'),
]


