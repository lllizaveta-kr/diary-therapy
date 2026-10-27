import hashlib
import random
import string
from datetime import date, timedelta

import mysql.connector

from config import DB_CONFIG


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG, connection_timeout=5)
    except mysql.connector.Error as err:
        logging.error(f"Ошибка подключения к БД: {err}")
        return None

def check_connection():
    try:
        conn = get_connection()
        if conn:
            conn.close()
            return True, ""
        return False, "Не удалось подключиться"
    except Exception as e:
        return False, str(e)


# ============== ПОЛЬЗОВАТЕЛИ ==============
def get_doctor_by_user(id_user):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_doctor FROM doctors WHERE id_user = %s", (id_user,))
        return cur.fetchone()
    finally:
        conn.close()


def get_patient_by_user(id_user):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_patient, id_user, id_doctor FROM patients WHERE id_user = %s",
            (id_user,),
        )
        return cur.fetchone()
    finally:
        conn.close()


def get_patient_profile(id_patient):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT u.full_name, p.birth_date, p.gender, p.policy_number, p.phone
            FROM patients p
            JOIN users u ON u.id_user = p.id_user
            WHERE p.id_patient = %s
        """,
            (id_patient,),
        )
        return cur.fetchone()
    finally:
        conn.close()


# ============== ПАЦИЕНТЫ ВРАЧА ==============
def get_my_patients(id_doctor):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.id_patient, u.full_name, p.birth_date, p.policy_number, p.phone
            FROM patients p
            JOIN users u ON u.id_user = p.id_user
            WHERE p.id_doctor = %s
        """,
            (id_doctor,),
        )
        return cur.fetchall()
    finally:
        conn.close()


_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def transliterate(text):
    return "".join(_TRANSLIT.get(c, c) for c in text.lower())


def generate_login(full_name):
    """Логин латиницей: фамилия + первая буква имени (kuznetsov_d).
    validate_login пропускает только латиницу, поэтому кириллицу транслитерируем."""
    parts = [transliterate(p) for p in full_name.split()]
    parts = ["".join(c for c in p if c.isascii() and c.isalnum()) for p in parts]
    parts = [p for p in parts if p]
    if not parts:
        return "user"
    base = parts[0] if len(parts) == 1 else f"{parts[0]}_{parts[1][0]}"
    return base[:40]


def find_free_login(base):
    """Возвращает base, а если он занят — base2, base3 и т.д."""
    conn = get_connection()
    if not conn:
        return base
    try:
        cur = conn.cursor()
        login, counter = base, 1
        while True:
            cur.execute("SELECT 1 FROM users WHERE login = %s", (login,))
            if cur.fetchone() is None:
                return login
            counter += 1
            login = f"{base}{counter}"
    finally:
        conn.close()


def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def create_patient_by_doctor(
    id_doctor, full_name, birth_date, gender, policy, phone, login, password
):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        cur.execute(
            """
            INSERT INTO users (login, password_hash, id_role, full_name)
            VALUES (%s, %s, (SELECT id_role FROM roles WHERE name_role = 'patient'), %s)
        """,
            (login, password_hash, full_name),
        )
        id_user = cur.lastrowid
        cur.execute(
            """
            INSERT INTO patients (id_user, id_doctor, birth_date, gender, policy_number, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (id_user, id_doctor, birth_date, gender, policy, phone),
        )
        conn.commit()
        return id_user
    except mysql.connector.Error as err:
        print(f"Ошибка создания пациента: {err}")
        conn.rollback()
        return None
    finally:
        conn.close()


# ============== ЛЕКАРСТВА ==============
def get_all_medications():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_medication, name_med, dosage FROM medications ORDER BY name_med")
        return cur.fetchall()
    finally:
        conn.close()


def search_medications(text):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_medication, name_med, dosage FROM medications
            WHERE name_med LIKE %s OR dosage LIKE %s
            ORDER BY name_med
        """,
            (f"%{text}%", f"%{text}%"),
        )
        return cur.fetchall()
    finally:
        conn.close()


def create_medication(name, form, dosage):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO medications (name_med, form, dosage) VALUES (%s, %s, %s)",
            (name, form, dosage),
        )
        conn.commit()
        return cur.lastrowid
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return None
    finally:
        conn.close()


