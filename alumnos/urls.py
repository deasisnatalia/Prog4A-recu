from django.urls import path
from .views import dashboard, crear_alumno, generar_pdf, exportar_csv

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("crear/", crear_alumno, name="crear_alumno"),
    path("pdf/<int:alumno_id>/", generar_pdf, name="generar_pdf"),
    path("exportar-csv/", exportar_csv, name="exportar_csv"),
]
