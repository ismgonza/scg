from django.contrib import admin
from .models import Usuario, Cuenta, Reporte

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'tipo', 'cuenta')

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id_reporte', 'fecha_reporte', 'target', 'cuenta_reporte')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cuenta)
admin.site.register(Reporte, ReporteAdmin)
