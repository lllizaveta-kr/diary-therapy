"""Панель администратора в виде CRM клиники."""
import re
from PySide6.QtCore import QDate, QRectF, Qt, QTimer, QTime
from PySide6.QtGui import (
    QBrush, QColor, QFont, QKeySequence, QPageLayout, QPageSize,
    QPainter, QPdfWriter, QPen, QPixmap, QShortcut
)
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QDialog,
    QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTimeEdit
)

import db
import pdf_exporter
from validators import (
    validate_birth_date, validate_login, validate_name, validate_password, validate_phone, validate_policy,
)
from windows import common
from windows import msgbox as mb
from windows import widgets as w

SPECIALTIES = ["Терапевт", "Кардиолог", "Эндокринолог", "Невролог", "Гастроэнтеролог", "Пульмонолог", "Педиатр",
               "Хирург"]

ACTION_NAMES = {
    "create_user": ("Создана учётная запись", "plus"),
    "delete_user": ("Удалена учётная запись", "trash"),
    "reset_password": ("Сброшен пароль", "key"),
    "reassign_doctor": ("Пациент прикреплён к врачу", "link"),
    "update_doctor": ("Обновлён профиль врача", "edit"),
    "update_patient": ("Обновлён профиль пациента", "edit"),
    "doctor_photo": ("Загружено фото врача", "camera"),
    "create_prescription": ("Создано назначение", "pill"),
    "set_diagnosis": ("Поставлен диагноз", "stethoscope"),
    "export_pdf": ("Выгружен PDF-отчёт", "file"),
}

TAB_COLORS = ["#163257", "#1E4470", "#2F5C8F", "#5A7CA6", "#7A9CC6"]


# ============== НОВЫЙ ВИДЖЕТ РАСПИСАНИЯ ==============
class ScheduleInput(QWidget):
    def __init__(self):
        super().__init__()
        pl = w.pal()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        # Дни недели
        days_lay = QHBoxLayout()
        days_lay.setSpacing(4)
        self.day_checks = {}
        for d in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            cb = QCheckBox(d)
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            self.day_checks[d] = cb
            days_lay.addWidget(cb)
        days_lay.addStretch()
        lay.addLayout(days_lay)

        # Время
        time_lay = QHBoxLayout()
        time_lay.setSpacing(8)
        self.time_start = QTimeEdit(QTime(8, 0))
        self.time_start.setDisplayFormat("HH:mm")
        self.time_end = QTimeEdit(QTime(14, 0))
        self.time_end.setDisplayFormat("HH:mm")

        time_lay.addWidget(w.label("с", 9, color=pl["muted"]))
        time_lay.addWidget(self.time_start)
        time_lay.addWidget(w.label("до", 9, color=pl["muted"]))
        time_lay.addWidget(self.time_end)
        time_lay.addStretch()
        lay.addLayout(time_lay)

    def get_text(self):
        days = [d for d, cb in self.day_checks.items() if cb.isChecked()]
        if not days:
            return ""
        s = self.time_start.time().toString("HH:mm")
        e = self.time_end.time().toString("HH:mm")
        return f"{', '.join(days)} {s}-{e}"

    def set_text(self, text):
        for cb in self.day_checks.values():
            cb.setChecked(False)
        if not text:
            return
        match = re.search(r'([А-Яа-я,\s]+)\s+(\d{2}:\d{2})-(\d{2}:\d{2})', text)
        if match:
            days_str, start, end = match.groups()
            for d in days_str.split(','):
                d = d.strip()
                if d in self.day_checks:
                    self.day_checks[d].setChecked(True)
            self.time_start.setTime(QTime.fromString(start, "HH:mm"))
            self.time_end.setTime(QTime.fromString(end, "HH:mm"))


# ============== ГРАФИКИ ==============
class ChartWidget(QWidget):
    def __init__(self, title: str = ""):
        super().__init__()
        self.title = title
        self.print_mode = False
        self.setMinimumHeight(220)

    def _colors(self):
        return w.LIGHT if self.print_mode else w.pal()

    def reload(self): self.update()

    def paintEvent(self, event):
        c = self._colors()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(c["card"]))
        painter.setPen(QColor(c["text"]))
        font = QFont(w.FONT)
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(0, 4, self.width(), 26), Qt.AlignmentFlag.AlignCenter, self.title)
        self.draw_content(painter, QRectF(0, 34, self.width(), self.height() - 34))

    def _no_data(self, painter, rect):
        painter.setPen(QColor(self._colors()["muted"]))
        painter.setFont(QFont(w.FONT, 10))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Нет данных")

    def draw_content(self, painter, rect): pass


class BarChartWidget(ChartWidget):
    def __init__(self):
        super().__init__("Пациенты по врачам")
        self.reload()

    def reload(self):
        self.labels, self.data = db.get_patients_by_doctor()
        self.update()

    def draw_content(self, painter, rect):
        if not self.data: self._no_data(painter, rect); return
        c = self._colors()
        margin = 30
        chart_rect = rect.adjusted(margin, 10, -10, -22)
        max_val = max(self.data) or 1
        gap = chart_rect.width() / len(self.data)
        bar_w = gap * 0.6
        painter.setFont(QFont(w.FONT, 8))
        for i, val in enumerate(self.data):
            h = chart_rect.height() * val / max_val
            x = chart_rect.left() + i * gap + (gap - bar_w) / 2
            y = chart_rect.bottom() - h
            painter.setBrush(QBrush(QColor("#2F5C8F")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_w, h), 5, 5)
            painter.setPen(QColor(c["text"]))
            painter.drawText(QRectF(x, y - 16, bar_w, 16), Qt.AlignmentFlag.AlignCenter, str(val))
            painter.drawText(QRectF(x - gap * 0.2, chart_rect.bottom() + 2, bar_w + gap * 0.4, 16),
                             Qt.AlignmentFlag.AlignCenter, w.short_name(str(self.labels[i])))


class PieChartWidget(ChartWidget):
    COLORS = [QColor("#2F5C8F"), QColor("#7A9CC6"), QColor("#4FC3B5"), QColor("#F2994A"), QColor("#C0504D"),
              QColor("#6C63FF")]

    def __init__(self):
        super().__init__("Приверженность лечению")
        self.reload()

    def reload(self):
        self.data = db.get_adherence()
        self.update()

    def draw_content(self, painter, rect):
        if not self.data: self._no_data(painter, rect); return
        c = self._colors()
        total = sum(v for _, v in self.data) or 1
        size = min(rect.width() * 0.55, rect.height() - 20)
        cx = rect.left() + 15
        cy = rect.top() + (rect.height() - size) / 2
        pie_rect = QRectF(cx, cy, size, size)
        start_angle = 90 * 16
        for i, (_, val) in enumerate(self.data):
            span = int(360 * 16 * val / total)
            painter.setBrush(QBrush(self.COLORS[i % len(self.COLORS)]))
            painter.setPen(QPen(QColor(c["card"]), 2))
            painter.drawPie(pie_rect, start_angle, -span)
            start_angle -= span
        painter.setFont(QFont(w.FONT, 8))
        lx = cx + size + 12
        ly = cy + 10
        for i, (name, val) in enumerate(self.data):
            painter.setBrush(QBrush(self.COLORS[i % len(self.COLORS)]))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(lx, ly, 12, 12), 3, 3)
            painter.setPen(QColor(c["text"]))
            painter.drawText(QRectF(lx + 18, ly, 160, 14), Qt.AlignmentFlag.AlignVCenter, f"{name} — {val}")
            ly += 20


