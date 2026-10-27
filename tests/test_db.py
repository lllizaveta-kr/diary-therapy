import random
import string
import db


def random_login():
    """Генерирует случайный логин, чтобы не засорять базу"""
    return "testuser_" + "".join(random.choices(string.ascii_lowercase, k=5))


def test_database_connection():
    """Проверяем, что приложение вообще может подключиться к БД"""
    ok, err = db.check_connection()
    assert ok is True, f"Нет подключения к БД: {err}"


def test_create_and_delete_user():
    """Проверяем создание пользователя и его удаление"""
    test_login = random_login()

    # 1. Создаем пользователя
    id_user = db.create_user(test_login, "password123", "admin", "Тестовый Админ")
    assert id_user is not None, "Не удалось создать пользователя"

    # 2. Проверяем, что он есть в базе
    users = db.get_all_users()
    found = any(u[1] == test_login for u in users)
    assert found is True, "Пользователь не найден в списке всех пользователей"

    # 3. Удаляем пользователя
    deleted = db.delete_user(id_user)
    assert deleted is True, "Не удалось удалить пользователя"

    # 4. Убеждаемся, что его больше нет
    users_after = db.get_all_users()
    found_after = any(u[1] == test_login for u in users_after)
    assert found_after is False, "Пользователь не удалился из базы"