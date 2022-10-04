from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContentView.as_view()),
    path("<int:content_id>/", views.ContentParamView.as_view()),
    path("filter/", views.ContentFilterView.as_view()),
]
