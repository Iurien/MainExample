import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from pytils.translit import slugify # Импорт кириллического slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_telegram_notification

def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
         'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
         'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
         'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
    transliterated = "".join(map(lambda x: d.get(x, x), s.lower()))
    return slugify(transliterated)

# --- МОДЕЛИ ---

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField("Изображение", upload_to="blog/posts/%Y/%m/%d/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_date']

    def get_absolute_url(self):
        # 'post_detail' должен совпадать с name в вашем urls.py
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            # pytils делает транслитерацию и приводит к формату slug автоматически
            base_slug = slugify(self.title)

            # Проверка на уникальность: если такой slug уже есть, добавляем суффикс
            if Post.objects.filter(slug=base_slug).exists():
                self.slug = f"{base_slug}-{uuid.uuid4().hex[:5]}"
            else:
                self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Запись")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"

    def __str__(self):
        return f'Сообщение от {self.name} {self.last_name}: {self.subject}'


class Order(models.Model):
    # Добавлена базовая модель, чтобы сигнал notify_new_order не вызывал ошибку
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ №{self.id}'


# --- СИГНАЛЫ ---

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    if created:
        # Укажите ваш рабочий домен (например, http://127.0.0.1:8000 для тестов)
        domain = "https://your-site.com"
        post_url = f"{domain}{instance.post.get_absolute_url()}"
        author_name = instance.author.get_full_name() or instance.author.username

        text = (
            f"💬 <b>Новый комментарий!</b>\n\n"
            f"👤 <b>Автор:</b> {author_name}\n"
            f"📝 <b>К посту:</b> <a href='{post_url}'>{instance.post.title}</a>\n"
            f"📄 <b>Текст:</b> <i>{instance.text[:100]}...</i>"
        )
        send_telegram_notification(text)


@receiver(post_save, sender=Order)
def notify_new_order(sender, instance, created, **kwargs):
    if created:
        text = (
            f"📦 <b>Новый заказ!</b>\n\n"
            f"<b>ID заказа:</b> {instance.id}\n"
            f"<b>Сумма:</b> {instance.total_price} руб."
        )
        send_telegram_notification(text)