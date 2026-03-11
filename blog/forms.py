from django import forms
from .models import ProjectRequest

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'modal__input', 'placeholder': 'Введите имя...'}),
        }