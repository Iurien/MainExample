from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, ProjectRequest

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Что отображаем в списке
    list_display = ('title', 'content','created_at', 'author', 'get_image', 'published_date')
    # По каким полям ищем
    search_fields = ('title', 'content')
    # Фильтры справа
    list_filter = ('author', 'created_at', 'published_date')
    # Возможность редактировать автора прямо из списка
    list_editable = ('published_date',)
    # Автоматическое создание slug (если добавите его в модель)
    # prepopulated_fields = {"slug": ("title",)}

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="auto">')
        return "Нет фото"
    get_image.short_description = "Миниатюра"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('author__username', 'text')
    # Быстрое включение/выключение комментариев
    list_editable = ('active',)

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',) # Запрещаем менять дату вручную