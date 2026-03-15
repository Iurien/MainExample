from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse_lazy
import requests

from .models import Post, Comment
from .forms import ProjectRequestForm, ContactForm


class TelegramNotifier:
    def __init__(self):
        # Токен в settings.py должен быть БЕЗ приставки 'bot' (например: '12345:ABCDE')
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        # ИСПРАВЛЕНО: Правильный формат URL API Telegram
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_notification(self, instance) -> bool:
        message_text = (
            f"🚀 *Новая заявка с сайта!*\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 *Имя:* {getattr(instance, 'name', 'Не указано')}\n"
            f"📞 *Телефон:* {getattr(instance, 'phone', '—')}\n"
            f"📧 *Email:* {getattr(instance, 'email', '—')}\n"
            f"📝 *Сообщение:* {getattr(instance, 'message', 'Без текста')}\n"
            f"━━━━━━━━━━━━━━━"
        )
        payload = {
            "chat_id": self.chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(self.base_url, json=payload, timeout=5)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Ошибка отправки в TG: {e}")
            return False


class ContactsView(FormView):
    template_name = 'contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:contacts')  # Куда редиректить после успеха

    def form_valid(self, form):
        # Данные уже проверены и находятся в form.cleaned_data
        data = form.cleaned_data
        full_message = f"Сообщение от: {data['name']}\nEmail: {data['email']}\n\nТекст:\n{data['message']}"

        try:
            send_mail(
                f"Новая заявка от {data['name']}",
                full_message,
                'your-email@gmail.com',
                ['admin@example.com'],
                fail_silently=False,
            )
            messages.success(self.request, 'Ваше сообщение успешно отправлено!')
        except Exception as e:
            messages.error(self.request, f'Ошибка при отправке: {e}')

        return super().form_valid(form)


class IndexView(CreateView):
    template_name = 'index.html'
    form_class = ProjectRequestForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        instance = form.save()
        # Отправка уведомления
        notifier = TelegramNotifier()
        notifier.send_notification(instance)
        messages.success(self.request, 'Ваше сообщение отправлено! Мы скоро свяжемся с вами.')
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.select_related('author').all().order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            text = request.POST.get('text')
            if text:
                Comment.objects.create(
                    post=self.object,
                    author=request.user,
                    text=text,
                    active=True
                )
                messages.success(request, "Комментарий добавлен!")
                return redirect('blog:post_detail', pk=self.object.pk)
        messages.error(request, "Ошибка при добавлении.")
        return self.get(request, *args, **kwargs)


class PhotoView(TemplateView):
    template_name = 'photo.html'


class VideoView(TemplateView):
    template_name = 'video.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан!')
            return redirect('blog:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})