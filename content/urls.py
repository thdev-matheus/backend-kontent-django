from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContentView.as_view())
]