# ============== НАЗНАЧЕНИЯ (statuss, commentt) ==============
def create_prescription(id_patient, id_doctor, id_medication, dosage, freq, start, end, comment):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO prescriptions
            (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, commentt, statuss)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'active')
        """,
            (id_patient, id_doctor, id_medication, dosage, freq, start, end, comment),
        )
        conn.commit()
        # Возвращаем id нового назначения (раньше брали MAX(id) — это ломалось,
        # если два врача создавали назначения одновременно)
        return cur.lastrowid
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_prescriptions_for_patient(id_patient):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.id_prescription, m.name_med, p.dosage, p.frequency, p.start_date, p.end_date, p.statuss
            FROM prescriptions p
            JOIN medications m ON m.id_medication = p.id_medication
            WHERE p.id_patient = %s
            ORDER BY p.start_date DESC
        """,
            (id_patient,),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ============== ДНЕВНИК (well_being_text) ==============
def create_diary_entry(id_patient, date, time, well_being, symptoms):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (id_patient, date, time, well_being, symptoms),
        )
        conn.commit()
        return cur.lastrowid
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return None
    finally:
        conn.close()


def get_diary_entries_for_patient(id_patient):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_diary, entry_date, entry_time, well_being_text, symptoms
            FROM diary_entries WHERE id_patient = %s
            ORDER BY entry_date DESC, entry_time DESC
        """,
            (id_patient,),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ============== ПОКАЗАТЕЛИ (valuee) ==============
def create_health_indicator(id_diary, type_name, value, unit):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO health_indicators (id_diary, indicator_type, valuee, unit)
            VALUES (%s, %s, %s, %s)
        """,
            (id_diary, type_name, value, unit),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_indicators_for_diary(id_diary):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT indicator_type, valuee, unit FROM health_indicators WHERE id_diary = %s",
            (id_diary,),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ============== ДИАГНОЗЫ (хранятся в diary_entries!) ==============
def get_all_diseases():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_disease, code, name FROM diseases ORDER BY code")
        return cur.fetchall()
    finally:
        conn.close()


def search_diseases(text):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_disease, code, name FROM diseases
            WHERE code LIKE %s OR name LIKE %s ORDER BY code
        """,
            (f"%{text}%", f"%{text}%"),
        )
        return cur.fetchall()
    finally:
        conn.close()


def get_diary_diagnosis(id_diary):
    conn = get_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT doctor_diagnosis AS diagnosis, id_disease
            FROM diary_entries WHERE id_diary = %s
        """,
            (id_diary,),
        )
        row = cur.fetchone()
        return row if row else {}
    finally:
        conn.close()


def set_diary_diagnosis_full(id_diary, diagnosis, id_disease, id_doctor):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE diary_entries
            SET doctor_diagnosis = %s, id_disease = %s, id_doctor_who_viewed = %s
            WHERE id_diary = %s
        """,
            (diagnosis, id_disease, id_doctor, id_diary),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


# ============== АДМИН: СТАТИСТИКА ==============
def get_patients_by_doctor():
    conn = get_connection()
    if not conn:
        return [], []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.full_name, COUNT(p.id_patient)
            FROM doctors d
            JOIN users u ON u.id_user = d.id_user
            LEFT JOIN patients p ON p.id_doctor = d.id_doctor
            GROUP BY d.id_doctor, u.full_name
            ORDER BY u.full_name
        """)
        rows = cur.fetchall()
        return [r[0] for r in rows], [r[1] for r in rows]
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return [], []
    finally:
        conn.close()


def get_adherence():
    conn = get_connection()
    if not conn:
        return [("Активные", 0), ("Завершённые", 0)]
    try:
        cur = conn.cursor()
        cur.execute("SELECT statuss, COUNT(*) FROM prescriptions GROUP BY statuss")
        rows = cur.fetchall()
        result = []
        for status, cnt in rows:
            name = "Активные" if (status or "").lower() == "active" else "Завершённые"
            result.append((name, int(cnt)))
        if not result:
            result = [("Активные", 0), ("Завершённые", 0)]
        return result
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return [("Активные", 0), ("Завершённые", 0)]
    finally:
        conn.close()


