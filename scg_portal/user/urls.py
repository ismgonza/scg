from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('<str:nombre_cuenta>/index/', views.index_view, name="index"),
    path('<str:nombre_cuenta>/', views.client_view, name="client"),
    path('<str:nombre_cuenta>/reports/<int:id_reporte>/', views.view_reporte, name='view_reporte'),
    path('<str:nombre_cuenta>/reports/<int:id_reporte>/download_html_content/', views.download_html_content, name='download_html_content'),
    path('<str:nombre_cuenta>/index/crear_reporte/', views.crear_reporte, name="crear_reporte"),
    path('<str:nombre_cuenta>/index/crear_cuenta/', views.crear_cuenta, name="crear_cuenta"),
    path('<str:nombre_cuenta>/index/crear_usuario/', views.crear_usuario, name="crear_usuario"),
]