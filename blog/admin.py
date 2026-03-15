from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, ProjectRequest


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 1. Добавлена оптимизация SQL-запросов (подгружаем автора одним запросом)
    list_select_related = ('author',)

    # 2. Вывод миниатюры и в список, и в карточку редактирования
    list_display = ('title', 'get_image', 'created_at', 'author', 'published_date')
    readonly_fields = ('get_image', 'created_at', 'updated_at')  # Чтобы видеть фото при редактировании

    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at', 'published_date')
    list_editable = ('published_date',)

    # 3. Современный способ описания метода (через декоратор)
    @admin.display(description="Миниатюра")
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" style="border-radius: 5px;">')
        return "Нет фото"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Оптимизация: подгружаем и автора, и пост
    list_select_related = ('author', 'post')
    list_display = ('author', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('author__username', 'text')
    list_editable = ('active',)


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',)
    # Добавим сортировку, чтобы новые заявки были сверху
    ordering = ('-created_at',)