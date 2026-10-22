from datetime import date

import pytest

from models import Student, Teacher

DAY = date(2026, 9, 20)


@pytest.fixture
def teacher() -> Teacher:
    return Teacher(1, "Сидоров П.П.", "Информатика", 2, "16:00")


@pytest.fixture
def students() -> list[Student]:
    return [
        Student(1, "Орлова Мария", "orlova@example.com", "ИВТ-21"),
        Student(2, "Волков Дмитрий", "volkov@example.com", "ПИ-22"),
        Student(3, "Соколова Анна", "sokolova@example.com", "ПИ-22"),
    ]
