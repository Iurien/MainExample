from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User


def home(request):
    return render(request,'home.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')


def video(request):
    return render(request,'video.html')

def photo(request):
    return render(request,'photo.html')


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    # Показываем только опубликованные посты, от новых к старым
    queryset = Post.objects.filter(published_date__isnull=False).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')  # Отправляем на вход, если не залогинен

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # <--- Вот здесь магия
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post, 'comments': comments, 'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматический вход после регистрации
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def support_view(request):
    # ваш код
    return render(request, 'support.html')