-- Создание базы данных
CREATE DATABASE IF NOT EXISTS diary_therapy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE diary_therapy;

-- 1. Роли
CREATE TABLE IF NOT EXISTS roles (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    name_role VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Пользователи
CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    id_role INT NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_role) REFERENCES roles(id_role)
);

-- 3. Врачи
CREATE TABLE IF NOT EXISTS doctors (
    id_doctor INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL UNIQUE,
    specialty VARCHAR(100),
    office VARCHAR(50),
    schedule VARCHAR(200),
    phone VARCHAR(50),
    email VARCHAR(100),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);

-- 4. Пациенты
CREATE TABLE IF NOT EXISTS patients (
    id_patient INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL UNIQUE,
    id_doctor INT,
    gender VARCHAR(10),
    birth_date DATE,
    policy_number VARCHAR(50),
    phone VARCHAR(50),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_doctor) REFERENCES doctors(id_doctor) ON DELETE SET NULL
);

-- 5. Справочник МКБ-10
CREATE TABLE IF NOT EXISTS diseases (
    id_disease INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- 6. Препараты
CREATE TABLE IF NOT EXISTS medications (
    id_medication INT AUTO_INCREMENT PRIMARY KEY,
    name_med VARCHAR(200) NOT NULL,
    form VARCHAR(50),
    dosage VARCHAR(50),
    manufacturer VARCHAR(200),
    description TEXT
);

-- 7. Назначения
CREATE TABLE IF NOT EXISTS prescriptions (
    id_prescription INT AUTO_INCREMENT PRIMARY KEY,
    id_patient INT NOT NULL,
    id_doctor INT NOT NULL,
    id_medication INT NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    statuss VARCHAR(20) DEFAULT 'active',
    commentt TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_patient) REFERENCES patients(id_patient) ON DELETE CASCADE,
    FOREIGN KEY (id_doctor) REFERENCES doctors(id_doctor) ON DELETE CASCADE,
    FOREIGN KEY (id_medication) REFERENCES medications(id_medication)
);

-- 8. Расписание приема
CREATE TABLE IF NOT EXISTS prescription_schedules (
    id_schedule INT AUTO_INCREMENT PRIMARY KEY,
    id_prescription INT NOT NULL,
    time_of_day TIME NOT NULL,
    dose VARCHAR(50),
    instructions VARCHAR(200),
    FOREIGN KEY (id_prescription) REFERENCES prescriptions(id_prescription) ON DELETE CASCADE
);

-- 9. Дневник самочувствия
CREATE TABLE IF NOT EXISTS diary_entries (
    id_diary INT AUTO_INCREMENT PRIMARY KEY,
    id_patient INT NOT NULL,
    entry_date DATE NOT NULL,
    entry_time TIME NOT NULL,
    well_being_text TEXT NOT NULL,
    symptoms TEXT,
    doctor_diagnosis TEXT,
    id_disease INT,
    id_doctor_who_viewed INT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_patient) REFERENCES patients(id_patient) ON DELETE CASCADE,
    FOREIGN KEY (id_disease) REFERENCES diseases(id_disease) ON DELETE SET NULL,
    FOREIGN KEY (id_doctor_who_viewed) REFERENCES doctors(id_doctor) ON DELETE SET NULL
);

-- 10. Показатели здоровья
CREATE TABLE IF NOT EXISTS health_indicators (
    id_indicator INT AUTO_INCREMENT PRIMARY KEY,
    id_diary INT NOT NULL,
    indicator_type VARCHAR(50) NOT NULL,
    valuee VARCHAR(50) NOT NULL,
    unit VARCHAR(20),
    FOREIGN KEY (id_diary) REFERENCES diary_entries(id_diary) ON DELETE CASCADE
);

-- 11. Комментарии врача
CREATE TABLE IF NOT EXISTS doctor_comments (
    id_comment INT AUTO_INCREMENT PRIMARY KEY,
    id_diary INT NOT NULL,
    id_doctor INT NOT NULL,
    commentt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_diary) REFERENCES diary_entries(id_diary) ON DELETE CASCADE,
    FOREIGN KEY (id_doctor) REFERENCES doctors(id_doctor) ON DELETE CASCADE
);

-- 12. Журнал действий
CREATE TABLE IF NOT EXISTS audit_log (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT,
    actionn VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INT,
    ip_address VARCHAR(45),
    timestampp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE SET NULL
);

-- 13. Напоминания
CREATE TABLE IF NOT EXISTS reminders (
    id_reminder INT AUTO_INCREMENT PRIMARY KEY,
    id_patient INT NOT NULL,
    id_prescription INT NOT NULL,
    remind_time TIME NOT NULL,
    typee VARCHAR(50),
    is_sent TINYINT DEFAULT 0,
    FOREIGN KEY (id_patient) REFERENCES patients(id_patient) ON DELETE CASCADE,
    FOREIGN KEY (id_prescription) REFERENCES prescriptions(id_prescription) ON DELETE CASCADE
);


INSERT INTO roles (name_role) VALUES ('admin'), ('doctor'), ('patient');

-- Создаем первого администратора (логин: admin, пароль: admin123)
INSERT INTO users (login, password_hash, id_role, full_name)
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 1, 'Администратор Системы');