def get_diary_dynamics():
    conn = get_connection()
    if not conn:
        return [], []
    try:
        cur = conn.cursor()
        today = date.today()
        start = today - timedelta(days=13)
        cur.execute(
            """
            SELECT entry_date, COUNT(*) FROM diary_entries
            WHERE entry_date >= %s
            GROUP BY entry_date ORDER BY entry_date
        """,
            (start,),
        )
        rows = cur.fetchall()
        counts = {str(r[0]): r[1] for r in rows}
        labels, data = [], []
        for i in range(14):
            d = start + timedelta(days=i)
            labels.append(d.strftime("%d.%m"))
            data.append(int(counts.get(str(d), 0)))
        return labels, data
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return [], []
    finally:
        conn.close()


# ============== АДМИН: ПОЛЬЗОВАТЕЛИ ==============
def get_all_users():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id_user, u.login, r.name_role, u.full_name
            FROM users u
            JOIN roles r ON r.id_role = u.id_role
            ORDER BY u.id_user
        """)
        return cur.fetchall()
    finally:
        conn.close()


def create_user(login, password, role_name, full_name):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_user FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            return None
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        cur.execute(
            """
            INSERT INTO users (login, password_hash, id_role, full_name)
            VALUES (%s, %s, (SELECT id_role FROM roles WHERE name_role = %s), %s)
        """,
            (login, password_hash, role_name, full_name),
        )
        conn.commit()
        return cur.lastrowid
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        conn.rollback()
        return None
    finally:
        conn.close()


def create_doctor(id_user, specialty="Терапевт"):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO doctors (id_user, specialty) VALUES (%s, %s)",
            (id_user, specialty),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def create_patient(id_user, full_name, birth_date, gender, policy, phone, id_doctor=None):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO patients (id_user, id_doctor, birth_date, gender, policy_number, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (id_user, id_doctor, birth_date, gender, policy, phone),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def delete_user(id_user):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        # Удаляем health_indicators через diary_entries
        cur.execute(
            """
            DELETE FROM health_indicators WHERE id_diary IN
            (SELECT id_diary FROM diary_entries WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s))
        """,
            (id_user,),
        )
        cur.execute(
            """
            DELETE FROM doctor_comments WHERE id_diary IN
            (SELECT id_diary FROM diary_entries WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s))
        """,
            (id_user,),
        )
        cur.execute(
            """
            DELETE FROM diary_entries WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s)
        """,
            (id_user,),
        )
        # Удаляем schedules через prescriptions
        cur.execute(
            """
            DELETE FROM prescription_schedules WHERE id_prescription IN
            (SELECT id_prescription FROM prescriptions WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s))
        """,
            (id_user,),
        )
        cur.execute(
            """
            DELETE FROM reminders WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s)
        """,
            (id_user,),
        )
        cur.execute(
            """
            DELETE FROM prescriptions WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s)
        """,
            (id_user,),
        )
        cur.execute("DELETE FROM patients WHERE id_user = %s", (id_user,))
        cur.execute("DELETE FROM doctors WHERE id_user = %s", (id_user,))
        cur.execute("DELETE FROM users WHERE id_user = %s", (id_user,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        conn.rollback()
        return False
    finally:
        conn.close()


def reset_user_password(id_user, new_password):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        password_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        cur.execute(
            "UPDATE users SET password_hash = %s WHERE id_user = %s",
            (password_hash, id_user),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_all_patients_with_doctors():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_patient, u.full_name,
                   COALESCE(du.full_name, '— не назначен —') AS doctor_name
            FROM patients p
            JOIN users u ON u.id_user = p.id_user
            LEFT JOIN doctors d ON d.id_doctor = p.id_doctor
            LEFT JOIN users du ON du.id_user = d.id_user
            ORDER BY u.full_name
        """)
        return cur.fetchall()
    finally:
        conn.close()


