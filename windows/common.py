"""Общие для окон администратора и врача части: диалоги, фото врача,
строка назначения с иконкой препарата, форматирование дат и возраста."""

import os
import time
from datetime import date

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import db
from path import resource_path
from windows import msgbox as mb
from windows import widgets as w

MED_FORMS = ["таблетки", "капсулы", "раствор", "сироп", "капли", "аэрозоль", "гель", "мазь"]


# ============== ДАТЫ И ВОЗРАСТ ==============
def age(birth):
    if not birth:
        return None
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def years(n):
    return w.plural(n, "год", "года", "лет")


def fmt_date(d):
    return d.strftime("%d.%m.%Y") if d else "—"


def patient_meta(birth, gender):
    """'72 года · мужской' для подписи под ФИО."""
    a = age(birth)
    parts = [years(a) if a is not None else "", gender or ""]
    return " · ".join(x for x in parts if x) or "данные не заполнены"


# ============== ФОТО ВРАЧА ==============
def save_doctor_photo(id_doctor, src_path, old_name=None):
    """Копирует фото в images/doctors, уменьшая до 600 px по большей стороне.
    Возвращает имя файла для поля doctors.photo."""
    pm = QPixmap(src_path)
    if pm.isNull():
        return old_name
    if max(pm.width(), pm.height()) > 600:
        pm = pm.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    folder = resource_path("images", "doctors")
    os.makedirs(folder, exist_ok=True)
    name = f"doctor_{id_doctor}_{int(time.time())}.jpg"
    if not pm.save(os.path.join(folder, name), "JPG", 90):
        return old_name
    remove_doctor_photo(old_name)
    return name


def remove_doctor_photo(name):
    if name:
        path = w.doctor_photo_path(name)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


# ============== НАЗНАЧЕНИЕ ==============
def rx_row(r):
    """Строка назначения для боковой панели: иконка препарата, доза, время, статус."""
    pl = w.pal()
    frame = QFrame()
    frame.setObjectName("rxRow")
    frame.setStyleSheet(
        f"QFrame#rxRow {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 14px; }}"
    )
    row = QHBoxLayout(frame)
    row.setContentsMargins(10, 10, 12, 10)
    row.setSpacing(12)
    row.addWidget(w.PillIcon(r["form"], r["name_med"], 48))
    col = QVBoxLayout()
    col.setSpacing(2)
    col.addWidget(w.label(f"{r['name_med']} · {r['dosage']}", 10, bold=True, wrap=True))
    details = r["frequency"] + (f" · в {r['times']}" if r.get("times") else "")
    col.addWidget(w.label(details, 9, color=pl["muted"], wrap=True))
    col.addWidget(w.label(f"{fmt_date(r['start_date'])} — {fmt_date(r['end_date'])}", 8, color=pl["muted"]))
    row.addLayout(col, 1)
    row.addWidget(status_chip(r["status"]))
    return frame


def status_chip(status):
    pl = w.pal()
    if status == "active":
        return w.chip("активно", pl["ok_soft"], pl["ok"])
    return w.chip("завершено", pl["card_alt"], pl["muted"])


# ============== ДИАЛОГИ ==============
class CredentialsDialog(QDialog):
    """Показ логина и пароля нового пользователя с кнопкой копирования."""

    def __init__(self, parent, login, password, title="Логин и пароль", note=""):
        super().__init__(parent)
        pl = w.pal()
        self.setWindowTitle(title)
        self.setMinimumWidth(440)
        self.setStyleSheet(f"QDialog {{ background: {pl['bg']}; }}" + w.input_qss())
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 24, 26, 22)
        lay.setSpacing(10)
        lay.addWidget(w.label(title, 14, bold=True))
        lay.addWidget(
            w.label(note or "Скопируйте данные и передайте пользователю.", 9, color=pl["muted"], wrap=True)
        )
        for caption, value in (("Логин", login), ("Пароль", password)):
            lay.addWidget(w.label(caption, 9, color=pl["muted"]))
            field = QLineEdit(value)
            field.setReadOnly(True)
            field.setFont(QFont("Consolas", 12))
            lay.addWidget(field)
        copy_btn = w.primary_button("Скопировать логин и пароль")

        def copy():
            QApplication.clipboard().setText(f"Логин: {login}\nПароль: {password}")
            copy_btn.setText("✓ Скопировано")
            QTimer.singleShot(1500, lambda: copy_btn.setText("Скопировать логин и пароль"))

        copy_btn.clicked.connect(copy)
        lay.addSpacing(6)
        lay.addWidget(copy_btn)
        close = w.ghost_button("Готово")
        close.clicked.connect(self.accept)
        lay.addWidget(close)


