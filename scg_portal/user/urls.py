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

    path('<str:nombre_cuenta>/index/', views.index_view, name="index"),
    path('<str:nombre_cuenta>/', views.client_view, name="client"),
    path('<str:nombre_cuenta>/reports', views.client_reports_view, name="reports"),
    path('<str:nombre_cuenta>/tasks', views.client_tasks_view, name="tasks"),
    path('<str:nombre_cuenta>/report/<int:id_reporte>/', views.view_reporte, name='view_reporte'),
    path('<str:nombre_cuenta>/report/<int:id_reporte>/download_report/', views.download_report, name='download_report'),
    path('<str:nombre_cuenta>/index/crear_reporte/', views.crear_reporte, name="crear_reporte"),
    path('<str:nombre_cuenta>/index/editar_reporte/<int:id_reporte>/', views.editar_reporte, name='editar_reporte'),
    path('<str:nombre_cuenta>/index/eliminar_reporte/<int:id_reporte>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('<str:nombre_cuenta>/index/crear_cuenta/', views.crear_cuenta, name="crear_cuenta"),
    path('<str:nombre_cuenta>/index/editar_cuenta/<int:id_cuenta>/', views.editar_cuenta, name='editar_cuenta'),
    path('<str:nombre_cuenta>/index/eliminar_cuenta/<int:id_cuenta>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('<str:nombre_cuenta>/index/crear_usuario/', views.crear_usuario, name="crear_usuario"),
    path('<str:nombre_cuenta>/index/editar_usuario/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('<str:nombre_cuenta>/index/eliminar_usuario/<int:id_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    path('<str:nombre_cuenta>/Perfil', views.view_perfil, name="perfil")
]