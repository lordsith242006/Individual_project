from datetime import date

import pytest

from appointments import (
    cancel_appointment,
    create_appointment,
    get_consultation_status,
    is_teacher_available,
)

DAY = date(2026, 9, 20)


@pytest.fixture
def teachers() -> dict[int, dict]:
    return {
        1: {
            "name": "Сидоров П.П.",
            "department": "Информатика",
            "max_students": 2,
            "consultation_time": "16:00",
        }
    }


def test_teacher_available_without_appointments(teachers):
    assert is_teacher_available([], teachers, 1, DAY)


def test_capacity_limit(teachers):
    appointments: list[dict] = []
    create_appointment(appointments, teachers, 1, "Орлова Мария", DAY)
    create_appointment(appointments, teachers, 1, "Волков Дмитрий", DAY)
    assert not is_teacher_available(appointments, teachers, 1, DAY)
    with pytest.raises(ValueError):
        create_appointment(appointments, teachers, 1, "Третий", DAY)


def test_duplicate_appointment_forbidden(teachers):
    appointments: list[dict] = []
    create_appointment(appointments, teachers, 1, "Орлова Мария", DAY)
    with pytest.raises(ValueError):
        create_appointment(appointments, teachers, 1, "Орлова Мария", DAY)


def test_cancel_appointment(teachers):
    appointments: list[dict] = []
    appointment = create_appointment(
        appointments, teachers, 1, "Орлова Мария", DAY
    )
    assert cancel_appointment(appointments, appointment["id"])
    assert not cancel_appointment(appointments, appointment["id"])


def test_get_consultation_status():
    assert get_consultation_status(False) == "Это время уже занято."
