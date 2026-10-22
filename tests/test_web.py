import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consultplan.settings")
django.setup()

from django.test import Client  # noqa: E402


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.parametrize(
    "url",
    [
        "/",
        "/teachers/",
        "/teachers/1/",
        "/teachers/available/",
        "/appointments/",
        "/appointments/1/",
        "/appointments/statistics/",
    ],
)
def test_pages_open(client, url):
    assert client.get(url).status_code == 200


def test_teacher_list_shows_data(client):
    html = client.get("/teachers/").content.decode()
    assert "Иванов И.И." in html


def test_teacher_search(client):
    html = client.get("/teachers/", {"q": "петрова"}).content.decode()
    assert "Петрова А.А." in html
    assert "Иванов И.И." not in html


def test_available_teachers_on_date(client):
    response = client.get("/teachers/available/", {"date": "2026-09-21"})
    html = response.content.decode()
    assert "Петрова А.А." in html
    assert "Сидоров П.П." not in html


def test_available_invalid_date(client):
    html = client.get("/teachers/available/", {"date": "abc"}).content
    assert "Неверный формат даты" in html.decode()


def test_statistics_counts(client):
    html = client.get("/appointments/statistics/").content.decode()
    assert "Смирнов Алексей" in html
    assert "Кузнецова Е.В." in html


@pytest.mark.parametrize("url", ["/teachers/999/", "/appointments/999/"])
def test_missing_objects_return_404(client, url):
    assert client.get(url).status_code == 404
