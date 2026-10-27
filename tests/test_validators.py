from validators import (
    validate_name, validate_login, validate_password,
    validate_phone, validate_policy, validate_pressure,
    validate_pulse, validate_sugar, validate_temperature,
    validate_height, validate_weight
)

# ============== ТЕСТЫ ФИО И ЛОГИНА ==============
def test_validate_name():
    assert validate_name("Иванов Иван Иванович")[0] is True
    assert validate_name("Петров-Водкин")[0] is True
    assert validate_name("")[0] is False
    assert validate_name("Иван 123")[0] is False  # цифры запрещены
    assert validate_name("И")[0] is False         # слишком коротко

def test_validate_login():
    assert validate_login("doctor_1")[0] is True
    assert validate_login("admin")[0] is True
    assert validate_login("маша")[0] is False     # кириллица запрещена
    assert validate_login("ab")[0] is False       # слишком коротко
    assert validate_login("user name")[0] is False # пробелы запрещены

def test_validate_password():
    assert validate_password("secret123")[0] is True
    assert validate_password("123")[0] is False    # слишком коротко
    assert validate_password("")[0] is False

# ============== ТЕСТЫ КОНТАКТОВ ==============
def test_validate_phone():
    assert validate_phone("+79991234567")[0] is True
    assert validate_phone("89991234567")[0] is True
    assert validate_phone("")[0] is True           # телефон необязателен
    assert validate_phone("12345")[0] is False     # мало цифр
    assert validate_phone("+7999ABC4567")[0] is False # буквы в телефоне

def test_validate_policy():
    assert validate_policy("1234567890123456")[0] is True  # 16 цифр
    assert validate_policy("")[0] is True                  # необязательно
    assert validate_policy("123456")[0] is False           # мало цифр

# ============== ТЕСТЫ МЕДИЦИНСКИХ ПОКАЗАТЕЛЕЙ ==============
def test_validate_pressure():
    assert validate_pressure("120/80")[0] is True
    assert validate_pressure("150/90")[0] is True
    assert validate_pressure("")[0] is True
    assert validate_pressure("120")[0] is False           # нет нижнего
    assert validate_pressure("банан")[0] is False
    assert validate_pressure("80/120")[0] is False        # нижнее больше верхнего
    assert validate_pressure("300/80")[0] is False        # слишком высокое

def test_validate_pulse():
    assert validate_pulse("72")[0] is True
    assert validate_pulse("")[0] is True
    assert validate_pulse("500")[0] is False
    assert validate_pulse("abc")[0] is False

def test_validate_sugar():
    assert validate_sugar("5.5")[0] is True
    assert validate_sugar("5,5")[0] is True
    assert validate_sugar("")[0] is True
    assert validate_sugar("-1")[0] is False
    assert validate_sugar("100")[0] is False

def test_validate_temperature():
    assert validate_temperature("36.6")[0] is True
    assert validate_temperature("36,6")[0] is True
    assert validate_temperature("")[0] is True
    assert validate_temperature("50")[0] is False

def test_validate_height():
    assert validate_height("170")[0] is True
    assert validate_height("")[0] is True
    assert validate_height("500")[0] is False

def test_validate_weight():
    assert validate_weight("70.5")[0] is True
    assert validate_weight("70,5")[0] is True
    assert validate_weight("")[0] is True
    assert validate_weight("-10")[0] is False