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
    ["/", "/teachers/", "/teachers/1/", "/appointments/", "/appointments/1/"],
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


@pytest.mark.parametrize("url", ["/teachers/999/", "/appointments/999/"])
def test_missing_objects_return_404(client, url):
    assert client.get(url).status_code == 404
