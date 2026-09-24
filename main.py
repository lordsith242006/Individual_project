from datetime import date

teachers = ["Иванов И.И.", "Петрова А.А.", "Сидоров П.П."]
consultation_date = date(2026, 9, 20)
available_time = "14:00"
student_name = "Смирнов Алексей"

def show_teachers():
    print("Доступные преподаватели:")
    for teacher in teachers:
        print(f"- {teacher}")

def show_consultation_info():
    print(f"Дата консультации: {consultation_date}")
    print(f"Время: {available_time}")

def book_consultation(is_free):
    if is_free:
        return f"Студент {student_name} записан на консультацию."
    return "Это время уже занято."

show_teachers()
show_consultation_info()
print(book_consultation(True))