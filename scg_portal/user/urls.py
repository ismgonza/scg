from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('index/', TemplateView.as_view(template_name="user/index.html"), name="index"),
    path('client/<str:nombre_cuenta>/', TemplateView.as_view(template_name="user/client.html"), name="client")
]
