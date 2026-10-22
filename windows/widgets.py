"""Общие виджеты интерфейса: карточки с анимацией, вкладки-папки,
аватары и фото, иконки препаратов, выезжающая боковая панель.

Всё рисуется средствами Qt (QPainter + QPropertyAnimation), без картинок,
поэтому одинаково выглядит на любом компьютере.
"""

import os
import math
import re

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QEvent,
    QPoint,
    QPointF,
    QPropertyAnimation,
    QRect,
    QRectF,
    QSize,
    Qt,
    QTimer,
    QVariantAnimation,
    Signal,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import theme
from path import resource_path

# Шрифт интерфейса задаётся в одном месте.
FONT = "Segoe UI"

# Палитра взята из исходных форм проекта (ui/*.ui):
# фон #EEF3F8, основной #2F5C8F, наведение #1E4470, светлый #7A9CC6.
LIGHT = {
    "bg": "#EEF3F8",
    "card": "#FFFFFF",
    "card_alt": "#F0F4FA",
    "text": "#1A1A1A",
    "muted": "#666666",
    "line": "#D6E3F3",
    "accent": "#2F5C8F",
    "accent_hover": "#1E4470",
    "accent_soft": "#E8EFF8",
    "accent_light": "#7A9CC6",
    "danger": "#C0392B",
    "danger_soft": "#FBE9E7",
    "ok": "#27AE60",
    "ok_soft": "#E3F5EA",
    "warn": "#E67E22",
    "warn_soft": "#FDF0E3",
    "shadow": QColor(47, 92, 143, 40),
    "shadow_hover": QColor(47, 92, 143, 90),
    "overlay": QColor(22, 50, 87, 90),
}

DARK = {
    "bg": "#1A1F2B",
    "card": "#232936",
    "card_alt": "#2A3140",
    "text": "#E8EAF0",
    "muted": "#A8B0C0",
    "line": "#2F3A4A",
    "accent": "#4A90D9",
    "accent_hover": "#3A7BBF",
    "accent_soft": "#2A3140",
    "accent_light": "#6BA3D9",
    "danger": "#E2665A",
    "danger_soft": "#3A2426",
    "ok": "#4CC27E",
    "ok_soft": "#1F3529",
    "warn": "#F0A35A",
    "warn_soft": "#3A2E20",
    "shadow": QColor(0, 0, 0, 90),
    "shadow_hover": QColor(0, 0, 0, 150),
    "overlay": QColor(0, 0, 0, 140),
}


def pal():
    """Текущая палитра (светлая или тёмная — по настройке темы)."""
    return DARK if theme.is_dark() else LIGHT


# Цвета вкладок-папок и карточек по ролям
ROLE_COLORS = {
    "admin": "#163257",
    "doctor": "#2F5C8F",
    "patient": "#5A7CA6",
}
ROLE_NAMES = {"admin": "Администратор", "doctor": "Врач", "patient": "Пациент"}

# Аватары — только оттенки синего, чтобы не выбиваться из темы
AVATAR_COLORS = [
    ("#3D6FA8", "#1E4470"),
    ("#7A9CC6", "#4F74A3"),
    ("#2F5C8F", "#163257"),
    ("#5A7CA6", "#2F5C8F"),
    ("#6A8CB6", "#3A5F8C"),
    ("#4A82BF", "#244E80"),
]


def name_color(name):
    """Стабильный цвет по имени: один и тот же человек всегда одного цвета."""
    h = sum(ord(c) * (i + 1) for i, c in enumerate(name or "?"))
    return AVATAR_COLORS[h % len(AVATAR_COLORS)]


def initials(full_name):
    parts = (full_name or "").split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


def plural(n, one, few, many):
    """Число со словом в нужной форме: plural(2, "пациент", "пациента", "пациентов")."""
    n = int(n)
    if n % 10 == 1 and n % 100 != 11:
        word = one
    elif 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        word = few
    else:
        word = many
    return f"{n} {word}"


def short_name(full_name):
    """Кузнецов Дмитрий Алексеевич -> Кузнецов Д. А."""
    parts = (full_name or "").split()
    if len(parts) < 2:
        return full_name or ""
    return parts[0] + " " + " ".join(p[0] + "." for p in parts[1:])


def doctor_photo_path(filename):
    if not filename:
        return ""
    return resource_path("images", "doctors", filename)


# ---------- самочувствие из дневника ----------
MOODS = [
    ("отлично", "Отлично", "#27AE60"),
    ("хорошо", "Хорошо", "#5DBB63"),
    ("удовлетвор", "Удовлетворительно", "#E2B93B"),
    ("очень плох", "Очень плохо", "#C0392B"),
    ("плохо", "Плохо", "#E67E22"),
]


def mood_of(well_being_text):
    """Возвращает (название, цвет) по тексту записи дневника."""
    main = (well_being_text or "").split(".")[0].strip().lower()
    for key, title, color in MOODS:
        if key in main:
            return title, color
    return "Нет данных", "#7A9CC6"


def parse_wellbeing(text):
    """Разбирает строку, которую собирает окно пациента:
    'Хорошо. интенсивность: 4/10. триггеры: стресс. заметки: ...'"""
    result = {"main": "", "intensity": None, "triggers": "", "notes": ""}
    if not text:
        return result
    result["main"] = text.split(".")[0].strip()
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


# ============== ТЕКСТ И КНОПКИ ==============
def label(text="", size=10, bold=False, color=None, wrap=False):
    lbl = QLabel(text)
    f = QFont(FONT, size)
    f.setBold(bold)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color: {color or pal()['text']}; background: transparent;")
    lbl.setWordWrap(wrap)
    if wrap:
        lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    return lbl


def chip(text, bg, fg="#FFFFFF", size=9):
    lbl = QLabel(text)
    f = QFont(FONT, size)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet(
        f"background-color: {bg}; color: {fg}; border-radius: 9px; padding: 3px 10px;"
    )
    lbl.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    return lbl


def _button(text, bg, fg, hover, border="none"):
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setMinimumHeight(38)
    btn.setFont(QFont(FONT, 10, QFont.Weight.DemiBold))
    btn.setStyleSheet(f"""
        QPushButton {{ background-color: {bg}; color: {fg}; border: {border};
            border-radius: 10px; padding: 8px 18px; }}
        QPushButton:hover {{ background-color: {hover}; }}
        QPushButton:disabled {{ background-color: {pal()['line']}; color: {pal()['muted']}; }}
    """)
    return btn


def primary_button(text):
    p = pal()
    return _button(text, p["accent"], "#FFFFFF", p["accent_hover"])


