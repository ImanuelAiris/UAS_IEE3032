from django.urls import path

from . import views

urlpatterns = [
    path('webview/', views.webview)
]