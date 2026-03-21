from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
import requests

from .models import Post, Comment, AudioFile, AboutPage, Feedback

from .forms import ProjectRequestForm, ContactForm, CommentForm, FeedbackForm


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


class AboutPageView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'about.html'
    success_url = reverse_lazy('blog:about')
    success_message = "Ваше сообщение успешно отправлено!"

    def form_valid(self, form):
        # 1. Сначала сохраняем объект в базу (стандартное поведение CreateView)
        response = super().form_valid(form)

        # 2. Получаем данные из формы для письма
        feedback = form.cleaned_data

        # 3. Отправляем письмо
        send_mail(
            subject=f"Новое сообщение от {feedback.get('name', 'Пользователя')}",
            message=f"Email: {feedback.get('email')}\n\nТекст сообщения:\n{feedback.get('message')}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # или другой ваш email
            fail_silently=False,
        )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_data'] = AboutPage.objects.first()
        return context


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
        # Добавляем список активных комментариев
        context['comments'] = self.object.comments.filter(active=True).order_by('-created_at')
        # Добавляем пустую форму в контекст
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        # Для обработки POST нам все равно нужен объект поста
        self.object = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, "Нужно войти в аккаунт, чтобы оставить комментарий.")
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.active = True
            comment.save()
            messages.success(request, "Комментарий успешно добавлен!")
            return redirect('blog:post_detail', pk=self.object.pk)

        # Если форма невалидна, возвращаем страницу с ошибками
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)


class GalleryView(TemplateView):
    template_name = 'gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['gallery1_images'] = [
            {'full': 'images/1_1.jpg', 'thumb': 'images/1_1_thumb.jpg', 'caption': 'Снежный барс'},
            {'full': 'images/1_2.jpg', 'thumb': 'images/1_2_thumb.jpg', 'caption': 'Пума'},
            {'full': 'images/1_3.jpg', 'thumb': 'images/1_3_thumb.jpg', 'caption': 'Кто это?'},
            {'full': 'images/1_4.jpg', 'thumb': 'images/1_4_thumb.jpg', 'caption': 'Рептилия'},
        ]

        context['gallery2_images'] = [
            {'full': 'images/2_1.jpg', 'thumb': 'images/2_1_thumb.jpg', 'alt': 'подводный мир'},
            {'full': 'images/2_2.jpg', 'thumb': 'images/2_2_thumb.jpg', 'alt': 'Дорожный знак'},
            {'full': 'images/2_3.jpg', 'thumb': 'images/2_3_thumb.jpg', 'alt': 'Воздушные шарики'},
            {'full': 'images/2_4.jpg', 'thumb': 'images/2_4_thumb.jpg', 'alt': 'Колонны'},
            {'full': 'images/2_5.jpg', 'thumb': 'images/2_5_thumb.jpg', 'alt': 'Пейзаж на закате'},
        ]

        context['gallery3_images'] = [
            {'full': 'images/3_1.jpg', 'thumb': 'images/3_1_thumb.jpg', 'alt': 'Описание 1'},
            {'full': 'images/3_2.jpg', 'thumb': 'images/3_2_thumb.jpg', 'alt': 'Описание 2'},
            {'full': 'images/3_3.jpg', 'thumb': 'images/3_3_thumb.jpg', 'alt': 'Описание 3'},
            {'full': 'images/3_4.jpg', 'thumb': 'images/3_4_thumb.jpg', 'alt': 'Описание 4'},
            {'full': 'images/3_5.jpg', 'thumb': 'images/3_5_thumb.jpg', 'alt': 'Описание 5'},
        ]

        return context

    def get_queryset(self):
        return GalleryImage.objects.all().order_by('my_order')

class VideoView(TemplateView):
    template_name = 'video.html'


class AudioListView(ListView):
    model = AudioFile
    template_name = 'audio.html' # Путь к вашему шаблону
    context_object_name = 'audios'     # Имя переменной в HTML


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