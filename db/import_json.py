"""Перенос данных проекта из JSON-файлов в базу SQLite.

Запуск из корня проекта:
    python -m db.import_json
"""

import json
import sqlite3
from pathlib import Path

from db.database import BASE_DIR, DB_PATH, create_schema, get_connection

DATA_DIR = BASE_DIR / "data"
TEACHERS_FILE = DATA_DIR / "teachers.json"
STUDENTS_FILE = DATA_DIR / "students.json"
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"


def load_json(filename: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_teachers(conn: sqlite3.Connection, filename: Path) -> int:
    """Перенести преподавателей. Вернуть количество записей."""
    rows = [
        (
            item["id"],
            item["name"],
            item["department"],
            item["max_students"],
            item["consultation_time"],
        )
        for item in load_json(filename)
    ]
    conn.executemany(
        "INSERT INTO teachers "
        "(id, name, department, max_students, consultation_time) "
        "VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def import_students(conn: sqlite3.Connection, filename: Path) -> int:
    """Перенести студентов. Вернуть количество записей."""
    rows = [
        (item["id"], item["name"], item["email"], item["group"])
        for item in load_json(filename)
    ]
    conn.executemany(
        "INSERT INTO students (id, name, email, group_name) "
        "VALUES (?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def import_appointments(conn: sqlite3.Connection, filename: Path) -> int:
    """Перенести записи на консультации. Вернуть количество записей."""
    rows = [
        (
            item["id"],
            item["teacher_id"],
            item["student_id"],
            item["consultation_date"],
            int(item.get("is_cancelled", False)),
        )
        for item in load_json(filename)
    ]
    conn.executemany(
        "INSERT INTO appointments "
        "(id, teacher_id, student_id, consultation_date, is_cancelled) "
        "VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def import_all(
    db_path: str | Path = DB_PATH,
    data_dir: Path = DATA_DIR,
) -> dict[str, int]:
    """Пересоздать таблицы и перенести в них все JSON-данные."""
    conn = get_connection(db_path)
    try:
        create_schema(conn)
        counts = {
            "teachers": import_teachers(conn, data_dir / TEACHERS_FILE.name),
            "students": import_students(conn, data_dir / STUDENTS_FILE.name),
            "appointments": import_appointments(
                conn, data_dir / APPOINTMENTS_FILE.name
            ),
        }
        conn.commit()
    except (OSError, json.JSONDecodeError, KeyError, sqlite3.Error):
        conn.rollback()
        raise
    finally:
        conn.close()
    return counts


def main() -> None:
    """Выполнить импорт и вывести количество перенесённых записей."""
    for table, count in import_all().items():
        print(f"{table}: {count}")
    print(f"База данных: {DB_PATH}")


if __name__ == "__main__":
    main()
