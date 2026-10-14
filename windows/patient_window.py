from datetime import datetime

from PySide6.QtCore import QDate, QTime, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QColor, QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QHeaderView,
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect,
    QMessageBox,
)

import db
import theme
from ui_py.ui_patient import Ui_PatientWindow
from windows import msgbox as mb


class PatientWindow(QMainWindow):
    def __init__(self, user_data, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.ui = Ui_PatientWindow()
        self.ui.setupUi(self)

        self.id_user = user_data["id_user"]
        self.full_name = user_data["full_name"]

        patient = db.get_patient_by_user(self.id_user)
        if not patient:
            mb.critical(self, "Ошибка", "Профиль пациента не найден")
            self.close()
            return
        self.id_patient = patient[0]

        self.ui.nameLabel.setText(self.full_name)
        self.ui.avatarLabel.setText(self.full_name[0].upper() if self.full_name else "?")

        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"
        short_name = self.full_name.split()[0] if self.full_name else ""
        self.ui.greetingLabel.setText(f"{greeting}, {short_name}!")

        for frame in (
            self.ui.cardToday,
            self.ui.cardDiaryHome,
            self.ui.cardHistoryHome,
        ):
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(28)
            shadow.setColor(QColor(47, 92, 143, 40))
            shadow.setOffset(0, 6)
            frame.setGraphicsEffect(shadow)

        self.ui.prescrTable.setColumnCount(6)
        self.ui.prescrTable.setHorizontalHeaderLabels(
            ["ID", "Лекарство", "Дозировка", "Кратность", "Начало", "Статус"]
        )
        self.ui.prescrTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.historyTable.setColumnCount(5)
        self.ui.historyTable.setHorizontalHeaderLabels(
            ["ID", "Дата", "Время", "Самочувствие", "Симптомы"]
        )
        self.ui.historyTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.nav_buttons = [
            self.ui.navHome,
            self.ui.navPrescr,
            self.ui.navDiary,
            self.ui.navHistory,
            self.ui.navProfile,
            self.ui.navHelp,
        ]
        self.ui.navHome.clicked.connect(lambda: self.go_to(0))
        self.ui.navPrescr.clicked.connect(lambda: self.go_to(1))
        self.ui.navDiary.clicked.connect(lambda: self.go_to(2))
        self.ui.navHistory.clicked.connect(lambda: self.go_to(3))
        self.ui.navProfile.clicked.connect(lambda: self.go_to(4))
        self.ui.navHelp.clicked.connect(lambda: self.go_to(5))

        self.ui.btnOpenPrescrFromHome.clicked.connect(lambda: self.go_to(1))
        self.ui.btnOpenDiaryFromHome.clicked.connect(lambda: self.go_to(2))
        self.ui.btnOpenHistoryFromHome.clicked.connect(lambda: self.go_to(3))

        self.ui.saveDiaryBtn.clicked.connect(self.save_diary)
        self.ui.refreshPrescrBtn.clicked.connect(self.load_prescriptions)
        self.ui.logoutBtn.clicked.connect(self.on_logout)
        self.ui.intensitySlider.valueChanged.connect(self.on_intensity_changed)

        self.load_history()
        self.load_prescriptions()
        self.load_profile()
        self.go_to(0, animate=False)

        self.ui.saveDiaryBtn.setToolTip("Сохранить запись в дневник")
        self.ui.refreshPrescrBtn.setToolTip("Обновить список назначений")

        QShortcut(QKeySequence("F1"), self, lambda: self.go_to(5))
        QShortcut(QKeySequence("Ctrl+Q"), self, self.on_logout)

        theme.apply_to_window(self, theme.is_dark())

        # === ТАЙМЕР НАПОМИНАНИЙ ===
        self._notified_today = set()  # чтобы не спамить одним и тем же
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(30_000)  # каждые 30 секунд
        # Проверяем сразу при запуске, но через 2 секунды,
        # чтобы окно успело отрисоваться
        QTimer.singleShot(2000, self.check_reminders)

    def go_to(self, index: int, animate: bool = True):
        self.ui.pages.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        titles = [
            "Главная",
            "Мои назначения",
            "Дневник самочувствия",
            "История записей",
            "Мой профиль",
            "Помощь",
        ]
        self.ui.pageTitleLabel.setText(titles[index])

        if animate:
            effect = QGraphicsOpacityEffect(self.ui.pages)
            self.ui.pages.setGraphicsEffect(effect)
            anim = QPropertyAnimation(effect, b"opacity", self)
            anim.setDuration(220)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim.start()
            self._anim = anim

    def on_intensity_changed(self, value):
        self.ui.intensityValueLabel.setText(str(value))

    def on_logout(self):
        if self.login_window:
            self.login_window.return_from_child()
        self.close()

    def load_profile(self):
        profile = db.get_patient_profile(self.id_patient)
        if not profile:
            return
        self.ui.profFullName.setText(str(profile.get("full_name") or "—"))
        self.ui.profBirthDate.setText(str(profile.get("birth_date") or "—"))
        self.ui.profGender.setText(str(profile.get("gender") or "не указан"))
        self.ui.profPolicy.setText(str(profile.get("policy_number") or "—"))
        self.ui.profPhone.setText(str(profile.get("phone") or "—"))

        patient = db.get_patient_by_user(self.id_user)
        if patient and patient[2]:
            id_doctor = patient[2]
            conn = db.get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        """
                        select u.full_name from doctors d
                        join users u on u.id_user = d.id_user
                        where d.id_doctor = %s
                    """,
                        (id_doctor,),
                    )
                    row = cur.fetchone()
                    if row:
                        self.ui.profDoctor.setText(str(row[0]))
                    else:
                        self.ui.profDoctor.setText("не назначен")
                finally:
                    conn.close()
            else:
                self.ui.profDoctor.setText("не назначен")
        else:
            self.ui.profDoctor.setText("не назначен")

    # ============== НАПОМИНАНИЯ О ПРИЁМЕ ==============
    def check_reminders(self):
        """Проверяет, не пора ли принять лекарство, и показывает уведомление."""
        try:
            schedules = db.get_today_schedules_for_patient(self.id_patient)
        except Exception as e:
            print(f"Ошибка получения расписания: {e}")
            return

        if not schedules:
            return

        now = QTime.currentTime()
        today_str = QDate.currentDate().toString("yyyy-MM-dd")

        for sched in schedules:
            id_prescription = sched[0]
            name_med = sched[1]
            dose = sched[2]
            time_of_day = sched[3]
            instructions = sched[4] or ""

            key = f"{id_prescription}_{time_of_day}_{today_str}"
            if key in self._notified_today:
                continue

            # time_of_day из MySQL может быть datetime.timedelta или
            # datetime.time
            try:
                if hasattr(time_of_day, "seconds"):
                    total_sec = time_of_day.seconds
                    h = total_sec // 3600
                    m = (total_sec % 3600) // 60
                else:
                    h = time_of_day.hour
                    m = time_of_day.minute
            except Exception:
                continue

            sched_time = QTime(h, m)
            # Разница в минутах между сейчас и временем приёма
            diff = now.secsTo(sched_time) / 60.0

            # Если время приёма наступило (в пределах ±1 минуты)
            if -1 <= diff <= 1:
                self._notified_today.add(key)
                self._show_reminder(name_med, dose, sched_time.toString("HH:mm"), instructions)

    def _show_reminder(self, name_med, dose, time_str, instructions):
        """Показывает всплывающее окно с напоминанием."""
        text = (
            f"💊 Время принять лекарство\n\n"
            f"Препарат: {name_med}\n"
            f"Доза: {dose}\n"
            f"Время: {time_str}"
        )
        if instructions:
            text += f"\n\nИнструкции: {instructions}"

        msg = QMessageBox(self)
        msg.setWindowTitle("Напоминание о приёме")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    # ============== ДНЕВНИК ==============
    def _collect_symptoms(self):
        checks = [
            (self.ui.chkHeadache, "головная боль"),
            (self.ui.chkWeakness, "слабость"),
            (self.ui.chkNausea, "тошнота"),
            (self.ui.chkDizzy, "головокружение"),
            (self.ui.chkHeart, "боль в сердце"),
            (self.ui.chkBreath, "одышка"),
            (self.ui.chkPressureUp, "повышение давления"),
            (self.ui.chkSleep, "нарушение сна"),
            (self.ui.chkAppetite, "потеря аппетита"),
            (self.ui.chkTremor, "тремор рук"),
            (self.ui.chkSweat, "повышенная потливость"),
            (self.ui.chkOtherSymptom, "другое"),
        ]
        return [name for chk, name in checks if chk.isChecked()]

    def _collect_triggers(self):
        checks = [
            (self.ui.trigStress, "стресс"),
            (self.ui.trigWeather, "смена погоды"),
            (self.ui.trigFood, "еда"),
            (self.ui.trigPhysical, "физическая нагрузка"),
            (self.ui.trigSleep, "недосып"),
            (self.ui.trigSkipMed, "пропуск лекарства"),
            (self.ui.trigAlcohol, "алкоголь"),
            (self.ui.trigOtherTrigger, "другое"),
        ]
        return [name for chk, name in checks if chk.isChecked()]

    def save_diary(self):
        from validators import (
            validate_pressure,
            validate_pulse,
            validate_sugar,
            validate_temperature,
            validate_height,
            validate_weight,
        )

        well_being = self.ui.wellBeingCombo.currentText()
        intensity = self.ui.intensitySlider.value()
        symptoms = self._collect_symptoms()
        triggers = self._collect_triggers()
        notes = self.ui.notesText.toPlainText().strip()

        # === ВАЛИДАЦИЯ ===
        pressure = self.ui.pressureLine.text().strip()
        pulse = self.ui.pulseLine.text().strip()
        sugar = self.ui.sugarLine.text().strip()
        temp = self.ui.tempLine.text().strip()
        height = self.ui.heightLine.text().strip() if hasattr(self.ui, "heightLine") else ""
        weight = self.ui.weightLine.text().strip() if hasattr(self.ui, "weightLine") else ""

        checks = [
            ("Давление", validate_pressure(pressure)),
            ("Пульс", validate_pulse(pulse)),
            ("Сахар", validate_sugar(sugar)),
            ("Температура", validate_temperature(temp)),
            ("Рост", validate_height(height)),
            ("Вес", validate_weight(weight)),
        ]

        for field_name, (ok, err) in checks:
            if not ok:
                mb.warning(self, f"Ошибка в поле «{field_name}»", err)
                return

        if not notes and not symptoms and intensity == 0:
            mb.warning(
                self,
                "Пустая запись",
                "Заполните хотя бы что-то: симптомы, показатели или заметки.",
            )
            return
        # === КОНЕЦ ВАЛИДАЦИИ ===

        parts = [well_being]
        if intensity > 0:
            parts.append(f"интенсивность: {intensity}/10")
        if triggers:
            parts.append("триггеры: " + ", ".join(triggers))
        if notes:
            parts.append("заметки: " + notes)
        well_being_text = ". ".join(parts)

        symptoms_text = ", ".join(symptoms) if symptoms else "нет"

        # === СОХРАНЕНИЕ В БД ===
        today = QDate.currentDate().toString("yyyy-MM-dd")
        now = QTime.currentTime().toString("HH:mm:ss")

        id_diary = db.create_diary_entry(
            self.id_patient, today, now, well_being_text, symptoms_text
        )
        if not id_diary:
            mb.critical(self, "Ошибка", "Не удалось сохранить запись")
            return

        if pressure:
            db.create_health_indicator(id_diary, "Давление", pressure, "мм рт.ст.")
        if pulse:
            db.create_health_indicator(id_diary, "Пульс", pulse, "уд/мин")
        if sugar:
            db.create_health_indicator(id_diary, "Сахар", sugar, "ммоль/л")
        if temp:
            db.create_health_indicator(id_diary, "Температура", temp, "°C")
        if height:
            db.create_health_indicator(id_diary, "Рост", height, "см")
        if weight:
            db.create_health_indicator(id_diary, "Вес", weight, "кг")

        mb.info(self, "Готово", "Запись сохранена")

        # === ОЧИСТКА ФОРМЫ ===
        self.ui.wellBeingCombo.setCurrentIndex(0)
        self.ui.intensitySlider.setValue(0)
        for chk in (
            self.ui.chkHeadache,
            self.ui.chkWeakness,
            self.ui.chkNausea,
            self.ui.chkDizzy,
            self.ui.chkHeart,
            self.ui.chkBreath,
            self.ui.chkPressureUp,
            self.ui.chkSleep,
            self.ui.chkAppetite,
            self.ui.chkTremor,
            self.ui.chkSweat,
            self.ui.chkOtherSymptom,
            self.ui.trigStress,
            self.ui.trigWeather,
            self.ui.trigFood,
            self.ui.trigPhysical,
            self.ui.trigSleep,
            self.ui.trigSkipMed,
            self.ui.trigAlcohol,
            self.ui.trigOtherTrigger,
        ):
            chk.setChecked(False)
        self.ui.pressureLine.clear()
        self.ui.pulseLine.clear()
        self.ui.sugarLine.clear()
        self.ui.tempLine.clear()
        if hasattr(self.ui, "heightLine"):
            self.ui.heightLine.clear()
        if hasattr(self.ui, "weightLine"):
            self.ui.weightLine.clear()
        self.ui.notesText.clear()

        self.load_history()

    def load_history(self):
        entries = db.get_diary_entries_for_patient(self.id_patient)
        self.ui.historyTable.setRowCount(len(entries))
        for r, e in enumerate(entries):
            self.ui.historyTable.setItem(r, 0, QTableWidgetItem(str(e[0])))
            self.ui.historyTable.setItem(r, 1, QTableWidgetItem(str(e[1])))
            self.ui.historyTable.setItem(r, 2, QTableWidgetItem(str(e[2])))
            self.ui.historyTable.setItem(r, 3, QTableWidgetItem(str(e[3] or "")))
            self.ui.historyTable.setItem(r, 4, QTableWidgetItem(str(e[4] or "")))

    def load_prescriptions(self):
        prescr = db.get_prescriptions_for_patient(self.id_patient)
        self.ui.prescrTable.setRowCount(len(prescr))
        active_lines = []
        for r, p in enumerate(prescr):
            self.ui.prescrTable.setItem(r, 0, QTableWidgetItem(str(p[0])))
            self.ui.prescrTable.setItem(r, 1, QTableWidgetItem(str(p[1])))
            self.ui.prescrTable.setItem(r, 2, QTableWidgetItem(str(p[2])))
            self.ui.prescrTable.setItem(r, 3, QTableWidgetItem(str(p[3])))
            self.ui.prescrTable.setItem(r, 4, QTableWidgetItem(str(p[4])))
            self.ui.prescrTable.setItem(r, 5, QTableWidgetItem(str(p[6])))
            if str(p[6]).lower() == "active":
                active_lines.append(f"• {p[1]} — {p[2]} ({p[3]})")

        count = len(active_lines)
        self.ui.todayCountLabel.setText(f"{count} приёмов")
        if active_lines:
            self.ui.todayListLabel.setText("\n".join(active_lines[:5]))
        else:
            self.ui.todayListLabel.setText("У вас нет активных назначений")
