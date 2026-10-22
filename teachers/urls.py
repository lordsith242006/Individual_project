from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.teacher_list, name="list"),
    path("available/", views.available_teachers, name="available"),
    path("<int:teacher_id>/", views.teacher_detail, name="detail"),
]
