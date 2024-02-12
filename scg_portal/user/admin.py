from django.contrib import admin
from .models import Usuario, Cuenta, Reporte, Tarea

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'tipo', 'cuenta')
    # Sobreescribe el método get_readonly_fields para hacer el campo de contraseña de solo lectura
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si está editando un objeto existente
            return ['password']
        else:  # Si está creando un nuevo objeto
            return []

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id_reporte', 'fecha_reporte', 'target', 'cuenta_reporte')

class TareaAdmin(admin.ModelAdmin):
    list_display = ('id_tarea', 'cuenta_tarea', 'status')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cuenta)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Tarea, TareaAdmin)
