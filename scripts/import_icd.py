import csv
import sys
import os

# Добавляем корневую папку в пути, чтобы скрипт видел db.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db


def import_icd_from_csv(filepath):
    """
    Импорт МКБ-10 из CSV.
    Ожидаемый формат: Код;Название;Описание (разделитель - точка с запятой)
    """
    conn = db.get_connection()
    if not conn:
        print("Ошибка: Нет подключения к БД. Проверь config.py.")
        return

    cur = conn.cursor()
    count = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) >= 2:
                    code = row[0].strip()
                    name = row[1].strip()
                    desc = row[2].strip() if len(row) > 2 else None

                    # INSERT IGNORE не даст упасть скрипту, если код уже есть
                    cur.execute("""
                        INSERT IGNORE INTO diseases (code, name, description)
                        VALUES (%s, %s, %s)
                    """, (code, name, desc))
                    count += 1
        conn.commit()
        print(f"Успешно обработано {count} строк МКБ-10.")
    except Exception as e:
        print(f"Ошибка чтения файла или записи в БД: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    # Путь к файлу с данными (создадим его ниже)
    file_path = os.path.join(os.path.dirname(__file__), "icd10_sample.csv")
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
    else:
        import_icd_from_csv(file_path)