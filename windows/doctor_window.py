import re
from datetime import datetime

from PySide6.QtCore import QDate, QPropertyAnimation, QEasingCurve, Qt, QTimer
from PySide6.QtGui import QColor, QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QHeaderView,
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QApplication,
    QFrame,
    QSizePolicy,
    QScrollArea,
    QWidget,
    QListWidget,
    QInputDialog,
    QMessageBox,
    QTableWidget,
)

import db
import theme
from ui_py.ui_doctor import Ui_DoctorWindow
from windows import msgbox as mb


class DoctorWindow(QMainWindow):
    def __init__(self, user_data, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.ui = Ui_DoctorWindow()
        self.ui.setupUi(self)

        self.id_user = user_data["id_user"]
        self.full_name = user_data["full_name"]

        doctor = db.get_doctor_by_user(self.id_user)
        if not doctor:
            mb.critical(self, "Ошибка", "Профиль врача не найден")
            self.close()
            return
        self.id_doctor = doctor[0]

        self.ui.nameLabel.setText(self.full_name)
        self.ui.avatarLabel.setText(self.full_name[0].upper() if self.full_name else "В")

        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"
        parts = self.full_name.split()
        short_name = parts[1] if len(parts) > 1 else ""
        self.ui.greetingLabel.setText(f"{greeting}, {short_name}!")

        for frame in (
            self.ui.cardPatients,
            self.ui.cardPrescrHome,
            self.ui.cardDiaryHome,
        ):
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(28)
            shadow.setColor(QColor(47, 92, 143, 40))
            shadow.setOffset(0, 6)
            frame.setGraphicsEffect(shadow)

        self.ui.patientsTable.setColumnCount(5)
        self.ui.patientsTable.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Дата рождения", "Полис", "Телефон"]
        )
        self.ui.patientsTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.nav_buttons = [
            self.ui.navHome,
            self.ui.navPatients,
            self.ui.navAddPatient,
            self.ui.navPrescriptions,
            self.ui.navDiaries,
            self.ui.navHelp,
        ]
        self.ui.navHome.clicked.connect(lambda: self.go_to(0))
        self.ui.navPatients.clicked.connect(lambda: self.go_to(1))
        self.ui.navAddPatient.clicked.connect(lambda: self.go_to(2))
        self.ui.navPrescriptions.clicked.connect(lambda: self.go_to(3))
        self.ui.navDiaries.clicked.connect(lambda: self.go_to(4))
        self.ui.navHelp.clicked.connect(lambda: self.go_to(5))

        self.ui.btnOpenPatientsFromHome.clicked.connect(lambda: self.go_to(1))
        self.ui.btnOpenPrescrFromHome.clicked.connect(lambda: self.go_to(3))
        self.ui.btnOpenDiariesFromHome.clicked.connect(lambda: self.go_to(4))

        self.ui.addPrescrBtn.clicked.connect(self.add_prescription)
        self.ui.addMedicationBtn.clicked.connect(self.add_new_medication)
        self.ui.medicationSearch.textChanged.connect(self.on_medication_search)
        self.ui.medicationList.itemClicked.connect(self.on_medication_selected)
        self.ui.viewDiaryBtn.clicked.connect(self.view_diary)
        self.ui.logoutBtn.clicked.connect(self.on_logout)
        self.ui.createPatientBtn.clicked.connect(self.create_patient)

        self.ui.startDate.setDate(QDate.currentDate())
        self.ui.endDate.setDate(QDate.currentDate().addDays(30))
        self.ui.newPatientBirthDate.setDate(QDate(2000, 1, 1))

        self._selected_medication_id = None
        self._meds_cache = []

        self.load_patients()
        self.load_medications()
        self.go_to(0, animate=False)

        self.ui.addPrescrBtn.setToolTip("Создать назначение")
        self.ui.createPatientBtn.setToolTip("Создать пациента")
        self.ui.viewDiaryBtn.setToolTip("Показать дневник")
        self.ui.addMedicationBtn.setToolTip("Добавить свой препарат в справочник")

        QShortcut(QKeySequence("F1"), self, lambda: self.go_to(5))
        QShortcut(QKeySequence("Ctrl+Q"), self, self.on_logout)
        QShortcut(QKeySequence("Ctrl+1"), self, lambda: self.go_to(0))
        QShortcut(QKeySequence("Ctrl+2"), self, lambda: self.go_to(1))
        QShortcut(QKeySequence("Ctrl+3"), self, lambda: self.go_to(2))
        QShortcut(QKeySequence("Ctrl+4"), self, lambda: self.go_to(3))
        QShortcut(QKeySequence("Ctrl+5"), self, lambda: self.go_to(4))

        theme.apply_to_window(self, theme.is_dark())

    def go_to(self, index: int, animate: bool = True):
        self.ui.pages.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

        titles = [
            "Главная",
            "Мои пациенты",
            "Добавить пациента",
            "Назначения",
            "Дневники пациентов",
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

    def on_logout(self):
        if self.login_window:
            self.login_window.return_from_child()
        self.close()

    # ============== СОЗДАНИЕ ПАЦИЕНТА ==============
    def create_patient(self):
        from validators import (
            validate_name,
            validate_phone,
            validate_policy,
            validate_birth_date,
        )

        full_name = self.ui.newPatientFullName.text().strip()
        policy = self.ui.newPatientPolicy.text().strip()
        phone = self.ui.newPatientPhone.text().strip()
        gender = self.ui.newPatientGender.currentText()
        birth = self.ui.newPatientBirthDate.date().toString("yyyy-MM-dd")

        # === ВАЛИДАЦИЯ ===
        ok, err = validate_name(full_name)
        if not ok:
            mb.warning(self, "Ошибка в ФИО", err)
            self.ui.newPatientFullName.setFocus()
            return

        ok, err = validate_policy(policy)
        if not ok:
            mb.warning(self, "Ошибка в полисе", err)
            self.ui.newPatientPolicy.setFocus()
            return

        ok, err = validate_phone(phone)
        if not ok:
            mb.warning(self, "Ошибка в телефоне", err)
            self.ui.newPatientPhone.setFocus()
            return

        ok, err = validate_birth_date(birth)
        if not ok:
            mb.warning(self, "Ошибка в дате рождения", err)
            return
        # === КОНЕЦ ВАЛИДАЦИИ ===

        login_base = db.generate_login(full_name)
        login = login_base
        counter = 1
        conn = db.get_connection()
        if conn:
            cur = conn.cursor()
            while True:
                cur.execute("select id_user from users where login = %s", (login,))
                if cur.fetchone() is None:
                    break
                counter += 1
                login = f"{login_base}{counter}"
            conn.close()

        password = db.generate_password()

        id_user = db.create_patient_by_doctor(
            self.id_doctor, full_name, birth, gender, policy, phone, login, password
        )
        if id_user is None:
            mb.critical(self, "Ошибка", "Не удалось создать пациента.")
            return

        self._show_credentials_dialog(login, password)

        self.ui.newPatientFullName.clear()
        self.ui.newPatientPolicy.clear()
        self.ui.newPatientPhone.clear()
        self.ui.newPatientGender.setCurrentIndex(0)
        self.ui.newPatientBirthDate.setDate(QDate(2000, 1, 1))

        self.load_patients()
        self.go_to(1)

    def _show_credentials_dialog(self, login: str, password: str):
        dlg = QDialog(self)
        dlg.setWindowTitle("Пациент создан")
        dlg.setMinimumWidth(460)
        dlg.setStyleSheet("""
            QDialog { background-color: #FFFFFF; }
            QLabel { color: #1A1A1A; font-family: "Times New Roman"; font-size: 13px; background: transparent; }
            QLineEdit { background-color: #F5F5F5; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 8px; padding: 10px 14px; font-family: "Times New Roman"; font-size: 14px; }
        """)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        info = QLabel(
            "Пациент успешно создан и привязан к вам.\n"
            "Скопируйте логин и пароль, передайте пациенту."
        )
        info.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addWidget(QLabel("Логин:"))
        login_field = QLineEdit(login)
        login_field.setReadOnly(True)
        layout.addWidget(login_field)

        layout.addWidget(QLabel("Пароль:"))
        pass_field = QLineEdit(password)
        pass_field.setReadOnly(True)
        layout.addWidget(pass_field)

        copy_all_btn = QPushButton("Скопировать логин и пароль")
        copy_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_all_btn.setStyleSheet("""
            QPushButton { background-color: #2F5C8F; color: white; border: none;
                border-radius: 8px; padding: 10px 16px; font-size: 13px; }
            QPushButton:hover { background-color: #1E4470; }
        """)

        close_btn = QPushButton("Закрыть")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background-color: #E0E0E0; color: #1A1A1A; border: none;
                border-radius: 8px; padding: 10px 24px; font-size: 13px; }
            QPushButton:hover { background-color: #D0D0D0; }
        """)

        def safe_set(btn, text):
            try:
                btn.setText(text)
            except RuntimeError:
                pass

        def copy_all():
            QApplication.clipboard().setText(f"Логин: {login}\nПароль: {password}")
            copy_all_btn.setText("✓ Скопировано")
            t = QTimer(dlg)
            t.setSingleShot(True)
            t.timeout.connect(lambda: safe_set(copy_all_btn, "Скопировать логин и пароль"))
            t.start(1500)

        copy_all_btn.clicked.connect(copy_all)
        close_btn.clicked.connect(dlg.accept)

        layout.addWidget(copy_all_btn)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(close_btn)
        layout.addLayout(row)

        dlg.exec()

    # ============== ПАЦИЕНТЫ ==============
    def load_patients(self):
        patients = db.get_my_patients(self.id_doctor)
        self.ui.patientsTable.setRowCount(len(patients))

        self.ui.patientCombo.clear()
        self.ui.diaryPatientCombo.clear()

        names_for_home = []
        for row, p in enumerate(patients):
            self.ui.patientsTable.setItem(row, 0, QTableWidgetItem(str(p[0])))
            self.ui.patientsTable.setItem(row, 1, QTableWidgetItem(str(p[1])))
            self.ui.patientsTable.setItem(row, 2, QTableWidgetItem(str(p[2])))
            self.ui.patientsTable.setItem(row, 3, QTableWidgetItem(str(p[3] or "")))
            self.ui.patientsTable.setItem(row, 4, QTableWidgetItem(str(p[4] or "")))

            self.ui.patientCombo.addItem(p[1], p[0])
            self.ui.diaryPatientCombo.addItem(p[1], p[0])
            names_for_home.append(f"• {p[1]}")

        count = len(patients)
        self.ui.patientsCountLabel.setText(f"{count} пациентов")
        if names_for_home:
            self.ui.patientsListLabel.setText("\n".join(names_for_home[:5]))
        else:
            self.ui.patientsListLabel.setText("У вас пока нет прикреплённых пациентов")

    # ============== ПРЕПАРАТЫ ==============
    def load_medications(self):
        meds = db.get_all_medications()
        self.ui.medicationList.clear()
        for m in meds:
            item_text = f"{m[1]} — {m[2]}" if m[2] else m[1]
            self.ui.medicationList.addItem(item_text)
        self._meds_cache = [(m[0], m[1], m[2]) for m in meds]

    def on_medication_search(self, text):
        text = text.strip()
        if not text:
            self.load_medications()
            return
        meds = db.search_medications(text)
        self.ui.medicationList.clear()
        for m in meds:
            item_text = f"{m[1]} — {m[2]}" if m[2] else m[1]
            self.ui.medicationList.addItem(item_text)
        self._meds_cache = [(m[0], m[1], m[2]) for m in meds]

    def on_medication_selected(self, item):
        idx = self.ui.medicationList.row(item)
        if 0 <= idx < len(self._meds_cache):
            med_id, name, dosage = self._meds_cache[idx]
            self._selected_medication_id = med_id
            self.ui.medicationSearch.setText(f"{name} — {dosage}")
            if not self.ui.dosageLine.text() and dosage:
                self.ui.dosageLine.setText(dosage)

    def add_new_medication(self):
        name, ok = QInputDialog.getText(self, "Новый препарат", "Введите название препарата:")
        if not ok or not name.strip():
            return
        name = name.strip()

        form, ok2 = QInputDialog.getText(
            self,
            "Форма выпуска",
            "Таблетки / Капсулы / Раствор / Аэрозоль / Гель / Другое:",
        )
        if not ok2:
            form = ""

        dosage, ok3 = QInputDialog.getText(self, "Дозировка", "Например: 10 мг, 500 мг, 5 мл:")
        if not ok3:
            dosage = ""

        med_id = db.create_medication(name, form.strip(), dosage.strip())
        if med_id:
            mb.info(self, "Готово", f"Препарат «{name}» добавлен в справочник")
            self._selected_medication_id = med_id
            self.ui.medicationSearch.setText(f"{name} — {dosage}")
            self.ui.dosageLine.setText(dosage)
            self.load_medications()
        else:
            mb.warning(self, "Ошибка", "Не удалось добавить препарат")

    def _get_selected_medication_id(self):
        if self._selected_medication_id:
            return self._selected_medication_id
        text = self.ui.medicationSearch.text().strip()
        if not text:
            return None
        name = text.split(" — ")[0].strip()
        meds = db.search_medications(name)
        if meds:
            return meds[0][0]
        return None

    def add_prescription(self):
        if self.ui.patientCombo.count() == 0:
            mb.warning(self, "Ошибка", "Нет пациентов")
            return

        id_patient = self.ui.patientCombo.currentData()
        id_medication = self._get_selected_medication_id()

        if not id_medication:
            mb.warning(
                self,
                "Не выбран препарат",
                "Выберите препарат из списка или введите новый,\n"
                "нажав кнопку «+ Добавить препарат».",
            )
            self.ui.medicationSearch.setFocus()
            return

        dosage = self.ui.dosageLine.text().strip()
        freq = self.ui.freqLine.text().strip()
        start = self.ui.startDate.date().toString("yyyy-MM-dd")
        end = self.ui.endDate.date().toString("yyyy-MM-dd")
        comment = self.ui.commentText.toPlainText().strip()

        if not dosage or not freq:
            mb.warning(self, "Ошибка", "Заполните дозировку и кратность.")
            return

        ok = db.create_prescription(
            id_patient,
            self.id_doctor,
            id_medication,
            dosage,
            freq,
            start,
            end,
            comment,
        )
        if not ok:
            mb.critical(self, "Ошибка", "Не удалось создать назначение")
            return

        # Спрашиваем врача: настроить расписание?
        reply = QMessageBox.question(
            self,
            "Расписание приёма",
            "Назначение создано.\n\n"
            "Хотите указать точное время приёма (например, 8:00, 14:00, 20:00)?\n"
            "Пациент получит напоминания в эти часы.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )

        if reply == QMessageBox.StandardButton.Yes:
            id_prescription = db.get_last_prescription_id()
            if id_prescription:
                self._open_schedule_dialog(id_prescription, dosage)

        mb.info(self, "Готово", "Назначение добавлено")
        self.ui.medicationSearch.clear()
        self.ui.dosageLine.clear()
        self.ui.freqLine.clear()
        self.ui.commentText.clear()
        self._selected_medication_id = None
        self.load_medications()

    def _open_schedule_dialog(self, id_prescription, default_dose):
        """Диалог настройки расписания приёма."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Расписание приёма")
        dlg.setMinimumWidth(560)
        dlg.setStyleSheet("""
            QDialog { background-color: #FFFFFF; }
            QLabel { color: #1A1A1A; font-family: "Times New Roman"; font-size: 13px; }
            QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC;
                border-radius: 8px; padding: 8px 12px; font-family: "Times New Roman"; font-size: 14px; }
            QTableWidget { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC;
                border-radius: 8px; font-family: "Times New Roman"; font-size: 13px; }
            QHeaderView::section { background-color: #F0F4FA; padding: 6px;
                font-family: "Times New Roman"; font-size: 12px; border: none; }
        """)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        info = QLabel(
            "Укажите, во сколько пациент должен принимать препарат.\n"
            "Можно добавить несколько времён (например, 8:00, 14:00, 20:00)."
        )
        info.setStyleSheet("color: #666666; font-size: 12px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Время (HH:MM)", "Доза", "Инструкции"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setRowCount(0)
        layout.addWidget(table)

        add_row = QHBoxLayout()
        time_input = QLineEdit()
        time_input.setPlaceholderText("08:00")
        time_input.setMaximumWidth(90)

        dose_input = QLineEdit(default_dose)

        instr_input = QLineEdit()
        instr_input.setPlaceholderText("Например: после еды")

        add_row.addWidget(QLabel("Время:"))
        add_row.addWidget(time_input)
        add_row.addWidget(QLabel("Доза:"))
        add_row.addWidget(dose_input)
        add_row.addWidget(QLabel("Инструкции:"))
        add_row.addWidget(instr_input, 1)
        layout.addLayout(add_row)

        def add_time():
            t = time_input.text().strip()
            if not t:
                mb.warning(dlg, "Ошибка", "Введите время в формате HH:MM")
                return
            if not re.match(r"^\d{1,2}:\d{2}$", t):
                mb.warning(dlg, "Ошибка", "Время в формате HH:MM (например, 08:00)")
                return
            h, m = t.split(":")
            h, m = int(h), int(m)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                mb.warning(dlg, "Ошибка", "Некорректное время")
                return
            t_full = f"{h:02d}:{m:02d}:00"

            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(t_full))
            table.setItem(row, 1, QTableWidgetItem(dose_input.text().strip() or default_dose))
            table.setItem(row, 2, QTableWidgetItem(instr_input.text().strip()))

            time_input.clear()
            instr_input.clear()
            time_input.setFocus()

        def remove_selected():
            row = table.currentRow()
            if row >= 0:
                table.removeRow(row)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Добавить время")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton { background-color: #7A9CC6; color: white; border: none;
                border-radius: 8px; padding: 8px 16px; font-size: 13px; }
            QPushButton:hover { background-color: #6A8CB6; }
        """)
        add_btn.clicked.connect(add_time)

        remove_btn = QPushButton("Удалить выбранное")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.setStyleSheet("""
            QPushButton { background-color: #E0E0E0; color: #1A1A1A; border: none;
                border-radius: 8px; padding: 8px 16px; font-size: 13px; }
            QPushButton:hover { background-color: #D0D0D0; }
        """)
        remove_btn.clicked.connect(remove_selected)

        btn_row.addWidget(add_btn)
        btn_row.addWidget(remove_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        save_row = QHBoxLayout()
        save_btn = QPushButton("Сохранить расписание")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton { background-color: #2F5C8F; color: white; border: none;
                border-radius: 8px; padding: 10px 20px; font-size: 14px; }
            QPushButton:hover { background-color: #1E4470; }
        """)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton { background-color: #E0E0E0; color: #1A1A1A; border: none;
                border-radius: 8px; padding: 10px 20px; font-size: 14px; }
            QPushButton:hover { background-color: #D0D0D0; }
        """)

        def save_schedule():
            if table.rowCount() == 0:
                mb.warning(dlg, "Пусто", "Добавьте хотя бы одно время приёма.")
                return
            saved = 0
            for r in range(table.rowCount()):
                t = table.item(r, 0).text()
                d = table.item(r, 1).text() if table.item(r, 1) else default_dose
                instr = table.item(r, 2).text() if table.item(r, 2) else ""
                if db.create_prescription_schedule(id_prescription, t, d, instr):
                    saved += 1
            mb.info(dlg, "Готово", f"Сохранено времён: {saved}")
            dlg.accept()

        save_btn.clicked.connect(save_schedule)
        cancel_btn.clicked.connect(dlg.reject)

        save_row.addStretch()
        save_row.addWidget(cancel_btn)
        save_row.addWidget(save_btn)
        layout.addLayout(save_row)

        dlg.exec()

    # ============== ДНЕВНИК ==============
    def _parse_wellbeing(self, text: str):
        result = {
            "main": text.strip() or "—",
            "intensity": None,
            "triggers": "",
            "notes": "",
        }
        if not text:
            return result
        main_part = text.split(".")[0].strip()
        result["main"] = main_part or "—"
        m = re.search(r"интенсивность:\s*(\d+)/10", text)
        if m:
            result["intensity"] = int(m.group(1))
        m = re.search(r"триггеры:\s*([^.]+)", text)
        if m:
            result["triggers"] = m.group(1).strip()
        m = re.search(r"заметки:\s*(.+)$", text)
        if m:
            result["notes"] = m.group(1).strip()
        return result

    def _wellbeing_color(self, main_text: str):
        t = main_text.lower()
        if "отлично" in t:
            return "#27AE60", "#FFFFFF"
        if "хорошо" in t:
            return "#2ECC71", "#FFFFFF"
        if "удовлетвор" in t:
            return "#F2C94C", "#1A1A1A"
        if "очень плохо" in t or "очень плох" in t:
            return "#C0392B", "#FFFFFF"
        if "плохо" in t:
            return "#E67E22", "#FFFFFF"
        return "#7A9CC6", "#FFFFFF"

    def _make_diary_card(self, entry):
        id_diary = entry[0]
        entry_date = str(entry[1])
        entry_time = str(entry[2])
        well_being_raw = str(entry[3] or "")
        symptoms = str(entry[4] or "")

        parsed = self._parse_wellbeing(well_being_raw)
        main = parsed["main"]
        intensity = parsed["intensity"]
        triggers = parsed["triggers"]
        notes = parsed["notes"]

        card = QFrame()
        card.setStyleSheet("""
            QFrame { background-color: #FFFFFF; border: 1px solid #E5EAF0; border-radius: 12px; }
            QLabel { background: transparent; border: none; color: #1A1A1A; }
            QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 6px; padding: 6px 10px; font-family: 'Times New Roman'; font-size: 13px; }
            QLineEdit:focus { border: 2px solid #2F5C8F; }
            QLineEdit::placeholder { color: #999999; }
            QListWidget { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 6px; font-family: 'Times New Roman'; font-size: 12px; }
            QListWidget::item { padding: 6px; color: #1A1A1A; }
            QListWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }
            QListWidget::item:hover { background-color: #E8EFF8; }
        """)
        card.setMinimumHeight(120)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        top = QHBoxLayout()
        top.setSpacing(10)
        date_label = QLabel(f"{entry_date}   {entry_time}")
        date_label.setStyleSheet(
            "font-family: 'Times New Roman'; font-size: 13px; color: #2F5C8F; font-weight: bold; background: transparent;"
        )

        bg, fg = self._wellbeing_color(main)
        badge = QLabel(main.upper())
        badge.setStyleSheet(f"""
            background-color: {bg}; color: {fg}; border-radius: 10px;
            padding: 5px 14px; font-family: 'Times New Roman';
            font-size: 12px; font-weight: bold;
        """)
        top.addWidget(date_label)
        top.addStretch()
        top.addWidget(badge)
        layout.addLayout(top)

        if intensity is not None:
            int_row = QHBoxLayout()
            int_row.setSpacing(10)
            int_label = QLabel("Интенсивность:")
            int_label.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #666666; background: transparent;"
            )
            bar_container = QFrame()
            bar_container.setFixedHeight(10)
            bar_container.setStyleSheet(
                "background-color: #EEF3F8; border-radius: 5px; border: none;"
            )
            bar_layout = QHBoxLayout(bar_container)
            bar_layout.setContentsMargins(0, 0, 0, 0)
            bar_layout.setSpacing(0)
            fill = QFrame()
            fill.setStyleSheet("background-color: #2F5C8F; border-radius: 5px;")
            fill.setFixedWidth(int(30 + intensity * 20))
            bar_layout.addWidget(fill)
            bar_layout.addStretch()
            int_val = QLabel(f"{intensity}/10")
            int_val.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #2F5C8F; font-weight: bold; background: transparent;"
            )
            int_row.addWidget(int_label)
            int_row.addWidget(bar_container, 1)
            int_row.addWidget(int_val)
            layout.addLayout(int_row)

        if symptoms and symptoms.lower() != "нет":
            sym_row = QHBoxLayout()
            sym_row.setSpacing(8)
            sym_label = QLabel("Симптомы:")
            sym_label.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #666666; background: transparent;"
            )
            sym_value = QLabel(symptoms)
            sym_value.setWordWrap(True)
            sym_value.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #1A1A1A; background: transparent;"
            )
            sym_row.addWidget(sym_label)
            sym_row.addWidget(sym_value, 1)
            layout.addLayout(sym_row)

        if triggers:
            tr_row = QHBoxLayout()
            tr_row.setSpacing(8)
            tr_label = QLabel("Триггеры:")
            tr_label.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #666666; background: transparent;"
            )
            tr_value = QLabel(triggers)
            tr_value.setWordWrap(True)
            tr_value.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #1A1A1A; background: transparent;"
            )
            tr_row.addWidget(tr_label)
            tr_row.addWidget(tr_value, 1)
            layout.addLayout(tr_row)

        if notes:
            n_row = QHBoxLayout()
            n_row.setSpacing(8)
            n_label = QLabel("Заметки:")
            n_label.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #666666; background: transparent;"
            )
            n_value = QLabel(notes)
            n_value.setWordWrap(True)
            n_value.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #1A1A1A; background: transparent; font-style: italic;"
            )
            n_row.addWidget(n_label)
            n_row.addWidget(n_value, 1)
            layout.addLayout(n_row)

        try:
            indicators = db.get_indicators_for_diary(id_diary)
        except Exception:
            indicators = []

        if indicators:
            ind_parts = []
            for ind in indicators:
                typ = str(ind[0])
                val = str(ind[1])
                unit = str(ind[2] or "")
                ind_parts.append(f"{typ}: {val} {unit}".strip())
            ind_label = QLabel("Показатели: " + "  ·  ".join(ind_parts))
            ind_label.setWordWrap(True)
            ind_label.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 12px; color: #2F5C8F; background: transparent;"
            )
            layout.addWidget(ind_label)

        # -------- ДИАГНОЗ С МКБ-10 --------
        diagnosis_info = db.get_diary_diagnosis(id_diary) or {}
        existing = diagnosis_info.get("diagnosis") or ""
        existing_disease_id = diagnosis_info.get("id_disease")

        diag_frame = QFrame()
        diag_frame.setStyleSheet(
            "background-color: #F0F4FA; border: 1px solid #D6E3F3; border-radius: 8px;"
        )
        diag_layout = QVBoxLayout(diag_frame)
        diag_layout.setContentsMargins(12, 10, 12, 10)
        diag_layout.setSpacing(8)

        diag_title = QLabel("ДИАГНОЗ ВРАЧА")
        diag_title.setStyleSheet(
            "font-family: 'Times New Roman'; font-size: 11px; "
            "color: #2F5C8F; font-weight: bold; background: transparent;"
        )
        diag_layout.addWidget(diag_title)

        lbl1 = QLabel("Болезнь (МКБ-10):")
        lbl1.setStyleSheet(
            "color: #1A1A1A; font-family: 'Times New Roman'; font-size: 12px; background: transparent;"
        )
        diag_layout.addWidget(lbl1)

        disease_search = QLineEdit()
        disease_search.setPlaceholderText("Поиск по коду или названию: I10, диабет, астма...")
        disease_search.setMinimumHeight(34)
        diag_layout.addWidget(disease_search)

        disease_list = QListWidget()
        disease_list.setMaximumHeight(120)
        diag_layout.addWidget(disease_list)

        all_diseases = db.get_all_diseases()
        disease_cache = [(d[0], d[1], d[2]) for d in all_diseases]
        for d in all_diseases:
            disease_list.addItem(f"{d[1]} — {d[2]}")

        selected_disease_id = [existing_disease_id]

        def on_disease_search(text):
            text = text.strip()
            if not text:
                disease_list.clear()
                for d in all_diseases:
                    disease_list.addItem(f"{d[1]} — {d[2]}")
                nonlocal disease_cache
                disease_cache = [(d[0], d[1], d[2]) for d in all_diseases]
                return
            results = db.search_diseases(text)
            disease_list.clear()
            for d in results:
                disease_list.addItem(f"{d[1]} — {d[2]}")
            disease_cache = [(d[0], d[1], d[2]) for d in results]

        def on_disease_selected(item):
            idx = disease_list.row(item)
            if 0 <= idx < len(disease_cache):
                d_id, code, name = disease_cache[idx]
                selected_disease_id[0] = d_id
                disease_search.setText(f"{code} — {name}")

        disease_search.textChanged.connect(on_disease_search)
        disease_list.itemClicked.connect(on_disease_selected)

        lbl2 = QLabel("Уточнения и рекомендации:")
        lbl2.setStyleSheet(
            "color: #1A1A1A; font-family: 'Times New Roman'; font-size: 12px; background: transparent;"
        )
        diag_layout.addWidget(lbl2)

        diag_text = QLineEdit()
        diag_text.setPlaceholderText("Дополнительные наблюдения...")
        diag_text.setText(existing)
        diag_text.setMinimumHeight(34)
        diag_layout.addWidget(diag_text)

        save_diag_btn = QPushButton("Сохранить диагноз")
        save_diag_btn.setMinimumHeight(34)
        save_diag_btn.setMaximumWidth(220)
        save_diag_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_diag_btn.setStyleSheet("""
            QPushButton { background-color: #2F5C8F; color: white;
                border: none; border-radius: 8px; font-size: 13px; }
            QPushButton:hover { background-color: #1E4470; }
        """)

        def save_diagnosis():
            text = diag_text.text().strip()
            d_id = selected_disease_id[0]
            if not d_id and not text:
                mb.warning(self, "Ошибка", "Выберите болезнь или введите комментарий.")
                return
            ok = db.set_diary_diagnosis_full(id_diary, text, d_id, self.id_doctor)
            if ok:
                mb.info(self, "Готово", "Диагноз сохранён")

        save_diag_btn.clicked.connect(save_diagnosis)
        diag_layout.addWidget(save_diag_btn)
        layout.addWidget(diag_frame)

        return card

    def view_diary(self):
        if self.ui.diaryPatientCombo.count() == 0:
            mb.warning(self, "Ошибка", "Нет пациентов")
            return

        id_patient = self.ui.diaryPatientCombo.currentData()
        patient_name = self.ui.diaryPatientCombo.currentText()
        entries = db.get_diary_entries_for_patient(id_patient)

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Дневник пациента: {patient_name}")
        dlg.resize(900, 700)
        dlg.setStyleSheet("""
            QDialog { background-color: #EEF3F8; }
            QLabel { color: #1A1A1A; font-family: "Times New Roman"; background: transparent; }
            QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 6px; padding: 6px 10px; font-family: 'Times New Roman'; font-size: 13px; }
            QLineEdit::placeholder { color: #999999; }
            QListWidget { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 6px; font-family: 'Times New Roman'; font-size: 12px; }
            QListWidget::item { padding: 6px; color: #1A1A1A; }
            QListWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }
            QListWidget::item:hover { background-color: #E8EFF8; }
        """)

        root = QVBoxLayout(dlg)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        header = QLabel(f"Пациент: {patient_name}  ·  Записей: {len(entries)}")
        header.setStyleSheet(
            "font-family: 'Times New Roman'; font-size: 15px; "
            "color: #2F5C8F; font-weight: bold; background: transparent;"
        )
        root.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { background: #FFFFFF; border: 1px solid #CCCCCC; border-radius: 12px; }
            QScrollArea > QWidget > QWidget { background: #FFFFFF; }
        """)

        container = QWidget()
        container.setStyleSheet("background: #FFFFFF;")
        list_layout = QVBoxLayout(container)
        list_layout.setContentsMargins(16, 16, 16, 16)
        list_layout.setSpacing(12)

        if not entries:
            empty = QLabel("У пациента пока нет записей в дневнике")
            empty.setStyleSheet(
                "font-family: 'Times New Roman'; font-size: 14px; "
                "color: #999999; padding: 40px; background: transparent;"
            )
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            list_layout.addWidget(empty)
        else:
            for entry in entries:
                card = self._make_diary_card(entry)
                list_layout.addWidget(card)
            list_layout.addStretch()

        scroll.setWidget(container)
        root.addWidget(scroll, 1)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton("Закрыть")
        close_btn.setMinimumSize(140, 40)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background-color: #2F5C8F; color: white; border: none;
                border-radius: 10px; font-family: "Times New Roman"; font-size: 14px; }
            QPushButton:hover { background-color: #1E4470; }
        """)
        close_btn.clicked.connect(dlg.accept)
        btn_row.addWidget(close_btn)
        root.addLayout(btn_row)

        dlg.exec()
