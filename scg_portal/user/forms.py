from django import forms
from django.utils.translation import gettext as _
from .models import Cuenta, Usuario, Reporte, Tarea

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

class UsuarioFormEdit(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ['password']  # Excluye el campo de contraseña del formulario
        fields = ['correo', 'tipo', 'cuenta']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'estilo-input'}),
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

class CambiarClaveForm(forms.Form):
    nueva_contraseña = forms.CharField(
        label=_('Nueva contraseña'),
        widget=forms.PasswordInput
    )

    confirmar_contraseña = forms.CharField(
        label=_('Confirmar nueva contraseña'),
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get('nueva_contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        if nueva_contraseña and confirmar_contraseña and nueva_contraseña != confirmar_contraseña:
            raise forms.ValidationError(_('Las contraseñas no coinciden.'))

        return cleaned_data
    
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['cuenta_tarea', 'descripcion', 'incidente', 'status', 'loe']
        widgets = {
            'cuenta_tarea': forms.Select(attrs={'class': 'estilo-input'}),
            'status': forms.Select(attrs={'class': 'estilo-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'estilo-input'}),
            'incidente': forms.TextInput(attrs={'class': 'estilo-input'}),
            'loe': forms.TextInput(attrs={'class': 'estilo-input'})
        }

    def __init__(self, *args, **kwargs):
        super(TareaForm, self).__init__(*args, **kwargs)
        # Personaliza el formulario según tus necesidades, si es necesario
        # Por ejemplo, podrías deshabilitar el campo 'cuenta_reporte' o proporcionar opciones específicas