import random
import hashlib
import mysql.connector
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QApplication, QWidget,
)
from PySide6.QtGui import QPixmap, QPainter, QColor, QPen
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    Property,
)

from ui_py.ui_login import Ui_LoginWindow
from windows import msgbox as mb
from config import DB_CONFIG
import theme
from path import images_path


class Bubble(QWidget):
    def __init__(self, parent, area_w, area_h, on_pop=None):
        super().__init__(parent)
        self.on_pop = on_pop
        self.area_w = area_w
        self.area_h = area_h
        self._opacity = 1.0

        size = random.randint(20, 70)
        self.resize(size, size)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.vy = random.uniform(0.4, 1.4)
        self.vx = random.uniform(-0.25, 0.25)
        self.move(
            random.randint(0, max(1, area_w - size)),
            area_h + random.randint(0, 200)
        )
        self.popping = False

    def _get_opacity(self):
        return self._opacity

    def _set_opacity(self, value):
        self._opacity = value
        self.update()

    opacity = Property(float, _get_opacity, _set_opacity)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        if w < 2 or h < 2:
            return
        op = self._opacity
        dark = theme.is_dark()
        if dark:
            main = QColor(80, 100, 140, int(90 * op))
            border = QColor(120, 140, 180, int(180 * op))
            shine = QColor(180, 200, 240, int(180 * op))
        else:
            main = QColor(200, 200, 205, int(90 * op))
            border = QColor(230, 230, 235, int(180 * op))
            shine = QColor(255, 255, 255, int(220 * op))
        p.setBrush(main)
        p.setPen(QPen(border, max(1, w // 40)))
        p.drawEllipse(2, 2, w - 4, h - 4)
        p.setBrush(shine)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(int(w * 0.25), int(h * 0.18),
                      int(w * 0.22), int(h * 0.18))

    def step(self):
        if self.popping:
            return
        x = self.x() + self.vx
        y = self.y() - self.vy
        if y < -self.height():
            x = random.randint(0, max(1, self.area_w - self.width()))
            y = self.area_h + random.randint(0, 150)
        self.move(int(x), int(y))

    def mousePressEvent(self, event):
        if self.popping:
            return
        self.pop()

    def pop(self):
        self.popping = True
        cx = self.x() + self.width() // 2
        cy = self.y() + self.height() // 2
        start_geom = self.geometry()
        new_w = int(self.width() * 2.2)
        new_h = int(self.height() * 2.2)
        end_geom = start_geom
        end_geom.setRect(cx - new_w // 2, cy - new_h // 2, new_w, new_h)

        geom_anim = QPropertyAnimation(self, b"geometry", self)
        geom_anim.setDuration(300)
        geom_anim.setStartValue(start_geom)
        geom_anim.setEndValue(end_geom)
        geom_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        opacity_anim = QPropertyAnimation(self, b"opacity", self)
        opacity_anim.setDuration(300)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        group = QParallelAnimationGroup(self)
        group.addAnimation(geom_anim)
        group.addAnimation(opacity_anim)

        def finish():
            if self.on_pop:
                self.on_pop(self)
            self.deleteLater()

        group.finished.connect(finish)
        group.start()
        self._group = group


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setFixedSize(900, 600)

        self.ui.gridLayout.setColumnStretch(0, 1)
        self.ui.gridLayout.setColumnStretch(1, 3)
        self.ui.gridLayout.setColumnStretch(2, 1)

        self.ui.leftBubblesLabel.setScaledContents(False)
        self.ui.rightBubblesLabel.setScaledContents(False)

        pix_left = QPixmap(images_path("bubbles_left.png"))
        if not pix_left.isNull():
            self.ui.leftBubblesLabel.setPixmap(
                pix_left.scaledToHeight(560,
                                        Qt.TransformationMode.SmoothTransformation)
            )
        pix_right = QPixmap(images_path("bubbles_right.png"))
        if not pix_right.isNull():
            self.ui.rightBubblesLabel.setPixmap(
                pix_right.scaledToHeight(560,
                                         Qt.TransformationMode.SmoothTransformation)
            )

        self.bubbles = []
        self.bubble_timer = QTimer(self)
        self.bubble_timer.timeout.connect(self.tick_bubbles)
        self.spawn_bubbles(20)
        self.bubble_timer.start(30)

        self.child_window = None

        self.ui.btnEnter.clicked.connect(self.on_login)
        self.ui.loginLine.returnPressed.connect(self.on_login)
        self.ui.passwrdLine.returnPressed.connect(self.on_login)
        self.ui.forgotPasswordBtn.clicked.connect(self.on_forgot_password)

        theme.apply_to_window(self, theme.is_dark())

        self.theme_btn = QPushButton(self)
        self.theme_btn.setText("☀️" if theme.is_dark() else "🌙")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setGeometry(852, 12, 36, 36)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(120, 130, 160, 100);
                border: none;
                border-radius: 18px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: rgba(120, 130, 160, 160);
            }
        """)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.raise_()

    def toggle_theme(self):
        new_dark = theme.toggle(QApplication.instance())
        self.theme_btn.setText("☀️" if new_dark else "🌙")
        for b in self.bubbles:
            b.update()

    def spawn_bubbles(self, count):
        for _ in range(count):
            b = Bubble(self, self.width(), self.height(), on_pop=self.on_bubble_popped)
            b.raise_()
            b.show()
            self.bubbles.append(b)

    def on_bubble_popped(self, bubble):
        if bubble in self.bubbles:
            self.bubbles.remove(bubble)
        new_b = Bubble(self, self.width(), self.height(), on_pop=self.on_bubble_popped)
        new_b.show()
        self.bubbles.append(new_b)

    def tick_bubbles(self):
        for b in self.bubbles:
            b.step()

    def on_forgot_password(self):
        mb.info(self, "Восстановление пароля",
                "Если вы забыли пароль — обратитесь к администратору.\n\n"
                "Администратор может сбросить ваш пароль через раздел\n"
                "«Управление пользователями» и выдать новый.")

    def on_login(self):
        login = self.ui.loginLine.text().strip()
        password = self.ui.passwrdLine.text().strip()

        if not login and not password:
            mb.warning(self, "Заполните форму",
                       "Введите логин и пароль для входа.")
            self.ui.loginLine.setFocus()
            return

        if not login:
            mb.warning(self, "Не указан логин",
                       "Введите ваш логин.\n\n"
                       "Если не знаете логин — обратитесь к администратору.")
            self.ui.loginLine.setFocus()
            return

        if not password:
            mb.warning(self, "Не указан пароль",
                       "Введите ваш пароль.\n\n"
                       "Если забыли — нажмите «Забыли пароль?».")
            self.ui.passwrdLine.setFocus()
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # ДОБАВИЛИ u.id_user В ЗАПРОС
            query = """
                SELECT u.id_user, u.password_hash, r.name_role, u.full_name 
                FROM users u 
                JOIN roles r ON u.id_role = r.id_role 
                WHERE u.login = %s
            """
            cursor.execute(query, (login,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                id_user = result[0]
                db_hash = str(result[1]).strip()
                role = result[2]
                full_name = result[3]
                input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

                if db_hash == input_hash:
                    # ПЕРЕДАЕМ id_user В СЛОВАРЕ
                    user = {
                        "id_user": id_user,
                        "role": role,
                        "full_name": full_name
                    }

                    if role == "admin":
                        from windows.admin_window import AdminAnalyticsWindow
                        self.child_window = AdminAnalyticsWindow(user["full_name"], self)
                        self.child_window.show()
                        self.hide()
                    elif role == "doctor":
                        from windows.doctor_window import DoctorWindow
                        self.child_window = DoctorWindow(user, self)
                        self.child_window.show()
                        self.hide()
                    elif role == "patient":
                        from windows.patient_window import PatientWindow
                        self.child_window = PatientWindow(user, self)
                        self.child_window.show()
                        self.hide()
                    else:
                        mb.warning(self, "Ошибка роли",
                                   f"Пользователь имеет неизвестную роль: {role}.\n\n"
                                   f"Обратитесь к администратору.")
                    return

            mb.warning(self, "Неверный логин или пароль",
                       "Проверьте раскладку клавиатуры и регистр букв.\n\n"
                       "Если забыли пароль — обратитесь к администратору.")
            self.ui.passwrdLine.selectAll()
            self.ui.passwrdLine.setFocus()

        except mysql.connector.Error as err:
            mb.critical(self, "Нет связи с базой данных",
                        f"Приложение не может подключиться к MySQL.\n\n"
                        f"Возможные причины:\n"
                        f"• Сервер MySQL не запущен\n"
                        f"• Неверный пароль в config.py\n"
                        f"• База данных не создана\n\n"
                        f"Техническая информация:\n{str(err)[:100]}")

    def return_from_child(self):
        self.ui.loginLine.clear()
        self.ui.passwrdLine.clear()
        self.child_window = None
        self.show()
        theme.apply_to_window(self, theme.is_dark())