"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
from datetime import date
from pathlib import Path
from typing import List

from models import Appointment, Student, Teacher
from models.students import find_student_by_id
from models.teachers import find_teacher_by_id


def load_json(filename: str | Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    При отсутствии файла или некорректном JSON возвращается пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные не загружены.")
        return []
    if not isinstance(data, list):
        print(f"Файл {filename} имеет неверный формат.")
        return []
    return data


def save_json(filename: str | Path, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_teachers(filename: str | Path) -> List[Teacher]:
    """Загрузить преподавателей: JSON -> объекты Teacher."""
    teachers = []
    for item in load_json(filename):
        try:
            teachers.append(Teacher.from_data(item))
        except (KeyError, ValueError):
            print(f"Пропущена некорректная запись преподавателя: {item}")
    return teachers


def save_teachers(filename: str | Path, teachers: List[Teacher]) -> None:
    """Сохранить преподавателей: объекты Teacher -> JSON."""
    save_json(filename, [teacher.to_data() for teacher in teachers])


def load_students(filename: str | Path) -> List[Student]:
    """Загрузить студентов: JSON -> объекты Student."""
    students = []
    for item in load_json(filename):
        try:
            students.append(Student.from_data(item))
        except KeyError:
            print(f"Пропущена некорректная запись студента: {item}")
    return students


def save_students(filename: str | Path, students: List[Student]) -> None:
    """Сохранить студентов: объекты Student -> JSON."""
    save_json(filename, [student.to_data() for student in students])


def load_appointments(
    filename: str | Path,
    teachers: List[Teacher],
    students: List[Student],
) -> List[Appointment]:
    """Загрузить записи: JSON -> объекты Appointment.

    Идентификаторы teacher_id и student_id заменяются ссылками на объекты.
    """
    appointments = []
    for item in load_json(filename):
        try:
            teacher = find_teacher_by_id(teachers, item["teacher_id"])
            student = find_student_by_id(students, item["student_id"])
            if teacher is None or student is None:
                raise LookupError
            appointments.append(Appointment(
                item["id"],
                teacher,
                student,
                date.fromisoformat(item["consultation_date"]),
                item.get("is_cancelled", False),
            ))
        except (KeyError, LookupError, ValueError):
            print(f"Пропущена некорректная запись: {item}")
    return appointments


def save_appointments(
    filename: str | Path,
    appointments: List[Appointment],
) -> None:
    """Сохранить записи: объекты Appointment -> JSON."""
    save_json(filename, [a.to_data() for a in appointments])
