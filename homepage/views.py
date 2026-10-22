from html import escape

from django.http import HttpRequest, HttpResponse

from storage import load_project_data

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Сформировать единый HTML-каркас страницы с навигацией."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} — КонсультПлан</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">КонсультПлан</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/teachers/">Преподаватели</a>
                <a class="nav-link" href="/appointments/">Записи</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
    <footer class="container text-muted small py-4">
        Сервис планирования консультационных часов
    </footer>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: назначение сервиса и сводка данных."""
    teachers, students, appointments = load_project_data()
    active = sum(1 for a in appointments if a.is_active)
    content = f"""
        <div class="p-4 bg-white rounded shadow-sm">
            <h1>Сервис планирования консультационных часов</h1>
            <p class="lead">Запись студентов на консультации
            к преподавателям: выбор преподавателя, проверка свободных
            мест на дату, создание и отмена записи.</p>
            <ul class="list-group mb-3">
                <li class="list-group-item">Преподавателей:
                    <strong>{len(teachers)}</strong></li>
                <li class="list-group-item">Студентов:
                    <strong>{len(students)}</strong></li>
                <li class="list-group-item">Активных записей:
                    <strong>{active}</strong></li>
            </ul>
            <a class="btn btn-primary" href="/teachers/">Преподаватели</a>
            <a class="btn btn-outline-primary" href="/appointments/">
                Записи на консультации</a>
        </div>"""
    return HttpResponse(page("Главная", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    content = """
        <div class="alert alert-warning">
            <h1>Страница не найдена (404)</h1>
            <p>Запрошенный адрес не существует.</p>
            <a class="btn btn-primary" href="/">На главную</a>
        </div>"""
    return HttpResponse(page("Страница не найдена", content), status=404)
