"""Личный кабинет пациента.

Вкладки-папки: Сегодня, Дневник, История, Назначения, Профиль.
Дневник заполняется «по шагам»: лицо-настроение, шкала интенсивности,
чипы симптомов и триггеров, плитки показателей. Формат сохранения
записи прежний — его разбирает окно врача.
"""

import logging
from datetime import date, datetime, timedelta

from PySide6.QtCore import Property, QEasingCurve, QPointF, QPropertyAnimation, QRectF, Qt, QTime, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QKeySequence, QPainter, QPainterPath, QPen, QShortcut
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import db
from validators import (
    validate_height,
    validate_pressure,
    validate_pulse,
    validate_sugar,
    validate_temperature,
    validate_weight,
)
from windows import common
from windows import msgbox as mb
from windows import widgets as w
from windows.common import DiaryCard, MoodTrend, RxCard, human_date, time_str

TAB_COLORS = ["#163257", "#1E4470", "#2F5C8F", "#5A7CA6", "#7A9CC6"]

# Варианты самочувствия — те же строки, что были в выпадающем списке
MOODS = [(5, "Отлично"), (4, "Хорошо"), (3, "Удовлетворительно"), (2, "Плохо"), (1, "Очень плохо")]

# Симптомы и триггеры — те же формулировки, что сохранялись раньше
SYMPTOMS = ["головная боль", "слабость", "тошнота", "головокружение", "боль в сердце", "одышка",
            "повышение давления", "нарушение сна", "потеря аппетита", "тремор рук",
            "повышенная потливость", "другое"]
TRIGGERS = ["стресс", "смена погоды", "еда", "физическая нагрузка", "недосып",
            "пропуск лекарства", "алкоголь", "другое"]

# (название в БД, единица, иконка, подсказка, функция проверки)
INDICATORS = [
    ("Давление", "мм рт.ст.", "gauge", "120/80", validate_pressure),
    ("Пульс", "уд/мин", "heart", "72", validate_pulse),
    ("Сахар", "ммоль/л", "drop", "5.5", validate_sugar),
    ("Температура", "°C", "thermo", "36.6", validate_temperature),
    ("Рост", "см", "ruler", "170", validate_height),
    ("Вес", "кг", "scale", "70", validate_weight),
]


def intensity_caption(v):
    if v == 0:
        return "не беспокоит"
    if v <= 3:
        return "слабо"
    if v <= 6:
        return "умеренно"
    if v <= 8:
        return "сильно"
    return "очень сильно"


def mood_color(title):
    return w.mood_of(title)[1]


