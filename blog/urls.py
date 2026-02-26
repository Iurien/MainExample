from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('video/',views.video,name='video'),
    path('photo/',views.photo,name='photo'),
    # Для функциональных представлений (FBV):
    # path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    # ИЛИ для классовых представлений (CBV):
     path('post_list/', views.PostListView.as_view(), name='post_list'),
     # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('support/', views.support_view, name='support'),
]