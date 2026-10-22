from html import escape

from django.http import HttpRequest, HttpResponse

from homepage.views import page
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

    rows = "".join(
        f"""<tr>
            <td><a href="/teachers/{t.id}/">{escape(t.name)}</a></td>
            <td>{escape(t.department)}</td>
            <td>{escape(t.consultation_time)}</td>
            <td>{t.max_students}</td>
        </tr>"""
        for t in sort_teachers(teachers)
    ) or '<tr><td colspan="4">Преподаватели не найдены.</td></tr>'

    content = f"""
        <h1>Преподаватели</h1>
        <form class="row g-2 mb-3" method="get">
            <div class="col-md-5">
                <input class="form-control" name="q" placeholder="ФИО"
                       value="{escape(query)}">
            </div>
            <div class="col-md-4">
                <input class="form-control" name="min_students" type="number"
                       min="1" placeholder="Мест не меньше"
                       value="{escape(min_students)}">
            </div>
            <div class="col-md-3">
                <button class="btn btn-primary w-100">Найти</button>
            </div>
        </form>
        <table class="table table-striped bg-white">
            <thead><tr><th>ФИО</th><th>Кафедра</th><th>Время</th>
                <th>Мест</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>"""
    return HttpResponse(page("Преподаватели", content))


def teacher_detail(request: HttpRequest, teacher_id: int) -> HttpResponse:
    """Карточка преподавателя и его активные записи."""
    teachers, _, appointments = load_project_data()
    teacher = find_teacher_by_id(teachers, teacher_id)
    if teacher is None:
        content = f"""
            <div class="alert alert-warning">
                Преподаватель с номером {teacher_id} не найден.
            </div>
            <a href="/teachers/">К списку преподавателей</a>"""
        return HttpResponse(
            page("Преподаватель не найден", content), status=404
        )

    items = "".join(
        f"""<li class="list-group-item">
            <a href="/appointments/{a.id}/">#{a.id}</a>
            {a.consultation_date.strftime('%d.%m.%Y')} —
            {escape(a.student.name)}</li>"""
        for a in appointments
        if a.teacher.id == teacher.id and a.is_active
    ) or '<li class="list-group-item">Активных записей нет.</li>'

    content = f"""
        <div class="card mb-3">
            <div class="card-body">
                <h1 class="card-title">{escape(teacher.name)}</h1>
                <p class="card-text">Кафедра: {escape(teacher.department)}</p>
                <p class="card-text">Время консультаций:
                    {escape(teacher.consultation_time)}</p>
                <p class="card-text">Мест на консультации:
                    {teacher.max_students}</p>
            </div>
        </div>
        <h2>Активные записи</h2>
        <ul class="list-group mb-3">{items}</ul>
        <a href="/teachers/">К списку преподавателей</a>"""
    return HttpResponse(page(teacher.name, content))
