from django import forms
from .models import ProjectRequest

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+(код страны) номер'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ваш email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Расскажите о вашем проекте...', 'rows': 4}),
        }
        labels = {
            'name': 'Имя',
            'phone': 'Телефон',
            'email': 'Электронная почта',
            'message': 'Сообщение',
        }


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)