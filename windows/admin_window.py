from PySide6.QtCore import Qt, QRectF, QTimer
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
    QPixmap,
    QPageSize,
    QPageLayout,
    QPdfWriter,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFileDialog,
    QTableWidgetItem,
    QGraphicsDropShadowEffect,
    QApplication,
    QHeaderView,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)

import db
import theme
from ui_py.ui_admin import Ui_AdminAnalyticsWindow
from windows import msgbox as mb


class ChartWidget(QWidget):
    def __init__(self, title: str = ""):
        super().__init__()
        self.title = title
        self.setMinimumHeight(220)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        painter.setPen(QColor("#2b2b3c"))
        font = QFont("Arial")
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(0, 4, self.width(), 26), Qt.AlignmentFlag.AlignCenter, self.title)
        self.draw_content(painter, QRectF(0, 34, self.width(), self.height() - 34))

    def draw_content(self, painter, rect):
        pass


class BarChartWidget(ChartWidget):
    def __init__(self):
        super().__init__("Пациенты по врачам")
        self.labels, self.data = db.get_patients_by_doctor()

    def draw_content(self, painter, rect):
        if not self.data:
            painter.setPen(QColor("#7a7a8c"))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Нет данных")
            return
        margin = 30
        chart_rect = rect.adjusted(margin, 10, -10, -22)
        max_val = max(self.data) or 1
        gap = chart_rect.width() / len(self.data)
        bar_w = gap * 0.6
        painter.setFont(QFont("Arial", 8))
        for i, val in enumerate(self.data):
            h = chart_rect.height() * val / max_val
            x = chart_rect.left() + i * gap + (gap - bar_w) / 2
            y = chart_rect.bottom() - h
            painter.setBrush(QBrush(QColor("#2F5C8F")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_w, h), 5, 5)
            painter.setPen(QColor("#2b2b3c"))
            painter.drawText(QRectF(x, y - 16, bar_w, 16), Qt.AlignmentFlag.AlignCenter, str(val))
            painter.drawText(
                QRectF(x, chart_rect.bottom() + 2, bar_w, 16),
                Qt.AlignmentFlag.AlignCenter,
                str(self.labels[i]),
            )


class PieChartWidget(ChartWidget):
    COLORS = [
        QColor("#2F5C8F"),
        QColor("#7A9CC6"),
        QColor("#4FC3B5"),
        QColor("#F2994A"),
        QColor("#C0504D"),
        QColor("#6C63FF"),
    ]

    def __init__(self):
        super().__init__("Приверженность лечению")
        self.data = db.get_adherence()

    def draw_content(self, painter, rect):
        if not self.data:
            painter.setPen(QColor("#7a7a8c"))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Нет данных")
            return
        total = sum(v for _, v in self.data) or 1
        size = min(rect.width() * 0.55, rect.height() - 20)
        cx = rect.left() + 15
        cy = rect.top() + (rect.height() - size) / 2
        pie_rect = QRectF(cx, cy, size, size)
        start_angle = 90 * 16
        for i, (_, val) in enumerate(self.data):
            span = int(360 * 16 * val / total)
            color = self.COLORS[i % len(self.COLORS)]
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor("#ffffff"), 2))
            painter.drawPie(pie_rect, start_angle, -span)
            start_angle -= span
        painter.setFont(QFont("Arial", 8))
        lx = cx + size + 12
        ly = cy + 10
        for i, (name, val) in enumerate(self.data):
            color = self.COLORS[i % len(self.COLORS)]
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(lx, ly, 12, 12), 3, 3)
            painter.setPen(QColor("#2b2b3c"))
            painter.drawText(
                QRectF(lx + 18, ly, 140, 14),
                Qt.AlignmentFlag.AlignVCenter,
                f"{name} — {val}",
            )
            ly += 20


