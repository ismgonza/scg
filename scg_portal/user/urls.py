from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),

    path('reset_password/', views.view_reset_correo, name='reset'),
    path('reset_password/sent/', TemplateView.as_view(template_name='user/reset_correo_sent.html'), name='reset_sent'),
    path('reset/<uidb64>/<token>/', views.confirmar_clave_view, name='reset_confirm'),
    path('reset_password/completed/', auth_views.PasswordResetCompleteView.as_view(template_name='user/reset_clave_done.html'), name='reset_complete'),

    path('<str:nombre_cuenta>/costumers/', views.index_view, name="index"),
    path('<str:nombre_cuenta>/costumers/report/<int:id_reporte>/', views.view_detalle_reporte_admin, name="view_report_admin"),
    path('<str:nombre_cuenta>/tasks/', views.view_admin_tasks, name="admin_tasks"),
    
    path('<str:nombre_cuenta>/tasks/<int:id_tarea>/', views.view_detalle_tarea_admin, name="view_task_admin"),
    path('<str:nombre_cuenta>/', views.client_view, name="client"),

    path('<str:nombre_cuenta>/reports/', views.client_reports_view, name="reports"),
    path('<str:nombre_cuenta>/tickets/', views.client_tasks_view, name="tasks"),
    path('<str:nombre_cuenta>/ticket/<int:id_tarea>/', views.view_detalle_tarea, name="view_task"),
    path('<str:nombre_cuenta>/report/<int:id_reporte>/', views.view_reporte, name='view_reporte'),
    path('<str:nombre_cuenta>/report/<int:id_reporte>/download_report/', views.download_report, name='download_report'),

    path('<str:nombre_cuenta>/costumers/get_account_data/', views.get_account_data, name='get_account_data'),

    path('<str:nombre_cuenta>/costumers/crear_reporte/', views.crear_reporte, name="crear_reporte"),
    path('<str:nombre_cuenta>/costumers/editar_reporte/<int:id_reporte>/', views.editar_reporte, name='editar_reporte'),
    path('<str:nombre_cuenta>/costumers/eliminar_reporte/<int:id_reporte>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('<str:nombre_cuenta>/costumers/crear_cuenta/', views.crear_cuenta, name="crear_cuenta"),
    path('<str:nombre_cuenta>/costumers/editar_cuenta/<int:id_cuenta>/', views.editar_cuenta, name='editar_cuenta'),
    path('<str:nombre_cuenta>/costumers/eliminar_cuenta/<int:id_cuenta>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('<str:nombre_cuenta>/costumers/crear_usuario/', views.crear_usuario, name="crear_usuario"),
    path('<str:nombre_cuenta>/costumers/editar_usuario/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('<str:nombre_cuenta>/costumers/eliminar_usuario/<int:id_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('<str:nombre_cuenta>/costumers/crear_tarea/', views.crear_tarea, name="crear_tarea"),
    path('<str:nombre_cuenta>/costumers/editar_tarea/<int:id_tarea>/', views.editar_tarea, name='editar_tarea'),
    path('<str:nombre_cuenta>/costumers/eliminar_tarea/<int:id_tarea>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('<str:nombre_cuenta>/costumers/crear_contrato/', views.crear_contrato, name="crear_contrato"),
    
    path('<str:nombre_cuenta>/Perfil', views.view_perfil, name="perfil")
]