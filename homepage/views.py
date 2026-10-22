from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_one


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: назначение сервиса и сводка данных из SQLite."""
    summary = fetch_one("""
        SELECT
            (SELECT COUNT(*) FROM teachers) AS teachers_count,
            (SELECT COUNT(*) FROM students) AS students_count,
            (SELECT COUNT(*) FROM appointments
             WHERE is_cancelled = 0) AS active_count
    """)
    return render(request, "homepage/index.html", dict(summary))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    return render(request, "404.html", status=404)
