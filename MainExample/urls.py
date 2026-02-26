"""
Настройка URL-адресов для проекта Mysite.

Список `urlpatterns` направляет URL-адреса к представлениям. Для получения дополнительной информации см.:

https://docs.djangoproject.com/en/6.0/topics/http/urls/
Примеры:
Функция Views

1. Добавьте импорт: from my_app import views

2. Добавьте URL-адрес в urlpatterns: path('', views.home, name='home')
Представления на основе классов

1. Добавьте импорт: from other_app.views import Home

2. Добавьте URL-адрес в urlpatterns: path('', Home.as_view(), name='home')
Включение еще одной конфигурации URL

1. Импортируйте функцию include(): from django.urls import include, path

2. Добавьте URL-адрес в urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