def ghost_button(text):
    p = pal()
    return _button(text, p["card"], p["text"], p["accent_soft"], f"1px solid {p['line']}")


def danger_button(text):
    p = pal()
    return _button(text, p["danger_soft"], p["danger"], p["line"])


def search_line(placeholder):
    p = pal()
    line = QLineEdit()
    line.setPlaceholderText(placeholder)
    line.setClearButtonEnabled(True)
    line.setMinimumHeight(40)
    line.setFont(QFont(FONT, 10))
    line.setStyleSheet(f"""
        QLineEdit {{ background: {p['card']}; color: {p['text']};
            border: 1px solid {p['line']}; border-radius: 12px; padding: 0 14px; }}
        QLineEdit:focus {{ border: 2px solid {p['accent']}; }}
    """)
    return line


def input_qss():
    """Стиль полей ввода внутри форм и боковой панели."""
    p = pal()
    return f"""
        QLineEdit, QComboBox, QDateEdit, QTextEdit, QPlainTextEdit {{
            background: {p['card']}; color: {p['text']};
            border: 1px solid {p['line']}; border-radius: 9px;
            padding: 7px 10px; font-family: '{FONT}'; font-size: 10pt;
        }}
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {{
            border: 2px solid {p['accent']};
        }}
        QComboBox::drop-down, QDateEdit::drop-down {{ border: none; width: 24px; }}
        QComboBox QAbstractItemView {{
            background: {p['card']}; color: {p['text']};
            selection-background-color: {p['accent']}; selection-color: #FFFFFF;
        }}
        QLabel {{ color: {p['text']}; background: transparent; font-family: '{FONT}'; }}
        QCheckBox {{ color: {p['text']}; font-family: '{FONT}'; font-size: 10pt; spacing: 8px; }}
    """


def scroll_qss():
    p = pal()
    return f"""
        QScrollArea {{ background: transparent; border: none; }}
        QScrollArea > QWidget > QWidget {{ background: transparent; }}
        QScrollBar:vertical {{ background: transparent; width: 10px; margin: 4px; }}
        QScrollBar::handle:vertical {{ background: {p['line']}; border-radius: 3px; min-height: 30px; }}
        QScrollBar::handle:vertical:hover {{ background: {p['muted']}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
    """


