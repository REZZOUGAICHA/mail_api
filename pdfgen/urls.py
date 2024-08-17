# pdfgen/urls.py
from django.urls import path
from .views import JsonToPdfView

urlpatterns = [
    path('json-to-pdf/', JsonToPdfView.as_view(), name='json-to-pdf'),
]
