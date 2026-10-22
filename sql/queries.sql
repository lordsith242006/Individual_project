-- SQL-запросы сервиса планирования консультационных часов.
-- Значения в условиях приведены для проверки в SQLite CLI;
-- в веб-приложении они передаются через параметры «?».

-- ============================================================
-- Выборка списков объектов
-- ============================================================

-- 1. Список преподавателей по алфавиту (страница /teachers/)
SELECT id, name, department, max_students, consultation_time
FROM teachers
ORDER BY name;

-- 2. Список студентов по группам и ФИО
SELECT id, name, email, group_name
FROM students
ORDER BY group_name, name;

-- ============================================================
-- Фильтрация (WHERE)
-- ============================================================

-- 3. Преподаватели, принимающие на консультации не меньше 3 студентов
--    (фильтр «Мест не меньше» на странице /teachers/)
SELECT id, name, max_students
FROM teachers
WHERE max_students >= 3
ORDER BY max_students;

-- 4. Поиск преподавателя по части ФИО
--    (в приложении: WHERE py_lower(name) LIKE ? — без учёта регистра)
SELECT id, name, department
FROM teachers
WHERE name LIKE '%Петров%';

-- 5. Преподаватели кафедры «Информатика»
SELECT id, name, consultation_time
FROM teachers
WHERE department = 'Информатика'
ORDER BY name;

-- ============================================================
-- Соединение таблиц (JOIN)
-- ============================================================

-- 6. Все записи с ФИО преподавателя и студента (страница /appointments/)
SELECT
    a.id,
    a.consultation_date,
    a.is_cancelled,
    t.id AS teacher_id,
    t.name AS teacher_name,
    t.consultation_time,
    s.name AS student_name
FROM appointments AS a
JOIN teachers AS t ON t.id = a.teacher_id
JOIN students AS s ON s.id = a.student_id
ORDER BY a.consultation_date, t.name;

-- 7. Полная информация о записи № 1 (страница /appointments/1/)
SELECT
    a.id,
    a.consultation_date,
    a.is_cancelled,
    t.id AS teacher_id,
    t.name AS teacher_name,
    t.department,
    t.consultation_time,
    s.name AS student_name,
    s.email,
    s.group_name
FROM appointments AS a
JOIN teachers AS t ON t.id = a.teacher_id
JOIN students AS s ON s.id = a.student_id
WHERE a.id = 1;

-- 8. Активные записи к преподавателю № 3 (страница /teachers/3/)
SELECT a.id, a.consultation_date, s.name AS student_name, s.group_name
FROM appointments AS a
JOIN students AS s ON s.id = a.student_id
WHERE a.teacher_id = 3 AND a.is_cancelled = 0
ORDER BY a.consultation_date;

-- ============================================================
-- Агрегатные функции
-- ============================================================

-- 9. Количество активных и отменённых записей
SELECT
    COUNT(*) AS total,
    SUM(is_cancelled = 0) AS active,
    SUM(is_cancelled = 1) AS cancelled
FROM appointments;

-- 10. Сводка по преподавателям: количество, суммарное и среднее число мест
SELECT
    COUNT(*) AS teachers_count,
    SUM(max_students) AS total_seats,
    ROUND(AVG(max_students), 1) AS avg_seats,
    MAX(max_students) AS max_seats
FROM teachers;

-- ============================================================
-- Группировка (GROUP BY) и фильтрация групп (HAVING)
-- ============================================================

-- 11. Количество активных записей к каждому преподавателю
--     (LEFT JOIN, чтобы показать и преподавателей без записей)
SELECT
    t.id,
    t.name AS teacher_name,
    COUNT(a.id) AS appointments_count
FROM teachers AS t
LEFT JOIN appointments AS a
    ON a.teacher_id = t.id AND a.is_cancelled = 0
GROUP BY t.id, t.name
ORDER BY appointments_count DESC, t.name;

-- 12. Количество преподавателей и мест по кафедрам
SELECT
    department,
    COUNT(*) AS teachers_count,
    SUM(max_students) AS total_seats
FROM teachers
GROUP BY department
ORDER BY teachers_count DESC, department;

-- 13. Студенты, у которых больше одной активной записи (HAVING)
SELECT
    s.name AS student_name,
    s.group_name,
    COUNT(a.id) AS appointments_count
FROM students AS s
JOIN appointments AS a ON a.student_id = s.id
WHERE a.is_cancelled = 0
GROUP BY s.id, s.name, s.group_name
HAVING COUNT(a.id) > 1
ORDER BY appointments_count DESC;

-- 14. Свободные места у преподавателей на 21.09.2026
--     (страница /teachers/available/, занятые места — активные записи)
SELECT
    t.id,
    t.name,
    t.department,
    t.consultation_time,
    t.max_students,
    t.max_students - COUNT(a.id) AS free_seats
FROM teachers AS t
LEFT JOIN appointments AS a
    ON a.teacher_id = t.id
    AND a.consultation_date = '2026-09-21'
    AND a.is_cancelled = 0
GROUP BY t.id
HAVING free_seats > 0
ORDER BY free_seats DESC, t.name;
