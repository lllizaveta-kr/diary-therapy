-- Тестовые данные для демонстрации приложения.
-- Запускать после diary_therapy_bd.sql на чистой базе.

USE diary_therapy;

-- =========================================================
-- БЕЗОПАСНАЯ ОЧИСТКА ДУБЛИКАТОВ ПЕРЕД ЗАГРУЗКОЙ
-- (Удаляет старые дубликаты, чтобы список лекарств был чистым)
-- =========================================================
SET SQL_SAFE_UPDATES = 0;


-- ============== СПРАВОЧНИК МКБ-10 ==============
INSERT IGNORE INTO diseases (code, name, description) VALUES
('I10',   'Эссенциальная (первичная) гипертензия', 'Стойкое повышение артериального давления без установленной причины'),
('I11.9', 'Гипертензивная болезнь с поражением сердца без сердечной недостаточности', NULL),
('I20.8', 'Другие формы стенокардии', NULL),
('I25.1', 'Атеросклеротическая болезнь сердца', NULL),
('I48',   'Фибрилляция и трепетание предсердий', NULL),
('I50.0', 'Застойная сердечная недостаточность', NULL),
('E11.9', 'Сахарный диабет 2 типа без осложнений', 'Инсулиннезависимый сахарный диабет'),
('E10.9', 'Сахарный диабет 1 типа без осложнений', NULL),
('E03.9', 'Гипотиреоз неуточнённый', NULL),
('E66.0', 'Ожирение, обусловленное избыточным поступлением энергетических ресурсов', NULL),
('E78.0', 'Чистая гиперхолестеринемия', NULL),
('J45.0', 'Астма с преобладанием аллергического компонента', NULL),
('J44.9', 'Хроническая обструктивная лёгочная болезнь неуточнённая', NULL),
('J06.9', 'Острая инфекция верхних дыхательных путей неуточнённая', 'ОРВИ'),
('J20.9', 'Острый бронхит неуточнённый', NULL),
('K21.0', 'Гастроэзофагеальный рефлюкс с эзофагитом', NULL),
('K29.5', 'Хронический гастрит неуточнённый', NULL),
('K58.9', 'Синдром раздражённого кишечника без диареи', NULL),
('G43.9', 'Мигрень неуточнённая', NULL),
('G44.2', 'Головная боль напряжённого типа', NULL),
('G47.0', 'Нарушения засыпания и поддержания сна (бессонница)', NULL),
('F41.1', 'Генерализованное тревожное расстройство', NULL),
('F32.0', 'Депрессивный эпизод лёгкой степени', NULL),
('M54.5', 'Боль внизу спины', NULL),
('M17.9', 'Гонартроз неуточнённый', NULL),
('M10.9', 'Подагра неуточнённая', NULL),
('N39.0', 'Инфекция мочевыводящих путей без установленной локализации', NULL),
('D50.9', 'Железодефицитная анемия неуточнённая', NULL),
('L20.9', 'Атопический дерматит неуточнённый', NULL),
('R51',   'Головная боль', 'Симптом без установленного диагноза');