class NewMedicationDialog(QDialog):
    """Добавление препарата в справочник (вместо трёх QInputDialog подряд).
    Справа — живое превью иконки препарата по выбранной форме."""

    def __init__(self, parent, name=""):
        super().__init__(parent)
        pl = w.pal()
        self.id_medication = None
        self.setWindowTitle("Новый препарат")
        self.setMinimumWidth(460)
        self.setStyleSheet(f"QDialog {{ background: {pl['bg']}; }}" + w.input_qss())
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 22, 26, 22)
        lay.setSpacing(8)

        head = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.addWidget(w.label("Новый препарат", 15, bold=True))
        title_col.addWidget(w.label("Появится в справочнике у всех врачей", 9, color=pl["muted"]))
        head.addLayout(title_col, 1)
        self.preview = w.PillIcon("таблетки", name, 64)
        head.addWidget(self.preview)
        lay.addLayout(head)

        self.name = QLineEdit(name)
        self.name.setPlaceholderText("Например: Лизиноприл")
        self.form = QComboBox()
        self.form.setEditable(True)
        self.form.addItems(MED_FORMS)
        self.dosage = QLineEdit()
        self.dosage.setPlaceholderText("10 мг, 500 мг, 5 мл")
        for caption, field in (("Название", self.name), ("Форма выпуска", self.form), ("Дозировка", self.dosage)):
            lay.addWidget(w.label(caption, 9, color=pl["muted"]))
            lay.addWidget(field)

        self.form.currentTextChanged.connect(self._update_preview)
        self.name.textChanged.connect(self._update_preview)

        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel = w.ghost_button("Отмена")
        cancel.clicked.connect(self.reject)
        save = w.primary_button("Добавить")
        save.clicked.connect(self._save)
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        lay.addSpacing(8)
        lay.addLayout(buttons)

    def _update_preview(self, *_):
        self.preview.form = self.form.currentText().lower()
        self.preview.name = self.name.text()
        self.preview.update()
        self.preview.wobble()

    def _save(self):
        name = self.name.text().strip()
        if len(name) < 2:
            mb.warning(self, "Название", "Введите название препарата.")
            self.name.setFocus()
            return
        self.id_medication = db.create_medication(
            name, self.form.currentText().strip(), self.dosage.text().strip()
        )
        if not self.id_medication:
            mb.critical(self, "Ошибка", "Не удалось добавить препарат")
            return
        self.accept()


# ============== ДНЕВНИК И НАЗНАЧЕНИЯ (общие для врача и пациента) ==============
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля",
          "августа", "сентября", "октября", "ноября", "декабря"]
WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
# Самочувствие -> балл для графика динамики
MOOD_SCORE = {"Отлично": 5, "Хорошо": 4, "Удовлетворительно": 3, "Плохо": 2, "Очень плохо": 1}


def human_date(d):
    """2026-10-20 -> '20 октября, вт'"""
    return f"{d.day} {MONTHS[d.month - 1]}, {WEEKDAYS[d.weekday()]}"


def time_str(t):
    """TIME из MySQL приходит как timedelta — приводим к 'ЧЧ:ММ'."""
    if hasattr(t, "seconds"):
        return f"{t.seconds // 3600:02d}:{t.seconds % 3600 // 60:02d}"
    return str(t)[:5]


class ProgressBar(QWidget):
    """Тонкая скруглённая полоска (интенсивность симптомов, ход курса)."""

    def __init__(self, value, color=None, height=8):
        super().__init__()
        self.value = max(0.0, min(1.0, value))
        self.color = color or w.pal()["accent"]
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect())
        rad = r.height() / 2
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(w.pal()["accent_soft"]))
        p.drawRoundedRect(r, rad, rad)
        if self.value > 0:
            p.setBrush(QColor(self.color))
            p.drawRoundedRect(QRectF(r.x(), r.y(), max(r.height(), r.width() * self.value), r.height()), rad, rad)


