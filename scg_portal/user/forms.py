from django import forms
from .models import Usuario

class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ["tipo"]
        labels = {
            "correo": "Su correo:",
            "password": "Su contraseña:"
        }
        widgets = {
            'correo': forms.EmailInput(),
            'password': forms.PasswordInput()
        }