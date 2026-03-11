from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from .models import Post
import requests
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import ProjectRequestForm
from django.urls import reverse_lazy




class IndexView(CreateView):
    template_name = 'index.html'
    form_class = ProjectRequestForm
    success_url = reverse_lazy('blog:index')  # Куда редиректить после успеха

    def form_valid(self, form):
        instance = form.save()

        # Создаем экземпляр нотификатора и отправляем сообщение
        notifier = TelegramNotifier()
        notifier.send_notification(instance.name)

        messages.success(self.request, 'Заявка отправлена! Бот уже шепнул нам о вас.')
        return super().form_valid(form)


class TelegramNotifier:
    """Класс для работы с уведомлениями в Telegram."""

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        # ИСПРАВЛЕННАЯ СТРОКА НИЖЕ:
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_notification(self, name: str) -> bool:
        """Отправляет сообщение о новой заявке."""
        payload = {
            "chat_id": self.chat_id,
            "text": f"🚀 *Новая заявка!*\n👤 Имя: {name}",
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка отправки в TG: {e}")
            return False


# Пример использования:
# notifier = TelegramNotifier()
# notifier.send_notification("Иван")


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Добавлен select_related('author') для оптимизации
        return Post.objects.select_related('author').all().order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все активные комментарии для этого поста
        # Убедитесь, что в модели Comment поле related_name='comments'
        context['comments'] = self.object.comments.filter(active=True).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        """Обработка отправки формы комментария."""
        self.object = self.get_object()

        if request.user.is_authenticated:
            text = request.POST.get('text')
            if text:
                # Создаем комментарий напрямую через модель
                from .models import Comment
                Comment.objects.create(
                    post=self.object,
                    author=request.user,
                    text=text,
                    active=True  # Сразу делаем активным
                )
                messages.success(request, "Комментарий успешно добавлен!")
                return redirect('blog:post_detail', pk=self.object.pk)

        messages.error(request, " Ошибка при добавлении комментария.")
        return self.get(request, *args, **kwargs)


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text'] # Укажите поля, которые можно править
    template_name = 'blog/post_edit.html'
    # После сохранения перекинет на страницу поста
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Шаблон подтверждения
    success_url = reverse_lazy('blog:post_list')     # Куда идти после удаления


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Сохраняем пользователя
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти.')
            return redirect('blog:login') # Перенаправляем на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})