def make_scroll(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setStyleSheet(scroll_qss())
    scroll.setWidget(widget)
    return scroll


# ============== ВЕКТОРНЫЕ ИКОНКИ ==============
def draw_icon(p, name, rect, color, width=None):
    """Рисует контурную иконку в прямоугольнике rect цветом color.
    Иконки нарисованы линиями, поэтому одинаково выглядят на любом ПК
    и всегда в цвет темы (в отличие от смайликов)."""
    p.save()
    s = min(rect.width(), rect.height())
    x0 = rect.x() + (rect.width() - s) / 2
    y0 = rect.y() + (rect.height() - s) / 2

    def P(x, y):
        return QPointF(x0 + x * s, y0 + y * s)

    def R(x, y, w_, h_):
        return QRectF(x0 + x * s, y0 + y * s, w_ * s, h_ * s)

    pen = QPen(QColor(color), width or max(1.4, s / 12))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    if name == "user":
        p.drawEllipse(R(0.33, 0.12, 0.34, 0.34))
        path = QPainterPath(P(0.14, 0.9))
        path.cubicTo(P(0.14, 0.58), P(0.86, 0.58), P(0.86, 0.9))
        p.drawPath(path)
    elif name == "users":
        p.drawEllipse(R(0.2, 0.16, 0.3, 0.3))
        path = QPainterPath(P(0.04, 0.86))
        path.cubicTo(P(0.04, 0.58), P(0.66, 0.58), P(0.66, 0.86))
        p.drawPath(path)
        p.drawArc(R(0.52, 0.2, 0.26, 0.26), 120 * 16, -270 * 16)
        path2 = QPainterPath(P(0.7, 0.58))
        path2.cubicTo(P(0.86, 0.6), P(0.96, 0.7), P(0.96, 0.86))
        p.drawPath(path2)
    elif name == "doctor":
        # голова + стетоскоп
        p.drawEllipse(R(0.33, 0.08, 0.34, 0.34))
        path = QPainterPath(P(0.14, 0.92))
        path.cubicTo(P(0.14, 0.58), P(0.86, 0.58), P(0.86, 0.92))
        p.drawPath(path)
        p.drawLine(P(0.5, 0.6), P(0.5, 0.78))
        p.drawEllipse(R(0.44, 0.76, 0.12, 0.12))
    elif name == "pill":
        p.translate(P(0.5, 0.5))
        p.rotate(-45)
        p.drawRoundedRect(QRectF(-0.4 * s, -0.17 * s, 0.8 * s, 0.34 * s), 0.17 * s, 0.17 * s)
        p.drawLine(QPointF(0, -0.17 * s), QPointF(0, 0.17 * s))
    elif name == "book":
        p.drawRoundedRect(R(0.18, 0.1, 0.64, 0.8), 0.06 * s, 0.06 * s)
        p.drawLine(P(0.3, 0.1), P(0.3, 0.9))
        p.drawLine(P(0.42, 0.32), P(0.7, 0.32))
        p.drawLine(P(0.42, 0.48), P(0.64, 0.48))
    elif name == "chart":
        p.drawLine(P(0.12, 0.88), P(0.9, 0.88))
        for x, top in ((0.2, 0.55), (0.42, 0.3), (0.64, 0.45)):
            p.drawRoundedRect(R(x, top, 0.14, 0.88 - top), 0.03 * s, 0.03 * s)
    elif name == "lock":
        p.drawRoundedRect(R(0.2, 0.44, 0.6, 0.46), 0.08 * s, 0.08 * s)
        p.drawArc(R(0.31, 0.12, 0.38, 0.5), 0, 180 * 16)
        p.drawLine(P(0.31, 0.37), P(0.31, 0.44))
        p.drawLine(P(0.69, 0.37), P(0.69, 0.44))
        p.drawLine(P(0.5, 0.6), P(0.5, 0.72))
    elif name == "clock":
        p.drawEllipse(R(0.1, 0.1, 0.8, 0.8))
        p.drawLine(P(0.5, 0.5), P(0.5, 0.27))
        p.drawLine(P(0.5, 0.5), P(0.67, 0.6))
    elif name == "plus":
        p.drawLine(P(0.5, 0.18), P(0.5, 0.82))
        p.drawLine(P(0.18, 0.5), P(0.82, 0.5))
    elif name == "key":
        p.drawEllipse(R(0.1, 0.32, 0.36, 0.36))
        p.drawLine(P(0.46, 0.5), P(0.9, 0.5))
        p.drawLine(P(0.76, 0.5), P(0.76, 0.66))
        p.drawLine(P(0.88, 0.5), P(0.88, 0.62))
    elif name == "trash":
        p.drawLine(P(0.16, 0.26), P(0.84, 0.26))
        p.drawLine(P(0.4, 0.26), P(0.42, 0.14))
        p.drawLine(P(0.42, 0.14), P(0.58, 0.14))
        p.drawLine(P(0.58, 0.14), P(0.6, 0.26))
        path = QPainterPath(P(0.24, 0.26))
        path.lineTo(P(0.3, 0.88))
        path.lineTo(P(0.7, 0.88))
        path.lineTo(P(0.76, 0.26))
        p.drawPath(path)
    elif name == "edit":
        path = QPainterPath(P(0.2, 0.8))
        path.lineTo(P(0.24, 0.62))
        path.lineTo(P(0.66, 0.2))
        path.lineTo(P(0.8, 0.34))
        path.lineTo(P(0.38, 0.76))
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(P(0.56, 0.3), P(0.7, 0.44))
    elif name == "camera":
        p.drawRoundedRect(R(0.1, 0.3, 0.8, 0.54), 0.08 * s, 0.08 * s)
        p.drawLine(P(0.36, 0.3), P(0.42, 0.18))
        p.drawLine(P(0.42, 0.18), P(0.58, 0.18))
        p.drawLine(P(0.58, 0.18), P(0.64, 0.3))
        p.drawEllipse(R(0.36, 0.42, 0.28, 0.28))
    elif name == "file":
        path = QPainterPath(P(0.22, 0.1))
        path.lineTo(P(0.6, 0.1))
        path.lineTo(P(0.8, 0.3))
        path.lineTo(P(0.8, 0.9))
        path.lineTo(P(0.22, 0.9))
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(P(0.36, 0.52), P(0.66, 0.52))
        p.drawLine(P(0.36, 0.68), P(0.66, 0.68))
    elif name == "link":
        p.translate(P(0.5, 0.5))
        p.rotate(-45)
        p.drawRoundedRect(QRectF(-0.42 * s, -0.13 * s, 0.46 * s, 0.26 * s), 0.13 * s, 0.13 * s)
        p.drawRoundedRect(QRectF(-0.04 * s, -0.13 * s, 0.46 * s, 0.26 * s), 0.13 * s, 0.13 * s)
    elif name == "stethoscope":
        p.drawLine(P(0.22, 0.12), P(0.22, 0.4))
        p.drawLine(P(0.58, 0.12), P(0.58, 0.4))
        p.drawArc(R(0.22, 0.2, 0.36, 0.4), 180 * 16, 180 * 16)
        path = QPainterPath(P(0.4, 0.6))
        path.cubicTo(P(0.4, 0.92), P(0.78, 0.92), P(0.78, 0.66))
        p.drawPath(path)
        p.drawEllipse(R(0.7, 0.5, 0.16, 0.16))
    elif name == "heart":
        path = QPainterPath(P(0.5, 0.86))
        path.cubicTo(P(0.1, 0.6), P(0.06, 0.3), P(0.28, 0.2))
        path.cubicTo(P(0.4, 0.15), P(0.48, 0.24), P(0.5, 0.32))
        path.cubicTo(P(0.52, 0.24), P(0.6, 0.15), P(0.72, 0.2))
        path.cubicTo(P(0.94, 0.3), P(0.9, 0.6), P(0.5, 0.86))
        p.drawPath(path)
        pulse = QPainterPath(P(0.22, 0.5))
        for x, y in ((0.36, 0.5), (0.42, 0.38), (0.5, 0.62), (0.56, 0.46), (0.78, 0.46)):
            pulse.lineTo(P(x, y))
        p.drawPath(pulse)
    elif name == "drop":
        path = QPainterPath(P(0.5, 0.1))
        path.cubicTo(P(0.62, 0.32), P(0.8, 0.48), P(0.8, 0.62))
        path.cubicTo(P(0.8, 0.8), P(0.66, 0.9), P(0.5, 0.9))
        path.cubicTo(P(0.34, 0.9), P(0.2, 0.8), P(0.2, 0.62))
        path.cubicTo(P(0.2, 0.48), P(0.38, 0.32), P(0.5, 0.1))
        p.drawPath(path)
        p.drawArc(R(0.32, 0.5, 0.26, 0.26), 180 * 16, 90 * 16)
    elif name == "thermo":
        p.drawRoundedRect(R(0.4, 0.08, 0.2, 0.56), 0.1 * s, 0.1 * s)
        p.drawEllipse(R(0.32, 0.6, 0.36, 0.32))
        p.drawLine(P(0.5, 0.36), P(0.5, 0.7))
        p.drawLine(P(0.66, 0.24), P(0.76, 0.24))
        p.drawLine(P(0.66, 0.38), P(0.76, 0.38))
    elif name == "ruler":
        p.translate(P(0.5, 0.5))
        p.rotate(-45)
        p.drawRoundedRect(QRectF(-0.42 * s, -0.14 * s, 0.84 * s, 0.28 * s), 0.05 * s, 0.05 * s)
        for i in range(-3, 4):
            ln = 0.1 if i % 2 else 0.05
            p.drawLine(QPointF(i * 0.1 * s, -0.14 * s), QPointF(i * 0.1 * s, (-0.14 + ln) * s))
    elif name == "scale":
        p.drawRoundedRect(R(0.12, 0.18, 0.76, 0.7), 0.14 * s, 0.14 * s)
        p.drawArc(R(0.3, 0.3, 0.4, 0.34), 30 * 16, 120 * 16)
        p.drawLine(P(0.5, 0.47), P(0.58, 0.36))
    elif name == "gauge":
        p.drawArc(R(0.1, 0.18, 0.8, 0.8), 0, 180 * 16)
        p.drawLine(P(0.1, 0.58), P(0.9, 0.58))
        p.drawLine(P(0.5, 0.58), P(0.68, 0.34))
        p.drawEllipse(R(0.46, 0.54, 0.08, 0.08))
    elif name == "bell":
        path = QPainterPath(P(0.2, 0.72))
        path.lineTo(P(0.26, 0.62))
        path.cubicTo(P(0.26, 0.2), P(0.74, 0.2), P(0.74, 0.62))
        path.lineTo(P(0.8, 0.72))
        path.closeSubpath()
        p.drawPath(path)
        p.drawArc(R(0.4, 0.66, 0.2, 0.18), 180 * 16, 180 * 16)
        p.drawLine(P(0.5, 0.14), P(0.5, 0.22))
    elif name == "calendar":
        p.drawRoundedRect(R(0.12, 0.2, 0.76, 0.68), 0.08 * s, 0.08 * s)
        p.drawLine(P(0.12, 0.4), P(0.88, 0.4))
        p.drawLine(P(0.32, 0.12), P(0.32, 0.26))
        p.drawLine(P(0.68, 0.12), P(0.68, 0.26))
    elif name == "check":
        path = QPainterPath(P(0.2, 0.52))
        path.lineTo(P(0.42, 0.72))
        path.lineTo(P(0.8, 0.3))
        p.drawPath(path)
    elif name == "note":
        p.drawRoundedRect(R(0.16, 0.12, 0.68, 0.76), 0.08 * s, 0.08 * s)
        for y in (0.34, 0.5, 0.66):
            p.drawLine(P(0.3, y), P(0.7 if y < 0.6 else 0.56, y))
    elif name == "sun":
        p.drawEllipse(R(0.32, 0.32, 0.36, 0.36))
        for k in range(8):
            a = k * math.pi / 4
            p.drawLine(P(0.5 + 0.27 * math.cos(a), 0.5 + 0.27 * math.sin(a)),
                       P(0.5 + 0.4 * math.cos(a), 0.5 + 0.4 * math.sin(a)))
    elif name == "moon":
        path = QPainterPath(P(0.62, 0.12))
        path.cubicTo(P(0.2, 0.14), P(0.08, 0.66), P(0.4, 0.84))
        path.cubicTo(P(0.6, 0.94), P(0.82, 0.84), P(0.9, 0.66))
        path.cubicTo(P(0.6, 0.74), P(0.38, 0.42), P(0.62, 0.12))
        p.drawPath(path)
    else:
        p.drawEllipse(R(0.4, 0.4, 0.2, 0.2))
    p.restore()


def icon(name, size=24, color="#FFFFFF"):
    """QIcon из векторной иконки — для обычных кнопок (QPushButton.setIcon)."""
    pm = QPixmap(size * 2, size * 2)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw_icon(p, name, QRectF(0, 0, size * 2, size * 2), color, size / 6)
    p.end()
    pm.setDevicePixelRatio(2)
    return QIcon(pm)


class Icon(QWidget):
    """Векторная иконка на мягкой подложке (как значок в карточке)."""

    def __init__(self, name, size=40, color=None, bg=None, radius=None):
        super().__init__()
        self.name = name
        self.color = color or pal()["accent"]
        self.bg = bg
        self.radius = size * 0.3 if radius is None else radius
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect())
        if self.bg:
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(self.bg))
            p.drawRoundedRect(r, self.radius, self.radius)
            pad = r.width() * 0.26
        else:
            pad = r.width() * 0.08
        draw_icon(p, self.name, r.adjusted(pad, pad, -pad, -pad), self.color)


