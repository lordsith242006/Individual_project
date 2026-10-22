import pytest

from models import Teacher
from models.teachers import (
    add_teacher,
    check_teacher_capacity,
    filter_teachers_by_capacity,
    find_teacher,
    sort_teachers,
)


@pytest.fixture
def teachers() -> list[Teacher]:
    data: list[Teacher] = []
    add_teacher(data, "Петрова А.А.", "Математика", 5, "12:30")
    add_teacher(data, "Иванов И.И.", "Информатика", 3, "14:00")
    return data


def test_teacher_object(teacher):
    assert teacher.name == "Сидоров П.П."
    assert teacher.is_suitable_for(2)
    assert not teacher.is_suitable_for(3)
    assert "Сидоров П.П." in str(teacher)


def test_validate_max_students():
    assert Teacher.validate_max_students(10)
    assert not Teacher.validate_max_students(0)
    with pytest.raises(ValueError):
        Teacher(1, "Ошибка", "Кафедра", -1, "10:00")


def test_from_data_and_to_data(teacher):
    assert Teacher.from_data(teacher.to_data()).to_data() == teacher.to_data()


def test_add_teacher(teachers):
    assert len(teachers) == 2
    assert isinstance(teachers[1], Teacher)
    assert teachers[1].id == 2


def test_find_teacher(teachers):
    assert [t.name for t in find_teacher(teachers, "иванов")] == [
        "Иванов И.И."
    ]


def test_check_teacher_capacity(teachers):
    assert check_teacher_capacity(teachers, 1, 5)
    assert not check_teacher_capacity(teachers, 2, 4)
    assert not check_teacher_capacity(teachers, 99, 1)


def test_filter_and_sort(teachers):
    assert [t.id for t in filter_teachers_by_capacity(teachers, 4)] == [1]
    assert [t.id for t in sort_teachers(teachers)] == [2, 1]
    assert [t.id for t in sort_teachers(teachers, "max_students")] == [2, 1]
