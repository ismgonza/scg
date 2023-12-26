from django.contrib import admin
from .models import Usuario, Cuenta

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'tipo')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cuenta)