class LineChartWidget(ChartWidget):
    def __init__(self):
        super().__init__("Активность в дневнике (14 дней)")
        self.reload()

    def reload(self):
        self.labels, self.data = db.get_diary_dynamics()
        self.update()

    def draw_content(self, painter, rect):
        if not self.data: self._no_data(painter, rect); return
        c = self._colors()
        margin = 30
        chart_rect = rect.adjusted(margin, 15, -28, -22)
        max_val = max(self.data) or 1
        step_x = chart_rect.width() / max(1, len(self.data) - 1)
        points = []
        for i, val in enumerate(self.data):
            x = chart_rect.left() + i * step_x
            y = chart_rect.bottom() - chart_rect.height() * val / max_val
            points.append((x, y))
        painter.setPen(QPen(QColor("#2F5C8F"), 2))
        for i in range(len(points) - 1):
            painter.drawLine(int(points[i][0]), int(points[i][1]), int(points[i + 1][0]), int(points[i + 1][1]))
        painter.setFont(QFont(w.FONT, 8))
        for i, (x, y) in enumerate(points):
            painter.setBrush(QBrush(QColor("#2F5C8F")))
            painter.setPen(QPen(QColor(c["card"]), 2))
            painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))
            painter.setPen(QColor(c["text"]))
            painter.drawText(QRectF(x - 20, y - 20, 40, 14), Qt.AlignmentFlag.AlignCenter, str(self.data[i]))
            painter.drawText(QRectF(x - 40, chart_rect.bottom() + 2, 80, 14), Qt.AlignmentFlag.AlignCenter,
                             str(self.labels[i]))


# ============== КАРТОЧКИ ==============
class PatientCard(w.AnimatedCard):
    def __init__(self, p):
        mood, mood_color = w.mood_of(p["last_wellbeing"])
        super().__init__(width=310, accent=mood_color)
        pl = w.pal()
        self.data = p
        top = QHBoxLayout()
        top.setSpacing(12)
        top.addWidget(w.Avatar(p["full_name"], 52))
        name_col = QVBoxLayout()
        name_col.setSpacing(2)
        name_col.addWidget(w.label(p["full_name"], 11, bold=True, wrap=True))
        age = common.age(p["birth_date"])
        meta = " · ".join(x for x in (common.years(age) if age is not None else "", p["gender"] or "") if x)
        name_col.addWidget(w.label(meta or "данные не заполнены", 9, color=pl["muted"]))
        top.addLayout(name_col, 1)
        self.body_layout.addLayout(top)

        mood_row = QHBoxLayout()
        mood_row.setSpacing(8)
        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background: {mood_color}; border-radius: 5px;")
        mood_row.addWidget(dot)
        when = p["last_entry"].strftime("%d.%m") if p["last_entry"] else ""
        mood_text = f"{mood} · {when}" if when else "Дневник пока пуст"
        mood_row.addWidget(w.label(mood_text, 9, color=pl["text"]))
        mood_row.addStretch()
        self.body_layout.addLayout(mood_row)

        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet(f"background: {pl['line']};")
        self.body_layout.addWidget(line)

        doc_row = QHBoxLayout()
        doc_row.setSpacing(8)
        if p["doctor_name"]:
            doc_row.addWidget(w.Avatar(p["doctor_name"], 26, w.doctor_photo_path(p["doctor_photo"])))
            doc_col = QVBoxLayout()
            doc_col.setSpacing(0)
            doc_col.addWidget(w.label(w.short_name(p["doctor_name"]), 9, bold=True))
            doc_col.addWidget(w.label(p["specialty"] or "", 8, color=pl["muted"]))
            doc_row.addLayout(doc_col, 1)
        else:
            doc_row.addWidget(w.chip("Без лечащего врача", pl["warn_soft"], pl["warn"]))
            doc_row.addStretch()
        self.body_layout.addLayout(doc_row)

        stats = QHBoxLayout()
        stats.setSpacing(6)
        stats.addWidget(
            w.chip(w.plural(p["active_rx"], "назначение", "назначения", "назначений"), pl["accent_soft"], pl["accent"]))
        stats.addWidget(w.chip(w.plural(p["diary_count"], "запись", "записи", "записей"), pl["card_alt"], pl["muted"]))
        stats.addStretch()
        self.body_layout.addLayout(stats)


class DoctorCard(w.AnimatedCard):
    def __init__(self, d):
        super().__init__(width=258, accent=w.ROLE_COLORS["doctor"])
        pl = w.pal()
        self.data = d
        self.body_layout.setContentsMargins(12, 12, 12, 16)
        photo = w.Avatar(d["full_name"], 210, w.doctor_photo_path(d["photo"]), shape="rounded", height=196)
        self.body_layout.addWidget(photo, 0, Qt.AlignmentFlag.AlignHCenter)
        if not photo.has_photo():
            hint = w.label("фото не загружено", 8, color=pl["accent_light"])
            hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.body_layout.addWidget(hint)
        info = QVBoxLayout()
        info.setContentsMargins(6, 4, 6, 0)
        info.setSpacing(6)
        info.addWidget(w.label(d["full_name"], 11, bold=True, wrap=True))
        info.addWidget(w.chip(d["specialty"] or "Специальность не указана", pl["accent"]))
        place = " · ".join(x for x in (f"каб. {d['office']}" if d["office"] else "", d["schedule"] or "") if x)
        if place: info.addWidget(w.label(place, 9, color=pl["muted"], wrap=True))
        stats = QHBoxLayout()
        stats.setSpacing(6)
        stats.addWidget(
            w.chip(w.plural(d["patients_count"], "пациент", "пациента", "пациентов"), pl["accent_soft"], pl["accent"]))
        stats.addWidget(
            w.chip(w.plural(d["active_rx"], "назначение", "назначения", "назначений"), pl["card_alt"], pl["muted"]))
        stats.addStretch()
        info.addLayout(stats)
        self.body_layout.addLayout(info)


