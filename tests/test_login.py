# test_login.py
import hashlib

import mysql.connector

from config import DB_CONFIG


def hash_password(password: str) -> str:
    """Хеширует пароль по алгоритму SHA-256"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str):
    """Проверяет логин и пароль. Возвращает название роли или None"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            SELECT u.password_hash, r.name_role
            FROM users u
            JOIN roles r ON u.id_role = r.id_role
            WHERE u.login = %s
        """
        cursor.execute(query, (login.strip(),))
        user_record = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_record:
            # ПРИНУДИТЕЛЬНО ПРЕВРАЩАЕМ В СТРОКУ И УБИРАЕМ ПРОБЕЛЫ
            db_hash = str(user_record[0]).strip()
            input_hash = hash_password(password).strip()

            # repr() покажет скрытые символы, если они есть (например, \n)
            print(f"1. Хеш из БД (repr):       {repr(db_hash)}")
            print(f"2. Хеш введенный (repr):   {repr(input_hash)}")

            if db_hash == input_hash:
                print("3. Пароли совпали!")
                return user_record[1]

        return None

    except mysql.connector.Error as err:
        print(f"Ошибка подключения к БД: {err}")
        return None


# --- ТЕСТОВЫЙ ЗАПУСК ---
if __name__ == "__main__":
    print("=== Проверка авторизации admin/admin123 ===")

    user_role = authenticate("admin", "admin123")

    if user_role:
        print(f"УСПЕХ! Пользователь вошел с ролью: {user_role}")
    else:
        print("ОШИБКА: Неверный логин/пароль или нет связи с БД.")