def get_all_doctors():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT d.id_doctor, u.full_name, u.login
            FROM doctors d
            JOIN users u ON u.id_user = d.id_user
            ORDER BY u.full_name
        """)
        return cur.fetchall()
    finally:
        conn.close()


def reassign_patient_doctor(id_patient, id_doctor):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE patients SET id_doctor = %s WHERE id_patient = %s",
            (id_doctor, id_patient),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


# ============== РАСПИСАНИЕ ПРИЁМА ==============
def create_prescription_schedule(id_prescription, time_of_day, dose, instructions):
    """Добавляет время приёма в расписание назначения.
    time_of_day — строка 'HH:MM:SS'."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO prescription_schedules
            (id_prescription, time_of_day, dose, instructions)
            VALUES (%s, %s, %s, %s)
        """,
            (id_prescription, time_of_day, dose, instructions),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка добавления расписания: {err}")
        return False
    finally:
        conn.close()


def get_schedules_for_prescription(id_prescription):
    """Возвращает список времён приёма для назначения."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_schedule, time_of_day, dose, instructions
            FROM prescription_schedules
            WHERE id_prescription = %s
            ORDER BY time_of_day
        """,
            (id_prescription,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def get_today_schedules_for_patient(id_patient):
    """Все приёмы на сегодня для пациента.
    Возвращает список: (id_prescription, name_med, dose, time_of_day, instructions)"""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT ps.id_prescription, m.name_med, ps.dose, ps.time_of_day, ps.instructions
            FROM prescription_schedules ps
            JOIN prescriptions p ON p.id_prescription = ps.id_prescription
            JOIN medications m ON m.id_medication = p.id_medication
            WHERE p.id_patient = %s
              AND p.statuss = 'active'
              AND CURDATE() BETWEEN p.start_date AND p.end_date
            ORDER BY ps.time_of_day
        """,
            (id_patient,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def get_last_prescription_id():
    """Возвращает id последнего созданного назначения."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id_prescription) FROM prescriptions")
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


# ============== CRM АДМИНИСТРАТОРА ==============
def get_crm_counters():
    """Числа для плашек на главной CRM."""
    conn = get_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor()
        queries = {
            "patients": "SELECT COUNT(*) FROM patients",
            "doctors": "SELECT COUNT(*) FROM doctors",
            "active_prescriptions": "SELECT COUNT(*) FROM prescriptions WHERE statuss = 'active'",
            "diary_week": "SELECT COUNT(*) FROM diary_entries "
            "WHERE entry_date >= CURDATE() - INTERVAL 6 DAY",
            "no_doctor": "SELECT COUNT(*) FROM patients WHERE id_doctor IS NULL",
        }
        result = {}
        for key, sql in queries.items():
            cur.execute(sql)
            result[key] = int(cur.fetchone()[0])
        return result
    finally:
        conn.close()


def get_patients_crm():
    """Пациенты со всем, что нужно для карточки в CRM."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.id_patient, p.id_user, u.full_name, u.login,
                   p.birth_date, p.gender, p.policy_number, p.phone,
                   p.id_doctor, du.full_name AS doctor_name, d.specialty, d.photo AS doctor_photo,
                   (SELECT COUNT(*) FROM prescriptions pr
                     WHERE pr.id_patient = p.id_patient AND pr.statuss = 'active') AS active_rx,
                   (SELECT COUNT(*) FROM diary_entries de
                     WHERE de.id_patient = p.id_patient) AS diary_count,
                   (SELECT de.well_being_text FROM diary_entries de
                     WHERE de.id_patient = p.id_patient
                     ORDER BY de.entry_date DESC, de.entry_time DESC LIMIT 1) AS last_wellbeing,
                   (SELECT MAX(de.entry_date) FROM diary_entries de
                     WHERE de.id_patient = p.id_patient) AS last_entry
            FROM patients p
            JOIN users u ON u.id_user = p.id_user
            LEFT JOIN doctors d ON d.id_doctor = p.id_doctor
            LEFT JOIN users du ON du.id_user = d.id_user
            ORDER BY u.full_name
        """)
        return cur.fetchall()
    finally:
        conn.close()


def get_doctors_crm():
    """Врачи с профилем, фото и числом пациентов."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT d.id_doctor, d.id_user, u.full_name, u.login,
                   d.specialty, d.office, d.schedule, d.phone, d.email, d.photo,
                   (SELECT COUNT(*) FROM patients p WHERE p.id_doctor = d.id_doctor) AS patients_count,
                   (SELECT COUNT(*) FROM prescriptions pr
                     WHERE pr.id_doctor = d.id_doctor AND pr.statuss = 'active') AS active_rx
            FROM doctors d
            JOIN users u ON u.id_user = d.id_user
            ORDER BY u.full_name
        """)
        return cur.fetchall()
    finally:
        conn.close()


def update_doctor_profile(id_doctor, specialty, office, schedule, phone, email, photo):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE doctors
            SET specialty = %s, office = %s, schedule = %s, phone = %s, email = %s, photo = %s
            WHERE id_doctor = %s
        """,
            (specialty, office, schedule, phone, email, photo, id_doctor),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def update_patient_profile(id_patient, birth_date, gender, policy, phone):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE patients
            SET birth_date = %s, gender = %s, policy_number = %s, phone = %s
            WHERE id_patient = %s
        """,
            (birth_date, gender, policy, phone, id_patient),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_users_crm():
    """Учётные записи с ролью и датой создания."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT u.id_user, u.login, r.name_role AS role, u.full_name, u.created_at,
                   d.photo
            FROM users u
            JOIN roles r ON r.id_role = u.id_role
            LEFT JOIN doctors d ON d.id_user = u.id_user
            ORDER BY u.created_at DESC, u.id_user DESC
        """)
        return cur.fetchall()
    finally:
        conn.close()


def log_action(id_user, action, entity_type=None, entity_id=None):
    """Запись в журнал действий. Ошибка журнала не должна ломать основное действие."""
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audit_log (id_user, actionn, entity_type, entity_id, ip_address)
            VALUES (%s, %s, %s, %s, '127.0.0.1')
        """,
            (id_user, action, entity_type, entity_id),
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Ошибка журнала: {err}")
    finally:
        conn.close()


def get_audit_log(limit=100):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT a.id_log, a.actionn AS action, a.entity_type, a.entity_id,
                   a.timestampp AS ts, u.full_name, r.name_role AS role
            FROM audit_log a
            LEFT JOIN users u ON u.id_user = a.id_user
            LEFT JOIN roles r ON r.id_role = u.id_role
            ORDER BY a.timestampp DESC, a.id_log DESC
            LIMIT %s
        """,
            (limit,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def get_prescriptions_full(id_patient):
    """Назначения пациента с формой выпуска препарата и расписанием приёма."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT p.id_prescription, m.name_med, m.form, p.dosage, p.frequency,
                   p.start_date, p.end_date, p.statuss AS status, p.commentt AS comment,
                   du.full_name AS doctor_name, d.photo AS doctor_photo,
                   (SELECT GROUP_CONCAT(TIME_FORMAT(ps.time_of_day, '%H:%i')
                           ORDER BY ps.time_of_day SEPARATOR ', ')
                      FROM prescription_schedules ps
                     WHERE ps.id_prescription = p.id_prescription) AS times
            FROM prescriptions p
            JOIN medications m ON m.id_medication = p.id_medication
            JOIN doctors d ON d.id_doctor = p.id_doctor
            JOIN users du ON du.id_user = d.id_user
            WHERE p.id_patient = %s
            ORDER BY p.statuss = 'active' DESC, p.start_date DESC
        """,
            (id_patient,),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ============== КАБИНЕТ ВРАЧА ==============
def get_doctor_crm(id_doctor):
    """Профиль одного врача (те же поля, что в get_doctors_crm)."""
    return next((d for d in get_doctors_crm() if d["id_doctor"] == id_doctor), None)


def get_medications_full():
    """Справочник препаратов с формой выпуска и частотой назначения."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT m.id_medication, m.name_med, m.form, m.dosage, m.manufacturer, m.description,
                   (SELECT COUNT(*) FROM prescriptions p WHERE p.id_medication = m.id_medication) AS used
            FROM medications m
            ORDER BY used DESC, m.name_med
        """)
        return cur.fetchall()
    finally:
        conn.close()


def get_prescriptions_by_doctor(id_doctor):
    """Все назначения врача с пациентом, формой препарата и временем приёма."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT p.id_prescription, p.id_patient, u.full_name AS patient_name,
                   m.name_med, m.form, p.dosage, p.frequency,
                   p.start_date, p.end_date, p.statuss AS status, p.commentt AS comment,
                   (SELECT GROUP_CONCAT(TIME_FORMAT(ps.time_of_day, '%H:%i')
                           ORDER BY ps.time_of_day SEPARATOR ', ')
                      FROM prescription_schedules ps
                     WHERE ps.id_prescription = p.id_prescription) AS times
            FROM prescriptions p
            JOIN medications m ON m.id_medication = p.id_medication
            JOIN patients pa ON pa.id_patient = p.id_patient
            JOIN users u ON u.id_user = pa.id_user
            WHERE p.id_doctor = %s
            ORDER BY p.statuss = 'active' DESC, p.start_date DESC
        """,
            (id_doctor,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def set_prescription_status(id_prescription, status):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE prescriptions SET statuss = %s WHERE id_prescription = %s",
            (status, id_prescription),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_diary_full(id_patient):
    """Записи дневника вместе с показателями, диагнозом МКБ-10 и комментариями врача.
    Делаем 3 запроса на всех вместо 3 запросов на каждую запись."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT de.id_diary, de.entry_date, de.entry_time, de.well_being_text, de.symptoms,
                   de.doctor_diagnosis, de.id_disease, ds.code AS disease_code, ds.name AS disease_name,
                   du.full_name AS viewed_by
            FROM diary_entries de
            LEFT JOIN diseases ds ON ds.id_disease = de.id_disease
            LEFT JOIN doctors d ON d.id_doctor = de.id_doctor_who_viewed
            LEFT JOIN users du ON du.id_user = d.id_user
            WHERE de.id_patient = %s
            ORDER BY de.entry_date DESC, de.entry_time DESC
        """,
            (id_patient,),
        )
        entries = cur.fetchall()
        by_id = {e["id_diary"]: e for e in entries}
        for e in entries:
            e["indicators"] = []
            e["comments"] = []
        if not entries:
            return []
        cur.execute(
            """
            SELECT hi.id_diary, hi.indicator_type, hi.valuee AS value, hi.unit
            FROM health_indicators hi
            JOIN diary_entries de ON de.id_diary = hi.id_diary
            WHERE de.id_patient = %s
            ORDER BY hi.id_indicator
        """,
            (id_patient,),
        )
        for row in cur.fetchall():
            by_id[row["id_diary"]]["indicators"].append(row)
        cur.execute(
            """
            SELECT dc.id_diary, dc.commentt AS text, dc.created_at, u.full_name AS doctor_name
            FROM doctor_comments dc
            JOIN diary_entries de ON de.id_diary = dc.id_diary
            JOIN doctors d ON d.id_doctor = dc.id_doctor
            JOIN users u ON u.id_user = d.id_user
            WHERE de.id_patient = %s
            ORDER BY dc.created_at
        """,
            (id_patient,),
        )
        for row in cur.fetchall():
            by_id[row["id_diary"]]["comments"].append(row)
        return entries
    finally:
        conn.close()


def add_doctor_comment(id_diary, id_doctor, text):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO doctor_comments (id_diary, id_doctor, commentt) VALUES (%s, %s, %s)",
            (id_diary, id_doctor, text),
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


# ============== КАБИНЕТ ПАЦИЕНТА ==============
def get_today_schedule_full(id_patient):
    """Приёмы лекарств на сегодня с формой препарата — для ленты «Сегодня»."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT ps.id_schedule, p.id_prescription, m.name_med, m.form, ps.dose,
                   ps.time_of_day, ps.instructions, p.frequency
            FROM prescription_schedules ps
            JOIN prescriptions p ON p.id_prescription = ps.id_prescription
            JOIN medications m ON m.id_medication = p.id_medication
            WHERE p.id_patient = %s
              AND p.statuss = 'active'
              AND CURDATE() BETWEEN p.start_date AND p.end_date
            ORDER BY ps.time_of_day
        """,
            (id_patient,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def update_user_password(id_user, old_password, new_password):
    """Меняет пароль пользователя, если старый пароль верный."""
    import hashlib
    conn = get_connection()
    if not conn: return False, "Нет связи с БД"
    try:
        cur = conn.cursor()

        # 1. Проверяем старый пароль
        cur.execute("SELECT password_hash FROM users WHERE id_user = %s", (id_user,))
        row = cur.fetchone()
        if not row:
            return False, "Пользователь не найден"

        old_hash = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
        if row[0] != old_hash:
            return False, "Текущий пароль введен неверно"

        # 2. Устанавливаем новый пароль
        new_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        cur.execute("UPDATE users SET password_hash = %s WHERE id_user = %s", (new_hash, id_user))
        conn.commit()

        logging.info(f"Пользователь id={id_user} сменил пароль")
        return True, "Пароль успешно изменен"

    except mysql.connector.Error as err:
        logging.error(f"Ошибка смены пароля: {err}")
        return False, "Ошибка базы данных"
    finally:
        conn.close()
