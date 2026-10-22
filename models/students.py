"""Класс Student и функции работы с коллекцией студентов."""

from typing import List, Optional


class Student:
    """Студент, записывающийся на консультации."""

    def __init__(
        self,
        student_id: int,
        name: str,
        email: str,
        group: str,
    ) -> None:
        """Создать объект студента."""
        self.id = student_id
        self.name = name
        self.email = email
        self.group = group

    @classmethod
    def from_data(cls, data: dict) -> "Student":
        """Создать студента из словаря (данных JSON)."""
        return cls(
            student_id=data["id"],
            name=data["name"],
            email=data["email"],
            group=data["group"],
        )

    def to_data(self) -> dict:
        """Преобразовать студента в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "group": self.group,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление студента."""
        return f"{self.name}, гр. {self.group} <{self.email}>"


def add_student(
    students: List[Student],
    name: str,
    email: str,
    group: str,
) -> Student:
    """Создать объект Student, добавить его в коллекцию и вернуть."""
    if find_student_by_email(students, email) is not None:
        raise ValueError("Студент с таким email уже зарегистрирован")
    student_id = max((s.id for s in students), default=0) + 1
    student = Student(student_id, name, email, group)
    students.append(student)
    return student


def find_student(students: List[Student], query: str) -> List[Student]:
    """Найти студентов по подстроке имени или email."""
    query = query.lower()
    return [
        student for student in students
        if query in student.name.lower() or query in student.email.lower()
    ]


def find_student_by_id(
    students: List[Student],
    student_id: int,
) -> Optional[Student]:
    """Найти студента по идентификатору."""
    for student in students:
        if student.id == student_id:
            return student
    return None


def find_student_by_email(
    students: List[Student],
    email: str,
) -> Optional[Student]:
    """Найти студента по email (без учёта регистра)."""
    for student in students:
        if student.email.lower() == email.lower():
            return student
    return None
