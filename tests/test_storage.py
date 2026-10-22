from storage import load_json, load_teachers, save_teachers


def test_save_and_load_teachers(tmp_path):
    filename = tmp_path / "teachers.json"
    teachers = {
        1: {
            "name": "Иванов И.И.",
            "department": "Информатика",
            "max_students": 3,
            "consultation_time": "14:00",
        }
    }
    save_teachers(filename, teachers)
    assert load_teachers(filename) == teachers


def test_load_missing_file(tmp_path):
    assert load_json(tmp_path / "missing.json") == []


def test_load_broken_file(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{not json", encoding="utf-8")
    assert load_json(filename) == []
