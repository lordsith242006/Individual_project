"""Сервис планирования консультационных часов: консольная версия."""

from pathlib import Path

from appointments import (
    cancel_appointment,
    create_appointment,
    get_consultation_status,
    is_teacher_available,
)
from storage import (
    load_appointments,
    load_teachers,
    save_appointments,
    save_teachers,
)
from teachers import (
    add_teacher,
    check_teacher_capacity,
    filter_teachers_by_capacity,
    find_teacher,
    find_teacher_id_by_name,
    sort_teachers,
)
from utils import format_date, input_date, input_int, input_text

DATA_DIR = Path(__file__).resolve().parent / "data"
TEACHERS_FILE = DATA_DIR / "teachers.json"
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
0. Выход"""


def show_teachers(teachers: dict[int, dict]) -> None:
    """Вывести список преподавателей в виде таблицы."""
    if not teachers:
        print("Преподаватели не найдены.")
        return
    print(f"{'ID':<4}{'ФИО':<22}{'Кафедра':<26}{'Время':<8}{'Мест':>5}")
    for teacher_id, teacher in sort_teachers(teachers):
        print(
            f"{teacher_id:<4}{teacher['name']:<22}"
            f"{teacher['department']:<26}"
            f"{teacher['consultation_time']:<8}"
            f"{teacher['max_students']:>5}"
        )


def show_appointments(
    appointments: list[dict],
    teachers: dict[int, dict],
) -> None:
    """Вывести список записей с ФИО преподавателя и датой."""
    if not appointments:
        print("Записей нет.")
        return
    for appointment in appointments:
        teacher = teachers.get(appointment["teacher_id"], {})
        print(
            f"#{appointment['id']}: {appointment['student_name']} -> "
            f"{teacher.get('name', '?')}, "
            f"{format_date(appointment['consultation_date'])} "
            f"{teacher.get('consultation_time', '')}"
        )


def ask_teacher_id(teachers: dict[int, dict]) -> int | None:
    """Запросить ФИО преподавателя и вернуть его id (или None)."""
    name = input_text("ФИО преподавателя: ")
    try:
        return find_teacher_id_by_name(teachers, name)
    except KeyError as error:
        print(error.args[0])
        return None


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    teachers = load_teachers(TEACHERS_FILE)
    appointments = load_appointments(APPOINTMENTS_FILE)

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
            teacher_id = ask_teacher_id(teachers)
            if teacher_id is not None:
                count = input_int("Сколько студентов придёт: ")
                if check_teacher_capacity(teachers, teacher_id, count):
                    print("Мест на консультации достаточно.")
                else:
                    print("Мест на консультации недостаточно.")
        elif choice == "5":
            teacher_id = ask_teacher_id(teachers)
            if teacher_id is not None:
                day = input_date("Дата (ДД.ММ.ГГГГ): ")
                print(get_consultation_status(
                    is_teacher_available(
                        appointments, teachers, teacher_id, day
                    )
                ))
        elif choice == "6":
            teacher_id = ask_teacher_id(teachers)
            if teacher_id is not None:
                student = input_text("ФИО студента: ")
                day = input_date("Дата (ДД.ММ.ГГГГ): ")
                try:
                    appointment = create_appointment(
                        appointments, teachers, teacher_id, student, day
                    )
                except ValueError as error:
                    print(error)
                else:
                    save_appointments(APPOINTMENTS_FILE, appointments)
                    print(f"Студент {student} записан на консультацию "
                          f"(запись #{appointment['id']}).")
        elif choice == "7":
            appointment_id = input_int("Номер записи: ")
            if cancel_appointment(appointments, appointment_id):
                save_appointments(APPOINTMENTS_FILE, appointments)
                print("Запись отменена.")
            else:
                print("Запись не найдена.")
        elif choice == "8":
            show_appointments(appointments, teachers)
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
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
