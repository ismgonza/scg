from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordResetForm
from .models import Cuenta, Usuario, Reporte, Tarea, Contrato

class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ["tipo", "cuenta", "nombre", "telefono", "status"]
        placeholders = {
            "correo": "Email",
            "password": "Password"
        }
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': placeholders['correo']}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': placeholders['password']})
        }

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        exclude = ["id_cuenta"]
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ["password", "status"]
        fields = ['correo', 'tipo', 'cuenta', 'nombre', 'telefono']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cuenta': forms.Select(attrs={'class': 'form-control form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'})
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
        exclude = ['target']
        fields = ['tipo_reporte', 'cuenta_reporte', 'source', 'file_report']
        widgets = {
            'tipo_reporte': forms.TextInput(attrs={'class': 'form-control'}),
            'cuenta_reporte': forms.Select(attrs={'class': 'form-control'}),
            'source': forms.FileInput(attrs={'class': 'form-control'}),  # Aplicar estilo a source
            'file_report': forms.FileInput(attrs={'class': 'form-control'})  # Aplicar estilo a file_report
        }

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.fields['source'].required = False  # Indicar que el campo no es obligatorio
        self.fields['file_report'].required = False  # Indicar que el campo no es obligatorio
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
        fields = ['cuenta_tarea','severity', 'descripcion', 'incidente']
        widgets = {
            'cuenta_tarea': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'incidente': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(TareaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False  # Indicar que el campo no es obligatorio
        # Personaliza el formulario según tus necesidades, si es necesario
        # Por ejemplo, podrías deshabilitar el campo 'cuenta_reporte' o proporcionar opciones específicas

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control", "placeholder": "Email"}),
    )

    def save(self, **kwargs):
        # Agrega aquí tu lógica personalizada, si es necesario
        # Por ejemplo, enviar el correo electrónico aquí
        super().save(**kwargs)  # Esto llama al método save() original para enviar el correo electrónico de restablecimiento de contraseña

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        exclude = ["status"]
        fields = ['cuenta_contrato', 'id_contrato', 'fecha_inicio', 'fecha_final']
        widgets = {
            'cuenta_contrato': forms.Select(attrs={'class': 'form-control'}),
            'id_contrato': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }