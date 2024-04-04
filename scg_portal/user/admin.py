from django.contrib import admin
from .models import Usuario, Cuenta, Reporte, Tarea, Contrato, Comment

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'user_id', 'tipo', 'cuenta')
    # Sobreescribe el método get_readonly_fields para hacer el campo de contraseña de solo lectura
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si está editando un objeto existente
            return ['password']
        else:  # Si está creando un nuevo objeto
            return []
        
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('id_cuenta', 'nombre')

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id_reporte', 'fecha_reporte', 'target', 'cuenta_reporte')

class TareaAdmin(admin.ModelAdmin):
    list_display = ('id_tarea', 'cuenta_tarea', 'fecha', 'status')

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id_contrato', 'cuenta_contrato', 'status')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id_comment', 'tarea_comment', 'fecha')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Comment, CommentAdmin)