class LineChartWidget(ChartWidget):
    def __init__(self):
        super().__init__("Активность в дневнике (14 дней)")
        self.labels, self.data = db.get_diary_dynamics()

    def draw_content(self, painter, rect):
        if not self.data:
            painter.setPen(QColor("#7a7a8c"))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Нет данных")
            return
        margin = 30
        chart_rect = rect.adjusted(margin, 15, -10, -22)
        max_val = max(self.data) or 1
        step_x = chart_rect.width() / max(1, len(self.data) - 1)
        points = []
        for i, val in enumerate(self.data):
            x = chart_rect.left() + i * step_x
            y = chart_rect.bottom() - chart_rect.height() * val / max_val
            points.append((x, y))
        painter.setPen(QPen(QColor("#2F5C8F"), 2))
        for i in range(len(points) - 1):
            painter.drawLine(
                int(points[i][0]),
                int(points[i][1]),
                int(points[i + 1][0]),
                int(points[i + 1][1]),
            )
        painter.setFont(QFont("Arial", 8))
        for i, (x, y) in enumerate(points):
            painter.setBrush(QBrush(QColor("#2F5C8F")))
            painter.setPen(QPen(QColor("#ffffff"), 2))
            painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))
            painter.setPen(QColor("#2b2b3c"))
            painter.drawText(
                QRectF(x - 20, y - 20, 40, 14),
                Qt.AlignmentFlag.AlignCenter,
                str(self.data[i]),
            )
            painter.drawText(
                QRectF(x - 40, chart_rect.bottom() + 2, 80, 14),
                Qt.AlignmentFlag.AlignCenter,
                str(self.labels[i]),
            )


