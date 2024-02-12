# qr_generator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage URL
    path('generate/', views.generate_qr, name='generate_qr'),  # QR Code generation URL
]
