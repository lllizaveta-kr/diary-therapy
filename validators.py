import re
from datetime import datetime, date


def validate_name(value: str) -> tuple[bool, str]:
    """Проверяет ФИО. Разрешены русские/латинские буквы, пробел, дефис."""
    value = value.strip()
    if not value:
        return False, "ФИО не может быть пустым"
    if len(value) < 2:
        return False, "ФИО слишком короткое"
    if len(value) > 200:
        return False, "ФИО слишком длинное (максимум 200 символов)"
    if not re.match(r"^[А-Яа-яЁёA-Za-z\s\-]+$", value):
        return False, "ФИО может содержать только буквы, пробел и дефис"
    return True, ""


def validate_login(value: str) -> tuple[bool, str]:
    """Логин: латиница, цифры, подчёркивание. 3-50 символов."""
    value = value.strip()
    if not value:
        return False, "Логин не может быть пустым"
    if len(value) < 3:
        return False, "Логин должен быть минимум 3 символа"
    if len(value) > 50:
        return False, "Логин слишком длинный (максимум 50)"
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        return False, "Логин: только латиница, цифры и подчёркивание"
    return True, ""


def validate_password(value: str) -> tuple[bool, str]:
    """Пароль: минимум 6 символов."""
    if not value:
        return False, "Пароль не может быть пустым"
    if len(value) < 6:
        return False, "Пароль должен быть минимум 6 символов"
    if len(value) > 100:
        return False, "Пароль слишком длинный"
    return True, ""


def validate_phone(value: str) -> tuple[bool, str]:
    """Телефон: +7XXXXXXXXXX или 8XXXXXXXXXX. Пустое значение ок."""
    value = value.strip()
    if not value:
        return True, ""  # необязательное
    cleaned = re.sub(r"[\s\-\(\)]", "", value)
    if not re.match(r"^(\+7|8)\d{10}$", cleaned):
        return False, "Телефон в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
    return True, ""


def validate_policy(value: str) -> tuple[bool, str]:
    """Полис ОМС: 16 цифр. Пустое значение ок."""
    value = value.strip()
    if not value:
        return True, ""
    if not re.match(r"^\d{16}$", value):
        return False, "Полис должен содержать 16 цифр"
    return True, ""


def validate_birth_date(value: str) -> tuple[bool, str]:
    """Дата рождения: не в будущем, не старше 120 лет."""
    try:
        if isinstance(value, str):
            d = datetime.strptime(value, "%Y-%m-%d").date()
        else:
            d = value
    except (ValueError, TypeError):
        return False, "Неверный формат даты"

    today = date.today()
    if d > today:
        return False, "Дата рождения не может быть в будущем"
    age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    if age > 120:
        return False, "Возраст не может быть больше 120 лет"
    return True, ""


def validate_pressure(value: str) -> tuple[bool, str]:
    """Давление: формат 120/80 или пусто. Верхнее 50-250, нижнее 30-150."""
    value = value.strip()
    if not value:
        return True, ""
    if not re.match(r"^\d{2,3}/\d{2,3}$", value):
        return False, "Давление в формате 120/80"
    upper, lower = map(int, value.split("/"))
    if not (50 <= upper <= 250):
        return False, "Верхнее давление от 50 до 250"
    if not (30 <= lower <= 150):
        return False, "Нижнее давление от 30 до 150"
    if upper <= lower:
        return False, "Верхнее давление должно быть больше нижнего"
    return True, ""


def validate_pulse(value: str) -> tuple[bool, str]:
    value = value.strip()
    if not value:
        return True, ""
    if not value.isdigit():
        return False, "Пульс — только цифры"
    n = int(value)
    if not (30 <= n <= 220):
        return False, "Пульс от 30 до 220"
    return True, ""


def validate_sugar(value: str) -> tuple[bool, str]:
    value = value.strip()
    if not value:
        return True, ""
    try:
        n = float(value.replace(",", "."))
    except ValueError:
        return False, "Сахар — число (например, 5.5)"
    if not (1.0 <= n <= 40.0):
        return False, "Сахар от 1.0 до 40.0 ммоль/л"
    return True, ""


def validate_temperature(value: str) -> tuple[bool, str]:
    value = value.strip()
    if not value:
        return True, ""
    try:
        n = float(value.replace(",", "."))
    except ValueError:
        return False, "Температура — число (например, 36.6)"
    if not (30.0 <= n <= 45.0):
        return False, "Температура от 30.0 до 45.0 °C"
    return True, ""


def validate_height(value: str) -> tuple[bool, str]:
    value = value.strip()
    if not value:
        return True, ""
    if not value.isdigit():
        return False, "Рост — целое число в см"
    n = int(value)
    if not (30 <= n <= 250):
        return False, "Рост от 30 до 250 см"
    return True, ""


def validate_weight(value: str) -> tuple[bool, str]:
    value = value.strip()
    if not value:
        return True, ""
    try:
        n = float(value.replace(",", "."))
    except ValueError:
        return False, "Вес — число (например, 65.5)"
    if not (2.0 <= n <= 400.0):
        return False, "Вес от 2.0 до 400.0 кг"
    return True, ""


def validate_intensity(value: int) -> tuple[bool, str]:
    if not (0 <= value <= 10):
        return False, "Интенсивность от 0 до 10"
    return True, ""