class UserCard(w.AnimatedCard):
    def __init__(self, u, is_me=False):
        color = w.ROLE_COLORS.get(u["role"], "#2F5C8F")
        super().__init__(width=300, accent=color)
        pl = w.pal()
        self.data = u
        row = QHBoxLayout()
        row.setSpacing(12)
        row.addWidget(w.Avatar(u["full_name"], 46, w.doctor_photo_path(u["photo"]), ring=color))
        col = QVBoxLayout()
        col.setSpacing(2)
        col.addWidget(w.label(u["full_name"], 10, bold=True, wrap=True))
        login = w.label(f"@{u['login']}", 9, color=pl["muted"])
        login.setFont(QFont("Consolas", 9))
        col.addWidget(login)
        row.addLayout(col, 1)
        self.body_layout.addLayout(row)
        bottom = QHBoxLayout()
        bottom.addWidget(w.chip(w.ROLE_NAMES.get(u["role"], u["role"]), color))
        if is_me: bottom.addWidget(w.chip("это вы", pl["ok_soft"], pl["ok"]))
        bottom.addStretch()
        created = u["created_at"].strftime("%d.%m.%Y") if u["created_at"] else ""
        bottom.addWidget(w.label(created, 8, color=pl["muted"]))
        self.body_layout.addLayout(bottom)


class JournalRow(w.AnimatedCard):
    def __init__(self, a):
        color = w.ROLE_COLORS.get(a["role"] or "", "#7A9CC6")
        super().__init__(accent=color, clickable=False)
        pl = w.pal()
        self.body_layout.setContentsMargins(16, 10, 16, 10)
        row = QHBoxLayout()
        row.setSpacing(12)
        title, icon = ACTION_NAMES.get(a["action"], (a["action"], ""))
        row.addWidget(w.Icon(icon, 36, pl["accent"], pl["accent_soft"], 18))
        col = QVBoxLayout()
        col.setSpacing(0)
        col.addWidget(w.label(title, 10, bold=True))
        who = a["full_name"] or "удалённый пользователь"
        role = w.ROLE_NAMES.get(a["role"] or "", "")
        col.addWidget(w.label(f"{who}" + (f" · {role}" if role else ""), 9, color=pl["muted"]))
        row.addLayout(col, 1)
        ts = a["ts"].strftime("%d.%m.%Y  %H:%M") if a["ts"] else ""
        row.addWidget(w.label(ts, 9, color=pl["muted"]))
        self.body_layout.addLayout(row)


# ============== ДИАЛОГ СОЗДАНИЯ ==============
class CreateUserDialog(QDialog):
    def __init__(self, parent, role="patient"):
        super().__init__(parent)
        pl = w.pal()
        self.result_data = None
        self._photo_src = None
        self._login_edited = False

        self.setWindowTitle("Новая учётная запись")
        self.setMinimumWidth(540)
        self.setStyleSheet(f"QDialog {{ background: {pl['bg']}; }}" + w.input_qss())

        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 22, 26, 22)
        lay.setSpacing(10)
        lay.addWidget(w.label("Новая учётная запись", 15, bold=True))

        self.role = w.SegmentedFilter([("patient", "Пациент"), ("doctor", "Врач"), ("admin", "Администратор")])
        lay.addWidget(self.role)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Фамилия Имя Отчество")
        self.login = QLineEdit()
        self.login.setPlaceholderText("латиница, цифры, _")
        self.password = QLineEdit(db.generate_password())

        regen = w.ghost_button("↻")
        regen.setFixedWidth(46)
        regen.setToolTip("Сгенерировать новый пароль")
        regen.clicked.connect(lambda: self.password.setText(db.generate_password()))

        pass_row = QHBoxLayout()
        pass_row.addWidget(self.password, 1)
        pass_row.addWidget(regen)

        grid.addWidget(w.label("ФИО", 9, color=pl["muted"]), 0, 0, 1, 2)
        grid.addWidget(self.full_name, 1, 0, 1, 2)
        grid.addWidget(w.label("Логин", 9, color=pl["muted"]), 2, 0)
        grid.addWidget(w.label("Пароль", 9, color=pl["muted"]), 2, 1)
        grid.addWidget(self.login, 3, 0)
        grid.addLayout(pass_row, 3, 1)
        lay.addLayout(grid)

        # --- Поля врача ---
        self.doctor_box = QWidget()
        dg = QGridLayout(self.doctor_box)
        dg.setContentsMargins(0, 6, 0, 0)
        dg.setHorizontalSpacing(12)
        dg.setVerticalSpacing(6)

        self.specialty = QComboBox()
        self.specialty.setEditable(True)
        self.specialty.addItems(SPECIALTIES)
        self.office = QLineEdit()
        self.office.setPlaceholderText("204")
        self.doc_phone = QLineEdit()
        self.doc_phone.setPlaceholderText("+7XXXXXXXXXX")
        self.photo_preview = w.Avatar("", 64, shape="rounded")
        photo_btn = w.ghost_button("Выбрать фото")
        photo_btn.clicked.connect(self._pick_photo)

        self.schedule = ScheduleInput()

        dg.addWidget(w.label("Специальность", 9, color=pl["muted"]), 0, 0)
        dg.addWidget(w.label("Кабинет", 9, color=pl["muted"]), 0, 1)
        dg.addWidget(self.specialty, 1, 0)
        dg.addWidget(self.office, 1, 1)

        dg.addWidget(w.label("Телефон", 9, color=pl["muted"]), 2, 0)
        dg.addWidget(self.doc_phone, 3, 0)

        dg.addWidget(w.label("График приёма", 9, color=pl["muted"]), 4, 0, 1, 2)
        dg.addWidget(self.schedule, 5, 0, 1, 2)

        photo_row = QHBoxLayout()
        photo_row.addWidget(self.photo_preview)
        photo_row.addWidget(photo_btn)
        photo_row.addStretch()
        dg.addLayout(photo_row, 6, 0, 1, 2)
        lay.addWidget(self.doctor_box)

        # --- Поля пациента ---
        self.patient_box = QWidget()
        pg = QGridLayout(self.patient_box)
        pg.setContentsMargins(0, 6, 0, 0)
        pg.setHorizontalSpacing(12)
        pg.setVerticalSpacing(6)

        self.birth = QDateEdit(QDate(1990, 1, 1))
        self.birth.setCalendarPopup(True)
        self.birth.setDisplayFormat("dd.MM.yyyy")
        self.gender = QComboBox()
        self.gender.addItems(["мужской", "женский"])
        self.policy = QLineEdit()
        self.policy.setPlaceholderText("16 цифр")
        self.pat_phone = QLineEdit()
        self.pat_phone.setPlaceholderText("+7XXXXXXXXXX")
        self.doctor = QComboBox()
        self.doctor.addItem("— не назначен —", None)
        for d in db.get_all_doctors(): self.doctor.addItem(d[1], d[0])

        pg.addWidget(w.label("Дата рождения", 9, color=pl["muted"]), 0, 0)
        pg.addWidget(w.label("Пол", 9, color=pl["muted"]), 0, 1)
        pg.addWidget(self.birth, 1, 0)
        pg.addWidget(self.gender, 1, 1)
        pg.addWidget(w.label("Полис ОМС", 9, color=pl["muted"]), 2, 0)
        pg.addWidget(w.label("Телефон", 9, color=pl["muted"]), 2, 1)
        pg.addWidget(self.policy, 3, 0)
        pg.addWidget(self.pat_phone, 3, 1)
        pg.addWidget(w.label("Лечащий врач", 9, color=pl["muted"]), 4, 0, 1, 2)
        pg.addWidget(self.doctor, 5, 0, 1, 2)
        lay.addWidget(self.patient_box)

        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel = w.ghost_button("Отмена")
        cancel.clicked.connect(self.reject)
        create = w.primary_button("Создать")
        create.clicked.connect(self._create)
        buttons.addWidget(cancel)
        buttons.addWidget(create)
        lay.addSpacing(6)
        lay.addLayout(buttons)

        self.full_name.textChanged.connect(self._suggest_login)
        self.login.textEdited.connect(lambda _: setattr(self, "_login_edited", True))
        self.role.changed.connect(self._on_role)

        self.role.set_value(role)
        self._on_role(role)
        self.adjustSize()

    def _on_role(self, role):
        self.doctor_box.setVisible(role == "doctor")
        self.patient_box.setVisible(role == "patient")
        self.adjustSize()

    def _suggest_login(self, text):
        if not self._login_edited and text.strip():
            self.login.setText(db.find_free_login(db.generate_login(text)))
        self.photo_preview.full_name = text
        self.photo_preview.update()

    def _pick_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Фото врача", "", "Изображения (*.png *.jpg *.jpeg *.bmp *.webp)")
        if path:
            self._photo_src = path
            self.photo_preview.set_photo(path)

    def _create(self):
        role = self.role.value()
        full_name = self.full_name.text().strip()
        login = self.login.text().strip()
        password = self.password.text().strip()

        for (ok, err), field, title in (
                (validate_name(full_name), self.full_name, "Ошибка в ФИО"),
                (validate_login(login), self.login, "Ошибка в логине"),
                (validate_password(password), self.password, "Ошибка в пароле"),
        ):
            if not ok:
                mb.warning(self, title, err)
                field.setFocus()
                return

        if role == "doctor":
            ok, err = validate_phone(self.doc_phone.text())
            if not ok:
                mb.warning(self, "Ошибка в телефоне", err)
                return

        if role == "patient":
            birth = self.birth.date().toString("yyyy-MM-dd")
            for ok, err in (
                    validate_birth_date(birth), validate_policy(self.policy.text()),
                    validate_phone(self.pat_phone.text())):
                if not ok:
                    mb.warning(self, "Ошибка в анкете", err)
                    return

        id_user = db.create_user(login, password, role, full_name)
        if id_user is None:
            mb.warning(self, "Логин занят", f"Логин «{login}» уже используется.")
            self.login.setFocus()
            self.login.selectAll()
            return

        if role == "doctor":
            db.create_doctor(id_user, self.specialty.currentText().strip() or "Терапевт")
            doctor = db.get_doctor_by_user(id_user)
            if doctor:
                photo = common.save_doctor_photo(doctor[0], self._photo_src) if self._photo_src else None
                db.update_doctor_profile(
                    doctor[0], self.specialty.currentText().strip() or "Терапевт",
                               self.office.text().strip() or None,
                    self.schedule.get_text(),
                               self.doc_phone.text().strip() or None, None, photo
                )
        elif role == "patient":
            db.create_patient(
                id_user, full_name, self.birth.date().toString("yyyy-MM-dd"),
                self.gender.currentText(), self.policy.text().strip(),
                self.pat_phone.text().strip(), self.doctor.currentData()
            )

        self.result_data = {"id_user": id_user, "login": login, "password": password, "role": role}
        self.accept()


