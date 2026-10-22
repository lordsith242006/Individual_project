from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("", views.appointment_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:appointment_id>/", views.appointment_detail, name="detail"),
]