# ============== FLOW LAYOUT ==============
class FlowLayout(QLayout):
    """Раскладка «плиткой»: карточки переносятся на новую строку,
    когда не помещаются по ширине (классический пример из документации Qt)."""

    def __init__(self, parent=None, spacing=16):
        super().__init__(parent)
        self._items = []
        self._spacing = spacing
        self.setContentsMargins(4, 4, 4, 4)

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index):
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        return size + QSize(m.left() + m.right(), m.top() + m.bottom())

    def clear(self):
        while self._items:
            item = self._items.pop()
            if item.widget():
                item.widget().deleteLater()

    def _do_layout(self, rect, test_only):
        m = self.contentsMargins()
        area = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        x, y, line_h = area.x(), area.y(), 0
        for item in self._items:
            hint = item.sizeHint()
            if item.hasHeightForWidth():
                hint.setHeight(max(hint.height(), item.heightForWidth(hint.width())))
            next_x = x + hint.width() + self._spacing
            if next_x - self._spacing > area.right() + 1 and line_h > 0:
                x = area.x()
                y += line_h + self._spacing
                next_x = x + hint.width() + self._spacing
                line_h = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x = next_x
            line_h = max(line_h, hint.height())
        return y + line_h - rect.y() + m.bottom()


class CardGrid(QWidget):
    """Контейнер для карточек с прокруткой и подписью «ничего не найдено»."""

    def __init__(self, empty_text="Ничего не найдено"):
        super().__init__()
        self.inner = QWidget()
        self.inner.setStyleSheet("background: transparent;")
        self.flow = FlowLayout(self.inner)
        self.empty = label(empty_text, 11, color=pal()["muted"])
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty.hide()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.empty)
        lay.addWidget(make_scroll(self.inner), 1)

    def set_cards(self, cards):
        """Заменяет карточки и проигрывает появление «лесенкой»."""
        self.flow.clear()
        for i, card in enumerate(cards):
            self.flow.addWidget(card)
            if isinstance(card, AnimatedCard):
                card.appear(delay=min(i, 12) * 45)
        self.empty.setVisible(not cards)


