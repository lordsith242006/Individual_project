"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
from pathlib import Path


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


def load_teachers(filename: str | Path) -> dict[int, dict]:
    """Загрузить преподавателей: список JSON -> словарь {id: данные}."""
    teachers = {}
    for item in load_json(filename):
        teacher = dict(item)
        teachers[teacher.pop("id")] = teacher
    return teachers


def save_teachers(filename: str | Path, teachers: dict[int, dict]) -> None:
    """Сохранить преподавателей: словарь {id: данные} -> список JSON."""
    data = [
        {"id": teacher_id, **teacher}
        for teacher_id, teacher in teachers.items()
    ]
    save_json(filename, data)


def load_appointments(filename: str | Path) -> list[dict]:
    """Загрузить записи на консультации."""
    return load_json(filename)


def save_appointments(filename: str | Path, appointments: list[dict]) -> None:
    """Сохранить записи на консультации."""
    save_json(filename, appointments)
