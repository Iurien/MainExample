from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, ContactMessage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Добавлено поле slug и author в fields
    list_display = ('title', 'author', 'get_html_photo', 'created_date', 'published_date' )
    readonly_fields = ('get_html_photo', 'created_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'text')

    # prepopulated_fields работает только с латиницей,
    # поэтому для кириллицы оставляем вашу логику в save()

    fields = ('title', 'slug', 'author', 'text', 'image', 'get_html_photo', 'published_date', 'created_date')

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        return "Нет фото"

    get_html_photo.short_description = "Миниатюра"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date')
    list_filter = ('created_date',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    readonly_fields = ('name', 'last_name', 'email', 'subject', 'message', 'created_at')