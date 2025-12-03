from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("alumnos/", include("alumnos.urls")),
    path("scraper/", include("scraper.urls")),
    path('', lambda request: redirect('login'), name='home'),
]
