from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post,Comment

admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Колонки в списке постов
    list_display = ('title', 'author', 'published_date', 'get_image_preview')

    # Фильтры справа
    list_filter = ('published_date', 'author')

    # Поиск по заголовку и тексту
    search_fields = ('title', 'text')

    # Поля только для чтения (превью в форме редактирования)
    readonly_fields = ('get_image_preview',)

    # Метод для показа миниатюры в админке
    def get_image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "Нет фото"

    get_image_preview.short_description = "Превью"