# ============== КАРТОЧКА С АНИМАЦИЕЙ ==============
class AnimatedCard(QWidget):
    """Карточка, которая:
    * появляется, всплывая снизу с проявлением;
    * при наведении приподнимается, тень становится глубже,
      а рамка подсвечивается цветом карточки;
    * по клику испускает сигнал clicked.

    Содержимое кладётся в self.body_layout.
    """

    clicked = Signal()
    LIFT = 6  # на сколько пикселей карточка поднимается при наведении
    RISE = 18  # с какой глубины всплывает при появлении

    def __init__(self, width=None, height=None, accent=None, clickable=True):
        super().__init__()
        p = pal()
        self._accent = accent or p["accent"]
        self._hover = 0.0
        self._appear = 1.0
        self._clickable = clickable

        self.body = QFrame(self)
        self.body.setObjectName("cardBody")
        self._apply_body_style(0.0)

        self.shadow = QGraphicsDropShadowEffect(self.body)
        self.shadow.setBlurRadius(18)
        self.shadow.setOffset(0, 4)
        self.shadow.setColor(p["shadow"])
        self.body.setGraphicsEffect(self.shadow)

        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(18, 16, 18, 16)
        self.body_layout.setSpacing(8)

        outer = QVBoxLayout(self)
        self._outer = outer
        outer.addWidget(self.body)
        self._update_margins()

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._hover_anim = QVariantAnimation(self)
        self._hover_anim.setDuration(180)
        self._hover_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._hover_anim.valueChanged.connect(self._set_hover)

        self._appear_anim = QVariantAnimation(self)
        self._appear_anim.setDuration(380)
        self._appear_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._appear_anim.setStartValue(0.0)
        self._appear_anim.setEndValue(1.0)
        self._appear_anim.valueChanged.connect(self._set_appear)
        self._appear_anim.finished.connect(self._appear_done)

    # --- оформление ---
    def _apply_body_style(self, hover):
        p = pal()
        selected = getattr(self, "_selected", False)
        border = _mix(QColor(p["line"]), QColor(self._accent), 1.0 if selected else hover).name()
        bg = p["accent_soft"] if selected else p["card"]
        width = 2 if selected else 1
        self.body.setStyleSheet(f"""
            QFrame#cardBody {{ background-color: {bg};
                border: {width}px solid {border}; border-radius: 16px; }}
            QFrame#cardBody QLabel {{ background: transparent; border: none; }}
        """)

    def set_selected(self, selected):
        """Выбранная карточка: синяя рамка и подложка (например, выбранный препарат)."""
        self._selected = bool(selected)
        self._apply_body_style(self._hover)

    def _update_margins(self):
        lift = int(self.LIFT * self._hover)
        rise = int(self.RISE * (1.0 - self._appear))
        # Сверху и снизу — запас под тень и подъём
        self._outer.setContentsMargins(8, 4 + self.LIFT - lift + rise, 8, 10 + lift)

    def _set_hover(self, v):
        self._hover = float(v)
        p = pal()
        self.shadow.setBlurRadius(18 + 18 * self._hover)
        self.shadow.setOffset(0, 4 + 8 * self._hover)
        self.shadow.setColor(_mix(p["shadow"], p["shadow_hover"], self._hover))
        self._apply_body_style(self._hover)
        self._update_margins()

    def _set_appear(self, v):
        self._appear = float(v)
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsOpacityEffect):
            effect.setOpacity(self._appear)
        self._update_margins()

    def _appear_done(self):
        # Эффект прозрачности больше не нужен — снимаем, чтобы не тормозило
        self.setGraphicsEffect(None)

    def appear(self, delay=0):
        self._appear = 0.0
        self.setGraphicsEffect(QGraphicsOpacityEffect(self))
        self.graphicsEffect().setOpacity(0.0)
        self._update_margins()
        QTimer.singleShot(delay, self._appear_anim.start)

    def _animate_hover(self, target):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(target)
        self._hover_anim.start()

    # --- события ---
    def enterEvent(self, event):
        if self._clickable:
            self._animate_hover(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._clickable:
            self._animate_hover(0.0)
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._clickable and event.button() == Qt.MouseButton.LeftButton:
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()
        super().mouseReleaseEvent(event)


def _mix(c1, c2, t):
    c1, c2 = QColor(c1), QColor(c2)
    return QColor(
        int(c1.red() + (c2.red() - c1.red()) * t),
        int(c1.green() + (c2.green() - c1.green()) * t),
        int(c1.blue() + (c2.blue() - c1.blue()) * t),
        int(c1.alpha() + (c2.alpha() - c1.alpha()) * t),
    )


# ============== АВАТАР / ФОТО ==============
class Avatar(QWidget):
    """Фото человека. Если фото нет — градиентный круг с инициалами.
    shape='circle' — круглое (для списков), 'rounded' — скруглённый
    прямоугольник (крупное фото врача на карточке)."""

    def __init__(self, full_name, size=48, photo=None, shape="circle", ring=None, height=None):
        super().__init__()
        self.full_name = full_name or ""
        self.shape = shape
        self.ring = ring
        self._pixmap = None
        self.set_photo(photo)
        self.setFixedSize(size, height or size)

    def set_photo(self, photo_path):
        self._pixmap = None
        if photo_path and os.path.exists(photo_path):
            pm = QPixmap(photo_path)
            if not pm.isNull():
                self._pixmap = pm
        self.update()

    def has_photo(self):
        return self._pixmap is not None

    def _clip_path(self, rect):
        path = QPainterPath()
        if self.shape == "circle":
            path.addEllipse(rect)
        else:
            path.addRoundedRect(rect, 14, 14)
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        rect = QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5)
        path = self._clip_path(rect)

        if self._pixmap:
            # Масштабируем «с обрезкой» (cover): лицо заполняет всю область
            scaled = self._pixmap.scaled(
                rect.size().toSize(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = rect.x() + (rect.width() - scaled.width()) / 2
            # Портреты обычно с лицом в верхней трети, поэтому обрезаем снизу
            y = rect.y() - max(0, (scaled.height() - rect.height()) * 0.25)
            painter.setClipPath(path)
            painter.drawPixmap(QPointF(x, y), scaled)
            painter.setClipping(False)
        else:
            c1, c2 = name_color(self.full_name)
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0, QColor(c1))
            grad.setColorAt(1, QColor(c2))
            painter.fillPath(path, QBrush(grad))
            # Лёгкий блик сверху
            painter.setClipPath(path)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(255, 255, 255, 34))
            painter.drawEllipse(
                QRectF(rect.x() - rect.width() * 0.2, rect.y() - rect.height() * 0.55,
                       rect.width() * 1.4, rect.height() * 0.95)
            )
            painter.setClipping(False)
            f = QFont(FONT)
            f.setBold(True)
            f.setPixelSize(int(min(rect.width(), rect.height()) * 0.36))
            painter.setFont(f)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, initials(self.full_name))

        if self.ring:
            painter.setPen(QPen(QColor(self.ring), 2.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)


# ============== ИКОНКА ПРЕПАРАТА ==============
PILL_COLORS = [
    ("#2F5C8F", "#FFFFFF"),
    ("#7A9CC6", "#FFFFFF"),
    ("#4A82BF", "#E8EFF8"),
    ("#5A7CA6", "#FFFFFF"),
    ("#1E4470", "#E8EFF8"),
]


class PillIcon(QWidget):
    """Рисует препарат по форме выпуска: таблетка, капсула, ингалятор,
    флакон, тюбик. При наведении иконка покачивается."""

    def __init__(self, form="", name="", size=56):
        super().__init__()
        self.form = (form or "").lower()
        self.name = name or ""
        self._angle = 0.0
        self.setFixedSize(size, size)
        h = sum(ord(c) for c in self.name)
        self.c1, self.c2 = PILL_COLORS[h % len(PILL_COLORS)]

        self._anim = QPropertyAnimation(self, b"angle", self)
        self._anim.setDuration(600)
        self._anim.setKeyValueAt(0, 0.0)
        self._anim.setKeyValueAt(0.25, -14.0)
        self._anim.setKeyValueAt(0.6, 9.0)
        self._anim.setKeyValueAt(1, 0.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    def _get_angle(self):
        return self._angle

    def _set_angle(self, v):
        self._angle = v
        self.update()

    angle = Property(float, _get_angle, _set_angle)

    def wobble(self):
        if self._anim.state() != QPropertyAnimation.State.Running:
            self._anim.start()

    def enterEvent(self, event):
        self.wobble()
        super().enterEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        s = min(self.width(), self.height())
        # Мягкая подложка
        p.setPen(Qt.PenStyle.NoPen)
        bg = QColor(self.c1)
        bg.setAlpha(40)
        p.setBrush(bg)
        p.drawRoundedRect(QRectF(0, 0, s, s), s * 0.3, s * 0.3)

        p.translate(s / 2, s / 2)
        p.rotate(self._angle)
        f = self.form
        if "капс" in f:
            self._capsule(p, s)
        elif "аэроз" in f or "ингал" in f or "спрей" in f:
            self._inhaler(p, s)
        elif "раствор" in f or "сироп" in f or "капли" in f or "флакон" in f:
            self._bottle(p, s)
        elif "гель" in f or "мазь" in f or "крем" in f:
            self._tube(p, s)
        else:
            self._tablet(p, s)

    def _tablet(self, p, s):
        """Две круглые таблетки «в объёме»: боковая грань, светлый верх, риска."""

        def one(cx, cy, r, base):
            thick = r * 0.28
            # боковая грань (толщина таблетки)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(base).darker(135))
            p.drawEllipse(QRectF(cx - r, cy - r * 0.62 + thick, 2 * r, 1.24 * r))
            p.drawRect(QRectF(cx - r, cy, 2 * r, thick))
            # верхняя грань
            grad = QLinearGradient(cx - r, cy - r, cx + r, cy + r)
            grad.setColorAt(0, QColor(base).lighter(150))
            grad.setColorAt(1, QColor(base))
            p.setBrush(grad)
            p.drawEllipse(QRectF(cx - r, cy - r * 0.62, 2 * r, 1.24 * r))
            # риска посередине и блик
            p.setPen(QPen(QColor(base).darker(125), max(1.2, s / 40), Qt.PenStyle.SolidLine,
                          Qt.PenCapStyle.RoundCap))
            p.drawLine(QPointF(cx - r * 0.55, cy - r * 0.1), QPointF(cx + r * 0.55, cy + r * 0.1))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(255, 255, 255, 120))
            p.drawEllipse(QRectF(cx - r * 0.6, cy - r * 0.48, r * 0.55, r * 0.25))

        one(s * 0.13, -s * 0.1, s * 0.17, QColor(self.c1).lighter(125))
        one(-s * 0.06, s * 0.06, s * 0.23, QColor(self.c1))

    def _capsule(self, p, s):
        p.rotate(-35)
        w, h = s * 0.62, s * 0.26
        path_left = QPainterPath()
        path_left.addRoundedRect(QRectF(-w / 2, -h / 2, w, h), h / 2, h / 2)
        left = QPainterPath()
        left.addRect(QRectF(-w / 2, -h / 2, w / 2, h))
        right = QPainterPath()
        right.addRect(QRectF(0, -h / 2, w / 2, h))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.c1))
        p.drawPath(path_left.intersected(left))
        p.setBrush(QColor("#FFFFFF"))
        p.drawPath(path_left.intersected(right))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(self.c1).darker(120), 1.6))
        p.drawPath(path_left)
        # блик
        p.setPen(QPen(QColor(255, 255, 255, 170), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(QPointF(-w * 0.36, -h * 0.18), QPointF(-w * 0.12, -h * 0.18))

    def _inhaler(self, p, s):
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.c1))
        p.drawRoundedRect(QRectF(-s * 0.13, -s * 0.3, s * 0.26, s * 0.42), 5, 5)
        p.setBrush(QColor(self.c1).darker(120))
        p.drawRoundedRect(QRectF(-s * 0.13, s * 0.06, s * 0.38, s * 0.18), 5, 5)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(-s * 0.08, -s * 0.36, s * 0.16, s * 0.1), 3, 3)
        # облачко аэрозоля
        p.setBrush(QColor(255, 255, 255, 200))
        for dx, dy, r in ((0.3, 0.12, 0.05), (0.38, 0.06, 0.04), (0.38, 0.19, 0.035)):
            p.drawEllipse(QPointF(s * dx, s * dy), s * r, s * r)

    def _bottle(self, p, s):
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.c1).darker(115))
        p.drawRoundedRect(QRectF(-s * 0.09, -s * 0.33, s * 0.18, s * 0.1), 3, 3)
        p.setBrush(QColor(self.c1))
        p.drawRoundedRect(QRectF(-s * 0.18, -s * 0.23, s * 0.36, s * 0.5), 8, 8)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRoundedRect(QRectF(-s * 0.13, -s * 0.08, s * 0.26, s * 0.18), 3, 3)

    def _tube(self, p, s):
        p.rotate(-30)
        path = QPainterPath()
        path.moveTo(-s * 0.3, -s * 0.13)
        path.lineTo(s * 0.18, -s * 0.1)
        path.lineTo(s * 0.18, s * 0.1)
        path.lineTo(-s * 0.3, s * 0.13)
        path.closeSubpath()
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.c1))
        p.drawPath(path)
        p.setBrush(QColor("#FFFFFF"))
        p.drawRect(QRectF(-s * 0.34, -s * 0.13, s * 0.05, s * 0.26))
        p.setBrush(QColor(self.c1).darker(125))
        p.drawRoundedRect(QRectF(s * 0.18, -s * 0.07, s * 0.12, s * 0.14), 2, 2)


