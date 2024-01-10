from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('<str:nombre_cuenta>/index/', views.index_view, name="index"),
    path('<str:nombre_cuenta>/client/', views.client_view, name="client"),
    path('<str:nombre_cuenta>/client/reports/<int:id_reporte>/', views.view_reporte, name='view_reporte'),
    path('<str:nombre_cuenta>/client/reports/<int:id_reporte>/download_html_content/', views.download_html_content, name='download_html_content')
]