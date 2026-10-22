# Сервис планирования консультационных часов (КонсультПлан)

Приложение для записи студентов на консультации к преподавателям.
Проект развивается от работы к работе:

| Этап | Что добавлено |
|------|---------------|
| ПР1 | простая программа: один преподаватель, одна дата, одна запись |
| ПР2 | коллекции, функции, модули, исключения, JSON-файлы, pytest, flake8 |
| ПР3 | объектная модель: `Teacher`, `Student`, `Appointment` |
| ПР5 | веб-интерфейс на Django: маршруты, view-функции, Bootstrap |
| ПР6 | шаблоны Django, наследование, `include`, фильтры, статические файлы |
| ПР7 | база данных SQLite, SQL-запросы, представления читают данные из БД |

Версия каждого этапа отмечена тегом Git (`pr2`, `pr3`, `pr5`, `pr6`, `pr7`).

## Целевая аудитория
Студенты и преподаватели.

## Предметная область
Преподаватель проводит консультации в определённое время и принимает
ограниченное число студентов (`max_students`). Студент записывается
на консультацию на конкретную дату. Активные записи занимают места,
отменённая запись место освобождает. Повторная запись студента на ту же
консультацию запрещена.

## Возможности
**Веб-интерфейс**
- главная страница со сводкой (количество преподавателей, студентов,
  активных записей);
- список преподавателей с поиском по ФИО и отбором по числу мест;
- карточка преподавателя с его активными записями;
- поиск преподавателей со свободными местами на выбранную дату;
- список записей (активные и отменённые) и страница отдельной записи;
- статистика: записи по преподавателям, кафедры, студенты
  с несколькими записями;
- собственная страница ошибки 404.

**Консольная версия** (`main.py`, данные в JSON)
- просмотр, поиск, отбор и добавление преподавателей;
- регистрация и поиск студентов;
- проверка мест, запись на консультацию и её отмена.

## Технологии
Python 3.10+, Django 5.2, SQLite (`sqlite3`), HTML, CSS, Bootstrap 5.3,
JavaScript, pytest, flake8.

## Объектная модель (ПР3)

### Teacher — преподаватель
Атрибуты: `id`, `name`, `department`, `max_students`, `consultation_time`.
Методы: `is_suitable_for()`, `validate_max_students()` (`@staticmethod`),
`from_data()` (`@classmethod`), `to_data()`, `__str__()`.

### Student — студент
Атрибуты: `id`, `name`, `email`, `group`.
Методы: `from_data()` (`@classmethod`), `to_data()`, `__str__()`.

### Appointment — запись на консультацию
Атрибуты: `id`, `teacher` (объект `Teacher`), `student` (объект `Student`),
`consultation_date`, `is_cancelled`.
Методы: `cancel()`, `is_active` (`@property`), `to_data()`, `__str__()`.

```
appointment
 ├── teacher → Teacher
 └── student → Student
```

## База данных (ПР7)
Файл базы: `data/consultplan.sqlite`.

| Таблица | Поля |
|---------|------|
| `teachers` | `id` PK, `name`, `department`, `max_students`, `consultation_time` |
| `students` | `id` PK, `name`, `email` UNIQUE, `group_name` |
| `appointments` | `id` PK, `teacher_id` FK → teachers, `student_id` FK → students, `consultation_date`, `is_cancelled` |

Связи: у преподавателя и у студента может быть много записей;
каждая запись относится к одному преподавателю и одному студенту.

* `sql/schema.sql` — создание таблиц (первичные и внешние ключи, `CHECK`,
  `UNIQUE`, индекс);
* `sql/queries.sql` — 14 проверенных SQL-запросов: выборка списков,
  `WHERE`, `JOIN`, агрегатные функции (`COUNT`, `SUM`, `AVG`, `MAX`),
  `GROUP BY`, `HAVING`;
* `db/database.py` — подключение: `PRAGMA foreign_keys = ON`,
  `row_factory = sqlite3.Row`, функции `fetch_all()` / `fetch_one()`;
* `db/import_json.py` — перенос данных из JSON в SQLite (`executemany()`,
  `commit()`).

Значения от пользователя передаются в запросы только через параметры `?`.
Для поиска по кириллице без учёта регистра в соединении регистрируется
функция `py_lower()` (встроенная `LOWER()` SQLite обрабатывает только латиницу).

## Веб-интерфейс

| URL | View | Страница |
|-----|------|----------|
| `/` | `homepage.views.index` | главная |
| `/teachers/` | `teachers.views.teacher_list` | преподаватели (поиск, отбор) |
| `/teachers/<id>/` | `teachers.views.teacher_detail` | преподаватель |
| `/teachers/available/?date=` | `teachers.views.available_teachers` | свободные места на дату |
| `/appointments/` | `appointments.views.appointment_list` | записи |
| `/appointments/<id>/` | `appointments.views.appointment_detail` | запись |
| `/appointments/statistics/` | `appointments.views.statistics` | статистика |

Схема данных: SQLite → SQL → `sqlite3` → Django view → context → шаблон.

### Шаблоны и статика
* `templates/base.html` — базовый шаблон (Bootstrap, CSS, навигация,
  блоки `title` и `content`, подвал, JS);
* `templates/includes/navigation.html` — меню с подсветкой раздела;
* `templates/404.html` — страница ошибки;
* шаблоны приложений расширяют `base.html`; фрагменты
  `teachers/includes/teacher_card.html` и
  `appointments/includes/appointment_status.html` подключаются через
  `{% include %}`;
* используются `{% for %}…{% empty %}`, `{% if %}`, `{% url %}`
  с пространствами имён, фильтры `default`, `length`, `truncatechars`,
  `upper`, `lower`, теги `{% static %}` и `{% now %}`;
* `homepage/static/homepage/` — `css/style.css`, `js/main.js`, `img/logo.png`.

## Структура проекта
```
Individual_project/
├── README.md
├── requirements.txt
├── manage.py
├── consultplan/          — настройки и корневые маршруты Django
├── templates/            — шаблоны уровня проекта
├── homepage/             — главная страница, статические файлы
├── teachers/             — преподаватели, свободные места
├── appointments/         — записи, статистика
├── db/
│   ├── database.py       — подключение к SQLite
│   └── import_json.py    — перенос JSON → SQLite
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── models/               — классы Teacher, Student, Appointment и функции
├── main.py               — консольная версия
├── storage.py            — JSON ↔ объекты
├── utils.py              — безопасный ввод
├── data/
│   ├── teachers.json
│   ├── students.json
│   ├── appointments.json
│   └── consultplan.sqlite
└── tests/                — тесты pytest (модели, JSON, БД, веб-страницы)
```

## Установка
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Создание базы данных
База уже есть в репозитории. Пересоздать её из JSON:
```
python -m db.import_json
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

## Проверка
```
python manage.py check
pytest -v
flake8 . --extend-exclude=venv
```

## План развития
- Django ORM и административная панель;
- пользователи и авторизация;
- запись на консультацию через веб-форму;
- REST API, Docker, CI/CD.
