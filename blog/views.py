from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Post, Comment, ContactMessage, Order
from .forms import CommentForm, ContactForm
from django.contrib.auth.forms import UserCreationForm


# --- Простые страницы ---
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def video(request):
    return render(request, 'video.html')


def photo(request):
    return render(request, 'photo.html')


def support_view(request):
    return render(request, 'support.html')


# --- Обратная связь ---
class ContactCreateView(CreateView):
    model = ContactMessage
    fields = ['name', 'last_name', 'email', 'subject', 'message']
    template_name = 'contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        data = form.cleaned_data
        subject = f"Новое сообщение: {data['subject']}"
        message = f"От: {data['name']} {data['last_name']} ({data['email']})\n\n{data['message']}"

        # Используем email из настроек
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # Добавьте ADMIN_EMAIL в settings.py
            fail_silently=False,
        )
        messages.success(self.request, "Ваше сообщение успешно отправлено!")
        return super().form_valid(form)


# --- Блог ---
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', CommentForm())
        context['comments'] = self.object.comments.select_related('author').all()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object() # Получаем объект поста
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен!")
            # ИСПОРАВЛЕНО: используем self.object.slug вместо post.slug
            return redirect('post_detail', slug=self.object.slug)

        return self.render_to_response(self.get_context_data(form=form))


# --- Заказы и Аккаунт ---
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['total_price']  # В идеале расчет цены должен быть в методе save() модели или в form_valid
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем заказ к текущему пользователю
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

