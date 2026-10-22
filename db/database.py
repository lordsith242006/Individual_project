"""Подключение к базе данных SQLite проекта."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "consultplan.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Открыть соединение с базой данных.

    Включается проверка внешних ключей, строки результата доступны
    по именам полей (sqlite3.Row). Функция py_lower() нужна для поиска
    без учёта регистра по кириллице: встроенная LOWER() SQLite
    преобразует только латиницу.
    """
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.create_function("py_lower", 1, str.lower, deterministic=True)
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Создать таблицы по файлу sql/schema.sql."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def fetch_all(
    sql: str,
    params: tuple = (),
    db_path: str | Path | None = None,
) -> list[sqlite3.Row]:
    """Выполнить SELECT и вернуть все строки результата."""
    conn = get_connection(db_path)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def fetch_one(
    sql: str,
    params: tuple = (),
    db_path: str | Path | None = None,
) -> sqlite3.Row | None:
    """Выполнить SELECT и вернуть первую строку (или None)."""
    conn = get_connection(db_path)
    try:
        return conn.execute(sql, params).fetchone()
    finally:
        conn.close()
