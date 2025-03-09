# pc_builder/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),  # главная логика
    path('accounts/', include('accounts.urls', namespace='accounts')),  # логика пользователей
]
