-- Схема базы данных сервиса планирования консультационных часов.
-- Пересоздание таблиц: сначала удаляется зависимая таблица appointments.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;

-- Преподаватели
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    max_students INTEGER NOT NULL CHECK (max_students > 0),
    consultation_time TEXT NOT NULL
);

-- Студенты (group — зарезервированное слово SQL, поэтому group_name)
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    group_name TEXT
);

-- Записи на консультации: связь «преподаватель — студент — дата»
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers (id),
    student_id INTEGER NOT NULL REFERENCES students (id),
    consultation_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0 CHECK (is_cancelled IN (0, 1))
);

CREATE INDEX idx_appointments_teacher_date
    ON appointments (teacher_id, consultation_date);
