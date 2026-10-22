from PySide6.QtWidgets import QMessageBox, QPushButton

BUTTON_STYLE = """
QPushButton {
    background-color: #2F5C8F;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 30px;
    min-width: 100px;
    min-height: 34px;
    font-family: "Times New Roman";
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover { background-color: #1E4470; }
QPushButton:pressed { background-color: #163257; }
"""

BOX_STYLE = """
QMessageBox { background-color: #FFFFFF; }
QMessageBox QLabel {
    color: #1A1A1A;
    font-family: "Times New Roman";
    font-size: 14px;
    background-color: transparent;
}
"""


def _style(box):
    box.setStyleSheet(BOX_STYLE)
    for btn in box.findChildren(QPushButton):
        btn.setStyleSheet(BUTTON_STYLE)


def info(parent, title, text):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Information)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    _style(box)
    return box.exec()


def warning(parent, title, text):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    _style(box)
    return box.exec()


def critical(parent, title, text):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Critical)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    _style(box)
    return box.exec()


def confirm(parent, title, text):
    """Вопрос Да/Нет в общем стиле. Возвращает True, если нажали «Да»."""
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Question)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    box.setDefaultButton(QMessageBox.StandardButton.No)
    box.button(QMessageBox.StandardButton.Yes).setText("Да")
    box.button(QMessageBox.StandardButton.No).setText("Нет")
    _style(box)
    return box.exec() == QMessageBox.StandardButton.Yes
