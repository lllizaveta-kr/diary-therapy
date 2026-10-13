# 🩺 Дневник терапии

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.5+-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Десктопное приложение для ведения дневника самочувствия пациентов, назначений врачей и аналитики для администратора.**

---

## 📖 О проекте

«Дневник терапии» — учебный проект на Python с использованием PySide6 и MySQL. Приложение автоматизирует ведение медицинских записей: врачи назначают лечение, пациенты отслеживают состояние, администраторы управляют пользователями и просматривают статистику.

### 🎯 Основные возможности

- **Авторизация** с хешированием паролей (SHA-256) и разграничением прав доступа.
- **Три роли:** администратор, врач, пациент — каждая со своим интерфейсом.
- **Дневник самочувствия:** симптомы, показатели (давление, пульс, сахар, температура, рост, вес), триггеры, заметки.
- **Назначения:** выбор препарата из справочника, дозировка, кратность, период приёма.
- **Справочник МКБ-10:** постановка диагноза с выбором болезни из классификатора.
- **Аналитика администратора:** графики и экспорт в PDF.
- **Тёмная тема** и **горячие клавиши** (F1 — помощь, Ctrl+Q — выход).

---

## 🛠 Технологии

| Технология | Назначение |
|------------|------------|
| Python 3.10+ | Язык программирования |
| PySide6 (Qt for Python) | Графический интерфейс |
| MySQL 8.0+ | База данных |
| mysql-connector-python | Драйвер подключения к MySQL |
| hashlib (SHA-256) | Хеширование паролей |
| Qt Designer | Создание UI-форм |

---

## 📸 Скриншоты

### Авторизация
![Авторизация](images/login.png)

### Окно администратора — статистика
![Админ статистика](images/admin_stats.png)

### Окно администратора — управление пользователями
![Админ пользователи](images/admin_users.png)

### Окно врача
![Врач](images/doctor.png)

### Окно пациента
![Пациент](images/patient.png)

---

## 🚀 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/lllizaveta-kr/diary-therapy.git
cd diary-therapy
```

### 2. Создать виртуальное окружение и установить зависимости

```bash
python -m venv .venv
.venv\Scripts\activate
pip install PySide6 mysql-connector-python
```

### 3. Настроить подключение к БД

Скопируйте `config.example.py` в `config.py` и укажите свой пароль от MySQL.

### 4. Создать базу данных

Выполните SQL-скрипт из папки `sql/` в MySQL Workbench.

### 5. Запустить приложение

```bash
python main.py
```

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---

## 👩‍💻 Автор

**Елизавета Кравцова**  
GitHub: [@lllizaveta-kr](https://github.com/lllizaveta-kr)