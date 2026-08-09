from django import forms
from .models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']
        labels = {
            'nombre': 'Nombre',
            'email': 'E-Mail',
            'mensaje': 'Mensaje',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Escriba su nombre'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'mensaje': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escriba su mensaje'}),
        }
