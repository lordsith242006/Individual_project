from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from storage import load_project_data


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: назначение сервиса и сводка данных."""
    teachers, students, appointments = load_project_data()
    context = {
        "teachers_count": len(teachers),
        "students_count": len(students),
        "active_count": sum(1 for a in appointments if a.is_active),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    return render(request, "404.html", status=404)