-- ============== ПРЕПАРАТЫ ==============
INSERT IGNORE INTO medications (name_med, form, dosage, manufacturer, description) VALUES
('Лизиноприл',      'таблетки', '10 мг',     'Гедеон Рихтер', 'Ингибитор АПФ, снижает давление'),
('Амлодипин',       'таблетки', '5 мг',      'Озон',          'Блокатор кальциевых каналов'),
('Бисопролол',      'таблетки', '5 мг',      'Мерк',          'Бета-адреноблокатор'),
('Лозартан',        'таблетки', '50 мг',     'КРКА',          'Блокатор рецепторов ангиотензина II'),
('Индапамид',       'таблетки', '2,5 мг',    'Сервье',        'Диуретик'),
('Аторвастатин',    'таблетки', '20 мг',     'Пфайзер',       'Снижает уровень холестерина'),
('Метформин',       'таблетки', '850 мг',    'Берлин-Хеми',   'Сахароснижающее средство'),
('Гликлазид',       'таблетки', '60 мг',     'Сервье',        'Сахароснижающее средство'),
('Левотироксин',    'таблетки', '50 мкг',    'Берлин-Хеми',   'Гормон щитовидной железы'),
('Омепразол',       'капсулы',  '20 мг',     'Озон',          'Снижает кислотность желудка'),
('Панкреатин',      'таблетки', '25000 ЕД',  'Берлин-Хеми',   'Ферментный препарат'),
('Сальбутамол',     'аэрозоль', '100 мкг',   'ГлаксоСмитКляйн', 'Бронхолитик быстрого действия'),
('Будесонид',       'аэрозоль', '200 мкг',   'АстраЗенека',   'Ингаляционный глюкокортикоид'),
('Ибупрофен',       'таблетки', '400 мг',    'Фармстандарт',  'НПВС, обезболивающее'),
('Парацетамол',     'таблетки', '500 мг',    'Фармстандарт',  'Жаропонижающее, обезболивающее'),
('Суматриптан',     'таблетки', '50 мг',     'Озон',          'Средство от мигрени'),
('Мелатонин',       'таблетки', '3 мг',      'Юнифарм',       'Регулятор сна'),
('Сертралин',       'таблетки', '50 мг',     'Пфайзер',       'Антидепрессант'),
('Ацетилсалициловая кислота', 'таблетки', '100 мг', 'Байер',  'Антиагрегант'),
('Железа сульфат',  'таблетки', '100 мг',    'Эгис',          'Препарат железа'),
('Амоксициллин',    'капсулы',  '500 мг',    'Сандоз',        'Антибиотик'),
('Цетиризин',       'таблетки', '10 мг',     'Доктор Реддис', 'Антигистаминное средство');

-- ============== ВРАЧИ ==============
INSERT IGNORE INTO users (login, password_hash, id_role, full_name) VALUES
('ivanova',  SHA2('doctor123', 256), (SELECT id_role FROM roles WHERE name_role = 'doctor' LIMIT 1), 'Иванова Елена Сергеевна'),
('petrov',   SHA2('doctor123', 256), (SELECT id_role FROM roles WHERE name_role = 'doctor' LIMIT 1), 'Петров Андрей Николаевич'),
('smirnova', SHA2('doctor123', 256), (SELECT id_role FROM roles WHERE name_role = 'doctor' LIMIT 1), 'Смирнова Ольга Викторовна');

INSERT IGNORE INTO doctors (id_user, specialty, office, schedule, phone, email) VALUES
((SELECT id_user FROM users WHERE login = 'ivanova' LIMIT 1),  'Терапевт',      '204', 'Пн-Пт 8:00-14:00',  '+74951112233', 'ivanova@clinic.ru'),
((SELECT id_user FROM users WHERE login = 'petrov' LIMIT 1),   'Кардиолог',     '310', 'Пн, Ср, Пт 12:00-18:00', '+74951112244', 'petrov@clinic.ru'),
((SELECT id_user FROM users WHERE login = 'smirnova' LIMIT 1), 'Эндокринолог',  '115', 'Вт, Чт 9:00-15:00', '+74951112255', 'smirnova@clinic.ru');

SET @d_ivanova  = (SELECT d.id_doctor FROM doctors d JOIN users u ON u.id_user = d.id_user WHERE u.login = 'ivanova' LIMIT 1);
SET @d_petrov   = (SELECT d.id_doctor FROM doctors d JOIN users u ON u.id_user = d.id_user WHERE u.login = 'petrov' LIMIT 1);
SET @d_smirnova = (SELECT d.id_doctor FROM doctors d JOIN users u ON u.id_user = d.id_user WHERE u.login = 'smirnova' LIMIT 1);

-- ============== ПАЦИЕНТЫ ==============
INSERT IGNORE INTO users (login, password_hash, id_role, full_name) VALUES
('kuznetsov', SHA2('patient123', 256), (SELECT id_role FROM roles WHERE name_role = 'patient' LIMIT 1), 'Кузнецов Дмитрий Алексеевич'),
('sokolova',  SHA2('patient123', 256), (SELECT id_role FROM roles WHERE name_role = 'patient' LIMIT 1), 'Соколова Марина Игоревна'),
('popov',     SHA2('patient123', 256), (SELECT id_role FROM roles WHERE name_role = 'patient' LIMIT 1), 'Попов Сергей Владимирович'),
('lebedeva',  SHA2('patient123', 256), (SELECT id_role FROM roles WHERE name_role = 'patient' LIMIT 1), 'Лебедева Анна Павловна'),
('kozlov',    SHA2('patient123', 256), (SELECT id_role FROM roles WHERE name_role = 'patient' LIMIT 1), 'Козлов Игорь Петрович'),
('novikova',  SHA2('patient123', 256), (SELECT id_role FROM roles WHERE name_role = 'patient' LIMIT 1), 'Новикова Татьяна Юрьевна');

