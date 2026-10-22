from models import Appointment
from storage import (
    load_appointments,
    load_json,
    load_teachers,
    save_appointments,
    save_teachers,
)
from tests.conftest import DAY


def test_save_and_load_teachers(tmp_path, teacher):
    filename = tmp_path / "teachers.json"
    save_teachers(filename, [teacher])
    loaded = load_teachers(filename)
    assert [t.to_data() for t in loaded] == [teacher.to_data()]


def test_appointments_restore_links(tmp_path, teacher, students):
    filename = tmp_path / "appointments.json"
    save_appointments(filename, [Appointment(1, teacher, students[1], DAY)])
    loaded = load_appointments(filename, [teacher], students)
    assert loaded[0].teacher is teacher
    assert loaded[0].student is students[1]
    assert loaded[0].consultation_date == DAY


def test_load_missing_file(tmp_path):
    assert load_json(tmp_path / "missing.json") == []


def test_load_broken_file(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{not json", encoding="utf-8")
    assert load_json(filename) == []
