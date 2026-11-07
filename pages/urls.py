from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("resources/", views.resources, name="resources"),
    path("about/", views.about, name="about"),
    path("resources/available/", views.available_resources, name="available_resources"),
]