INSERT IGNORE INTO patients (id_user, id_doctor, gender, birth_date, policy_number, phone) VALUES
((SELECT id_user FROM users WHERE login = 'kuznetsov' LIMIT 1), @d_petrov,   'мужской', '1961-03-14', '7745123456789012', '+79161234501'),
((SELECT id_user FROM users WHERE login = 'sokolova' LIMIT 1),  @d_smirnova, 'женский', '1975-08-22', '7745123456789023', '+79161234502'),
((SELECT id_user FROM users WHERE login = 'popov' LIMIT 1),     @d_ivanova,  'мужской', '1988-11-05', '7745123456789034', '+79161234503'),
((SELECT id_user FROM users WHERE login = 'lebedeva' LIMIT 1),  @d_ivanova,  'женский', '1993-02-17', '7745123456789045', '+79161234504'),
((SELECT id_user FROM users WHERE login = 'kozlov' LIMIT 1),    @d_petrov,   'мужской', '1954-06-30', '7745123456789056', '+79161234505'),
((SELECT id_user FROM users WHERE login = 'novikova' LIMIT 1),  @d_smirnova, 'женский', '1969-12-09', '7745123456789067', '+79161234506');

SET @p_kuznetsov = (SELECT p.id_patient FROM patients p JOIN users u ON u.id_user = p.id_user WHERE u.login = 'kuznetsov' LIMIT 1);
SET @p_sokolova  = (SELECT p.id_patient FROM patients p JOIN users u ON u.id_user = p.id_user WHERE u.login = 'sokolova' LIMIT 1);
SET @p_popov     = (SELECT p.id_patient FROM patients p JOIN users u ON u.id_user = p.id_user WHERE u.login = 'popov' LIMIT 1);
SET @p_lebedeva  = (SELECT p.id_patient FROM patients p JOIN users u ON u.id_user = p.id_user WHERE u.login = 'lebedeva' LIMIT 1);
SET @p_kozlov    = (SELECT p.id_patient FROM patients p JOIN users u ON u.id_user = p.id_user WHERE u.login = 'kozlov' LIMIT 1);
SET @p_novikova  = (SELECT p.id_patient FROM patients p JOIN users u ON u.id_user = p.id_user WHERE u.login = 'novikova' LIMIT 1);

-- ============== НАЗНАЧЕНИЯ ==============
-- Хелпер для поиска препарата по названию (Добавлен LIMIT 1)
SET @m_lizinopril  = (SELECT id_medication FROM medications WHERE name_med = 'Лизиноприл' LIMIT 1);
SET @m_amlodipin   = (SELECT id_medication FROM medications WHERE name_med = 'Амлодипин' LIMIT 1);
SET @m_bisoprolol  = (SELECT id_medication FROM medications WHERE name_med = 'Бисопролол' LIMIT 1);
SET @m_atorva      = (SELECT id_medication FROM medications WHERE name_med = 'Аторвастатин' LIMIT 1);
SET @m_metformin   = (SELECT id_medication FROM medications WHERE name_med = 'Метформин' LIMIT 1);
SET @m_levotirox   = (SELECT id_medication FROM medications WHERE name_med = 'Левотироксин' LIMIT 1);
SET @m_omeprazol   = (SELECT id_medication FROM medications WHERE name_med = 'Омепразол' LIMIT 1);
SET @m_ibuprofen   = (SELECT id_medication FROM medications WHERE name_med = 'Ибупрофен' LIMIT 1);
SET @m_sumatriptan = (SELECT id_medication FROM medications WHERE name_med = 'Суматриптан' LIMIT 1);
SET @m_melatonin   = (SELECT id_medication FROM medications WHERE name_med = 'Мелатонин' LIMIT 1);
SET @m_aspirin     = (SELECT id_medication FROM medications WHERE name_med = 'Ацетилсалициловая кислота' LIMIT 1);
SET @m_amoxicillin = (SELECT id_medication FROM medications WHERE name_med = 'Амоксициллин' LIMIT 1);

