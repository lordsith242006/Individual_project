"""Класс Teacher и функции работы с коллекцией преподавателей."""

from typing import Iterator, List, Optional


class Teacher:
    """Преподаватель, проводящий консультации."""

    def __init__(
        self,
        teacher_id: int,
        name: str,
        department: str,
        max_students: int,
        consultation_time: str,
    ) -> None:
        """Создать объект преподавателя."""
        if not Teacher.validate_max_students(max_students):
            raise ValueError("Количество мест должно быть положительным")
        self.id = teacher_id
        self.name = name
        self.department = department
        self.max_students = max_students
        self.consultation_time = consultation_time

    @staticmethod
    def validate_max_students(max_students: int) -> bool:
        """Проверить корректность количества мест на консультации."""
        return isinstance(max_students, int) and max_students > 0

    @classmethod
    def from_data(cls, data: dict) -> "Teacher":
        """Создать преподавателя из словаря (данных JSON)."""
        return cls(
            teacher_id=data["id"],
            name=data["name"],
            department=data["department"],
            max_students=data["max_students"],
            consultation_time=data["consultation_time"],
        )

    def to_data(self) -> dict:
        """Преобразовать преподавателя в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "max_students": self.max_students,
            "consultation_time": self.consultation_time,
        }

    def is_suitable_for(self, students_count: int) -> bool:
        """Проверить, хватит ли мест на консультации для students_count."""
        return self.max_students >= students_count

    def __str__(self) -> str:
        """Вернуть строковое представление преподавателя."""
        return (
            f"{self.name} ({self.department}), консультации в "
            f"{self.consultation_time}, мест: {self.max_students}"
        )


def add_teacher(
    teachers: List[Teacher],
    name: str,
    department: str,
    max_students: int,
    consultation_time: str,
) -> Teacher:
    """Создать объект Teacher, добавить его в коллекцию и вернуть."""
    teacher_id = max((t.id for t in teachers), default=0) + 1
    teacher = Teacher(
        teacher_id, name, department, max_students, consultation_time
    )
    teachers.append(teacher)
    return teacher


def find_teacher(teachers: List[Teacher], query: str) -> List[Teacher]:
    """Найти преподавателей по подстроке ФИО (без учёта регистра)."""
    query = query.lower()
    return [teacher for teacher in teachers if query in teacher.name.lower()]


def find_teacher_by_id(
    teachers: List[Teacher],
    teacher_id: int,
) -> Optional[Teacher]:
    """Найти преподавателя по идентификатору."""
    for teacher in teachers:
        if teacher.id == teacher_id:
            return teacher
    return None


def find_teacher_by_name(
    teachers: List[Teacher],
    name: str,
) -> Optional[Teacher]:
    """Найти преподавателя по точному ФИО (без учёта регистра)."""
    for teacher in teachers:
        if teacher.name.lower() == name.lower():
            return teacher
    return None


def check_teacher_capacity(
    teachers: List[Teacher],
    teacher_id: int,
    students_count: int,
) -> bool:
    """Найти преподавателя и проверить количество мест."""
    teacher = find_teacher_by_id(teachers, teacher_id)
    return teacher is not None and teacher.is_suitable_for(students_count)


def iter_teachers_by_capacity(
    teachers: List[Teacher],
    min_students: int,
) -> Iterator[Teacher]:
    """Генератор преподавателей, принимающих не меньше min_students."""
    for teacher in teachers:
        if teacher.is_suitable_for(min_students):
            yield teacher


def filter_teachers_by_capacity(
    teachers: List[Teacher],
    min_students: int,
) -> List[Teacher]:
    """Отобрать преподавателей по количеству мест на консультации."""
    return list(iter_teachers_by_capacity(teachers, min_students))


def filter_teachers_by_department(
    teachers: List[Teacher],
    department: str,
) -> List[Teacher]:
    """Отобрать преподавателей указанной кафедры."""
    return [
        teacher for teacher in teachers
        if teacher.department.lower() == department.lower()
    ]


def sort_teachers(
    teachers: List[Teacher],
    key: str = "name",
) -> List[Teacher]:
    """Отсортировать преподавателей по атрибуту key."""
    return sorted(teachers, key=lambda teacher: getattr(teacher, key))
