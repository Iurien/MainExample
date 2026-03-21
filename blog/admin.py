from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, ProjectRequest, AudioFile, AboutPage, AboutImage, Feedback

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

# Сначала описываем Inline для фотографий
class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 3

# Теперь регистрируем AboutPage ОДИН РАЗ со всеми настройками
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