-- Кузнецов (кардиолог Петров): гипертония
INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_kuznetsov, @d_petrov, @m_lizinopril, '10 мг', '1 раз в день', CURDATE() - INTERVAL 20 DAY, CURDATE() + INTERVAL 70 DAY, 'active', 'Утром, независимо от еды. Контроль давления ежедневно.');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '08:00:00', '1 таблетка', 'Запить водой');

INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_kuznetsov, @d_petrov, @m_atorva, '20 мг', '1 раз в день', CURDATE() - INTERVAL 20 DAY, CURDATE() + INTERVAL 160 DAY, 'active', 'Вечером');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '20:00:00', '1 таблетка', 'После ужина');

-- Козлов (кардиолог Петров): ИБС
INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_kozlov, @d_petrov, @m_bisoprolol, '5 мг', '1 раз в день', CURDATE() - INTERVAL 30 DAY, CURDATE() + INTERVAL 60 DAY, 'active', 'Не отменять резко');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '08:00:00', '1 таблетка', 'Утром');

INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_kozlov, @d_petrov, @m_aspirin, '100 мг', '1 раз в день', CURDATE() - INTERVAL 30 DAY, CURDATE() + INTERVAL 150 DAY, 'active', NULL);
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '14:00:00', '1 таблетка', 'После обеда');

INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_kozlov, @d_petrov, @m_amlodipin, '5 мг', '1 раз в день', CURDATE() - INTERVAL 90 DAY, CURDATE() - INTERVAL 31 DAY, 'completed', 'Заменён на бисопролол');

-- Соколова (эндокринолог Смирнова): диабет 2 типа
INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_sokolova, @d_smirnova, @m_metformin, '850 мг', '2 раза в день', CURDATE() - INTERVAL 14 DAY, CURDATE() + INTERVAL 76 DAY, 'active', 'Во время еды. Контроль сахара натощак.');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '08:00:00', '1 таблетка', 'Во время завтрака'),
(@rx, '20:00:00', '1 таблетка', 'Во время ужина');

-- Новикова (эндокринолог Смирнова): гипотиреоз
INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_novikova, @d_smirnova, @m_levotirox, '50 мкг', '1 раз в день', CURDATE() - INTERVAL 40 DAY, CURDATE() + INTERVAL 140 DAY, 'active', 'Натощак, за 30 минут до завтрака');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '07:00:00', '1 таблетка', 'Натощак');

-- Попов (терапевт Иванова): гастрит, ОРВИ завершено
INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_popov, @d_ivanova, @m_omeprazol, '20 мг', '1 раз в день', CURDATE() - INTERVAL 7 DAY, CURDATE() + INTERVAL 21 DAY, 'active', 'За 30 минут до завтрака');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '07:30:00', '1 капсула', 'До еды');

INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_popov, @d_ivanova, @m_amoxicillin, '500 мг', '3 раза в день', CURDATE() - INTERVAL 45 DAY, CURDATE() - INTERVAL 38 DAY, 'completed', 'Курс 7 дней');

-- Лебедева (терапевт Иванова): мигрень, бессонница
INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_lebedeva, @d_ivanova, @m_sumatriptan, '50 мг', 'при приступе', CURDATE() - INTERVAL 10 DAY, CURDATE() + INTERVAL 50 DAY, 'active', 'Не более 2 таблеток в сутки');

INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_lebedeva, @d_ivanova, @m_melatonin, '3 мг', '1 раз в день', CURDATE() - INTERVAL 10 DAY, CURDATE() + INTERVAL 20 DAY, 'active', 'За час до сна');
SET @rx = LAST_INSERT_ID();
INSERT IGNORE INTO prescription_schedules (id_prescription, time_of_day, dose, instructions) VALUES
(@rx, '22:00:00', '1 таблетка', 'За час до сна');

INSERT IGNORE INTO prescriptions (id_patient, id_doctor, id_medication, dosage, frequency, start_date, end_date, statuss, commentt)
VALUES (@p_lebedeva, @d_ivanova, @m_ibuprofen, '400 мг', 'при боли', CURDATE() - INTERVAL 60 DAY, CURDATE() - INTERVAL 30 DAY, 'completed', NULL);

