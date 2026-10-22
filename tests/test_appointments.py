from models import Appointment
from models.appointments import (
    cancel_appointment,
    create_appointment,
    get_consultation_status,
    is_teacher_available,
)
from tests.conftest import DAY


def test_teacher_available_without_appointments(teacher):
    assert is_teacher_available([], teacher, DAY)


def test_create_appointment_links_objects(teacher, students):
    appointments: list[Appointment] = []
    appointment = create_appointment(appointments, teacher, students[0], DAY)
    assert appointment is not None
    assert appointment.teacher is teacher
    assert appointment.student.name == "Орлова Мария"
    assert appointment in appointments


def test_capacity_limit(teacher, students):
    appointments: list[Appointment] = []
    create_appointment(appointments, teacher, students[0], DAY)
    create_appointment(appointments, teacher, students[1], DAY)
    assert not is_teacher_available(appointments, teacher, DAY)
    assert create_appointment(appointments, teacher, students[2], DAY) is None


def test_duplicate_appointment_forbidden(teacher, students):
    appointments: list[Appointment] = []
    create_appointment(appointments, teacher, students[0], DAY)
    assert create_appointment(appointments, teacher, students[0], DAY) is None


def test_cancelled_appointment_frees_seat(teacher, students):
    appointments: list[Appointment] = []
    first = create_appointment(appointments, teacher, students[0], DAY)
    create_appointment(appointments, teacher, students[1], DAY)
    assert cancel_appointment(appointments, first.id)
    assert first.is_cancelled
    assert len(appointments) == 2
    assert is_teacher_available(appointments, teacher, DAY)
    assert not cancel_appointment(appointments, first.id)


def test_get_consultation_status():
    assert get_consultation_status(False) == "Это время уже занято."