# ============== ВКЛАДКИ-ПАПКИ ==============
class FolderTabBar(QWidget):
    """Полоса вкладок в виде корешков папок с файлами.
    Неактивные вкладки «утоплены» в папку; выбранная плавно
    выдвигается вверх, при наведении вкладка чуть приподнимается."""

    currentChanged = Signal(int)
    HEIGHT = 58
    RISE = 14  # насколько выдвигается выбранная вкладка

    def __init__(self):
        super().__init__()
        self.tabs = []  # (title, icon, color)
        self._current = 0
        self._hovered = -1
        self._rise = []
        self._anims = []
        self.setFixedHeight(self.HEIGHT)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def add_tab(self, title, icon, color):
        self.tabs.append((title, icon, color))
        self._rise.append(1.0 if len(self.tabs) == 1 else 0.0)
        anim = QVariantAnimation(self)
        anim.setDuration(260)
        anim.setEasingCurve(QEasingCurve.Type.OutBack)
        idx = len(self.tabs) - 1
        anim.valueChanged.connect(lambda v, i=idx: self._set_rise(i, v))
        self._anims.append(anim)
        self.update()

    def current(self):
        return self._current

    def current_color(self):
        return self.tabs[self._current][2] if self.tabs else pal()["accent"]

    def _set_rise(self, i, v):
        self._rise[i] = float(v)
        self.update()

    def _target(self, i):
        if i == self._current:
            return 1.0
        if i == self._hovered:
            return 0.4
        return 0.0

    def _animate_all(self):
        for i, anim in enumerate(self._anims):
            target = self._target(i)
            if abs(self._rise[i] - target) < 0.001:
                continue
            anim.stop()
            anim.setStartValue(self._rise[i])
            anim.setEndValue(target)
            anim.start()

    def set_current(self, i):
        if i == self._current or not (0 <= i < len(self.tabs)):
            return
        self._current = i
        self._animate_all()
        self.currentChanged.emit(i)

    def _tab_rects(self):
        n = len(self.tabs)
        if not n:
            return []
        overlap = 18
        w = min(210, (self.width() + overlap * (n - 1)) / n)
        return [QRectF(i * (w - overlap), 0, w, self.HEIGHT) for i in range(n)]

    def _tab_at(self, pos):
        rects = self._tab_rects()
        # Сначала проверяем выбранную — она лежит поверх соседних
        order = [self._current] + [i for i in range(len(rects)) if i != self._current]
        for i in order:
            r = rects[i]
            top = r.top() + self.RISE * (1 - self._rise[i])
            if r.left() + 8 <= pos.x() <= r.right() - 8 and pos.y() >= top:
                return i
        return -1

    def mouseMoveEvent(self, event):
        i = self._tab_at(event.position())
        if i != self._hovered:
            self._hovered = i
            self._animate_all()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self._animate_all()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        i = self._tab_at(event.position())
        if i >= 0:
            self.set_current(i)
        super().mousePressEvent(event)

    def _tab_path(self, r, top):
        """Корешок папки: скошенные бока и скруглённый верх."""
        slope = 16
        radius = 10
        bottom = r.bottom() + 1
        path = QPainterPath()
        path.moveTo(r.left(), bottom)
        path.cubicTo(
            r.left() + slope * 0.5, bottom,
            r.left() + slope * 0.5, top,
            r.left() + slope + radius, top,
        )
        path.lineTo(r.right() - slope - radius, top)
        path.cubicTo(
            r.right() - slope * 0.5, top,
            r.right() - slope * 0.5, bottom,
            r.right(), bottom,
        )
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        p = pal()
        rects = self._tab_rects()
        order = [i for i in range(len(rects)) if i != self._current] + [self._current]
        for i in order:
            title, icon, color = self.tabs[i]
            r = rects[i]
            rise = self._rise[i]
            top = r.top() + self.RISE * (1 - rise) + 2
            path = self._tab_path(r, top)
            active = i == self._current
            base = QColor(color)
            if active:
                fill = QColor(p["card"])
            else:
                fill = _mix(QColor(p["card_alt"]), base, 0.16 + 0.12 * rise)
            # Тень корешка
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 0, 0, 22))
            painter.drawPath(path.translated(0, -2))
            painter.setBrush(fill)
            painter.drawPath(path)
            # Цветная полоска-«ярлычок» сверху
            painter.save()
            painter.setClipPath(path)
            painter.setBrush(base)
            painter.drawRect(QRectF(r.left(), top, r.width(), 4 if active else 3))
            painter.restore()
            if not active:
                painter.setPen(QPen(QColor(p["line"]), 1))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawPath(path)
            # Подпись
            f = QFont(FONT, 10)
            f.setBold(active)
            painter.setFont(f)
            painter.setPen(QColor(color) if active else QColor(p["muted"]))
            text_rect = QRectF(r.left() + 18, top + 4, r.width() - 36, r.bottom() - top - 4)
            icon_w = 26
            total = icon_w + painter.fontMetrics().horizontalAdvance(title)
            x0 = text_rect.center().x() - total / 2
            painter.drawText(
                QRectF(x0 + icon_w, text_rect.top(), total, text_rect.height()),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                title,
            )
            cy = text_rect.center().y()
            draw_icon(
                painter, icon, QRectF(x0, cy - 9, 18, 18),
                QColor(color) if active else QColor(p["muted"]), 1.6,
            )


