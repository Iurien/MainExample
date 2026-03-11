from django.db import models
from django.contrib.auth.models import User


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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    class Meta:
        verbose_name='Запрос проекта'
        verbose_name_plural='Запросы проектов'

    def __str__(self):
        return f"Заявка от {self.name}"