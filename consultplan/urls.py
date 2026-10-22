"""Корневая конфигурация маршрутов проекта."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("teachers/", include("teachers.urls")),
    path("appointments/", include("appointments.urls")),
]

handler404 = "homepage.views.page_not_found"
