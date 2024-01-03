from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('index/<str:nombre_cuenta>/', views.index_view, name="index"),
    path('client/<str:nombre_cuenta>/', views.client_view, name="client"),
]
