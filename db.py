import hashlib
import random
import string
from datetime import date, timedelta
import mysql.connector
from config import DB_CONFIG


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Ошибка подключения: {err}")
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
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_doctor FROM doctors WHERE id_user = %s", (id_user,))
        return cur.fetchone()
    finally:
        conn.close()


def get_patient_by_user(id_user):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_patient, id_user, id_doctor FROM patients WHERE id_user = %s", (id_user,))
        return cur.fetchone()
    finally:
        conn.close()


def get_patient_profile(id_patient):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT u.full_name, p.birth_date, p.gender, p.policy_number, p.phone
            FROM patients p
            JOIN users u ON u.id_user = p.id_user
            WHERE p.id_patient = %s
        """, (id_patient,))
        return cur.fetchone()
    finally:
        conn.close()


# ============== ПАЦИЕНТЫ ВРАЧА ==============
def get_my_patients(id_doctor):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_patient, u.full_name, p.birth_date, p.policy_number, p.phone
            FROM patients p
            JOIN users u ON u.id_user = p.id_user
            WHERE p.id_doctor = %s
        """, (id_doctor,))
        return cur.fetchall()
    finally:
        conn.close()


def generate_login(full_name):
    parts = full_name.lower().split()
    base = "".join(parts[:2]) if len(parts) >= 2 else parts[0]
    base = "".join(c for c in base if c.isalnum())
    return base or "patient"


def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def create_patient_by_doctor(id_doctor, full_name, birth_date, gender, policy, phone, login, password):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cur.execute("""
            INSERT INTO users (login, password_hash, id_role, full_name)
            VALUES (%s, %s, (SELECT id_role FROM roles WHERE name_role = 'patient'), %s)
        """, (login, password_hash, full_name))
        id_user = cur.lastrowid
        cur.execute("""
            INSERT INTO patients (id_user, id_doctor, birth_date, gender, policy_number, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_user, id_doctor, birth_date, gender, policy, phone))
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
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_medication, name_med, dosage FROM medications ORDER BY name_med")
        return cur.fetchall()
    finally:
        conn.close()


def search_medications(text):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_medication, name_med, dosage FROM medications
            WHERE name_med LIKE %s OR dosage LIKE %s
            ORDER BY name_med
        """, (f"%{text}%", f"%{text}%"))
        return cur.fetchall()
    finally:
        conn.close()


def create_medication(name, form, dosage):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO medications (name_med, form, dosage) VALUES (%s, %s, %s)", (name, form, dosage))
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
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO prescriptions
            (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, commentt, statuss)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'active')
        """, (id_patient, id_doctor, id_medication, dosage, freq, start, end, comment))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_prescriptions_for_patient(id_patient):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_prescription, m.name_med, p.dosage, p.frequency, p.start_date, p.end_date, p.statuss
            FROM prescriptions p
            JOIN medications m ON m.id_medication = p.id_medication
            WHERE p.id_patient = %s
            ORDER BY p.start_date DESC
        """, (id_patient,))
        return cur.fetchall()
    finally:
        conn.close()


# ============== ДНЕВНИК (well_being_text) ==============
def create_diary_entry(id_patient, date, time, well_being, symptoms):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_patient, date, time, well_being, symptoms))
        conn.commit()
        return cur.lastrowid
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return None
    finally:
        conn.close()


def get_diary_entries_for_patient(id_patient):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_diary, entry_date, entry_time, well_being_text, symptoms
            FROM diary_entries WHERE id_patient = %s
            ORDER BY entry_date DESC, entry_time DESC
        """, (id_patient,))
        return cur.fetchall()
    finally:
        conn.close()


# ============== ПОКАЗАТЕЛИ (valuee) ==============
def create_health_indicator(id_diary, type_name, value, unit):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO health_indicators (id_diary, indicator_type, valuee, unit)
            VALUES (%s, %s, %s, %s)
        """, (id_diary, type_name, value, unit))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_indicators_for_diary(id_diary):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT indicator_type, valuee, unit FROM health_indicators WHERE id_diary = %s", (id_diary,))
        return cur.fetchall()
    finally:
        conn.close()


# ============== ДИАГНОЗЫ (хранятся в diary_entries!) ==============
def get_all_diseases():
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_disease, code, name FROM diseases ORDER BY code")
        return cur.fetchall()
    finally:
        conn.close()


