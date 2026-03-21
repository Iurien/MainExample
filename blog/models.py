import os
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст поста")
    # Поле для фото (нужно установить Pillow: pip install Pillow)
    image = models.ImageField(
        upload_to='posts/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Автор")

    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']  # Новые посты сверху

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    text = models.TextField(verbose_name="Текст комментария")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата написания")
    active = models.BooleanField(default=True, verbose_name="Отображать")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']  # Комментарии идут по порядку (старые сверху)

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post.title}'


class ProjectRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)       # Добавить это
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True) # И это
    message = models.TextField(verbose_name="Сообщение", blank=True, null=True)  # И это
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    class Meta:
        verbose_name='Запрос проекта'
        verbose_name_plural='Запросы проектов'

    def __str__(self):
        return f"Заявка от {self.name}"


def validate_file_size(value):
    filesize = value.size
    # Лимит 10 МБ (10 * 1024 * 1024 байт)
    if filesize > 10485760:
        raise ValidationError("Максимальный размер файла — 10 МБ")

class AudioFile(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(
        upload_to='audio/',
        verbose_name="Файл",
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg']),
            validate_file_size
        ],
        help_text="Допустимые форматы: mp3, wav, ogg. Макс. размер: 10 МБ."
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Аудиозапись"
        verbose_name_plural = "Аудиозаписи"


class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="О нас", verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст страницы")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.title

class AboutImage(models.Model):
    # Связь с основной страницей
    page = models.ForeignKey(AboutPage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about_gallery/', verbose_name="Изображение")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Описание (alt)")

    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Галерея изображений"


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"