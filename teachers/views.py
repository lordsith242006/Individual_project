from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.teachers import (
    filter_teachers_by_capacity,
    find_teacher,
    find_teacher_by_id,
    sort_teachers,
)
from storage import load_project_data


def teacher_list(request: HttpRequest) -> HttpResponse:
    """Список преподавателей с поиском по ФИО и отбором по местам."""
    teachers, _, _ = load_project_data()
    query = request.GET.get("q", "").strip()
    min_students = request.GET.get("min_students", "").strip()
    if query:
        teachers = find_teacher(teachers, query)
    if min_students.isdigit():
        teachers = filter_teachers_by_capacity(teachers, int(min_students))
    context = {
        "teachers": sort_teachers(teachers),
        "query": query,
        "min_students": min_students,
    }
    return render(request, "teachers/teacher_list.html", context)


def teacher_detail(request: HttpRequest, teacher_id: int) -> HttpResponse:
    """Карточка преподавателя и его активные записи."""
    teachers, _, appointments = load_project_data()
    teacher = find_teacher_by_id(teachers, teacher_id)
    context = {
        "teacher": teacher,
        "teacher_id": teacher_id,
        "appointments": [
            a for a in appointments
            if teacher and a.teacher.id == teacher.id and a.is_active
        ],
    }
    return render(
        request,
        "teachers/teacher_detail.html",
        context,
        status=200 if teacher else 404,
    )
