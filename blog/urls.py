from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('video/',views.video,name='video'),
    path('photo/',views.photo,name='photo'),
    # Главная страница со списком постов
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    # Детальная страница поста (используем slug, как в методе get_absolute_url)
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    # Обратная связь (ContactMessage)
    path('contact/', views.ContactCreateView.as_view(), name='contact'),
    path('order/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('support/', views.support_view, name='support'),
]