-- ============== ДНЕВНИК САМОЧУВСТВИЯ ==============
-- Кузнецов: давление постепенно снижается на фоне лечения
INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_kuznetsov, CURDATE() - INTERVAL 13 DAY, '08:40:00', 'Плохо. интенсивность: 6/10. триггеры: стресс, недосып. заметки: С утра давит в затылке', 'головная боль, повышение давления');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '158/96', 'мм рт.ст.'), (@e, 'Пульс', '84', 'уд/мин');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms, doctor_diagnosis, id_disease, id_doctor_who_viewed) VALUES
(@p_kuznetsov, CURDATE() - INTERVAL 10 DAY, '09:10:00', 'Удовлетворительно. интенсивность: 4/10. триггеры: смена погоды', 'головная боль', 'Артериальная гипертензия, подбор терапии', (SELECT id_disease FROM diseases WHERE code = 'I10' LIMIT 1), @d_petrov);
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '146/90', 'мм рт.ст.'), (@e, 'Пульс', '78', 'уд/мин');
INSERT IGNORE INTO doctor_comments (id_diary, id_doctor, commentt) VALUES
(@e, @d_petrov, 'Продолжайте приём лизиноприла, давление измерять утром и вечером.');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_kuznetsov, CURDATE() - INTERVAL 6 DAY, '08:30:00', 'Хорошо. заметки: Голова не болит', 'нет');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '138/86', 'мм рт.ст.'), (@e, 'Пульс', '74', 'уд/мин');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_kuznetsov, CURDATE() - INTERVAL 2 DAY, '08:20:00', 'Хорошо', 'нет');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '132/84', 'мм рт.ст.'), (@e, 'Пульс', '72', 'уд/мин'), (@e, 'Вес', '91', 'кг');

-- Козлов
INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms, doctor_diagnosis, id_disease, id_doctor_who_viewed) VALUES
(@p_kozlov, CURDATE() - INTERVAL 12 DAY, '10:00:00', 'Плохо. интенсивность: 5/10. триггеры: физическая нагрузка. заметки: Одышка при подъёме на 2 этаж', 'одышка, боль в сердце, слабость', 'Стабильная стенокардия напряжения', (SELECT id_disease FROM diseases WHERE code = 'I20.8' LIMIT 1), @d_petrov);
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '142/88', 'мм рт.ст.'), (@e, 'Пульс', '92', 'уд/мин');
INSERT IGNORE INTO doctor_comments (id_diary, id_doctor, commentt) VALUES
(@e, @d_petrov, 'Ограничить нагрузки, при боли в груди дольше 15 минут вызывать скорую.');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_kozlov, CURDATE() - INTERVAL 7 DAY, '09:45:00', 'Удовлетворительно. интенсивность: 3/10', 'слабость');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '134/82', 'мм рт.ст.'), (@e, 'Пульс', '68', 'уд/мин');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_kozlov, CURDATE() - INTERVAL 1 DAY, '09:30:00', 'Хорошо. заметки: Прошёл 2 км без одышки', 'нет');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '128/80', 'мм рт.ст.'), (@e, 'Пульс', '64', 'уд/мин');

-- Соколова: сахар
INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms, doctor_diagnosis, id_disease, id_doctor_who_viewed) VALUES
(@p_sokolova, CURDATE() - INTERVAL 13 DAY, '07:50:00', 'Удовлетворительно. интенсивность: 3/10. триггеры: еда. заметки: Сильная жажда', 'слабость, повышенная потливость', 'Сахарный диабет 2 типа, впервые выявленный', (SELECT id_disease FROM diseases WHERE code = 'E11.9' LIMIT 1), @d_smirnova);
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Сахар', '9.4', 'ммоль/л'), (@e, 'Вес', '84', 'кг'), (@e, 'Рост', '165', 'см');
INSERT IGNORE INTO doctor_comments (id_diary, id_doctor, commentt) VALUES
(@e, @d_smirnova, 'Начинаем метформин. Записывайте сахар натощак каждый день.');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_sokolova, CURDATE() - INTERVAL 9 DAY, '07:45:00', 'Плохо. интенсивность: 4/10. заметки: Тошнит после таблетки', 'тошнота');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Сахар', '8.1', 'ммоль/л');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_sokolova, CURDATE() - INTERVAL 5 DAY, '07:40:00', 'Удовлетворительно', 'нет');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Сахар', '7.2', 'ммоль/л');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_sokolova, CURDATE(), '07:35:00', 'Хорошо', 'нет');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Сахар', '6.4', 'ммоль/л'), (@e, 'Вес', '82.5', 'кг');

