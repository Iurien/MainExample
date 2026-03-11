from django import forms
from django.core.exceptions import ValidationError  # Добавлено
from .models import ContactMessage, Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        # Добавили 'subject' в список полей
        fields = ['name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            # Новый виджет для темы сообщения
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема сообщения'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваше сообщение...'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            max_size = 5 * 1024 * 1024  # 5 МБ
            if file.size > max_size:
                raise ValidationError("Файл слишком большой. Максимальный размер — 5 МБ.")
        return file

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите комментарий...',
                'class': 'form-control'
            }),
        }
        labels = {'text': ''}