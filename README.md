# Сервис планирования консультационных часов

Приложение для записи студентов на консультации к преподавателям.
Предметная область представлена объектной моделью (классы `Teacher`,
`Student`, `Appointment`). Проект имеет консольную версию (`main.py`)
и веб-интерфейс на Django (проект `consultplan`).

## Целевая аудитория
Студенты и преподаватели.

## Предметная область
Организация консультаций: выбор преподавателя, проверка свободных мест
на выбранную дату, создание и отмена записи студента.

## Основные классы

### Teacher — преподаватель
Атрибуты: `id`, `name`, `department`, `max_students` (мест на консультации),
`consultation_time`.
Методы:
* `is_suitable_for(students_count)` — хватит ли мест;
* `validate_max_students()` — `@staticmethod`, проверка количества мест;
* `from_data()` — `@classmethod`, создание объекта из данных JSON;
* `to_data()` — преобразование в словарь для JSON;
* `__str__()`.

### Student — студент
Атрибуты: `id`, `name`, `email`, `group`.
Методы: `from_data()` (`@classmethod`), `to_data()`, `__str__()`.

### Appointment — запись на консультацию
Атрибуты: `id`, `teacher` (объект `Teacher`), `student` (объект `Student`),
`consultation_date`, `is_cancelled`.
Методы:
* `cancel()` — отмена записи (объект остаётся в коллекции);
* `is_active` — `@property`, запись не отменена;
* `to_data()`, `__str__()`.

## Взаимодействие объектов
```
appointment
 ├── teacher → Teacher
 └── student → Student
```
Запись хранит ссылки на объекты, поэтому данные доступны напрямую:
`appointment.teacher.name`, `appointment.student.email`.
Активные записи занимают места у преподавателя на дату; отменённая запись
место не занимает. В JSON сохраняются только идентификаторы
(`teacher_id`, `student_id`), при загрузке они заменяются ссылками на объекты.

## Основные операции
* преподаватели: `add_teacher()`, `find_teacher()`, `find_teacher_by_id()`,
  `check_teacher_capacity()`, `filter_teachers_by_capacity()`,
  `filter_teachers_by_department()`, `sort_teachers()`;
* студенты: `add_student()`, `find_student()`, `find_student_by_email()`;
* записи: `is_teacher_available()`, `create_appointment()`,
  `cancel_appointment()`, `get_consultation_status()` (функция из ПР1).

## Веб-интерфейс (Django)
Технологии: Python, Django 5.2, HTML, CSS и Bootstrap 5.3.

Django-приложения:
* `homepage` — главная страница, общий HTML-каркас `page()`, страница 404;
* `teachers` — список преподавателей (поиск по ФИО, отбор по местам)
  и карточка преподавателя;
* `appointments` — список записей и страница отдельной записи.

| URL | View | Страница |
|-----|------|----------|
| `/` | `homepage.views.index` | главная |
| `/teachers/` | `teachers.views.teacher_list` | преподаватели |
| `/teachers/<id>/` | `teachers.views.teacher_detail` | преподаватель |
| `/appointments/` | `appointments.views.appointment_list` | записи |
| `/appointments/<id>/` | `appointments.views.appointment_detail` | запись |

View-функции получают данные через `storage.load_project_data()`
(JSON → объекты `Teacher`, `Student`, `Appointment`) и формируют HTML-ответ.
Для несуществующих объектов возвращается код 404.

## Структура проекта
```
Individual_project/
├── README.md
├── requirements.txt
├── manage.py            — управление Django-проектом
├── consultplan/         — настройки и корневые маршруты Django
├── homepage/            — приложение главной страницы
├── teachers/            — приложение преподавателей
├── appointments/        — приложение записей
├── main.py              — консольная версия: меню, вывод данных
├── storage.py           — JSON ↔ объекты
├── utils.py             — безопасный ввод чисел, дат и строк
├── models/
│   ├── __init__.py
│   ├── teachers.py      — класс Teacher и функции коллекции
│   ├── students.py      — класс Student и функции коллекции
│   └── appointments.py  — класс Appointment и функции записи
├── data/
│   ├── teachers.json
│   ├── students.json
│   └── appointments.json
└── tests/
    ├── conftest.py
    ├── test_teachers.py
    ├── test_students.py
    ├── test_appointments.py
    ├── test_storage.py
    └── test_web.py      — проверка страниц Django
```

## Требования
- Python 3.10+;
- Django 5.2;
- pytest, flake8.

```
python -m venv venv
venv\Scriptsctivate
pip install -r requirements.txt
```

## Запуск веб-приложения
```
python manage.py runserver
```
Адрес: http://127.0.0.1:8000/

## Запуск консольной версии
```
python main.py
```

## Тестирование
```
pytest -v
```

## Проверка качества кода
```
flake8
```

## План развития
- шаблоны Django и статические файлы;
- база данных;
- пользователи и авторизация;
- REST API, Docker, CI/CD.