class MoodTrend(QWidget):
    """Динамика самочувствия по записям дневника: линия от «очень плохо» до «отлично»,
    точки окрашены цветом самочувствия."""

    def __init__(self, entries, height=110):
        super().__init__()
        # записи приходят от новых к старым — разворачиваем
        self.points = []
        for e in reversed(entries[:20]):
            mood, color = w.mood_of(e["well_being_text"])
            if mood in MOOD_SCORE:
                self.points.append((e["entry_date"], MOOD_SCORE[mood], color))
        self.setMinimumHeight(height)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pl = w.pal()
        r = QRectF(self.rect()).adjusted(34, 10, -12, -20)
        p.setFont(QFont(w.FONT, 7))
        for score, name in ((5, "отл."), (3, "удовл."), (1, "оч. пл.")):
            y = r.bottom() - (score - 1) / 4 * r.height()
            p.setPen(QPen(QColor(pl["line"]), 1, Qt.PenStyle.DashLine))
            p.drawLine(QPointF(r.left(), y), QPointF(r.right(), y))
            p.setPen(QColor(pl["muted"]))
            p.drawText(QRectF(0, y - 7, 32, 14), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, name)
        if not self.points:
            p.setPen(QColor(pl["muted"]))
            p.setFont(QFont(w.FONT, 9))
            p.drawText(r, Qt.AlignmentFlag.AlignCenter, "Пока нет записей")
            return
        n = len(self.points)
        step = r.width() / max(1, n - 1)
        pts = [
            QPointF(r.left() + (i * step if n > 1 else r.width() / 2),
                    r.bottom() - (score - 1) / 4 * r.height())
            for i, (_, score, _) in enumerate(self.points)
        ]
        # заливка под линией
        if n > 1:
            area = QPainterPath(QPointF(pts[0].x(), r.bottom()))
            for pt in pts:
                area.lineTo(pt)
            area.lineTo(QPointF(pts[-1].x(), r.bottom()))
            fill = QColor(pl["accent"])
            fill.setAlpha(28)
            p.fillPath(area, fill)
            p.setPen(QPen(QColor(pl["accent"]), 2))
            for a, b in zip(pts, pts[1:]):
                p.drawLine(a, b)
        p.setFont(QFont(w.FONT, 7))
        for i, (pt, (d, _, color)) in enumerate(zip(pts, self.points)):
            p.setPen(QPen(QColor(pl["card"]), 2))
            p.setBrush(QColor(color))
            p.drawEllipse(pt, 5, 5)
            if i == 0 or i == n - 1 or n <= 8:
                p.setPen(QColor(pl["muted"]))
                p.drawText(QRectF(pt.x() - 24, r.bottom() + 4, 48, 14), Qt.AlignmentFlag.AlignCenter,
                           d.strftime("%d.%m"))


def soft_chip(text, outlined=False):
    pl = w.pal()
    lbl = QLabel(text)
    lbl.setFont(QFont(w.FONT, 9))
    border = f"1px solid {pl['line']}" if outlined else "none"
    bg = pl["card"] if outlined else pl["accent_soft"]
    lbl.setStyleSheet(
        f"background: {bg}; color: {pl['accent']}; border: {border}; border-radius: 10px; padding: 3px 10px;"
    )
    return lbl


def chips_row(texts, outlined=False):
    box = QWidget()
    box.setStyleSheet("background: transparent;")
    flow = w.FlowLayout(box, spacing=6)
    flow.setContentsMargins(0, 0, 0, 0)
    for t in texts:
        flow.addWidget(soft_chip(t, outlined))
    return box


