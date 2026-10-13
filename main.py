import sys
from PySide6.QtWidgets import QApplication
from windows.login_window import LoginWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("DiaryTherapy")
    app.setApplicationName("App")

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
