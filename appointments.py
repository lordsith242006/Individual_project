"""Функции для записи студентов на консультации."""

from datetime import date


def count_appointments(
    appointments: list[dict],
    teacher_id: int,
    consultation_date: date,
) -> int:
    """Подсчитать записи к преподавателю на указанную дату."""
    date_text = consultation_date.isoformat()
    return sum(
        1
        for appointment in appointments
        if appointment["teacher_id"] == teacher_id
        and appointment["consultation_date"] == date_text
    )


def is_teacher_available(
    appointments: list[dict],
    teachers: dict[int, dict],
    teacher_id: int,
    consultation_date: date,
) -> bool:
    """Проверить, есть ли свободные места на консультации в эту дату."""
    taken = count_appointments(appointments, teacher_id, consultation_date)
    return taken < teachers[teacher_id]["max_students"]


def is_student_booked(
    appointments: list[dict],
    teacher_id: int,
    student_name: str,
    consultation_date: date,
) -> bool:
    """Проверить, записан ли студент к преподавателю на эту дату."""
    date_text = consultation_date.isoformat()
    for appointment in appointments:
        if (
            appointment["teacher_id"] == teacher_id
            and appointment["consultation_date"] == date_text
            and appointment["student_name"] == student_name
        ):
            return True
    return False


def create_appointment(
    appointments: list[dict],
    teachers: dict[int, dict],
    teacher_id: int,
    student_name: str,
    consultation_date: date,
) -> dict:
    """Записать студента на консультацию.

    Выбрасывает ValueError, если мест нет или студент уже записан.
    """
    if teacher_id not in teachers:
        raise KeyError(f"Преподаватель с id={teacher_id} не найден")
    if is_student_booked(
        appointments, teacher_id, student_name, consultation_date
    ):
        raise ValueError("Студент уже записан на эту консультацию")
    if not is_teacher_available(
        appointments, teachers, teacher_id, consultation_date
    ):
        raise ValueError("Свободных мест на консультации нет")
    appointment = {
        "id": max((a["id"] for a in appointments), default=0) + 1,
        "teacher_id": teacher_id,
        "student_name": student_name,
        "consultation_date": consultation_date.isoformat(),
    }
    appointments.append(appointment)
    return appointment


def cancel_appointment(appointments: list[dict], appointment_id: int) -> bool:
    """Отменить запись по идентификатору. Вернуть True, если она найдена."""
    for index, appointment in enumerate(appointments):
        if appointment["id"] == appointment_id:
            del appointments[index]
            return True
    return False


def get_consultation_status(is_free: bool) -> str:
    """Вернуть текстовый статус консультации (функция из ПР1)."""
    if is_free:
        return "На консультации есть свободные места."
    return "Это время уже занято."