class RxCard(w.AnimatedCard):
    """Карточка назначения: препарат, пациент, время приёма, ход курса."""

    def __init__(self, r):
        super().__init__(width=320)
        pl = w.pal()
        self.data = r
        top = QHBoxLayout()
        top.setSpacing(12)
        top.addWidget(w.PillIcon(r["form"], r["name_med"], 54), 0, Qt.AlignmentFlag.AlignTop)
        col = QVBoxLayout()
        col.setSpacing(1)
        col.addWidget(w.label(f"{r['name_med']} · {r['dosage']}", 10, bold=True, wrap=True))
        col.addWidget(w.label(r["form"] or "", 8, color=pl["muted"]))
        col.addWidget(status_chip(r["status"]))
        top.addLayout(col, 1)
        self.body_layout.addLayout(top)

        who_name = r.get("patient_name") or r.get("doctor_name")
        if who_name:
            who = QHBoxLayout()
            who.setSpacing(8)
            who.addWidget(w.Avatar(who_name, 24, w.doctor_photo_path(r.get("doctor_photo"))))
            prefix = "" if r.get("patient_name") else "назначил: "
            who.addWidget(w.label(prefix + w.short_name(who_name) if prefix else who_name, 9, bold=True), 1)
            self.body_layout.addLayout(who)

        self.body_layout.addWidget(w.label(r["frequency"], 9, color=pl["muted"]))
        if r.get("comment"):
            note = w.label(r["comment"], 9, wrap=True)
            note.setStyleSheet(note.styleSheet() + f"font-style: italic; border-left: 3px solid {pl['accent_light']};"
                                                   " padding-left: 8px;")
            self.body_layout.addWidget(note)
        if r["times"]:
            self.body_layout.addWidget(chips_row(r["times"].split(", ")))

        total = max(1, (r["end_date"] - r["start_date"]).days)
        passed = (date.today() - r["start_date"]).days
        if r["status"] == "active":
            progress = passed / total
            caption = (f"день {max(0, passed) + 1} из {total + 1}" if 0 <= passed <= total
                       else ("курс ещё не начался" if passed < 0 else "срок курса истёк"))
        else:
            progress, caption = 1.0, "курс завершён"
        bar_row = QHBoxLayout()
        bar_row.addWidget(ProgressBar(progress, pl["accent"] if r["status"] == "active" else pl["muted"]), 1)
        bar_row.addWidget(w.label(caption, 8, color=pl["muted"]))
        self.body_layout.addLayout(bar_row)
        self.body_layout.addWidget(
            w.label(f"{fmt_date(r['start_date'])} — {fmt_date(r['end_date'])}", 8, color=pl["muted"])
        )


class DiaryCard(w.AnimatedCard):
    """Запись дневника пациента: самочувствие, интенсивность, симптомы,
    триггеры, показатели, диагноз и комментарии врача."""

    def __init__(self, e, on_diagnose=None):
        mood, mood_color = w.mood_of(e["well_being_text"])
        super().__init__(accent=mood_color, clickable=False)
        pl = w.pal()
        parsed = w.parse_wellbeing(e["well_being_text"])
        self.body_layout.setContentsMargins(0, 0, 18, 16)
        self.body_layout.setSpacing(0)

        # Цветная полоса слева — самочувствие видно, даже пролистывая быстро
        outer = QHBoxLayout()
        outer.setSpacing(16)
        stripe = QFrame()
        stripe.setFixedWidth(6)
        stripe.setStyleSheet(f"background: {mood_color}; border-top-left-radius: 15px;"
                             f"border-bottom-left-radius: 15px;")
        outer.addWidget(stripe)
        content = QVBoxLayout()
        content.setContentsMargins(0, 14, 0, 0)
        content.setSpacing(10)
        outer.addLayout(content, 1)
        self.body_layout.addLayout(outer)

        head = QHBoxLayout()
        head.setSpacing(10)
        head.addWidget(w.label(human_date(e["entry_date"]), 11, bold=True))
        head.addWidget(w.label(time_str(e["entry_time"]), 9, color=pl["muted"]))
        head.addWidget(w.chip(mood, mood_color))
        head.addStretch()
        if on_diagnose:
            btn = w.ghost_button("Диагноз и комментарий")
            btn.setMinimumHeight(32)
            btn.clicked.connect(lambda: on_diagnose(e))
            head.addWidget(btn)
        content.addLayout(head)

        if parsed["intensity"] is not None:
            row = QHBoxLayout()
            row.addWidget(w.label("Интенсивность", 9, color=pl["muted"]))
            row.addWidget(ProgressBar(parsed["intensity"] / 10, mood_color), 1)
            row.addWidget(w.label(f"{parsed['intensity']}/10", 9, bold=True))
            content.addLayout(row)

        symptoms = [s.strip() for s in (e["symptoms"] or "").split(",") if s.strip() and s.strip() != "нет"]
        if symptoms:
            content.addWidget(w.label("Симптомы", 8, color=pl["muted"]))
            content.addWidget(chips_row(symptoms))
        if parsed["triggers"]:
            content.addWidget(w.label("Триггеры", 8, color=pl["muted"]))
            content.addWidget(chips_row([t.strip() for t in parsed["triggers"].split(",")], outlined=True))
        if parsed["notes"]:
            note = w.label(f"«{parsed['notes']}»", 10, wrap=True)
            note.setStyleSheet(note.styleSheet() + f"font-style: italic; border-left: 3px solid {pl['accent_light']};"
                                                   " padding-left: 10px;")
            content.addWidget(note)

        if e["indicators"]:
            tiles = QHBoxLayout()
            tiles.setSpacing(8)
            for ind in e["indicators"]:
                tile = QFrame()
                tile.setObjectName("indTile")
                tile.setStyleSheet(f"QFrame#indTile {{ background: {pl['card_alt']}; border-radius: 10px; }}")
                tl = QVBoxLayout(tile)
                tl.setContentsMargins(12, 6, 12, 6)
                tl.setSpacing(0)
                tl.addWidget(w.label(ind["indicator_type"], 8, color=pl["muted"]))
                tl.addWidget(w.label(f"{ind['value']} {ind['unit'] or ''}".strip(), 10, bold=True))
                tiles.addWidget(tile)
            tiles.addStretch()
            content.addLayout(tiles)

        if e["disease_code"] or e["doctor_diagnosis"] or e["comments"]:
            box = QFrame()
            box.setObjectName("diagBox")
            box.setStyleSheet(f"QFrame#diagBox {{ background: {pl['accent_soft']}; border-radius: 12px; }}")
            bl = QVBoxLayout(box)
            bl.setContentsMargins(14, 10, 14, 10)
            bl.setSpacing(4)
            if e["disease_code"]:
                bl.addWidget(w.label(f"МКБ-10 {e['disease_code']} · {e['disease_name']}", 10, bold=True,
                                     color=pl["accent"], wrap=True))
            if e["doctor_diagnosis"]:
                bl.addWidget(w.label(e["doctor_diagnosis"], 9, wrap=True))
            if e["viewed_by"] and (e["disease_code"] or e["doctor_diagnosis"]):
                bl.addWidget(w.label(f"диагноз: {w.short_name(e['viewed_by'])}", 8, color=pl["muted"]))
            for c in e["comments"]:
                when = c["created_at"].strftime("%d.%m %H:%M") if c["created_at"] else ""
                bl.addWidget(w.label(f"Комментарий врача · {w.short_name(c['doctor_name'])} · {when}", 8, bold=True,
                                     color=pl["muted"]))
                bl.addWidget(w.label(c["text"], 9, wrap=True))
            content.addWidget(box)


