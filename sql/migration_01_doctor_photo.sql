-- Миграция для уже развёрнутой базы: поле с фотографией врача.
-- В photo хранится имя файла из папки images/doctors.
USE diary_therapy;
ALTER TABLE doctors ADD COLUMN photo VARCHAR(255) NULL AFTER email;
