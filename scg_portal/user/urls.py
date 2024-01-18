from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('reset_password/', views.view_reset, name='reset'),
    path('<str:nombre_cuenta>/index/', views.index_view, name="index"),
    path('<str:nombre_cuenta>/', views.client_view, name="client"),
    path('<str:nombre_cuenta>/report/<int:id_reporte>/', views.view_reporte, name='view_reporte'),
    path('<str:nombre_cuenta>/report/<int:id_reporte>/download_report/', views.download_report, name='download_report'),
    path('<str:nombre_cuenta>/index/crear_reporte/', views.crear_reporte, name="crear_reporte"),
    path('<str:nombre_cuenta>/index/crear_cuenta/', views.crear_cuenta, name="crear_cuenta"),
    path('<str:nombre_cuenta>/index/crear_usuario/', views.crear_usuario, name="crear_usuario"),
    path('<str:nombre_cuenta>/Perfil', views.view_perfil, name="perfil")
]