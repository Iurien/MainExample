from django.urls import path, include
from .views import PostListView, PostDetailView, IndexView, ContactsView, PhotoView, VideoView
from django.contrib.auth import views as auth_views
from .views import register
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('photo/', PhotoView.as_view(), name='photo'),
    path('video/', VideoView.as_view(), name='video'),
    # Для списка постов
    path('post_list/', PostListView.as_view(), name='post_list'),
    # Для одного поста. DetailView по умолчанию ищет 'pk' в URL
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]