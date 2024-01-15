from django import forms
from .models import Cuenta, Usuario, Reporte 

class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ["tipo", "cuenta"]
        labels = {
            "correo": "Su correo:",
            "password": "Su contraseña:"
        }
        widgets = {
            'correo': forms.EmailInput(),
            'password': forms.PasswordInput()
        }

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'estilo-input'})
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo', 'password', 'tipo', 'cuenta']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'estilo-input'}),
            'password': forms.PasswordInput(attrs={'class': 'estilo-input'}),
            'tipo': forms.Select(attrs={'class': 'estilo-input'}),
            'cuenta': forms.Select(attrs={'class': 'estilo-input'})
        }

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['tipo_reporte', 'target', 'cuenta_reporte', 'source', 'file_report']
        widgets = {
            'tipo_reporte': forms.TextInput(attrs={'class': 'estilo-input'}),
            'target': forms.TextInput(attrs={'class': 'estilo-input'}),
            'cuenta_reporte': forms.Select(attrs={'class': 'estilo-input'})
        }

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        # Personaliza el formulario según tus necesidades, si es necesario
        # Por ejemplo, podrías deshabilitar el campo 'cuenta_reporte' o proporcionar opciones específicas