# ============== ЛИЦА-НАСТРОЕНИЯ ==============
class MoodFace(QWidget):
    """Кружок-лицо, нарисованный кодом (не смайлик-шрифт): от грустного
    до улыбающегося. При наведении и выборе плавно увеличивается."""

    clicked = Signal()

    def __init__(self, score, title, size=86, show_title=True):
        super().__init__()
        self.score = score
        self.title = title
        self.color = QColor(mood_color(title))
        self.selected = False
        self.show_title = show_title
        self._grow = 0.0
        self._hover = False
        self.face = size
        self.setFixedSize(size + 24, size + (34 if show_title else 6))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(title)
        self._anim = QPropertyAnimation(self, b"grow", self)
        self._anim.setDuration(220)
        self._anim.setEasingCurve(QEasingCurve.Type.OutBack)

    def _get_grow(self):
        return self._grow

    def _set_grow(self, v):
        self._grow = v
        self.update()

    grow = Property(float, _get_grow, _set_grow)

    def _animate(self):
        target = 1.0 if self.selected else (0.5 if self._hover else 0.0)
        self._anim.stop()
        self._anim.setStartValue(self._grow)
        self._anim.setEndValue(target)
        self._anim.start()

    def set_selected(self, v):
        self.selected = v
        self._animate()

    def enterEvent(self, e):
        self._hover = True
        self._animate()

    def leaveEvent(self, e):
        self._hover = False
        self._animate()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def paintEvent(self, event):
        pl = w.pal()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx = self.width() / 2
        r = self.face / 2 * (0.82 + 0.18 * self._grow)
        cy = 4 + self.face / 2
        circle = QRectF(cx - r, cy - r, 2 * r, 2 * r)
        if self.selected:
            p.setPen(Qt.PenStyle.NoPen)
            glow = QColor(self.color)
            glow.setAlpha(50)
            p.setBrush(glow)
            p.drawEllipse(circle.adjusted(-5, -5, 5, 5))
            p.setBrush(self.color)
            feature = QColor("#FFFFFF")
        else:
            soft = QColor(self.color)
            soft.setAlpha(int(30 + 40 * self._grow))
            p.setBrush(soft)
            p.setPen(QPen(self.color, 2))
            feature = self.color.darker(115)
        p.drawEllipse(circle)

        # глаза
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(feature)
        eye_r = r * 0.09
        for dx in (-0.32, 0.32):
            p.drawEllipse(QPointF(cx + dx * r, cy - 0.18 * r), eye_r, eye_r * (0.6 if self.score == 5 else 1))
        # брови у «плохо» и «очень плохо»
        pen = QPen(feature, max(2.0, r * 0.08), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        if self.score <= 2:
            tilt = 0.12 if self.score == 1 else 0.06
            p.drawLine(QPointF(cx - 0.46 * r, cy - (0.38 - tilt) * r), QPointF(cx - 0.18 * r, cy - 0.42 * r))
            p.drawLine(QPointF(cx + 0.46 * r, cy - (0.38 - tilt) * r), QPointF(cx + 0.18 * r, cy - 0.42 * r))
        # рот: кривизна от улыбки (5) до грусти (1)
        bend = (self.score - 3) * 0.2 * r
        y = cy + 0.3 * r - (bend * 0.3)
        mouth = QPainterPath(QPointF(cx - 0.4 * r, y))
        mouth.quadTo(QPointF(cx, y + bend), QPointF(cx + 0.4 * r, y))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(mouth)

        if self.show_title:
            f = QFont(w.FONT, 9)
            f.setBold(self.selected)
            p.setFont(f)
            p.setPen(QColor(pl["text"] if self.selected else pl["muted"]))
            p.drawText(QRectF(0, self.face + 8, self.width(), 24), Qt.AlignmentFlag.AlignCenter,
                       self.title if len(self.title) < 12 else "Удовл.")


class MoodPicker(QWidget):
    changed = Signal(str)

    def __init__(self, size=86, show_title=True):
        super().__init__()
        self._value = None
        self.faces = []
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        for score, title in MOODS:
            face = MoodFace(score, title, size, show_title)
            face.clicked.connect(lambda t=title: self.set_value(t, emit=True))
            lay.addWidget(face)
        self.faces = [lay.itemAt(i).widget() for i in range(lay.count())]
        lay.addStretch()

    def value(self):
        return self._value

    def set_value(self, title, emit=False):
        self._value = title
        for f in self.faces:
            f.set_selected(f.title == title)
        if emit:
            self.changed.emit(title or "")


class IntensityPicker(QWidget):
    """Шкала 0–10 из делений: клик или перетаскивание мышью."""

    changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.value = 0
        self._hover = -1
        self.setFixedHeight(46)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _cell_at(self, x):
        n = 11
        cw = self.width() / n
        return max(0, min(10, int(x // cw)))

    def set_value(self, v):
        self.value = v
        self.update()
        self.changed.emit(v)

    def mousePressEvent(self, e):
        self.set_value(self._cell_at(e.position().x()))

    def mouseMoveEvent(self, e):
        i = self._cell_at(e.position().x())
        if e.buttons() & Qt.MouseButton.LeftButton:
            if i != self.value:
                self.set_value(i)
        if i != self._hover:
            self._hover = i
            self.update()

    def leaveEvent(self, e):
        self._hover = -1
        self.update()

    def paintEvent(self, event):
        pl = w.pal()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        n = 11
        gap = 5
        cw = (self.width() - gap * (n - 1)) / n
        light, dark = QColor(pl["accent_light"]), QColor(pl["accent_hover"])
        p.setFont(QFont(w.FONT, 9, QFont.Weight.DemiBold))
        for i in range(n):
            rect = QRectF(i * (cw + gap), 0, cw, self.height())
            active = i <= self.value and self.value > 0 and i > 0
            if active:
                color = w._mix(light, dark, i / 10)
            elif i == 0 and self.value == 0:
                color = QColor(pl["accent_soft"])
            else:
                color = QColor(pl["card_alt"])
            p.setPen(QPen(QColor(pl["accent"]), 2) if i == self._hover else Qt.PenStyle.NoPen)
            p.setBrush(color)
            p.drawRoundedRect(rect, 10, 10)
            p.setPen(QColor("#FFFFFF") if active else QColor(pl["muted"]))
            p.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(i))


class ToggleChip(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        pl = w.pal()
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(36)
        self.setFont(QFont(w.FONT, 10))
        self.setStyleSheet(f"""
            QPushButton {{ background: {pl['card']}; color: {pl['text']}; border: 1px solid {pl['line']};
                border-radius: 18px; padding: 4px 16px; }}
            QPushButton:hover {{ border-color: {pl['accent']}; color: {pl['accent']}; }}
            QPushButton:checked {{ background: {pl['accent']}; color: white; border-color: {pl['accent']}; }}
        """)


class IndicatorTile(QFrame):
    """Плитка показателя: иконка, название, поле ввода и единица измерения."""

    def __init__(self, name, unit, icon, hint):
        super().__init__()
        pl = w.pal()
        self.name = name
        self.unit = unit
        self.setObjectName("indicator")
        self.setFixedWidth(196)
        self._style(False)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(6)
        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(w.Icon(icon, 30, pl["accent"], pl["accent_soft"], 9))
        head.addWidget(w.label(name, 10, bold=True), 1)
        lay.addLayout(head)
        row = QHBoxLayout()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(hint)
        self.edit.setFont(QFont(w.FONT, 12, QFont.Weight.DemiBold))
        self.edit.textChanged.connect(lambda _: self.set_error(""))
        row.addWidget(self.edit, 1)
        row.addWidget(w.label(unit, 9, color=pl["muted"]))
        lay.addLayout(row)
        self.error = w.label("", 8, color=pl["danger"], wrap=True)
        self.error.hide()
        lay.addWidget(self.error)

    def _style(self, bad):
        pl = w.pal()
        border = pl["danger"] if bad else pl["line"]
        self.setStyleSheet(f"QFrame#indicator {{ background: {pl['card']}; border: 1px solid {border};"
                           f" border-radius: 14px; }}")

    def set_error(self, text):
        self.error.setText(text)
        self.error.setVisible(bool(text))
        self._style(bool(text))

    def text(self):
        return self.edit.text().strip()


class ReminderDialog(QDialog):
    """Напоминание о приёме лекарства — в стиле приложения, без смайликов."""

    def __init__(self, parent, name_med, form, dose, time_text, instructions):
        super().__init__(parent)
        pl = w.pal()
        self.setWindowTitle("Напоминание о приёме")
        self.setMinimumWidth(420)
        self.setStyleSheet(f"QDialog {{ background: {pl['bg']}; }}")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 24, 26, 22)
        lay.setSpacing(10)
        head = QHBoxLayout()
        head.setSpacing(14)
        pill = w.PillIcon(form, name_med, 72)
        head.addWidget(pill)
        QTimer.singleShot(250, pill.wobble)
        col = QVBoxLayout()
        col.addWidget(w.label("Время принять лекарство", 9, bold=True, color=pl["accent"]))
        col.addWidget(w.label(name_med, 15, bold=True, wrap=True))
        col.addWidget(w.label(f"{dose} · в {time_text}", 10, color=pl["muted"]))
        head.addLayout(col, 1)
        lay.addLayout(head)
        if instructions:
            note = w.label(instructions, 10, wrap=True)
            note.setStyleSheet(note.styleSheet() + f"border-left: 3px solid {pl['accent_light']}; padding-left: 8px;")
            lay.addWidget(note)
        ok = w.primary_button("Хорошо")
        ok.clicked.connect(self.accept)
        lay.addSpacing(6)
        lay.addWidget(ok)


def section(number, title, subtitle=""):
    """Заголовок шага в дневнике: номер в кружке + вопрос."""
    pl = w.pal()
    row = QHBoxLayout()
    row.setSpacing(12)
    badge = QLabel(str(number))
    badge.setFixedSize(30, 30)
    badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
    badge.setFont(QFont(w.FONT, 10, QFont.Weight.Bold))
    badge.setStyleSheet(f"background: {pl['accent']}; color: white; border-radius: 15px;")
    row.addWidget(badge)
    col = QVBoxLayout()
    col.setSpacing(0)
    col.addWidget(w.label(title, 12, bold=True))
    if subtitle:
        col.addWidget(w.label(subtitle, 9, color=pl["muted"]))
    row.addLayout(col, 1)
    return row


# ============== ОКНО ПАЦИЕНТА ==============
class PatientWindow(QMainWindow):
    def __init__(self, user_data, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.id_user = user_data["id_user"]
        self.full_name = user_data["full_name"]

        patient = db.get_patient_by_user(self.id_user)
        if not patient:
            mb.critical(self, "Ошибка", "Профиль пациента не найден")
            self.close()
            return
        self.id_patient = patient[0]

        pl = w.pal()
        self.setWindowTitle("Дневник терапии — личный кабинет")
        self.resize(1360, 900)
        self.setMinimumSize(1120, 740)
        central = QWidget()
        central.setObjectName("patRoot")
        central.setStyleSheet(f"QWidget#patRoot {{ background: {pl['bg']}; }}" + w.input_qss())
        self.setCentralWidget(central)

        self.load_data()

        root = QVBoxLayout(central)
        root.setContentsMargins(26, 18, 26, 14)
        root.setSpacing(14)
        root.addLayout(self._build_header())

        self.tabs = w.FolderTabs()
        self.tabs.add_tab(self._build_today(), "Сегодня", "calendar", TAB_COLORS[0])
        self.tabs.add_tab(self._build_diary(), "Дневник", "note", TAB_COLORS[1])
        self.tabs.add_tab(self._build_history(), "История", "book", TAB_COLORS[2])
        self.tabs.add_tab(self._build_prescriptions(), "Назначения", "pill", TAB_COLORS[3])
        self.tabs.add_tab(self._build_profile(), "Профиль", "user", TAB_COLORS[4])
        self.tabs.currentChanged.connect(lambda _: self.panel.close_panel())
        root.addWidget(self.tabs, 1)
        self.panel = w.SidePanel(central)

        QShortcut(QKeySequence("F1"), self, lambda: self.tabs.set_current(4))
        QShortcut(QKeySequence("Ctrl+Q"), self, self.on_logout)
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_diary)
        for i in range(5):
            QShortcut(QKeySequence(f"Ctrl+{i + 1}"), self, lambda i=i: self.tabs.set_current(i))

        self.render_all()

        # === ТАЙМЕР НАПОМИНАНИЙ (логика прежняя: проверка раз в 30 секунд) ===
        self._notified_today = set()
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(30_000)
        QTimer.singleShot(2000, self.check_reminders)
        # Обновляем «следующий приём через …» раз в минуту
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._render_today_doses)
        self.clock_timer.start(60_000)

    # ---------- данные ----------
    def load_data(self):
        self.me = next((p for p in db.get_patients_crm() if p["id_patient"] == self.id_patient), {})
        self.doctor = db.get_doctor_crm(self.me["id_doctor"]) if self.me.get("id_doctor") else None
        self.entries = db.get_diary_full(self.id_patient)
        self.rx = db.get_prescriptions_full(self.id_patient)
        self.today = db.get_today_schedule_full(self.id_patient)

    def render_all(self):
        self._render_today_doses()
        self._render_today_side()
        self._render_history()
        self._render_rx()

    # ---------- шапка ----------
    def _build_header(self):
        pl = w.pal()
        row = QHBoxLayout()
        row.setSpacing(14)
        logo = QLabel("ДТ")
        logo.setFixedSize(44, 44)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont(w.FONT, 13, QFont.Weight.Bold))
        logo.setStyleSheet("color: white; border-radius: 13px;"
                           "background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #2F5C8F, stop:1 #163257);")
        row.addWidget(logo)
        hour = datetime.now().hour
        greeting = ("Доброе утро" if 5 <= hour < 12 else "Добрый день" if hour < 18
        else "Добрый вечер" if hour < 23 else "Доброй ночи")
        parts = self.full_name.split()
        # Раньше бралось первое слово — то есть фамилия; обращаемся по имени
        name = parts[1] if len(parts) > 1 else self.full_name
        col = QVBoxLayout()
        col.setSpacing(0)
        col.addWidget(w.label(f"{greeting}, {name}!", 15, bold=True))
        col.addWidget(w.label("Личный кабинет · Дневник терапии", 9, color=pl["muted"]))
        row.addLayout(col)
        row.addStretch()

        new_entry = w.primary_button("+  Запись в дневник")
        new_entry.clicked.connect(lambda: self.tabs.set_current(1))
        row.addWidget(new_entry)

        if self.doctor:
            btn = QPushButton()
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip("Мой лечащий врач")
            btn.setMinimumHeight(56)
            btn.setStyleSheet(f"""
                QPushButton {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 28px; }}
                QPushButton:hover {{ border-color: {pl['accent']}; }}
            """)
            lay = QHBoxLayout(btn)
            lay.setContentsMargins(5, 4, 16, 4)
            lay.setSpacing(10)
            lay.addWidget(w.Avatar(self.doctor["full_name"], 46, w.doctor_photo_path(self.doctor["photo"]),
                                   ring=pl["accent"]))
            dc = QVBoxLayout()
            dc.setSpacing(0)
            dc.addWidget(w.label("Мой врач", 8, color=pl["muted"]))
            dc.addWidget(w.label(w.short_name(self.doctor["full_name"]), 10, bold=True))
            lay.addLayout(dc)
            btn.setMinimumWidth(120 + btn.fontMetrics().horizontalAdvance(w.short_name(self.doctor["full_name"])))
            btn.clicked.connect(self.open_doctor)
            row.addWidget(btn)

        logout = w.ghost_button("Выйти")
        logout.setToolTip("Ctrl+Q")
        logout.clicked.connect(self.on_logout)
        row.addWidget(logout)
        return row

    # ---------- вкладка «Сегодня» ----------
    def _build_today(self):
        page = QWidget()
        lay = QHBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(18)

        doses = w.AnimatedCard(clickable=False)
        head = QHBoxLayout()
        head.addWidget(w.Icon("bell", 40, w.pal()["accent"], w.pal()["accent_soft"], 12))
        hc = QVBoxLayout()
        hc.setSpacing(0)
        hc.addWidget(w.label("Приёмы лекарств на сегодня", 13, bold=True))
        hc.addWidget(w.label(human_date(date.today()).capitalize(), 9, color=w.pal()["muted"]))
        head.addLayout(hc, 1)
        doses.body_layout.addLayout(head)
        self.doses_inner = QWidget()
        self.doses_inner.setStyleSheet("background: transparent;")
        self.doses_layout = QVBoxLayout(self.doses_inner)
        self.doses_layout.setContentsMargins(0, 8, 6, 0)
        self.doses_layout.setSpacing(0)
        doses.body_layout.addWidget(w.make_scroll(self.doses_inner), 1)
        lay.addWidget(doses, 3)

        side_inner = QWidget()
        side_inner.setStyleSheet("background: transparent;")
        self.side_layout = QVBoxLayout(side_inner)
        self.side_layout.setContentsMargins(0, 0, 6, 0)
        self.side_layout.setSpacing(4)
        side = w.make_scroll(side_inner)
        side.setFixedWidth(470)
        lay.addWidget(side)
        return page

    def _render_today_doses(self):
        pl = w.pal()
        while self.doses_layout.count():
            item = self.doses_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        if not self.today:
            empty = QVBoxLayout()
            box = QWidget()
            box.setLayout(empty)
            empty.addSpacing(40)
            icon = w.Icon("check", 64, pl["accent"], pl["accent_soft"], 32)
            empty.addWidget(icon, 0, Qt.AlignmentFlag.AlignHCenter)
            msg = w.label("На сегодня приёмов нет", 12, bold=True)
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.addWidget(msg)
            sub = w.label("Когда врач назначит лекарство с временем приёма, оно появится здесь", 9,
                          color=pl["muted"], wrap=True)
            sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.addWidget(sub)
            self.doses_layout.addWidget(box)
            self.doses_layout.addStretch()
            return

        now = datetime.now()
        now_min = now.hour * 60 + now.minute
        next_idx = None
        for i, s in enumerate(self.today):
            t = s["time_of_day"]
            minutes = t.seconds // 60 if hasattr(t, "seconds") else t.hour * 60 + t.minute
            s["_min"] = minutes
            if next_idx is None and minutes >= now_min:
                next_idx = i

        for i, s in enumerate(self.today):
            past = s["_min"] < now_min
            is_next = i == next_idx
            row = QHBoxLayout()
            row.setSpacing(14)
            # время слева, карточка приёма справа
            tl = w.label(time_str(s["time_of_day"]), 13, bold=True,
                         color=pl["muted"] if past else (pl["accent"] if is_next else pl["text"]))
            tl.setFixedWidth(64)
            row.addWidget(tl, 0, Qt.AlignmentFlag.AlignTop)

            card = QFrame()
            card.setObjectName("doseCard")
            border = pl["accent"] if is_next else pl["line"]
            bg = pl["accent_soft"] if is_next else (pl["card_alt"] if past else pl["card"])
            card.setStyleSheet(f"QFrame#doseCard {{ background: {bg}; border: {2 if is_next else 1}px solid {border};"
                               f" border-radius: 14px; }}")
            cl = QHBoxLayout(card)
            cl.setContentsMargins(12, 10, 14, 10)
            cl.setSpacing(12)
            pill = w.PillIcon(s["form"], s["name_med"], 50)
            cl.addWidget(pill)
            info = QVBoxLayout()
            info.setSpacing(1)
            info.addWidget(w.label(s["name_med"], 11, bold=True, color=pl["muted"] if past else pl["text"]))
            info.addWidget(w.label(" · ".join(x for x in (s["dose"], s["instructions"]) if x), 9,
                                   color=pl["muted"], wrap=True))
            cl.addLayout(info, 1)
            if past:
                cl.addWidget(w.chip("прошло", pl["card"], pl["muted"]))
            elif is_next:
                left = s["_min"] - now_min
                when = "сейчас" if left <= 1 else (
                    f"через {left} мин" if left < 60 else f"через {left // 60} ч {left % 60:02d} мин")
                cl.addWidget(w.chip(f"следующий · {when}", pl["accent"]))
                QTimer.singleShot(400, pill.wobble)
            else:
                cl.addWidget(w.chip("позже", pl["card_alt"], pl["accent"]))
            row.addWidget(card, 1)
            holder = QWidget()
            holder.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
            holder.setLayout(row)
            holder.setStyleSheet("background: transparent;")
            self.doses_layout.addWidget(holder)
            self.doses_layout.addSpacing(10)
        self.doses_layout.addStretch()

    def _render_today_side(self):
        pl = w.pal()
        while self.side_layout.count():
            item = self.side_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Как вы сегодня?
        mood_card = w.AnimatedCard(clickable=False)
        today_entries = [e for e in self.entries if e["entry_date"] == date.today()]
        mood_card.body_layout.addWidget(w.label("Как вы себя чувствуете?", 12, bold=True))
        if today_entries:
            title, color = w.mood_of(today_entries[0]["well_being_text"])
            r = QHBoxLayout()
            r.addWidget(w.label(f"Сегодня уже есть запись · {time_str(today_entries[0]['entry_time'])}", 9,
                                color=pl["muted"]))
            r.addStretch()
            r.addWidget(w.chip(title, color))
            mood_card.body_layout.addLayout(r)
        else:
            mood_card.body_layout.addWidget(
                w.label("Отметьте самочувствие — откроется дневник", 9, color=pl["muted"]))
        quick = MoodPicker(size=52, show_title=False)
        quick.changed.connect(self._quick_mood)
        mood_card.body_layout.addWidget(quick)
        self.side_layout.addWidget(mood_card)

        # Мой врач
        if self.doctor:
            d = self.doctor
            doc = w.AnimatedCard()
            doc.clicked.connect(self.open_doctor)
            r = QHBoxLayout()
            r.setSpacing(14)
            r.addWidget(w.Avatar(d["full_name"], 92, w.doctor_photo_path(d["photo"]), shape="rounded", height=104))
            c = QVBoxLayout()
            c.setSpacing(3)
            c.addWidget(w.label("Мой лечащий врач", 8, bold=True, color=pl["muted"]))
            c.addWidget(w.label(d["full_name"], 11, bold=True, wrap=True))
            c.addWidget(w.chip(d["specialty"] or "врач", pl["accent"]))
            place = " · ".join(x for x in (f"каб. {d['office']}" if d["office"] else "", d["schedule"] or "") if x)
            if place:
                c.addWidget(w.label(place, 9, color=pl["muted"], wrap=True))
            r.addLayout(c, 1)
            doc.body_layout.addLayout(r)
            self.side_layout.addWidget(doc)
        else:
            nod = w.AnimatedCard(clickable=False)
            nod.body_layout.addWidget(w.label("Лечащий врач пока не назначен", 10, bold=True))
            nod.body_layout.addWidget(w.label("Обратитесь в регистратуру клиники", 9, color=pl["muted"]))
            self.side_layout.addWidget(nod)

        # Динамика
        trend = w.AnimatedCard(clickable=False)
        trend.body_layout.addWidget(w.label("Моё самочувствие", 12, bold=True))
        trend.body_layout.addWidget(MoodTrend(self.entries, 120))
        self.side_layout.addWidget(trend)
        self.side_layout.addStretch()
        for i in range(self.side_layout.count()):
            wd = self.side_layout.itemAt(i).widget()
            if isinstance(wd, w.AnimatedCard):
                wd.appear(i * 80)

    def _quick_mood(self, title):
        self.mood.set_value(title)
        self.tabs.set_current(1)

    # ---------- вкладка «Дневник» ----------
    def _build_diary(self):
        pl = w.pal()
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)

        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        col = QVBoxLayout(inner)
        col.setContentsMargins(0, 0, 8, 0)
        col.setSpacing(4)

        # 1. самочувствие
        c1 = w.AnimatedCard(clickable=False)
        c1.body_layout.addLayout(section(1, "Как вы себя чувствуете?", "Выберите одно"))
        self.mood = MoodPicker()
        c1.body_layout.addWidget(self.mood)
        col.addWidget(c1)

        # 2. интенсивность
        c2 = w.AnimatedCard(clickable=False)
        c2.body_layout.addLayout(section(2, "Насколько сильно беспокоят симптомы?", "0 — совсем не беспокоят"))
        self.intensity = IntensityPicker()
        self.intensity_caption = w.label("0 — не беспокоит", 10, bold=True, color=pl["accent"])
        self.intensity.changed.connect(
            lambda v: self.intensity_caption.setText(f"{v} — {intensity_caption(v)}"))
        c2.body_layout.addWidget(self.intensity)
        c2.body_layout.addWidget(self.intensity_caption)
        col.addWidget(c2)

        # 3. симптомы
        c3 = w.AnimatedCard(clickable=False)
        c3.body_layout.addLayout(section(3, "Что беспокоит?", "Можно выбрать несколько"))
        self.symptom_chips = self._chip_box(SYMPTOMS, c3)
        col.addWidget(c3)

        # 4. триггеры
        c4 = w.AnimatedCard(clickable=False)
        c4.body_layout.addLayout(section(4, "Что могло повлиять?", "Помогает врачу найти причину"))
        self.trigger_chips = self._chip_box(TRIGGERS, c4)
        col.addWidget(c4)

        # 5. показатели
        c5 = w.AnimatedCard(clickable=False)
        c5.body_layout.addLayout(section(5, "Показатели", "Заполните то, что измеряли"))
        box = QWidget()
        box.setStyleSheet("background: transparent;")
        flow = w.FlowLayout(box, spacing=10)
        flow.setContentsMargins(0, 4, 0, 0)
        self.indicator_tiles = []
        for name, unit, icon, hint, _ in INDICATORS:
            tile = IndicatorTile(name, unit, icon, hint)
            flow.addWidget(tile)
            self.indicator_tiles.append(tile)
        c5.body_layout.addWidget(box)
        col.addWidget(c5)

        # 6. заметка
        c6 = w.AnimatedCard(clickable=False)
        c6.body_layout.addLayout(section(6, "Заметка", "Что ещё важно рассказать врачу"))
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Например: давило в затылке после работы, прошло после отдыха")
        self.notes.setFixedHeight(90)
        c6.body_layout.addWidget(self.notes)
        col.addWidget(c6)
        col.addStretch()
        self._diary_cards = [c1, c2, c3, c4, c5, c6]
        outer.addWidget(w.make_scroll(inner), 1)

        bar = QHBoxLayout()
        bar.addWidget(w.label("Ctrl+S — сохранить", 9, color=pl["muted"]))
        bar.addStretch()
        clear = w.ghost_button("Очистить")
        clear.clicked.connect(self.clear_diary)
        save = w.primary_button("Сохранить запись")
        save.setMinimumWidth(220)
        save.clicked.connect(self.save_diary)
        bar.addWidget(clear)
        bar.addWidget(save)
        outer.addLayout(bar)
        return page

    def _chip_box(self, items, card):
        box = QWidget()
        box.setStyleSheet("background: transparent;")
        flow = w.FlowLayout(box, spacing=8)
        flow.setContentsMargins(0, 4, 0, 0)
        chips = []
        for text in items:
            chip = ToggleChip(text)
            flow.addWidget(chip)
            chips.append(chip)
        card.body_layout.addWidget(box)
        return chips

    # ---------- вкладка «История» ----------
    def _build_history(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        bar = QHBoxLayout()
        self.history_count = w.label("", 11, bold=True)
        bar.addWidget(self.history_count)
        bar.addStretch()
        self.history_filter = w.SegmentedFilter([("all", "Все"), ("week", "За неделю"), ("month", "За месяц"),
                                                 ("doctor", "С ответом врача")])
        self.history_filter.changed.connect(self._render_history)
        bar.addWidget(self.history_filter)
        lay.addLayout(bar)
        self.history_inner = QWidget()
        self.history_inner.setStyleSheet("background: transparent;")
        self.history_layout = QVBoxLayout(self.history_inner)
        self.history_layout.setContentsMargins(0, 0, 8, 0)
        self.history_layout.setSpacing(4)
        lay.addWidget(w.make_scroll(self.history_inner), 1)
        return page

    def _render_history(self, *_):
        pl = w.pal()
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        mode = self.history_filter.value()
        border = {"week": 7, "month": 31}.get(mode)
        entries = []
        for e in self.entries:
            if border and e["entry_date"] < date.today() - timedelta(days=border - 1):
                continue
            if mode == "doctor" and not (e["disease_code"] or e["doctor_diagnosis"] or e["comments"]):
                continue
            entries.append(e)
        self.history_count.setText(w.plural(len(entries), "запись", "записи", "записей"))

        trend = w.AnimatedCard(clickable=False)
        trend.body_layout.addWidget(w.label("Динамика самочувствия", 11, bold=True))
        trend.body_layout.addWidget(MoodTrend(entries, 120))
        self.history_layout.addWidget(trend)
        trend.appear(0)
        if not entries:
            self.history_layout.addWidget(w.label("Записей нет — заполните дневник на вкладке «Дневник»", 10,
                                                  color=pl["muted"]))
        for i, e in enumerate(entries):
            card = DiaryCard(e)
            self.history_layout.addWidget(card)
            card.appear(60 + min(i, 10) * 50)
        self.history_layout.addStretch()

    # ---------- вкладка «Назначения» ----------
    def _build_prescriptions(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        bar = QHBoxLayout()
        bar.addWidget(w.label("Мои назначения", 13, bold=True))
        bar.addStretch()
        self.rx_filter = w.SegmentedFilter([("active", "Принимаю сейчас"), ("completed", "Завершённые"),
                                            ("all", "Все")])
        self.rx_filter.changed.connect(self._render_rx)
        bar.addWidget(self.rx_filter)
        lay.addLayout(bar)
        self.rx_grid = w.CardGrid("Назначений нет")
        lay.addWidget(self.rx_grid, 1)
        return page

    def _render_rx(self, *_):
        mode = self.rx_filter.value()
        cards = []
        for r in self.rx:
            if mode != "all" and r["status"] != mode:
                continue
            card = RxCard(r)
            card.clicked.connect(lambda r=r: self.open_prescription(r))
            cards.append(card)
        self.rx_grid.set_cards(cards)

    # ---------- вкладка «Профиль» ----------
    def _build_profile(self):
        pl = w.pal()
        p = self.me
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        flow = w.FlowLayout(inner, spacing=12)

        me = w.AnimatedCard(width=420, clickable=False)
        head = QHBoxLayout()
        head.setSpacing(14)
        head.addWidget(w.Avatar(self.full_name, 84, ring=pl["accent"]))
        hc = QVBoxLayout()
        hc.addWidget(w.label(self.full_name, 14, bold=True, wrap=True))
        hc.addWidget(w.label(common.patient_meta(p.get("birth_date"), p.get("gender")), 9, color=pl["muted"]))
        head.addLayout(hc, 1)
        me.body_layout.addLayout(head)
        me.body_layout.addWidget(w.info_block([
            ("Дата рождения", common.fmt_date(p.get("birth_date"))),
            ("Пол", p.get("gender") or "не указан"),
            ("Полис ОМС", p.get("policy_number")),
            ("Телефон", p.get("phone")),
            ("Логин", p.get("login")),
        ]))

        # --- НОВАЯ КНОПКА СМЕНЫ ПАРОЛЯ ---
        change_pass_btn = w.ghost_button("Сменить пароль")
        change_pass_btn.clicked.connect(self.open_change_password)
        me.body_layout.addWidget(change_pass_btn)
        # ---------------------------------

        me.body_layout.addWidget(w.label("Чтобы изменить данные, обратитесь к врачу или администратору.", 8,
                                         color=pl["muted"], wrap=True))
        flow.addWidget(me)

        if self.doctor:
            d = self.doctor
            doc = w.AnimatedCard(width=420, clickable=False)
            doc.body_layout.addWidget(w.label("Мой лечащий врач", 11, bold=True))
            r = QHBoxLayout()
            r.setSpacing(14)
            r.addWidget(w.Avatar(d["full_name"], 130, w.doctor_photo_path(d["photo"]), shape="rounded", height=150))
            c = QVBoxLayout()
            c.addWidget(w.label(d["full_name"], 12, bold=True, wrap=True))
            c.addWidget(w.chip(d["specialty"] or "врач", pl["accent"]))
            for cap, val in (("Кабинет", d["office"]), ("Приём", d["schedule"]), ("Телефон", d["phone"]),
                             ("E-mail", d["email"])):
                if val:
                    c.addWidget(w.label(f"{cap}: {val}", 9, color=pl["muted"], wrap=True))
            c.addStretch()
            r.addLayout(c, 1)
            doc.body_layout.addLayout(r)
            flow.addWidget(doc)

        help_card = w.AnimatedCard(width=420, clickable=False)
        help_card.body_layout.addWidget(w.label("Как пользоваться", 11, bold=True))
        for icon, text in (
                ("calendar", "«Сегодня» — какие лекарства и во сколько принять. В назначенное время "
                             "появится напоминание."),
                ("note",
                 "«Дневник» — отметьте самочувствие, симптомы и показатели. Достаточно выбрать лицо-настроение."),
                ("book", "«История» — ваши записи, диагнозы и комментарии врача."),
                ("pill", "«Назначения» — все препараты и ход курса."),
        ):
            r = QHBoxLayout()
            r.setSpacing(10)
            r.addWidget(w.Icon(icon, 30, pl["accent"], pl["accent_soft"], 9), 0, Qt.AlignmentFlag.AlignTop)
            r.addWidget(w.label(text, 9, color=pl["muted"], wrap=True), 1)
            help_card.body_layout.addLayout(r)
        help_card.body_layout.addWidget(w.label("Ctrl+1…5 — вкладки · Ctrl+S — сохранить запись · Ctrl+Q — выйти",
                                                8, bold=True, color=pl["accent"], wrap=True))
        flow.addWidget(help_card)
        return w.make_scroll(inner)

    # ---------- дневник: сохранение ----------
    def clear_diary(self):
        self.mood.set_value(None)
        self.intensity.set_value(0)
        for chip in self.symptom_chips + self.trigger_chips:
            chip.setChecked(False)
        for tile in self.indicator_tiles:
            tile.edit.clear()
            tile.set_error("")
        self.notes.clear()

    def save_diary(self):
        if self.tabs.bar.current() != 1:
            return
        well_being = self.mood.value()
        if not well_being:
            mb.warning(self, "Самочувствие", "Выберите, как вы себя чувствуете (шаг 1).")
            return
        intensity = self.intensity.value
        symptoms = [c.text() for c in self.symptom_chips if c.isChecked()]
        triggers = [c.text() for c in self.trigger_chips if c.isChecked()]
        notes = self.notes.toPlainText().strip()

        # === ВАЛИДАЦИЯ показателей: ошибка подсвечивается прямо в плитке ===
        values = {}
        bad = False
        for tile, (name, unit, _, _, check) in zip(self.indicator_tiles, INDICATORS):
            ok, err = check(tile.text())
            if not ok:
                tile.set_error(err)
                bad = True
            values[name] = (tile.text(), unit)
        if bad:
            mb.warning(self, "Проверьте показатели", "Некоторые показатели заполнены неверно — они выделены красным.")
            return

        # === Тот же формат, что и раньше (его разбирает окно врача) ===
        parts = [well_being]
        if intensity > 0:
            parts.append(f"интенсивность: {intensity}/10")
        if triggers:
            parts.append("триггеры: " + ", ".join(triggers))
        if notes:
            parts.append("заметки: " + notes)
        well_being_text = ". ".join(parts)
        symptoms_text = ", ".join(symptoms) if symptoms else "нет"

        today = date.today().strftime("%Y-%m-%d")
        now = QTime.currentTime().toString("HH:mm:ss")
        id_diary = db.create_diary_entry(self.id_patient, today, now, well_being_text, symptoms_text)
        if not id_diary:
            mb.critical(self, "Ошибка", "Не удалось сохранить запись")
            return
        for name, (value, unit) in values.items():
            if value:
                db.create_health_indicator(id_diary, name, value, unit)

        self.clear_diary()
        self.load_data()
        self.render_all()
        self.history_filter.set_value("all")
        self.tabs.set_current(2)
        mb.info(self, "Готово", "Запись сохранена. Врач увидит её в своём кабинете.")

    # ---------- боковые панели ----------
    def open_doctor(self):
        if not self.doctor:
            return
        pl = w.pal()
        d = self.doctor
        self.panel.open_panel("Мой лечащий врач")
        lay = self.panel.content_layout
        lay.addWidget(w.Avatar(d["full_name"], 240, w.doctor_photo_path(d["photo"]), shape="rounded", height=260),
                      0, Qt.AlignmentFlag.AlignHCenter)
        lay.addWidget(w.label(d["full_name"], 15, bold=True, wrap=True))
        lay.addWidget(w.chip(d["specialty"] or "врач", pl["accent"]))
        lay.addWidget(w.info_block([
            ("Кабинет", d["office"]),
            ("График приёма", d["schedule"]),
            ("Телефон", d["phone"]),
            ("E-mail", d["email"]),
        ]))
        active = [r for r in self.rx if r["status"] == "active"]
        lay.addWidget(w.section_title(f"Назначил вам · {len(active)}"))
        for r in active:
            lay.addWidget(common.rx_row(r))
        lay.addStretch()

    def open_prescription(self, r):
        pl = w.pal()
        self.panel.open_panel("Назначение")
        lay = self.panel.content_layout
        head = QHBoxLayout()
        head.setSpacing(14)
        pill = w.PillIcon(r["form"], r["name_med"], 84)
        QTimer.singleShot(350, pill.wobble)
        head.addWidget(pill)
        c = QVBoxLayout()
        c.addWidget(w.label(r["name_med"], 15, bold=True, wrap=True))
        c.addWidget(w.label(f"{r['dosage']} · {r['form'] or ''}", 10, color=pl["muted"]))
        c.addWidget(common.status_chip(r["status"]))
        head.addLayout(c, 1)
        lay.addLayout(head)
        lay.addWidget(w.info_block([
            ("Как принимать", r["frequency"]),
            ("Время приёма", r["times"] or "по самочувствию"),
            ("Начало", common.fmt_date(r["start_date"])),
            ("Окончание", common.fmt_date(r["end_date"])),
            ("Назначил", w.short_name(r["doctor_name"])),
        ]))
        if r["comment"]:
            lay.addWidget(w.section_title("Рекомендация врача"))
            lay.addWidget(w.label(r["comment"], 11, wrap=True))
        lay.addStretch()

    # ---------- смена пароля ----------
    def open_change_password(self):
        dlg = common.ChangePasswordDialog(self, self.id_user)
        dlg.exec()

    # ---------- напоминания ----------
    def check_reminders(self):
        """Проверяет, не пора ли принять лекарство, и показывает уведомление."""
        try:
            schedules = db.get_today_schedule_full(self.id_patient)
        except Exception as e:
            logging.error(f"Ошибка получения расписания: {e}")
            return
        now = QTime.currentTime()
        today_str = date.today().isoformat()
        for s in schedules:
            t = s["time_of_day"]
            key = f"{s['id_prescription']}_{t}_{today_str}"
            if key in self._notified_today:
                continue
            # TIME из MySQL может прийти как timedelta или как time
            try:
                if hasattr(t, "seconds"):
                    h, m = t.seconds // 3600, (t.seconds % 3600) // 60
                else:
                    h, m = t.hour, t.minute
            except Exception:
                continue
            diff = now.secsTo(QTime(h, m)) / 60.0
            if -1 <= diff <= 1:
                self._notified_today.add(key)
                ReminderDialog(self, s["name_med"], s["form"], s["dose"] or "", f"{h:02d}:{m:02d}",
                               s["instructions"] or "").exec()

    def on_logout(self):
        if self.login_window:
            self.login_window.return_from_child()
        self.close()