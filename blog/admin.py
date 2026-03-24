from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, ProjectRequest, AudioFile, AboutPage, AboutImage, Feedback, Video

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_select_related = ('author',)
    list_display = ('title', 'get_image', 'created_at', 'author', 'published_date')
    readonly_fields = ('get_image', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at', 'published_date')
    list_editable = ('published_date',)

    @admin.display(description="Миниатюра")
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" style="border-radius: 5px;">')
        return "Нет фото"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_select_related = ('author', 'post')
    list_display = ('author', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('author__username', 'text')
    list_editable = ('active',)

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    search_fields = ('title',)


class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1
    readonly_fields = ('preview',)  # Добавляем поле для предпросмотра

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "Нет изображения"

    preview.short_description = "Предпросмотр"


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    inlines = [AboutImageInline]

    def has_add_permission(self, request):
        # Запрещает создание новой записи, если одна уже существует
        return not AboutPage.objects.exists()

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    # Столбцы, которые будут видны в списке всех видео
    list_display = ('title', 'video_url', 'created_at')

    # Поля, по которым можно искать (справа вверху появится поиск)
    search_fields = ('title', 'description')

    # Фильтр справа (по дате создания)
    list_filter = ('created_at',)

    # Порядок сортировки в админке
    ordering = ('-created_at',)