-- Новикова
INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_novikova, CURDATE() - INTERVAL 11 DAY, '19:20:00', 'Удовлетворительно. интенсивность: 3/10. триггеры: недосып', 'слабость, нарушение сна');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Пульс', '58', 'уд/мин'), (@e, 'Температура', '35.9', '°C');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_novikova, CURDATE() - INTERVAL 4 DAY, '19:00:00', 'Хорошо. заметки: Стало больше сил', 'нет');
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Пульс', '64', 'уд/мин'), (@e, 'Температура', '36.4', '°C');

-- Попов
INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms, doctor_diagnosis, id_disease, id_doctor_who_viewed) VALUES
(@p_popov, CURDATE() - INTERVAL 8 DAY, '13:15:00', 'Плохо. интенсивность: 6/10. триггеры: еда, стресс. заметки: Изжога и боль после острого', 'тошнота, потеря аппетита', 'Обострение хронического гастрита', (SELECT id_disease FROM diseases WHERE code = 'K29.5' LIMIT 1), @d_ivanova);
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO doctor_comments (id_diary, id_doctor, commentt) VALUES
(@e, @d_ivanova, 'Щадящая диета, исключить острое и кофе. Омепразол 3 недели.');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_popov, CURDATE() - INTERVAL 3 DAY, '13:00:00', 'Удовлетворительно. интенсивность: 2/10', 'нет');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_popov, CURDATE(), '12:40:00', 'Отлично. заметки: Изжоги нет', 'нет');

-- Лебедева
INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms, doctor_diagnosis, id_disease, id_doctor_who_viewed) VALUES
(@p_lebedeva, CURDATE() - INTERVAL 12 DAY, '21:30:00', 'Очень плохо. интенсивность: 9/10. триггеры: смена погоды, недосып. заметки: Приступ мигрени, свет раздражает', 'головная боль, тошнота, головокружение', 'Мигрень без ауры', (SELECT id_disease FROM diseases WHERE code = 'G43.9' LIMIT 1), @d_ivanova);
SET @e = LAST_INSERT_ID();
INSERT IGNORE INTO health_indicators (id_diary, indicator_type, valuee, unit) VALUES
(@e, 'Давление', '118/76', 'мм рт.ст.');
INSERT IGNORE INTO doctor_comments (id_diary, id_doctor, commentt) VALUES
(@e, @d_ivanova, 'Суматриптан при начале приступа. Ведите учёт триггеров.');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_lebedeva, CURDATE() - INTERVAL 9 DAY, '23:10:00', 'Плохо. интенсивность: 4/10. триггеры: стресс. заметки: Не могу уснуть', 'нарушение сна');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_lebedeva, CURDATE() - INTERVAL 5 DAY, '21:00:00', 'Удовлетворительно. интенсивность: 3/10. триггеры: алкоголь', 'головная боль');

INSERT IGNORE INTO diary_entries (id_patient, entry_date, entry_time, well_being_text, symptoms) VALUES
(@p_lebedeva, CURDATE() - INTERVAL 1 DAY, '22:15:00', 'Хорошо. заметки: С мелатонином сплю лучше', 'нет');

-- ============== ЖУРНАЛ ДЕЙСТВИЙ ==============
INSERT IGNORE INTO audit_log (id_user, actionn, entity_type, entity_id, ip_address) VALUES
((SELECT id_user FROM users WHERE login = 'admin' LIMIT 1),   'create_user',     'users',         (SELECT id_user FROM users WHERE login = 'ivanova' LIMIT 1), '127.0.0.1'),
((SELECT id_user FROM users WHERE login = 'petrov' LIMIT 1),  'create_prescription', 'prescriptions', NULL, '127.0.0.1'),
((SELECT id_user FROM users WHERE login = 'ivanova' LIMIT 1), 'set_diagnosis',   'diary_entries', NULL, '127.0.0.1');