class FolderTabs(QWidget):
    """Вкладки-папки + содержимое, которое лежит «внутри папки».
    При переключении страница выезжает и проявляется."""

    currentChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.bar = FolderTabBar()
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")

        self.folder = QFrame()
        self.folder.setObjectName("folderBody")
        folder_lay = QVBoxLayout(self.folder)
        folder_lay.setContentsMargins(22, 20, 22, 20)
        folder_lay.addWidget(self.stack)

        shadow = QGraphicsDropShadowEffect(self.folder)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(pal()["shadow"])
        self.folder.setGraphicsEffect(shadow)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        bar_row = QHBoxLayout()
        bar_row.setContentsMargins(14, 0, 14, 0)
        bar_row.addWidget(self.bar)
        lay.addLayout(bar_row)
        lay.addWidget(self.folder, 1)

        self.bar.currentChanged.connect(self._on_changed)
        self._update_folder_style()

    def add_tab(self, widget, title, icon, color):
        self.stack.addWidget(widget)
        self.bar.add_tab(title, icon, color)
        self._update_folder_style()

    def set_current(self, i):
        self.bar.set_current(i)

    def _update_folder_style(self):
        p = pal()
        color = self.bar.current_color()
        self.folder.setStyleSheet(f"""
            QFrame#folderBody {{ background-color: {p['card']};
                border-top: 4px solid {color}; border-radius: 18px; }}
        """)

    def _on_changed(self, i):
        self.stack.setCurrentIndex(i)
        self._update_folder_style()
        page = self.stack.currentWidget()
        effect = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(effect)
        anim = QVariantAnimation(self)
        anim.setDuration(260)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        start_pos = page.pos()

        def step(v):
            effect.setOpacity(v)
            page.move(start_pos.x(), start_pos.y() + int(16 * (1 - v)))

        def done():
            page.setGraphicsEffect(None)
            page.move(start_pos)

        anim.valueChanged.connect(step)
        anim.finished.connect(done)
        anim.start()
        self._page_anim = anim
        self.currentChanged.emit(i)


