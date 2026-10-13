from PySide6.QtWidgets import QApplication, QWidget, QTableWidget
from PySide6.QtCore import Qt, QSettings


COLOR_MAP = {
    "#EEF3F8": "#1A1F2B",
    "#F5F5F5": "#1A1F2B",
    "#FFFFFF": "#232936",
    "#FAFAFA": "#232936",
    "#1A1A1A": "#E8EAF0",
    "#666666": "#A8B0C0",
    "#999999": "#7880A0",
    "#D6E3F3": "#2F3A4A",
    "#888888": "#7880A0",
    "#2F5C8F": "#4A90D9",
    "#7A9CC6": "#6BA3D9",
    "#1E4470": "#3A7BBF",
    "#163257": "#2F66A0",
    "#CCCCCC": "#3A4250",
    "#E5EAF0": "#2A3140",
    "#EEEEEE": "#2A3140",
    "#C0504D": "#D9534F",
    "#A0403D": "#C44A47",
    "#803533": "#B04340",
    "#F2994A": "#F0A96A",
    "#E0842F": "#D89050",
    "#C07020": "#B06020",
    "#F0F4FA": "#2A3140",
    "#E0E0E0": "#3A4250",
    "#D0D0D0": "#4A5260",
    "#C0C0C0": "#5A6270",
}


TABLE_QSS_TEMPLATE = """
QTableWidget {
    background-color: __BG__;
    color: __FG__;
    gridline-color: __GRID__;
    border: 1px solid __BORDER__;
    border-radius: 10px;
    outline: none;
}
QTableWidget::item {
    background-color: __BG__;
    color: __FG__;
    padding: 8px;
    border: none;
}
QTableWidget::item:hover {
    background-color: __HOVER__;
    color: __FG__;
}
QTableWidget::item:selected {
    background-color: __SEL_BG__;
    color: __SEL_FG__;
}
QTableWidget::item:focus {
    background-color: __BG__;
    color: __FG__;
    border: none;
}
QHeaderView {
    background-color: __HEAD_BG__;
    border: none;
}
QHeaderView::section {
    background-color: __HEAD_BG__;
    color: __HEAD_FG__;
    padding: 10px;
    border: none;
    font-weight: bold;
}
QHeaderView::section:hover {
    background-color: __HEAD_BG__;
}
QTableCornerButton::section {
    background-color: __HEAD_BG__;
    border: none;
}
QScrollBar:vertical, QScrollBar:horizontal {
    background: __SCROLL_BG__;
    border: none;
    width: 10px;
    height: 10px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: __SCROLL_HANDLE__;
    border-radius: 5px;
    min-height: 20px;
    min-width: 20px;
}
QScrollBar::handle:hover {
    background: __SCROLL_HANDLE_HOVER__;
}
QScrollBar::add-line, QScrollBar::sub-line {
    background: none;
    height: 0px;
    width: 0px;
}
QScrollBar::add-page, QScrollBar::sub-page {
    background: none;
}
"""


def _table_qss(dark: bool) -> str:
    if dark:
        values = {
            "__BG__": "#232936",
            "__FG__": "#E8EAF0",
            "__GRID__": "#2A3140",
            "__BORDER__": "#3A4250",
            "__HOVER__": "#2F3A50",
            "__SEL_BG__": "#4A90D9",
            "__SEL_FG__": "#FFFFFF",
            "__HEAD_BG__": "#2F5C8F",
            "__HEAD_FG__": "#FFFFFF",
            "__SCROLL_BG__": "#1E2430",
            "__SCROLL_HANDLE__": "#4A6080",
            "__SCROLL_HANDLE_HOVER__": "#5A7090",
        }
    else:
        values = {
            "__BG__": "#FFFFFF",
            "__FG__": "#1A1A1A",
            "__GRID__": "#EEEEEE",
            "__BORDER__": "#CCCCCC",
            "__HOVER__": "#F0F4FA",
            "__SEL_BG__": "#7A9CC6",
            "__SEL_FG__": "#FFFFFF",
            "__HEAD_BG__": "#2F5C8F",
            "__HEAD_FG__": "#FFFFFF",
            "__SCROLL_BG__": "#F0F0F0",
            "__SCROLL_HANDLE__": "#B0B0B0",
            "__SCROLL_HANDLE_HOVER__": "#909090",
        }

    result = TABLE_QSS_TEMPLATE
    for key, val in values.items():
        result = result.replace(key, val)
    return result


def _darken(style: str) -> str:
    if not style:
        return style
    result = style
    for light, dark in COLOR_MAP.items():
        result = result.replace(light, dark)
    return result


_ORIGINAL_STYLES = {}


def _walk(widget):
    yield widget
    for child in widget.findChildren(
        QWidget,
        options=Qt.FindChildOption.FindDirectChildrenOnly,
    ):
        yield from _walk(child)


def _apply_to_widget(widget, dark):
    for w in _walk(widget):
        key = id(w)
        if key not in _ORIGINAL_STYLES:
            _ORIGINAL_STYLES[key] = w.styleSheet() or ""
        orig = _ORIGINAL_STYLES[key]

        if isinstance(w, QTableWidget):
            base = orig + "\n" + _table_qss(dark)
            w.setStyleSheet(base)
            w.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            w.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            continue

        new_style = _darken(orig) if dark else orig
        w.setStyleSheet(new_style)


def apply_to_window(window, dark: bool):
    _apply_to_widget(window, dark)


def apply_globally(app, dark: bool):
    for w in app.topLevelWidgets():
        _apply_to_widget(w, dark)
    settings = QSettings("DiaryTherapy", "App")
    settings.setValue("dark_theme", dark)


def is_dark() -> bool:
    settings = QSettings("DiaryTherapy", "App")
    return settings.value("dark_theme", False, type=bool)


def toggle(app) -> bool:
    new_value = not is_dark()
    apply_globally(app, new_value)
    return new_value