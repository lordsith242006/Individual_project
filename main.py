"""Сервис планирования консультационных часов: консольная версия."""

from pathlib import Path
from typing import List, Optional

from models import Appointment, Student, Teacher
from models.appointments import (
    cancel_appointment,
    create_appointment,
    get_consultation_status,
    is_student_booked,
    is_teacher_available,
)
from models.students import add_student, find_student, find_student_by_email
from models.teachers import (
    add_teacher,
    check_teacher_capacity,
    filter_teachers_by_capacity,
    find_teacher,
    find_teacher_by_name,
    sort_teachers,
)
from storage import (
    load_appointments,
    load_students,
    load_teachers,
    save_appointments,
    save_students,
    save_teachers,
)
from utils import input_date, input_int, input_text

DATA_DIR = Path(__file__).resolve().parent / "data"
TEACHERS_FILE = DATA_DIR / "teachers.json"
STUDENTS_FILE = DATA_DIR / "students.json"
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"

MENU = """
=== Сервис планирования консультаций ===
1. Показать преподавателей
2. Найти преподавателя по ФИО
3. Показать преподавателей с достаточным числом мест
4. Проверить количество мест
5. Проверить наличие мест на дату
6. Записаться на консультацию
7. Отменить запись
8. Показать записи
9. Добавить преподавателя
10. Показать студентов
11. Найти студента
12. Зарегистрировать студента
0. Выход"""


def show_teachers(teachers: List[Teacher]) -> None:
    """Вывести преподавателей, отсортированных по ФИО."""
    if not teachers:
        print("Преподаватели не найдены.")
        return
    for teacher in sort_teachers(teachers):
        print(f"[{teacher.id}] {teacher}")


def show_students(students: List[Student]) -> None:
    """Вывести список студентов."""
    if not students:
        print("Студенты не найдены.")
        return
    for student in students:
        print(f"[{student.id}] {student}")


def show_appointments(appointments: List[Appointment]) -> None:
    """Вывести список записей с указанием состояния."""
    if not appointments:
        print("Записей нет.")
        return
    for appointment in appointments:
        print(appointment)


def ask_teacher(teachers: List[Teacher]) -> Optional[Teacher]:
    """Запросить ФИО преподавателя и вернуть объект (или None)."""
    teacher = find_teacher_by_name(teachers, input_text("ФИО преподавателя: "))
    if teacher is None:
        print("Преподаватель не найден.")
    return teacher


def ask_student(students: List[Student]) -> Optional[Student]:
    """Запросить email студента и вернуть объект (или None)."""
    student = find_student_by_email(students, input_text("Email студента: "))
    if student is None:
        print("Студент не найден. Сначала зарегистрируйте его (пункт 12).")
    return student


def book(
    appointments: List[Appointment],
    teachers: List[Teacher],
    students: List[Student],
) -> None:
    """Сценарий записи студента на консультацию."""
    teacher = ask_teacher(teachers)
    if teacher is None:
        return
    student = ask_student(students)
    if student is None:
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    appointment = create_appointment(appointments, teacher, student, day)
    if appointment is None:
        if is_student_booked(appointments, teacher, student, day):
            print("Студент уже записан на эту консультацию.")
        else:
            print(get_consultation_status(False))
        return
    save_appointments(APPOINTMENTS_FILE, appointments)
    print(f"Студент {student.name} записан на консультацию: {appointment}")


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    teachers = load_teachers(TEACHERS_FILE)
    students = load_students(STUDENTS_FILE)
    appointments = load_appointments(APPOINTMENTS_FILE, teachers, students)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_teachers(teachers)
        elif choice == "2":
            show_teachers(find_teacher(teachers, input_text("Запрос: ")))
        elif choice == "3":
            count = input_int("Сколько студентов придёт: ")
            show_teachers(filter_teachers_by_capacity(teachers, count))
        elif choice == "4":
            teacher = ask_teacher(teachers)
            if teacher is not None:
                count = input_int("Сколько студентов придёт: ")
                if check_teacher_capacity(teachers, teacher.id, count):
                    print("Мест на консультации достаточно.")
                else:
                    print("Мест на консультации недостаточно.")
        elif choice == "5":
            teacher = ask_teacher(teachers)
            if teacher is not None:
                day = input_date("Дата (ДД.ММ.ГГГГ): ")
                print(get_consultation_status(
                    is_teacher_available(appointments, teacher, day)
                ))
        elif choice == "6":
            book(appointments, teachers, students)
        elif choice == "7":
            appointment_id = input_int("Номер записи: ")
            if cancel_appointment(appointments, appointment_id):
                save_appointments(APPOINTMENTS_FILE, appointments)
                print("Запись отменена.")
            else:
                print("Активная запись с таким номером не найдена.")
        elif choice == "8":
            show_appointments(appointments)
        elif choice == "9":
            name = input_text("ФИО: ")
            department = input_text("Кафедра: ")
            max_students = input_int("Мест на консультации: ")
            time = input_text("Время консультации (ЧЧ:ММ): ")
            try:
                add_teacher(teachers, name, department, max_students, time)
            except ValueError as error:
                print(error)
            else:
                save_teachers(TEACHERS_FILE, teachers)
                print("Преподаватель добавлен.")
        elif choice == "10":
            show_students(students)
        elif choice == "11":
            show_students(find_student(students, input_text("Запрос: ")))
        elif choice == "12":
            name = input_text("ФИО: ")
            email = input_text("Email: ")
            group = input_text("Группа: ")
            try:
                add_student(students, name, email, group)
            except ValueError as error:
                print(error)
            else:
                save_students(STUDENTS_FILE, students)
                print("Студент зарегистрирован.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