# ============== ПЛАШКА С ЧИСЛОМ ==============
class KpiTile(AnimatedCard):
    """Плашка-показатель: число «набегает» от нуля при появлении."""

    def __init__(self, icon, caption, value, color, hint=""):
        super().__init__(height=118, accent=color, clickable=False)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._value = int(value)
        row = QHBoxLayout()
        row.setSpacing(14)
        badge = Icon(icon, 46, color, pal()["accent_soft"], 14)
        col = QVBoxLayout()
        col.setSpacing(0)
        self.number = label("0", 21, bold=True)
        cap = label(caption, 9, color=pal()["muted"])
        col.addWidget(self.number)
        col.addWidget(cap)
        if hint:
            col.addWidget(label(hint, 8, color=color))
        row.addWidget(badge, 0, Qt.AlignmentFlag.AlignTop)
        row.addLayout(col, 1)
        self.body_layout.addLayout(row)

        self._count = QVariantAnimation(self)
        self._count.setDuration(900)
        self._count.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._count.valueChanged.connect(lambda v: self.number.setText(str(int(v))))

    def set_value(self, value):
        self._value = int(value)
        self._count.stop()
        self._count.setStartValue(0)
        self._count.setEndValue(self._value)
        self._count.start()

    def appear(self, delay=0):
        super().appear(delay)
        QTimer.singleShot(delay + 120, lambda: self.set_value(self._value))


# ============== ВЫЕЗЖАЮЩАЯ ПАНЕЛЬ ==============
class SidePanel(QWidget):
    """Карточка клиента в стиле CRM: панель выезжает справа поверх окна,
    фон затемняется. Закрывается кнопкой, клавишей Esc или кликом по фону."""

    WIDTH = 500

    def __init__(self, host):
        super().__init__(host)
        self.host = host
        self.hide()
        self._overlay_alpha = 0.0

        self.panel = QFrame(self)
        self.panel.setObjectName("sidePanel")
        p = pal()
        self.panel.setStyleSheet(
            f"QFrame#sidePanel {{ background-color: {p['bg']};"
            f" border-top-left-radius: 20px; border-bottom-left-radius: 20px; }}"
            + input_qss()
        )
        shadow = QGraphicsDropShadowEffect(self.panel)
        shadow.setBlurRadius(40)
        shadow.setOffset(-6, 0)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.panel.setGraphicsEffect(shadow)

        pl = QVBoxLayout(self.panel)
        pl.setContentsMargins(0, 0, 0, 0)
        pl.setSpacing(0)

        head = QHBoxLayout()
        head.setContentsMargins(22, 16, 14, 6)
        self.title = label("", 13, bold=True)
        close = QPushButton("✕")
        close.setFixedSize(34, 34)
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {p['muted']}; border: none;"
            f" border-radius: 17px; font-size: 14pt; }}"
            f"QPushButton:hover {{ background: {p['line']}; color: {p['text']}; }}"
        )
        close.clicked.connect(self.close_panel)
        head.addWidget(self.title, 1)
        head.addWidget(close)
        pl.addLayout(head)

        self.content = QWidget()
        self.content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(22, 6, 22, 22)
        self.content_layout.setSpacing(14)
        pl.addWidget(make_scroll(self.content), 1)

        self._anim = QVariantAnimation(self)
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.valueChanged.connect(self._step)
        self._anim.finished.connect(self._finished)
        self._closing = False
        host.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.host and event.type() == QEvent.Type.Resize and self.isVisible():
            self._layout(1.0)
        return False

    def _layout(self, t):
        self.setGeometry(self.host.rect())
        w = min(self.WIDTH, self.width() - 40)
        x = self.width() - int(w * t)
        self.panel.setGeometry(x, 0, w, self.height())
        self._overlay_alpha = t
        self.update()

    def _step(self, v):
        self._layout(float(v))

    def _finished(self):
        if self._closing:
            self.hide()

    def clear(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                _clear_layout(item.layout())

    def open_panel(self, title):
        """Очищает панель, ставит заголовок и выдвигает её.
        Содержимое добавляется в self.content_layout после вызова."""
        self.clear()
        self.title.setText(title)
        self._closing = False
        if not self.isVisible():
            self._layout(0.0)
            self.show()
            self.raise_()
            self._anim.stop()
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(1.0)
            self._anim.start()
        self.setFocus()

    def close_panel(self):
        if not self.isVisible() or self._closing:
            return
        self._closing = True
        self._anim.stop()
        self._anim.setStartValue(self._overlay_alpha)
        self._anim.setEndValue(0.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        c = QColor(pal()["overlay"])
        c.setAlpha(int(c.alpha() * self._overlay_alpha))
        painter.fillRect(self.rect(), c)

    def mousePressEvent(self, event):
        if not self.panel.geometry().contains(event.position().toPoint()):
            self.close_panel()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close_panel()
        else:
            super().keyPressEvent(event)


def _clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            _clear_layout(item.layout())


def section_title(text):
    p = pal()
    lbl = label(text.upper(), 8, bold=True, color=p["muted"])
    lbl.setStyleSheet(lbl.styleSheet() + "letter-spacing: 1px; padding-top: 6px;")
    return lbl


def info_block(rows):
    """Белый блок «подпись — значение» для боковой панели."""
    p = pal()
    frame = QFrame()
    frame.setObjectName("infoBlock")
    frame.setStyleSheet(
        f"QFrame#infoBlock {{ background: {p['card']}; border-radius: 14px;"
        f" border: 1px solid {p['line']}; }}"
    )
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(16, 12, 16, 12)
    lay.setSpacing(8)
    for caption, value in rows:
        row = QHBoxLayout()
        row.addWidget(label(caption, 9, color=p["muted"]))
        row.addStretch()
        v = label(str(value) if value not in (None, "") else "—", 10, bold=True)
        v.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        row.addWidget(v)
        lay.addLayout(row)
    return frame


class SegmentedFilter(QWidget):
    """Переключатель-«таблетки»: Все / Врачи / Пациенты и т.п."""

    changed = Signal(str)

    def __init__(self, options):
        super().__init__()
        self._buttons = {}
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        p = pal()
        for key, text in options:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(34)
            btn.setFont(QFont(FONT, 9, QFont.Weight.DemiBold))
            btn.setStyleSheet(f"""
                QPushButton {{ background: {p['card']}; color: {p['muted']};
                    border: 1px solid {p['line']}; border-radius: 17px; padding: 4px 16px; }}
                QPushButton:hover {{ color: {p['text']}; border-color: {p['accent']}; }}
                QPushButton:checked {{ background: {p['accent']}; color: #FFFFFF;
                    border-color: {p['accent']}; }}
            """)
            btn.clicked.connect(lambda _=False, k=key: self.set_value(k))
            lay.addWidget(btn)
            self._buttons[key] = btn
        self._value = options[0][0]
        self._buttons[self._value].setChecked(True)

    def value(self):
        return self._value

    def set_value(self, key):
        self._value = key
        for k, b in self._buttons.items():
            b.setChecked(k == key)
        self.changed.emit(key)
