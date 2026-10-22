from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one

APPOINTMENT_FIELDS = """
    a.id,
    strftime('%d.%m.%Y', a.consultation_date) AS date_display,
    a.is_cancelled,
    t.id AS teacher_id,
    t.name AS teacher_name,
    t.department,
    t.consultation_time,
    s.name AS student_name,
    s.email,
    s.group_name
FROM appointments AS a
JOIN teachers AS t ON t.id = a.teacher_id
JOIN students AS s ON s.id = a.student_id
"""


def appointment_list(request: HttpRequest) -> HttpResponse:
    """Список всех записей на консультации (JOIN трёх таблиц)."""
    appointments = fetch_all(
        f"SELECT {APPOINTMENT_FIELDS} ORDER BY a.consultation_date, t.name"
    )
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
    appointment = fetch_one(
        f"SELECT {APPOINTMENT_FIELDS} WHERE a.id = ?",
        (appointment_id,),
    )
    return render(
        request,
        "appointments/appointment_detail.html",
        {"appointment": appointment, "appointment_id": appointment_id},
        status=200 if appointment else 404,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    """Статистика записей: агрегаты, GROUP BY и HAVING."""
    totals = fetch_one("""
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(is_cancelled = 0), 0) AS active,
            COALESCE(SUM(is_cancelled = 1), 0) AS cancelled
        FROM appointments
    """)
    by_teacher = fetch_all("""
        SELECT
            t.id,
            t.name AS teacher_name,
            t.max_students,
            COUNT(a.id) AS appointments_count
        FROM teachers AS t
        LEFT JOIN appointments AS a
            ON a.teacher_id = t.id AND a.is_cancelled = 0
        GROUP BY t.id, t.name
        ORDER BY appointments_count DESC, t.name
    """)
    by_department = fetch_all("""
        SELECT
            department,
            COUNT(*) AS teachers_count,
            SUM(max_students) AS total_seats
        FROM teachers
        GROUP BY department
        ORDER BY teachers_count DESC, department
    """)
    frequent_students = fetch_all("""
        SELECT
            s.name AS student_name,
            s.group_name,
            COUNT(a.id) AS appointments_count
        FROM students AS s
        JOIN appointments AS a ON a.student_id = s.id
        WHERE a.is_cancelled = 0
        GROUP BY s.id, s.name, s.group_name
        HAVING COUNT(a.id) > 1
        ORDER BY appointments_count DESC
    """)
    context = {
        "totals": totals,
        "by_teacher": by_teacher,
        "by_department": by_department,
        "frequent_students": frequent_students,
    }
    return render(request, "appointments/statistics.html", context)