class AdminAnalyticsWindow(QMainWindow):
    def __init__(self, user_name: str = "", login_window=None):
        super().__init__()
        self.login_window = login_window
        self.ui = Ui_AdminAnalyticsWindow()
        self.ui.setupUi(self)

        for frame in (
            self.ui.barChartFrame,
            self.ui.pieChartFrame,
            self.ui.lineChartFrame,
        ):
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(24)
            shadow.setColor(QColor(47, 92, 143, 40))
            shadow.setOffset(0, 6)
            frame.setGraphicsEffect(shadow)

        self.barChartView = BarChartWidget()
        self.pieChartView = PieChartWidget()
        self.lineChartView = LineChartWidget()

        self.ui.barChartLayout.addWidget(self.barChartView)
        self.ui.pieChartLayout.addWidget(self.pieChartView)
        self.ui.lineChartLayout.addWidget(self.lineChartView)

        self.ui.exportPdfButton.clicked.connect(self.on_export_pdf)
        self.ui.logoutBtn.clicked.connect(self.on_logout)

        self.ui.usersTable.setColumnCount(4)
        self.ui.usersTable.setHorizontalHeaderLabels(["ID", "Логин", "Роль", "ФИО"])
        self.ui.usersTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.usersTable.setEditTriggers(self.ui.usersTable.EditTrigger.NoEditTriggers)
        self.ui.usersTable.setSelectionBehavior(self.ui.usersTable.SelectionBehavior.SelectRows)

        self.ui.generateBtn.clicked.connect(self.on_generate)
        self.ui.addBtn.clicked.connect(self.on_add)
        self.ui.deleteBtn.clicked.connect(self.on_delete)
        self.ui.resetPasswordBtn.clicked.connect(self.on_reset_password)

        self.ui.assignTable.setColumnCount(3)
        self.ui.assignTable.setHorizontalHeaderLabels(["ID", "Пациент", "Текущий врач"])
        self.ui.assignTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.assignTable.setEditTriggers(self.ui.assignTable.EditTrigger.NoEditTriggers)
        self.ui.assignTable.setSelectionBehavior(self.ui.assignTable.SelectionBehavior.SelectRows)

        self.ui.assignBtn.clicked.connect(self.on_assign_patient)

        self.load_users()
        self.load_assignments()

        self.ui.exportPdfButton.setToolTip("Сформировать PDF-отчёт")
        self.ui.generateBtn.setToolTip("Сгенерировать логин и пароль")
        self.ui.resetPasswordBtn.setToolTip("Сменить пароль пользователю")
        self.ui.deleteBtn.setToolTip("Удалить пользователя")
        self.ui.assignBtn.setToolTip("Прикрепить пациента к врачу")

        self._update_status_bar()
        theme.apply_to_window(self, theme.is_dark())

    def _update_status_bar(self):
        ok, err = db.check_connection()
        if ok:
            self.ui.statusLabel.setText("● Подключено к базе данных")
            self.ui.statusLabel.setStyleSheet("color: #27AE60; padding: 4px 8px; font-size: 10px;")
        else:
            self.ui.statusLabel.setText(f"● Нет связи с БД: {err[:60]}")
            self.ui.statusLabel.setStyleSheet("color: #C0392B; padding: 4px 8px; font-size: 10px;")

    def on_logout(self):
        if self.login_window:
            self.login_window.return_from_child()
        self.close()

    def load_users(self):
        users = db.get_all_users()
        self.ui.usersTable.setRowCount(len(users))
        for row, u in enumerate(users):
            self.ui.usersTable.setItem(row, 0, QTableWidgetItem(str(u[0])))
            self.ui.usersTable.setItem(row, 1, QTableWidgetItem(str(u[1])))
            self.ui.usersTable.setItem(row, 2, QTableWidgetItem(str(u[2])))
            self.ui.usersTable.setItem(row, 3, QTableWidgetItem(str(u[3])))

    def on_generate(self):
        full_name = self.ui.fullNameLine.text().strip()
        if not full_name:
            mb.warning(self, "Не заполнено ФИО", "Сначала введите ФИО пользователя.")
            self.ui.fullNameLine.setFocus()
            return
        login = db.generate_login(full_name)
        password = db.generate_password()
        self.ui.loginLine.setText(login)
        self.ui.passwordLine.setText(password)
        self._show_credentials_dialog(login, password, title="Логин и пароль")

    def on_add(self):
        login = self.ui.loginLine.text().strip()
        password = self.ui.passwordLine.text().strip()
        full_name = self.ui.fullNameLine.text().strip()
        role = self.ui.roleCombo.currentText()

        # === ВАЛИДАЦИЯ ===
        from validators import validate_login, validate_password, validate_name

        ok, err = validate_login(login)
        if not ok:
            mb.warning(self, "Ошибка в логине", err)
            self.ui.loginLine.setFocus()
            return

        ok, err = validate_password(password)
        if not ok:
            mb.warning(self, "Ошибка в пароле", err)
            self.ui.passwordLine.setFocus()
            return

        ok, err = validate_name(full_name)
        if not ok:
            mb.warning(self, "Ошибка в ФИО", err)
            self.ui.fullNameLine.setFocus()
            return
        # === КОНЕЦ ВАЛИДАЦИИ ===

        # === СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ ===
        id_user = db.create_user(login, password, role, full_name)
        if id_user is None:
            mb.warning(
                self,
                "Не удалось создать пользователя",
                f"Логин «{login}» уже используется.\n\n"
                f"Измените логин или удалите старого пользователя.",
            )
            self.ui.loginLine.setFocus()
            self.ui.loginLine.selectAll()
            return

        if role == "doctor":
            db.create_doctor(id_user, "Терапевт")
        elif role == "patient":
            db.create_patient(id_user, full_name, "2000-01-01", "", "", None)

        mb.info(self, "Пользователь создан", f"«{login}» добавлен.\n\nПароль: {password}")

        self.ui.loginLine.clear()
        self.ui.passwordLine.clear()
        self.ui.fullNameLine.clear()
        self.load_users()
        self.load_assignments()

    def on_delete(self):
        row = self.ui.usersTable.currentRow()
        if row < 0:
            mb.warning(self, "Не выбран пользователь", "Кликните по строке таблицы.")
            return
        id_user = int(self.ui.usersTable.item(row, 0).text())
        login = self.ui.usersTable.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Удалить пользователя «{login}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        db.delete_user(id_user)
        mb.info(self, "Готово", f"Пользователь «{login}» удалён")
        self.load_users()
        self.load_assignments()

    def on_reset_password(self):
        row = self.ui.usersTable.currentRow()
        if row < 0:
            mb.warning(self, "Не выбран пользователь", "Кликните по строке таблицы.")
            return
        id_user = int(self.ui.usersTable.item(row, 0).text())
        login = self.ui.usersTable.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение сброса",
            f"Сбросить пароль «{login}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        new_password = db.generate_password()
        ok = db.reset_user_password(id_user, new_password)
        if ok:
            self._show_credentials_dialog(login, new_password, title="Пароль сброшен")
        else:
            mb.critical(self, "Ошибка", "Не удалось сбросить пароль")

    def load_assignments(self):
        patients = db.get_all_patients_with_doctors()
        self.ui.assignPatientCombo.clear()
        self.ui.assignTable.setRowCount(len(patients))
        for row, p in enumerate(patients):
            self.ui.assignTable.setItem(row, 0, QTableWidgetItem(str(p[0])))
            self.ui.assignTable.setItem(row, 1, QTableWidgetItem(str(p[1])))
            self.ui.assignTable.setItem(row, 2, QTableWidgetItem(str(p[2])))
            self.ui.assignPatientCombo.addItem(p[1], p[0])

        doctors = db.get_all_doctors()
        self.ui.assignDoctorCombo.clear()
        for d in doctors:
            self.ui.assignDoctorCombo.addItem(f"{d[1]} ({d[2]})", d[0])

    def on_assign_patient(self):
        if self.ui.assignPatientCombo.count() == 0:
            mb.warning(self, "Нет пациентов", "В системе нет пациентов.")
            return
        if self.ui.assignDoctorCombo.count() == 0:
            mb.warning(self, "Нет врачей", "В системе нет врачей.")
            return

        id_patient = self.ui.assignPatientCombo.currentData()
        id_doctor = self.ui.assignDoctorCombo.currentData()
        patient_name = self.ui.assignPatientCombo.currentText()
        doctor_name = self.ui.assignDoctorCombo.currentText()

        ok = db.reassign_patient_doctor(id_patient, id_doctor)
        if ok:
            mb.info(self, "Готово", f"«{patient_name}» прикреплён к «{doctor_name}»")
            self.load_assignments()
        else:
            mb.critical(self, "Ошибка", "Не удалось прикрепить")

    def _show_credentials_dialog(self, login: str, password: str, title: str = "Логин и пароль"):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.setMinimumWidth(460)
        dlg.setStyleSheet("""
            QDialog { background-color: #FFFFFF; }
            QLabel { color: #1A1A1A; font-family: "Times New Roman"; font-size: 13px; }
            QLineEdit { background-color: #F5F5F5; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 8px; padding: 10px 14px; font-family: "Times New Roman"; font-size: 14px; }
        """)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        info = QLabel("Скопируйте данные и передайте пользователю.")
        info.setStyleSheet("color: #666666; font-size: 12px;")
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

        copy_all_btn = QPushButton("Скопировать всё")
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

        def copy_all():
            QApplication.clipboard().setText(f"Логин: {login}\nПароль: {password}")
            copy_all_btn.setText("✓ Скопировано")
            t = QTimer(dlg)
            t.setSingleShot(True)
            t.timeout.connect(lambda: copy_all_btn.setText("Скопировать всё"))
            t.start(1500)

        copy_all_btn.clicked.connect(copy_all)
        close_btn.clicked.connect(dlg.accept)

        layout.addWidget(copy_all_btn)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(close_btn)
        layout.addLayout(row)

        dlg.exec()

    def on_export_pdf(self):
        selected = []
        if self.ui.barChartCheckBox.isChecked():
            selected.append(("Столбчатая — Пациенты по врачам", BarChartWidget))
        if self.ui.pieChartCheckBox.isChecked():
            selected.append(("Круговая — Приверженность лечению", PieChartWidget))
        if self.ui.lineChartCheckBox.isChecked():
            selected.append(("Линейная — Активность в дневнике", LineChartWidget))

        if not selected:
            mb.warning(self, "Ничего не выбрано", "Отметьте хотя бы одну диаграмму.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить отчёт как PDF",
            "analytics_report.pdf",
            "PDF Files (*.pdf)",
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        try:
            writer = QPdfWriter(file_path)
            writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            writer.setPageOrientation(QPageLayout.Orientation.Portrait)
            writer.setResolution(300)
            PAGE_W = 2480
            PAGE_H = 3508
            margin = 150

            painter = QPainter(writer)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            for idx, (name, cls) in enumerate(selected):
                if idx > 0:
                    writer.newPage()

                painter.setPen(QColor("#1a1a2e"))
                tf = QFont("Arial")
                tf.setPointSize(28)
                tf.setBold(True)
                painter.setFont(tf)
                painter.drawText(
                    QRectF(margin, margin, PAGE_W - 2 * margin, 80),
                    Qt.AlignmentFlag.AlignCenter,
                    "Отчёт по аналитике",
                )

                painter.setPen(QColor("#2F5C8F"))
                lf = QFont("Arial")
                lf.setPointSize(20)
                lf.setBold(True)
                painter.setFont(lf)
                painter.drawText(
                    QRectF(margin, margin + 90, PAGE_W - 2 * margin, 60),
                    Qt.AlignmentFlag.AlignCenter,
                    name,
                )

                chart_x = margin
                chart_y = margin + 180
                chart_w = PAGE_W - 2 * margin
                chart_h = PAGE_H - chart_y - margin

                temp = cls()
                temp.resize(chart_w, chart_h)
                temp.setStyleSheet("background-color: #FFFFFF;")
                temp.show()
                QApplication.processEvents()

                pixmap = QPixmap(chart_w, chart_h)
                pixmap.fill(QColor("#FFFFFF"))
                temp.render(pixmap)
                temp.hide()
                temp.deleteLater()

                painter.drawPixmap(chart_x, chart_y, pixmap)

            painter.end()
            mb.info(self, "Готово", f"Отчёт сохранён:\n{file_path}")
        except Exception as e:
            mb.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