def search_diseases(text):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_disease, code, name FROM diseases
            WHERE code LIKE %s OR name LIKE %s ORDER BY code
        """, (f"%{text}%", f"%{text}%"))
        return cur.fetchall()
    finally:
        conn.close()


def get_diary_diagnosis(id_diary):
    conn = get_connection()
    if not conn: return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT doctor_diagnosis AS diagnosis, id_disease 
            FROM diary_entries WHERE id_diary = %s
        """, (id_diary,))
        row = cur.fetchone()
        return row if row else {}
    finally:
        conn.close()


def set_diary_diagnosis_full(id_diary, diagnosis, id_disease, id_doctor):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE diary_entries 
            SET doctor_diagnosis = %s, id_disease = %s, id_doctor_who_viewed = %s
            WHERE id_diary = %s
        """, (diagnosis, id_disease, id_doctor, id_diary))
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
    if not conn: return [], []
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
    if not conn: return [("Активные", 0), ("Завершённые", 0)]
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
    if not conn: return [], []
    try:
        cur = conn.cursor()
        today = date.today()
        start = today - timedelta(days=13)
        cur.execute("""
            SELECT entry_date, COUNT(*) FROM diary_entries
            WHERE entry_date >= %s
            GROUP BY entry_date ORDER BY entry_date
        """, (start,))
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
    if not conn: return []
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
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_user FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            return None
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cur.execute("""
            INSERT INTO users (login, password_hash, id_role, full_name)
            VALUES (%s, %s, (SELECT id_role FROM roles WHERE name_role = %s), %s)
        """, (login, password_hash, role_name, full_name))
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
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO doctors (id_user, specialty) VALUES (%s, %s)", (id_user, specialty))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def create_patient(id_user, full_name, birth_date, gender, policy, phone, id_doctor=None):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (id_user, id_doctor, birth_date, gender, policy_number, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_user, id_doctor, birth_date, gender, policy, phone))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def delete_user(id_user):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        # Удаляем health_indicators через diary_entries
        cur.execute("""
            DELETE FROM health_indicators WHERE id_diary IN
            (SELECT id_diary FROM diary_entries WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s))
        """, (id_user,))
        cur.execute("""
            DELETE FROM doctor_comments WHERE id_diary IN
            (SELECT id_diary FROM diary_entries WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s))
        """, (id_user,))
        cur.execute("""
            DELETE FROM diary_entries WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s)
        """, (id_user,))
        # Удаляем schedules через prescriptions
        cur.execute("""
            DELETE FROM prescription_schedules WHERE id_prescription IN
            (SELECT id_prescription FROM prescriptions WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s))
        """, (id_user,))
        cur.execute("""
            DELETE FROM reminders WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s)
        """, (id_user,))
        cur.execute("""
            DELETE FROM prescriptions WHERE id_patient IN
            (SELECT id_patient FROM patients WHERE id_user = %s)
        """, (id_user,))
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
    if not conn: return False
    try:
        cur = conn.cursor()
        password_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        cur.execute("UPDATE users SET password_hash = %s WHERE id_user = %s", (password_hash, id_user))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        conn.close()


def get_all_patients_with_doctors():
    conn = get_connection()
    if not conn: return []
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
    if not conn: return []
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
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("UPDATE patients SET id_doctor = %s WHERE id_patient = %s", (id_doctor, id_patient))
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
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO prescription_schedules 
            (id_prescription, time_of_day, dose, instructions)
            VALUES (%s, %s, %s, %s)
        """, (id_prescription, time_of_day, dose, instructions))
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
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_schedule, time_of_day, dose, instructions
            FROM prescription_schedules
            WHERE id_prescription = %s
            ORDER BY time_of_day
        """, (id_prescription,))
        return cur.fetchall()
    finally:
        conn.close()


def get_today_schedules_for_patient(id_patient):
    """Все приёмы на сегодня для пациента.
    Возвращает список: (id_prescription, name_med, dose, time_of_day, instructions)"""
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ps.id_prescription, m.name_med, ps.dose, ps.time_of_day, ps.instructions
            FROM prescription_schedules ps
            JOIN prescriptions p ON p.id_prescription = ps.id_prescription
            JOIN medications m ON m.id_medication = p.id_medication
            WHERE p.id_patient = %s
              AND p.statuss = 'active'
              AND CURDATE() BETWEEN p.start_date AND p.end_date
            ORDER BY ps.time_of_day
        """, (id_patient,))
        return cur.fetchall()
    finally:
        conn.close()


def get_last_prescription_id():
    """Возвращает id последнего созданного назначения."""
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id_prescription) FROM prescriptions")
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()