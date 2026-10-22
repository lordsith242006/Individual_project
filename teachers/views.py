from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def teacher_list(request: HttpRequest) -> HttpResponse:
    """Список преподавателей с поиском по ФИО и отбором по местам."""
    query = request.GET.get("q", "").strip()
    min_students = request.GET.get("min_students", "").strip()

    conditions = []
    params: list = []
    if query:
        conditions.append("py_lower(name) LIKE ?")
        params.append(f"%{query.lower()}%")
    if min_students.isdigit():
        conditions.append("max_students >= ?")
        params.append(int(min_students))
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    teachers = fetch_all(
        f"""
        SELECT id, name, department, max_students, consultation_time
        FROM teachers
        {where}
        ORDER BY name
        """,
        tuple(params),
    )
    context = {
        "teachers": teachers,
        "query": query,
        "min_students": min_students,
    }
    return render(request, "teachers/teacher_list.html", context)


def teacher_detail(request: HttpRequest, teacher_id: int) -> HttpResponse:
    """Карточка преподавателя и его активные записи."""
    teacher = fetch_one(
        """
        SELECT id, name, department, max_students, consultation_time
        FROM teachers
        WHERE id = ?
        """,
        (teacher_id,),
    )
    appointments = fetch_all(
        """
        SELECT
            a.id,
            strftime('%d.%m.%Y', a.consultation_date) AS date_display,
            s.name AS student_name,
            s.group_name
        FROM appointments AS a
        JOIN students AS s ON s.id = a.student_id
        WHERE a.teacher_id = ? AND a.is_cancelled = 0
        ORDER BY a.consultation_date
        """,
        (teacher_id,),
    )
    context = {
        "teacher": teacher,
        "teacher_id": teacher_id,
        "appointments": appointments,
    }
    return render(
        request,
        "teachers/teacher_detail.html",
        context,
        status=200 if teacher else 404,
    )


def available_teachers(request: HttpRequest) -> HttpResponse:
    """Преподаватели со свободными местами на выбранную дату."""
    selected = request.GET.get("date", "")
    error = ""
    teachers = []
    if selected:
        try:
            date.fromisoformat(selected)
        except ValueError:
            error = "Неверный формат даты."
        else:
            teachers = fetch_all(
                """
                SELECT
                    t.id,
                    t.name,
                    t.department,
                    t.consultation_time,
                    t.max_students,
                    t.max_students - COUNT(a.id) AS free_seats
                FROM teachers AS t
                LEFT JOIN appointments AS a
                    ON a.teacher_id = t.id
                    AND a.consultation_date = ?
                    AND a.is_cancelled = 0
                GROUP BY t.id
                HAVING free_seats > 0
                ORDER BY free_seats DESC, t.name
                """,
                (selected,),
            )
    context = {
        "selected_date": selected,
        "teachers": teachers,
        "error": error,
    }
    return render(request, "teachers/available.html", context)
