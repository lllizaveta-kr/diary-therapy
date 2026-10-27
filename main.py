import sys

from PySide6.QtWidgets import QApplication

from windows.login_window import LoginWindow
from logger import setup_logging
setup_logging()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("DiaryTherapy")
    app.setApplicationName("App")

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