class ChangePasswordDialog(QDialog):
    def __init__(self, parent, id_user):
        super().__init__(parent)
        self.id_user = id_user
        pl = w.pal()
        self.setWindowTitle("Смена пароля")
        self.setMinimumWidth(400)
        self.setStyleSheet(f"QDialog {{ background: {pl['bg']}; }}" + w.input_qss())

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(10)

        lay.addWidget(w.label("Смена пароля", 15, bold=True))

        lay.addWidget(w.label("Текущий пароль", 9, color=pl["muted"]))
        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.old_pass)

        lay.addWidget(w.label("Новый пароль (мин. 6 символов)", 9, color=pl["muted"]))
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.new_pass)

        lay.addWidget(w.label("Повторите новый пароль", 9, color=pl["muted"]))
        self.confirm_pass = QLineEdit()
        self.confirm_pass.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.confirm_pass)

        btns = QHBoxLayout()
        btns.addStretch()
        cancel = w.ghost_button("Отмена")
        cancel.clicked.connect(self.reject)
        save = w.primary_button("Сохранить")
        save.clicked.connect(self.do_save)
        btns.addWidget(cancel)
        btns.addWidget(save)
        lay.addLayout(btns)

    def do_save(self):
        old_p = self.old_pass.text()
        new_p = self.new_pass.text()
        conf_p = self.confirm_pass.text()

        if not old_p or not new_p or not conf_p:
            mb.warning(self, "Ошибка", "Заполните все поля")
            return

        if new_p != conf_p:
            mb.warning(self, "Ошибка", "Новые пароли не совпадают")
            return

        if len(new_p) < 6:
            mb.warning(self, "Ошибка", "Новый пароль должен быть минимум 6 символов")
            return

        ok, msg = db.update_user_password(self.id_user, old_p, new_p)
        if ok:
            mb.info(self, "Готово", msg)
            self.accept()
        else:
            mb.warning(self, "Ошибка", msg)