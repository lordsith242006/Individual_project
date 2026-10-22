"""Функции для работы с преподавателями."""

from typing import Iterator


def add_teacher(
    teachers: dict[int, dict],
    name: str,
    department: str,
    max_students: int,
    consultation_time: str,
) -> int:
    """Добавить преподавателя в словарь teachers.

    Идентификатор формируется как максимальный существующий + 1.
    Возвращает идентификатор нового преподавателя.
    """
    if max_students <= 0:
        raise ValueError("Количество мест должно быть положительным")
    teacher_id = max(teachers, default=0) + 1
    teachers[teacher_id] = {
        "name": name,
        "department": department,
        "max_students": max_students,
        "consultation_time": consultation_time,
    }
    return teacher_id


def find_teacher(teachers: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти преподавателей по подстроке ФИО (без учёта регистра)."""
    query = query.lower()
    return {
        teacher_id: teacher
        for teacher_id, teacher in teachers.items()
        if query in teacher["name"].lower()
    }


def find_teacher_id_by_name(teachers: dict[int, dict], name: str) -> int:
    """Вернуть идентификатор преподавателя по точному ФИО.

    Если преподаватель не найден, выбрасывается KeyError.
    """
    for teacher_id, teacher in teachers.items():
        if teacher["name"].lower() == name.lower():
            return teacher_id
    raise KeyError(f"Преподаватель «{name}» не найден")


def check_teacher_capacity(
    teachers: dict[int, dict],
    teacher_id: int,
    students_count: int,
) -> bool:
    """Проверить, хватит ли мест на консультации для students_count."""
    return teachers[teacher_id]["max_students"] >= students_count


def iter_teachers_by_capacity(
    teachers: dict[int, dict],
    min_students: int,
) -> Iterator[tuple[int, dict]]:
    """Генератор преподавателей, принимающих не меньше min_students."""
    for teacher_id, teacher in teachers.items():
        if teacher["max_students"] >= min_students:
            yield teacher_id, teacher


def filter_teachers_by_capacity(
    teachers: dict[int, dict],
    min_students: int,
) -> dict[int, dict]:
    """Отобрать преподавателей по количеству мест на консультации."""
    return dict(iter_teachers_by_capacity(teachers, min_students))


def filter_teachers_by_department(
    teachers: dict[int, dict],
    department: str,
) -> dict[int, dict]:
    """Отобрать преподавателей указанной кафедры."""
    return {
        teacher_id: teacher
        for teacher_id, teacher in teachers.items()
        if teacher["department"].lower() == department.lower()
    }


def sort_teachers(
    teachers: dict[int, dict],
    key: str = "name",
) -> list[tuple[int, dict]]:
    """Отсортировать преподавателей по полю key (name или max_students)."""
    return sorted(teachers.items(), key=lambda item: item[1][key])
