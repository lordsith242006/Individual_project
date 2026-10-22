import sqlite3

import pytest

from db.database import fetch_all, fetch_one, get_connection
from db.import_json import import_all


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test.sqlite"
    import_all(path)
    return path


def test_import_counts(tmp_path):
    counts = import_all(tmp_path / "test.sqlite")
    assert counts == {"teachers": 4, "students": 4, "appointments": 5}


def test_rows_accessible_by_name(db_path):
    teacher = fetch_one(
        "SELECT name, max_students FROM teachers WHERE id = ?",
        (1,),
        db_path,
    )
    assert teacher["name"] == "Иванов И.И."
    assert teacher["max_students"] == 3


def test_join_appointment_with_names(db_path):
    rows = fetch_all(
        """
        SELECT t.name AS teacher_name, s.name AS student_name
        FROM appointments AS a
        JOIN teachers AS t ON t.id = a.teacher_id
        JOIN students AS s ON s.id = a.student_id
        WHERE a.id = ?
        """,
        (2,),
        db_path,
    )
    assert dict(rows[0]) == {
        "teacher_name": "Сидоров П.П.",
        "student_name": "Орлова Мария",
    }


def test_case_insensitive_cyrillic_search(db_path):
    rows = fetch_all(
        "SELECT name FROM teachers WHERE py_lower(name) LIKE ?",
        ("%петров%",),
        db_path,
    )
    assert [row["name"] for row in rows] == ["Петрова А.А."]


def test_foreign_keys_enforced(db_path):
    conn = get_connection(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO appointments "
            "(teacher_id, student_id, consultation_date) VALUES (?, ?, ?)",
            (999, 1, "2026-09-30"),
        )
    conn.close()
