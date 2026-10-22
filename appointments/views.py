from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.appointments import find_appointment_by_id
from storage import load_project_data


def appointment_list(request: HttpRequest) -> HttpResponse:
    """Список всех записей на консультации."""
    _, _, appointments = load_project_data()
    return render(
        request,
        "appointments/appointment_list.html",
        {"appointments": appointments},
    )


def appointment_detail(
    request: HttpRequest,
    appointment_id: int,
) -> HttpResponse:
    """Подробная информация о записи."""
    _, _, appointments = load_project_data()
    appointment = find_appointment_by_id(appointments, appointment_id)
    return render(
        request,
        "appointments/appointment_detail.html",
        {"appointment": appointment, "appointment_id": appointment_id},
        status=200 if appointment else 404,
    )
