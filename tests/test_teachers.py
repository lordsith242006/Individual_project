import pytest

from teachers import (
    add_teacher,
    check_teacher_capacity,
    filter_teachers_by_capacity,
    find_teacher,
    sort_teachers,
)


@pytest.fixture
def teachers() -> dict[int, dict]:
    data: dict[int, dict] = {}
    add_teacher(data, "Иванов И.И.", "Информатика", 3, "14:00")
    add_teacher(data, "Петрова А.А.", "Математика", 5, "12:30")
    return data


def test_add_teacher(teachers):
    assert len(teachers) == 2
    assert teachers[2]["name"] == "Петрова А.А."


def test_add_teacher_invalid_capacity(teachers):
    with pytest.raises(ValueError):
        add_teacher(teachers, "Сидоров П.П.", "Информатика", 0, "16:00")


def test_find_teacher(teachers):
    assert list(find_teacher(teachers, "иванов")) == [1]


def test_check_teacher_capacity(teachers):
    assert check_teacher_capacity(teachers, 2, 5)
    assert not check_teacher_capacity(teachers, 1, 4)


def test_filter_and_sort(teachers):
    assert list(filter_teachers_by_capacity(teachers, 4)) == [2]
    by_capacity = sort_teachers(teachers, "max_students")
    assert [teacher_id for teacher_id, _ in by_capacity] == [1, 2]