# ============== ГЛАВНОЕ ОКНО ==============
class AdminAnalyticsWindow(QMainWindow):
    def __init__(self, user_name: str = "", login_window=None, id_user=None):
        super().__init__()
        self.login_window = login_window
        self.user_name = user_name
        self.id_user = id_user
        pl = w.pal()
        self.setWindowTitle("Дневник терапии — CRM клиники")
        self.resize(1400, 900)
        self.setMinimumSize(1100, 720)
        central = QWidget()
        central.setObjectName("crmRoot")
        central.setStyleSheet(f"QWidget#crmRoot {{ background: {pl['bg']}; }}" + w.input_qss())
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(26, 18, 26, 12)
        root.setSpacing(14)
        root.addLayout(self._build_header())
        self.kpi_row = QHBoxLayout()
        self.kpi_row.setSpacing(8)
        root.addLayout(self.kpi_row)
        self.tabs = w.FolderTabs()
        self.tabs.add_tab(self._build_analytics(), "Аналитика", "chart", TAB_COLORS[0])
        self.tabs.add_tab(self._build_patients(), "Пациенты", "users", TAB_COLORS[1])
        self.tabs.add_tab(self._build_doctors(), "Врачи", "stethoscope", TAB_COLORS[2])
        self.tabs.add_tab(self._build_accounts(), "Учётные записи", "lock", TAB_COLORS[3])
        self.tabs.add_tab(self._build_journal(), "Журнал", "clock", TAB_COLORS[4])
        self.tabs.currentChanged.connect(self._on_tab)
        root.addWidget(self.tabs, 1)
        self.statusLabel = w.label("", 8)
        root.addWidget(self.statusLabel)
        self.panel = w.SidePanel(central)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.on_logout)
        QShortcut(QKeySequence("Ctrl+F"), self, self._focus_search)
        QShortcut(QKeySequence("Ctrl+N"), self, lambda: self.on_create_user())
        for i in range(5): QShortcut(QKeySequence(f"Ctrl+{i + 1}"), self, lambda i=i: self.tabs.set_current(i))
        self._update_status_bar()
        QTimer.singleShot(50, self.refresh_all)

    def _build_header(self):
        pl = w.pal()
        row = QHBoxLayout()
        row.setSpacing(14)
        logo = QLabel("ДТ")
        logo.setFixedSize(44, 44)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont(w.FONT, 13, QFont.Weight.Bold))
        logo.setStyleSheet(
            "color: white; border-radius: 13px; background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #2F5C8F, stop:1 #163257);")
        row.addWidget(logo)
        titles = QVBoxLayout()
        titles.setSpacing(0)
        titles.addWidget(w.label("Дневник терапии", 15, bold=True))
        titles.addWidget(w.label("CRM клиники · панель администратора", 9, color=pl["muted"]))
        row.addLayout(titles)
        row.addStretch()
        add_btn = w.primary_button("+  Новая учётная запись")
        add_btn.setToolTip("Ctrl+N")
        add_btn.clicked.connect(lambda: self.on_create_user())
        row.addWidget(add_btn)
        me = QFrame()
        me.setObjectName("meChip")
        me.setStyleSheet(
            f"QFrame#meChip {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 24px; }}")
        me_lay = QHBoxLayout(me)
        me_lay.setContentsMargins(6, 4, 14, 4)
        me_lay.addWidget(w.Avatar(self.user_name or "Админ", 36, ring=w.ROLE_COLORS["admin"]))
        me_col = QVBoxLayout()
        me_col.setSpacing(0)
        me_col.addWidget(w.label(w.short_name(self.user_name) or "Администратор", 9, bold=True))
        me_col.addWidget(w.label("администратор", 8, color=pl["muted"]))
        me_lay.addLayout(me_col)
        row.addWidget(me)
        self.logoutBtn = w.ghost_button("Выйти")
        self.logoutBtn.setToolTip("Ctrl+Q")
        self.logoutBtn.clicked.connect(self.on_logout)
        row.addWidget(self.logoutBtn)
        return row

    def _build_analytics(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        self.barChartView = BarChartWidget()
        self.pieChartView = PieChartWidget()
        self.lineChartView = LineChartWidget()
        grid = QGridLayout()
        grid.setSpacing(4)
        for chart, r, c, cs in (
                (self.barChartView, 0, 0, 1), (self.pieChartView, 0, 1, 1), (self.lineChartView, 1, 0, 2)):
            card = w.AnimatedCard(clickable=False)
            card.body_layout.setContentsMargins(12, 10, 12, 16)
            card.body_layout.addWidget(chart)
            grid.addWidget(card, r, c, 1, cs)
        lay.addLayout(grid, 1)
        export = QHBoxLayout()
        export.setSpacing(16)
        export.addWidget(w.label("В отчёт:", 10, bold=True))
        self.barChartCheckBox = QCheckBox("Пациенты по врачам")
        self.pieChartCheckBox = QCheckBox("Приверженность лечению")
        self.lineChartCheckBox = QCheckBox("Активность в дневнике")
        for cb in (self.barChartCheckBox, self.pieChartCheckBox, self.lineChartCheckBox):
            cb.setChecked(True)
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            export.addWidget(cb)
        export.addStretch()
        self.exportPdfButton = w.primary_button("Скачать PDF-отчёт")
        self.exportPdfButton.clicked.connect(self.on_export_pdf)
        export.addWidget(self.exportPdfButton)
        lay.addLayout(export)
        return page

    def _build_patients(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)
        bar = QHBoxLayout()
        bar.setSpacing(10)
        self.patient_search = w.search_line("Поиск по ФИО, логину, полису, телефону")
        self.patient_search_timer = QTimer(self)
        self.patient_search_timer.setSingleShot(True)
        self.patient_search_timer.timeout.connect(self._render_patients)
        self.patient_search.textChanged.connect(lambda: self.patient_search_timer.start(300))
        self.patient_filter = w.SegmentedFilter(
            [("all", "Все"), ("attention", "Требуют внимания"), ("no_doctor", "Без врача")])
        self.patient_filter.changed.connect(self._render_patients)
        self.patient_doctor = QComboBox()
        self.patient_doctor.setMinimumWidth(220)
        self.patient_doctor.currentIndexChanged.connect(self._render_patients)
        add = w.ghost_button("+ Пациент")
        add.clicked.connect(lambda: self.on_create_user("patient"))
        export_btn = w.ghost_button("Выгрузить список PDF")
        export_btn.clicked.connect(self.export_patients_pdf)
        bar.addWidget(self.patient_search, 1)
        bar.addWidget(self.patient_filter)
        bar.addWidget(self.patient_doctor)
        bar.addWidget(add)
        bar.addWidget(export_btn)
        lay.addLayout(bar)
        self.patients_count = w.label("", 9, color=w.pal()["muted"])
        lay.addWidget(self.patients_count)
        self.patients_grid = w.CardGrid("Пациенты не найдены")
        lay.addWidget(self.patients_grid, 1)
        return page

    def _build_doctors(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)
        bar = QHBoxLayout()
        bar.setSpacing(10)
        self.doctor_search = w.search_line("Поиск по ФИО, специальности, кабинету")
        self.doctor_search_timer = QTimer(self)
        self.doctor_search_timer.setSingleShot(True)
        self.doctor_search_timer.timeout.connect(self._render_doctors)
        self.doctor_search.textChanged.connect(lambda: self.doctor_search_timer.start(300))
        self.doctor_spec = QComboBox()
        self.doctor_spec.setMinimumWidth(200)
        self.doctor_spec.currentIndexChanged.connect(self._render_doctors)
        add = w.ghost_button("+ Врач")
        add.clicked.connect(lambda: self.on_create_user("doctor"))
        bar.addWidget(self.doctor_search, 1)
        bar.addWidget(self.doctor_spec)
        bar.addWidget(add)
        lay.addLayout(bar)
        self.doctors_grid = w.CardGrid("Врачи не найдены")
        lay.addWidget(self.doctors_grid, 1)
        return page

    def _build_accounts(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)
        bar = QHBoxLayout()
        bar.setSpacing(10)
        self.user_search = w.search_line("Поиск по ФИО или логину")
        self.user_search_timer = QTimer(self)
        self.user_search_timer.setSingleShot(True)
        self.user_search_timer.timeout.connect(self._render_accounts)
        self.user_search.textChanged.connect(lambda: self.user_search_timer.start(300))
        self.user_role = w.SegmentedFilter(
            [("all", "Все"), ("admin", "Администраторы"), ("doctor", "Врачи"), ("patient", "Пациенты")])
        self.user_role.changed.connect(self._render_accounts)
        bar.addWidget(self.user_search, 1)
        bar.addWidget(self.user_role)
        lay.addLayout(bar)
        self.users_grid = w.CardGrid("Учётные записи не найдены")
        lay.addWidget(self.users_grid, 1)
        return page

    def _build_journal(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        lay.addWidget(w.label("Последние действия в системе", 11, bold=True))
        self.journal_inner = QWidget()
        self.journal_inner.setStyleSheet("background: transparent;")
        self.journal_layout = QVBoxLayout(self.journal_inner)
        self.journal_layout.setContentsMargins(0, 0, 6, 0)
        self.journal_layout.setSpacing(0)
        lay.addWidget(w.make_scroll(self.journal_inner), 1)
        return page

    def refresh_all(self):
        try:
            self.patients = db.get_patients_crm()
            self.doctors = db.get_doctors_crm()
            self.users = db.get_users_crm()
            self._fill_combo(self.patient_doctor,
                             [("Все врачи", None)] + [(d["full_name"], d["id_doctor"]) for d in self.doctors])
            specs = sorted({d["specialty"] for d in self.doctors if d["specialty"]})
            self._fill_combo(self.doctor_spec, [("Все специальности", None)] + [(s, s) for s in specs])
            self._render_kpi()
            for chart in (self.barChartView, self.pieChartView, self.lineChartView): chart.reload()
            self._render_patients()
            self._render_doctors()
            self._render_accounts()
            self._render_journal()
        except Exception as e:
            mb.critical(self, "Ошибка базы данных",
                        "Потеряно соединение с базой данных.\n\n"
                        "Проверьте, запущен ли сервер MySQL и верны ли данные в config.py.\n\n"
                        f"Техническая информация: {e}")
            self.statusLabel.setText("● Нет связи с БД")
            self.statusLabel.setStyleSheet("color: #C0392B; background: transparent;")

    @staticmethod
    def _fill_combo(combo, items):
        current = combo.currentData()
        combo.blockSignals(True)
        combo.clear()
        for text, data in items: combo.addItem(text, data)
        idx = combo.findData(current)
        combo.setCurrentIndex(idx if idx >= 0 else 0)
        combo.blockSignals(False)

    def _render_kpi(self):
        while self.kpi_row.count():
            item = self.kpi_row.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        c = db.get_crm_counters()
        tiles = [
            w.KpiTile("users", "пациентов", c.get("patients", 0), "#2F5C8F",
                      f"{c['no_doctor']} без врача" if c.get("no_doctor") else ""),
            w.KpiTile("stethoscope", "врачей", c.get("doctors", 0), "#2F5C8F"),
            w.KpiTile("pill", "активных назначений", c.get("active_prescriptions", 0), "#2F5C8F"),
            w.KpiTile("book", "записей в дневниках за 7 дней", c.get("diary_week", 0), "#2F5C8F"),
        ]
        for i, t in enumerate(tiles): self.kpi_row.addWidget(t); t.appear(i * 70)

    def _render_patients(self, *_):
        text = self.patient_search.text().strip().lower()
        mode = self.patient_filter.value()
        id_doctor = self.patient_doctor.currentData()
        result = []
        for p in self.patients:
            hay = " ".join(str(p[k] or "") for k in ("full_name", "login", "policy_number", "phone")).lower()
            if text and text not in hay: continue
            if id_doctor and p["id_doctor"] != id_doctor: continue
            if mode == "no_doctor" and p["id_doctor"]: continue
            if mode == "attention" and w.mood_of(p["last_wellbeing"])[0] not in ("Плохо", "Очень плохо"): continue
            result.append(p)
        cards = []
        for p in result:
            card = PatientCard(p)
            card.clicked.connect(lambda p=p: self.open_patient(p["id_patient"]))
            cards.append(card)
        self.patients_grid.set_cards(cards)
        self.patients_count.setText(f"Показано {len(result)} из {len(self.patients)}")

    def _render_doctors(self, *_):
        text = self.doctor_search.text().strip().lower()
        spec = self.doctor_spec.currentData()
        cards = []
        for d in self.doctors:
            hay = " ".join(str(d[k] or "") for k in ("full_name", "specialty", "office", "login")).lower()
            if text and text not in hay: continue
            if spec and d["specialty"] != spec: continue
            card = DoctorCard(d)
            card.clicked.connect(lambda d=d: self.open_doctor(d["id_doctor"]))
            cards.append(card)
        self.doctors_grid.set_cards(cards)

    def _render_accounts(self, *_):
        text = self.user_search.text().strip().lower()
        role = self.user_role.value()
        cards = []
        for u in self.users:
            if role != "all" and u["role"] != role: continue
            if text and text not in f"{u['full_name']} {u['login']}".lower(): continue
            card = UserCard(u, is_me=u["id_user"] == self.id_user)
            card.clicked.connect(lambda u=u: self.open_user(u["id_user"]))
            cards.append(card)
        self.users_grid.set_cards(cards)

    def _render_journal(self):
        while self.journal_layout.count():
            item = self.journal_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        rows = db.get_audit_log(100)
        if not rows: self.journal_layout.addWidget(w.label("Журнал пуст", 10, color=w.pal()["muted"]))
        for i, a in enumerate(rows):
            row = JournalRow(a)
            self.journal_layout.addWidget(row)
            row.appear(min(i, 12) * 35)
        self.journal_layout.addStretch()

    def _on_tab(self, i):
        self.panel.close_panel()

    def _focus_search(self):
        searches = {1: self.patient_search, 2: self.doctor_search, 3: self.user_search}
        line = searches.get(self.tabs.bar.current())
        if line: line.setFocus(); line.selectAll()

    def _log(self, action, entity_type=None, entity_id=None):
        db.log_action(self.id_user, action, entity_type, entity_id)

    def open_patient(self, id_patient):
        p = next((x for x in self.patients if x["id_patient"] == id_patient), None)
        if not p: return
        pl = w.pal()
        self.panel.open_panel("Карточка пациента")
        lay = self.panel.content_layout
        head = QHBoxLayout()
        head.setSpacing(14)
        mood, mood_color = w.mood_of(p["last_wellbeing"])
        head.addWidget(w.Avatar(p["full_name"], 72, ring=mood_color))
        col = QVBoxLayout()
        col.setSpacing(4)
        col.addWidget(w.label(p["full_name"], 14, bold=True, wrap=True))
        col.addWidget(w.label(f"@{p['login']}", 9, color=pl["muted"]))
        col.addWidget(w.chip(f"Самочувствие: {mood}", mood_color))
        head.addLayout(col, 1)
        lay.addLayout(head)

        exp_diary = w.ghost_button("Выгрузить дневник в PDF")
        exp_diary.clicked.connect(lambda: self.export_single_diary(id_patient, p["full_name"]))
        lay.addWidget(exp_diary)

        lay.addWidget(w.section_title("Анкета"))
        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(4)
        b0 = p["birth_date"]
        birth = QDateEdit(QDate(b0.year, b0.month, b0.day) if b0 else QDate(1990, 1, 1))
        birth.setCalendarPopup(True)
        birth.setDisplayFormat("dd.MM.yyyy")
        gender = QComboBox()
        gender.addItems(["мужской", "женский"])
        if p["gender"]: gender.setCurrentText(p["gender"])
        policy = QLineEdit(p["policy_number"] or "")
        phone = QLineEdit(p["phone"] or "")
        for i, (cap, field) in enumerate(
                (("Дата рождения", birth), ("Пол", gender), ("Полис ОМС", policy), ("Телефон", phone))):
            form.addWidget(w.label(cap, 9, color=pl["muted"]), (i // 2) * 2, i % 2)
            form.addWidget(field, (i // 2) * 2 + 1, i % 2)
        lay.addLayout(form)
        save = w.primary_button("Сохранить анкету")

        def save_profile():
            b = birth.date().toString("yyyy-MM-dd")
            for ok, err in (validate_birth_date(b), validate_policy(policy.text()), validate_phone(phone.text())):
                if not ok: mb.warning(self, "Ошибка в анкете", err); return
            if db.update_patient_profile(id_patient, b, gender.currentText(), policy.text().strip(),
                                         phone.text().strip()):
                self._log("update_patient", "patients", id_patient)
                save.setText("✓ Сохранено")
                QTimer.singleShot(1400, lambda: save.setText("Сохранить анкету"))
                self.refresh_all()

        save.clicked.connect(save_profile)
        lay.addWidget(save)

        lay.addWidget(w.section_title("Лечащий врач"))
        doc_row = QHBoxLayout()
        doctor = QComboBox()
        doctor.addItem("— не назначен —", None)
        for d in self.doctors: doctor.addItem(f"{d['full_name']} ({d['specialty'] or 'врач'})", d["id_doctor"])
        doctor.setCurrentIndex(max(0, doctor.findData(p["id_doctor"])))
        doctor.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        doctor.setMinimumContentsLength(12)
        assign = w.ghost_button("Прикрепить")

        def do_assign():
            if db.reassign_patient_doctor(id_patient, doctor.currentData()):
                self._log("reassign_doctor", "patients", id_patient)
                self.refresh_all()
                self.open_patient(id_patient)

        assign.clicked.connect(do_assign)
        doc_row.addWidget(doctor, 1)
        doc_row.addWidget(assign)
        lay.addLayout(doc_row)

        rx = db.get_prescriptions_full(id_patient)
        lay.addWidget(w.section_title(f"Назначения · {len(rx)}"))
        if not rx: lay.addWidget(w.label("Назначений пока нет", 9, color=pl["muted"]))
        for r in rx: lay.addWidget(common.rx_row(r))

        entries = db.get_diary_entries_for_patient(id_patient)[:5]
        lay.addWidget(w.section_title("Последние записи дневника"))
        if not entries: lay.addWidget(w.label("Записей нет", 9, color=pl["muted"]))
        for e in entries:
            m, color = w.mood_of(e[3])
            row = QHBoxLayout()
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background: {color}; border-radius: 5px;")
            row.addWidget(dot)
            row.addWidget(w.label(e[1].strftime("%d.%m.%Y"), 9, bold=True))
            row.addWidget(w.label(m, 9, color=color))
            sym = e[4] if e[4] and e[4] != "нет" else ""
            row.addWidget(w.label(sym, 9, color=pl["muted"]), 1)
            lay.addLayout(row)

        self._account_actions(lay, p["id_user"], p["login"], p["full_name"])
        lay.addStretch()

    def open_doctor(self, id_doctor):
        d = next((x for x in self.doctors if x["id_doctor"] == id_doctor), None)
        if not d: return
        pl = w.pal()
        self.panel.open_panel("Карточка врача")
        lay = self.panel.content_layout
        photo = w.Avatar(d["full_name"], 240, w.doctor_photo_path(d["photo"]), shape="rounded", height=260)
        lay.addWidget(photo, 0, Qt.AlignmentFlag.AlignHCenter)
        photo_row = QHBoxLayout()
        upload = w.primary_button("Загрузить фото" if not d["photo"] else "Заменить фото")
        photo_row.addWidget(upload)
        if d["photo"]:
            remove = w.danger_button("Убрать")
            photo_row.addWidget(remove)

            def do_remove():
                if mb.confirm(self, "Фото врача", "Удалить фотографию врача?"):
                    common.remove_doctor_photo(d["photo"])
                    db.update_doctor_profile(id_doctor, d["specialty"], d["office"], d["schedule"], d["phone"],
                                             d["email"], None)
                    self.refresh_all()
                    self.open_doctor(id_doctor)

            remove.clicked.connect(do_remove)

        def do_upload():
            path, _ = QFileDialog.getOpenFileName(self, "Фото врача", "",
                                                  "Изображения (*.png *.jpg *.jpeg *.bmp *.webp)")
            if not path: return
            name = common.save_doctor_photo(id_doctor, path, d["photo"])
            if not name or name == d["photo"]: mb.warning(self, "Фото", "Не удалось открыть изображение."); return
            db.update_doctor_profile(id_doctor, d["specialty"], d["office"], d["schedule"], d["phone"], d["email"],
                                     name)
            self._log("doctor_photo", "doctors", id_doctor)
            self.refresh_all()
            self.open_doctor(id_doctor)

        upload.clicked.connect(do_upload)
        lay.addLayout(photo_row)
        lay.addWidget(w.label(d["full_name"], 14, bold=True, wrap=True))
        lay.addWidget(w.label(f"@{d['login']}", 9, color=pl["muted"]))

        lay.addWidget(w.section_title("Профиль"))
        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(4)
        specialty = QComboBox()
        specialty.setEditable(True)
        specialty.addItems(SPECIALTIES)
        specialty.setCurrentText(d["specialty"] or "")
        office = QLineEdit(d["office"] or "")
        phone = QLineEdit(d["phone"] or "")
        email = QLineEdit(d["email"] or "")

        schedule = ScheduleInput()
        schedule.set_text(d["schedule"] or "")

        form.addWidget(w.label("Специальность", 9, color=pl["muted"]), 0, 0)
        form.addWidget(w.label("Кабинет", 9, color=pl["muted"]), 0, 1)
        form.addWidget(specialty, 1, 0)
        form.addWidget(office, 1, 1)

        form.addWidget(w.label("Телефон", 9, color=pl["muted"]), 2, 0)
        form.addWidget(w.label("E-mail", 9, color=pl["muted"]), 2, 1)
        form.addWidget(phone, 3, 0)
        form.addWidget(email, 3, 1)

        form.addWidget(w.label("График приёма", 9, color=pl["muted"]), 4, 0, 1, 2)
        form.addWidget(schedule, 5, 0, 1, 2)

        lay.addLayout(form)
        save = w.primary_button("Сохранить профиль")

        def save_profile():
            ok, err = validate_phone(phone.text())
            if not ok: mb.warning(self, "Ошибка в телефоне", err); return
            mail = email.text().strip()
            if mail and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", mail): mb.warning(self, "Ошибка в e-mail",
                                                                                      "Введите адрес вида name@clinic.ru"); return

            new_sched = schedule.get_text()

            if db.update_doctor_profile(id_doctor, specialty.currentText().strip(), office.text().strip(), new_sched,
                                        phone.text().strip(), mail, d["photo"]):
                self._log("update_doctor", "doctors", id_doctor)
                save.setText("✓ Сохранено")
                QTimer.singleShot(1400, lambda: save.setText("Сохранить профиль"))
                self.refresh_all()

        save.clicked.connect(save_profile)
        lay.addWidget(save)

        mine = [p for p in self.patients if p["id_doctor"] == id_doctor]
        lay.addWidget(w.section_title(f"Пациенты · {len(mine)}"))
        if not mine: lay.addWidget(w.label("Пациентов пока нет", 9, color=pl["muted"]))
        for p in mine:
            btn = QPushButton()
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                f"QPushButton {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 12px; }} QPushButton:hover {{ border-color: {pl['accent']}; }}")
            btn.setMinimumHeight(52)
            bl = QHBoxLayout(btn)
            bl.setContentsMargins(10, 6, 10, 6)
            bl.addWidget(w.Avatar(p["full_name"], 36))
            bl.addWidget(w.label(p["full_name"], 10, bold=True), 1)
            m, color = w.mood_of(p["last_wellbeing"])
            bl.addWidget(w.chip(m, color))
            btn.clicked.connect(lambda _=False, i=p["id_patient"]: self.open_patient(i))
            lay.addWidget(btn)
        self._account_actions(lay, d["id_user"], d["login"], d["full_name"])
        lay.addStretch()

    def open_user(self, id_user):
        u = next((x for x in self.users if x["id_user"] == id_user), None)
        if not u: return
        if u["role"] == "patient":
            p = db.get_patient_by_user(id_user)
            if p: self.open_patient(p[0]); return
        if u["role"] == "doctor":
            d = db.get_doctor_by_user(id_user)
            if d: self.open_doctor(d[0]); return
        self.panel.open_panel("Учётная запись")
        lay = self.panel.content_layout
        color = w.ROLE_COLORS.get(u["role"], "#2F5C8F")
        head = QHBoxLayout()
        head.addWidget(w.Avatar(u["full_name"], 72, ring=color))
        col = QVBoxLayout()
        col.addWidget(w.label(u["full_name"], 14, bold=True, wrap=True))
        col.addWidget(w.chip(w.ROLE_NAMES.get(u["role"], u["role"]), color))
        head.addLayout(col, 1)
        lay.addLayout(head)
        lay.addWidget(w.info_block([("Логин", u["login"]), (
            "Создана", u["created_at"].strftime("%d.%m.%Y %H:%M") if u["created_at"] else "—")]))
        self._account_actions(lay, id_user, u["login"], u["full_name"])
        lay.addStretch()

    def _account_actions(self, lay, id_user, login, full_name):
        lay.addWidget(w.section_title("Учётная запись"))
        row = QHBoxLayout()
        reset = w.ghost_button("Сбросить пароль")
        reset.clicked.connect(lambda: self.on_reset_password(id_user, login))
        row.addWidget(reset)
        if id_user != self.id_user:
            delete = w.danger_button("Удалить")
            delete.clicked.connect(lambda: self.on_delete(id_user, login, full_name))
            row.addWidget(delete)
        lay.addLayout(row)

    def on_create_user(self, role="patient"):
        dlg = CreateUserDialog(self, role)
        if dlg.exec() and dlg.result_data:
            r = dlg.result_data
            self._log("create_user", "users", r["id_user"])
            self.refresh_all()
            common.CredentialsDialog(self, r["login"], r["password"], "Учётная запись создана").exec()

    def on_reset_password(self, id_user, login):
        if not mb.confirm(self, "Сброс пароля", f"Сгенерировать новый пароль для «{login}»?"): return
        new_password = db.generate_password()
        if db.reset_user_password(id_user, new_password):
            self._log("reset_password", "users", id_user)
            common.CredentialsDialog(self, login, new_password, "Пароль сброшен").exec()
            self._render_journal()
        else:
            mb.critical(self, "Ошибка", "Не удалось сбросить пароль")

    def on_delete(self, id_user, login, full_name):
        if not mb.confirm(self, "Удаление",
                          f"Удалить «{full_name}» (@{login})?\n\nВместе с пациентом удаляются его дневник и назначения."): return
        d = db.get_doctor_by_user(id_user)
        photo = None
        if d: photo = next((x["photo"] for x in self.doctors if x["id_doctor"] == d[0]), None)
        if db.delete_user(id_user):
            common.remove_doctor_photo(photo)
            self._log("delete_user", "users", id_user)
            self.panel.close_panel()
            self.refresh_all()
        else:
            mb.critical(self, "Ошибка", "Не удалось удалить пользователя")

    def _update_status_bar(self):
        ok, err = db.check_connection()
        if ok:
            self.statusLabel.setText("● Подключено к базе данных")
            self.statusLabel.setStyleSheet("color: #27AE60; background: transparent;")
        else:
            self.statusLabel.setText(f"● Нет связи с БД: {err[:60]}")
            self.statusLabel.setStyleSheet("color: #C0392B; background: transparent;")

    def on_logout(self):
        if self.login_window: self.login_window.return_from_child()
        self.close()

    def export_patients_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить список", "patients.pdf", "PDF (*.pdf)")
        if not path: return
        if not path.endswith(".pdf"): path += ".pdf"
        try:
            pdf_exporter.export_patients_to_pdf(path, self.patients, "Список пациентов клиники")
            mb.info(self, "Готово", "Список пациентов выгружен.")
        except Exception as e:
            mb.critical(self, "Ошибка", f"Не удалось: {e}")

    def export_single_diary(self, id_patient, name):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить дневник", f"diary_{name}.pdf", "PDF (*.pdf)")
        if not path: return
        if not path.endswith(".pdf"): path += ".pdf"
        entries = db.get_diary_entries_for_patient(id_patient)
        try:
            pdf_exporter.export_diary_to_pdf(path, name, entries, db.get_indicators_for_diary)
            mb.info(self, "Готово", "Дневник выгружен.")
        except Exception as e:
            mb.critical(self, "Ошибка", f"Не удалось: {e}")

    def on_export_pdf(self):
        selected = []
        if self.barChartCheckBox.isChecked(): selected.append(("Столбчатая — Пациенты по врачам", BarChartWidget))
        if self.pieChartCheckBox.isChecked(): selected.append(("Круговая — Приверженность лечению", PieChartWidget))
        if self.lineChartCheckBox.isChecked(): selected.append(("Линейная — Активность в дневнике", LineChartWidget))
        if not selected: mb.warning(self, "Ничего не выбрано", "Отметьте хотя бы одну диаграмму."); return
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчёт как PDF", "analytics_report.pdf",
                                                   "PDF Files (*.pdf)")
        if not file_path: return
        if not file_path.lower().endswith(".pdf"): file_path += ".pdf"

        charts = []
        for name, cls in selected:
            temp = cls()
            temp.print_mode = True
            temp.resize(2000, 1500)
            temp.show()
            QApplication.processEvents()
            pixmap = QPixmap(2000, 1500)
            pixmap.fill(QColor("#FFFFFF"))
            temp.render(pixmap)
            temp.hide()
            temp.deleteLater()
            charts.append((name, pixmap))

        try:
            pdf_exporter.export_charts_to_pdf(file_path, charts)
            self._log("export_pdf")
            self._render_journal()
            mb.info(self, "Готово", f"Отчёт сохранён:\n{file_path}")
        except Exception as e:
            mb.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")