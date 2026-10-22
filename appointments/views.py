from html import escape

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models import Appointment
from models.appointments import find_appointment_by_id
from storage import load_project_data


def status_badge(appointment: Appointment) -> str:
    """HTML-метка состояния записи."""
    if appointment.is_cancelled:
        return '<span class="badge bg-secondary">отменена</span>'
    return '<span class="badge bg-success">активна</span>'


def appointment_list(request: HttpRequest) -> HttpResponse:
    """Список всех записей на консультации."""
    _, _, appointments = load_project_data()
    rows = "".join(
        f"""<tr>
            <td><a href="/appointments/{a.id}/">#{a.id}</a></td>
            <td>{a.consultation_date.strftime('%d.%m.%Y')}
                {escape(a.teacher.consultation_time)}</td>
            <td><a href="/teachers/{a.teacher.id}/">
                {escape(a.teacher.name)}</a></td>
            <td>{escape(a.student.name)}</td>
            <td>{status_badge(a)}</td>
        </tr>"""
        for a in appointments
    ) or '<tr><td colspan="5">Записей нет.</td></tr>'
    content = f"""
        <h1>Записи на консультации</h1>
        <table class="table table-striped bg-white">
            <thead><tr><th>№</th><th>Дата и время</th>
                <th>Преподаватель</th><th>Студент</th><th>Статус</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>"""
    return HttpResponse(page("Записи", content))


def appointment_detail(
    request: HttpRequest,
    appointment_id: int,
) -> HttpResponse:
    """Подробная информация о записи."""
    _, _, appointments = load_project_data()
    appointment = find_appointment_by_id(appointments, appointment_id)
    if appointment is None:
        content = f"""
            <div class="alert alert-warning">
                Запись с номером {appointment_id} не найдена.
            </div>
            <a href="/appointments/">К списку записей</a>"""
        return HttpResponse(page("Запись не найдена", content), status=404)

    teacher, student = appointment.teacher, appointment.student
    content = f"""
        <div class="card mb-3">
            <div class="card-body">
                <h1 class="card-title">Запись #{appointment.id}
                    {status_badge(appointment)}</h1>
                <p>Дата: {appointment.consultation_date.strftime('%d.%m.%Y')}
                   в {escape(teacher.consultation_time)}</p>
                <p>Преподаватель: <a href="/teachers/{teacher.id}/">
                   {escape(teacher.name)}</a>
                   ({escape(teacher.department)})</p>
                <p>Студент: {escape(student.name)}, гр.
                   {escape(student.group)}, {escape(student.email)}</p>
            </div>
        </div>
        <a href="/appointments/">К списку записей</a>"""
    return HttpResponse(page(f"Запись #{appointment.id}", content))
