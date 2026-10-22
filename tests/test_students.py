import pytest

from models import Student
from models.students import add_student, find_student, find_student_by_id


def test_student_object():
    student = Student(1, "Орлова Мария", "orlova@example.com", "ИВТ-21")
    assert student.email == "orlova@example.com"
    assert "ИВТ-21" in str(student)


def test_from_data():
    data = {"id": 5, "name": "Тест", "email": "t@example.com", "group": "А"}
    student = Student.from_data(data)
    assert student.id == 5
    assert student.to_data() == data


def test_add_and_find_student(students):
    student = add_student(students, "Новиков Олег", "new@example.com", "А")
    assert student.id == 4
    assert find_student_by_id(students, 4) is student
    assert find_student(students, "NEW@") == [student]


def test_duplicate_email_forbidden(students):
    with pytest.raises(ValueError):
        add_student(students, "Двойник", "ORLOVA@example.com", "А")
