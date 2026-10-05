from django.urls import path

from . import views

app_name = "conversor"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/convertir/", views.api_convertir, name="api_convertir"),
]
