from django.urls import path
from . import views

urlpatterns = [
    path("", views.buscar, name="scraper_home"),
    path("buscar/", views.buscar, name="buscar"),
    path("enviar/", views.enviar_resultados, name="enviar_resultados"),
]
