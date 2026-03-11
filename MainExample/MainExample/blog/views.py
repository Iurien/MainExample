from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView

from .models import Post, Comment, ContactMessage
from .forms import CommentForm, ContactForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact_instance = form.save()
            data = form.cleaned_data

            email = EmailMessage(
                subject=f"Сообщение: {data.get('subject')}",
                body=f"От: {data.get('name')}...",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
            )

            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                # Передаем объект файла напрямую, не вызывая .read()
                # Django сам прочитает его кусками при отправке
                email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

            try:
                email.send(fail_silently=False)
                messages.success(request, 'Сообщение успешно отправлено.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке почты: {e}')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def video(request):
    return render(request, 'video.html')


def photo(request):
    return render(request, 'photo.html')


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 3  # Количество постов на одной странице

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def support_view(request):
    return render(request, 'support.html')


