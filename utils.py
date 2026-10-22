"""Вспомогательные функции безопасного ввода."""

from datetime import date, datetime

DATE_FORMAT = "%d.%m.%Y"


def input_int(prompt: str) -> int:
    """Запросить целое число; при ошибке ввода повторить запрос."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при ошибке повторить запрос."""
    while True:
        try:
            return datetime.strptime(input(prompt), DATE_FORMAT).date()
        except ValueError:
            print("Неверный формат даты. Пример: 20.09.2026")


def input_text(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Значение не может быть пустым.")
