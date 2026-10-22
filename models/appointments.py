"""Класс Appointment и функции записи студентов на консультации."""

from datetime import date
from typing import List, Optional

from .students import Student
from .teachers import Teacher


class Appointment:
    """Запись студента на консультацию к преподавателю."""

    def __init__(
        self,
        appointment_id: int,
        teacher: Teacher,
        student: Student,
        consultation_date: date,
        is_cancelled: bool = False,
    ) -> None:
        """Создать объект записи."""
        self.id = appointment_id
        self.teacher = teacher
        self.student = student
        self.consultation_date = consultation_date
        self.is_cancelled = is_cancelled

    @property
    def is_active(self) -> bool:
        """Запись действует, если она не отменена."""
        return not self.is_cancelled

    def cancel(self) -> None:
        """Отменить запись (объект остаётся в коллекции)."""
        self.is_cancelled = True

    def to_data(self) -> dict:
        """Преобразовать запись в словарь для JSON (ссылки -> id)."""
        return {
            "id": self.id,
            "teacher_id": self.teacher.id,
            "student_id": self.student.id,
            "consultation_date": self.consultation_date.isoformat(),
            "is_cancelled": self.is_cancelled,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление записи с учётом состояния."""
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"#{self.id}: {self.student.name} -> {self.teacher.name}, "
            f"{self.consultation_date.strftime('%d.%m.%Y')} "
            f"{self.teacher.consultation_time} ({status})"
        )


def count_active_appointments(
    appointments: List[Appointment],
    teacher: Teacher,
    consultation_date: date,
) -> int:
    """Подсчитать активные записи к преподавателю на дату."""
    return sum(
        1
        for appointment in appointments
        if appointment.is_active
        and appointment.teacher.id == teacher.id
        and appointment.consultation_date == consultation_date
    )


def is_teacher_available(
    appointments: List[Appointment],
    teacher: Teacher,
    consultation_date: date,
) -> bool:
    """Проверить, есть ли свободные места на консультации в эту дату."""
    taken = count_active_appointments(
        appointments, teacher, consultation_date
    )
    return teacher.is_suitable_for(taken + 1)


def is_student_booked(
    appointments: List[Appointment],
    teacher: Teacher,
    student: Student,
    consultation_date: date,
) -> bool:
    """Проверить, есть ли у студента активная запись на эту консультацию."""
    return any(
        appointment.is_active
        and appointment.teacher.id == teacher.id
        and appointment.student.id == student.id
        and appointment.consultation_date == consultation_date
        for appointment in appointments
    )


def create_appointment(
    appointments: List[Appointment],
    teacher: Teacher,
    student: Student,
    consultation_date: date,
) -> Optional[Appointment]:
    """Создать запись и добавить её в коллекцию.

    Возвращает None, если мест нет или студент уже записан.
    """
    if is_student_booked(appointments, teacher, student, consultation_date):
        return None
    if not is_teacher_available(appointments, teacher, consultation_date):
        return None
    appointment = Appointment(
        max((a.id for a in appointments), default=0) + 1,
        teacher,
        student,
        consultation_date,
    )
    appointments.append(appointment)
    return appointment


def find_appointment_by_id(
    appointments: List[Appointment],
    appointment_id: int,
) -> Optional[Appointment]:
    """Найти запись по идентификатору."""
    for appointment in appointments:
        if appointment.id == appointment_id:
            return appointment
    return None


def find_student_appointments(
    appointments: List[Appointment],
    student: Student,
) -> List[Appointment]:
    """Вернуть все записи студента."""
    return [a for a in appointments if a.student.id == student.id]


def cancel_appointment(
    appointments: List[Appointment],
    appointment_id: int,
) -> bool:
    """Найти активную запись и отменить её. Вернуть True при успехе."""
    appointment = find_appointment_by_id(appointments, appointment_id)
    if appointment is None or appointment.is_cancelled:
        return False
    appointment.cancel()
    return True


def get_consultation_status(is_free: bool) -> str:
    """Вернуть текстовый статус консультации (функция из ПР1)."""
    if is_free:
        return "На консультации есть свободные места."
    return "Это время уже занято."
