# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.resize(900, 600)
        LoginWindow.setStyleSheet(u"QMainWindow { background-color: #EEF3F8; }\n"
"QLabel { color: #1A1A1A; background-color: transparent; }\n"
"QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 14px; }\n"
"QLineEdit::placeholder { color: #999999; }\n"
"QLineEdit:focus { border: 2px solid #2F5C8F; }\n"
"QPushButton { outline: none; }\n"
"QPushButton:focus { outline: none; }")
        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.leftBubblesFrame = QFrame(self.centralwidget)
        self.leftBubblesFrame.setObjectName(u"leftBubblesFrame")
        self.leftBubblesFrame.setMinimumSize(QSize(120, 0))
        self.leftBubblesFrame.setMaximumSize(QSize(180, 16777215))
        self.leftBubblesFrame.setStyleSheet(u"background-color: transparent; border: none;")
        self.leftBubblesLayout = QVBoxLayout(self.leftBubblesFrame)
        self.leftBubblesLayout.setObjectName(u"leftBubblesLayout")
        self.leftBubblesLayout.setContentsMargins(0, 0, 0, 0)
        self.leftBubblesLabel = QLabel(self.leftBubblesFrame)
        self.leftBubblesLabel.setObjectName(u"leftBubblesLabel")
        self.leftBubblesLabel.setAlignment(Qt.AlignCenter)

        self.leftBubblesLayout.addWidget(self.leftBubblesLabel)


        self.gridLayout.addWidget(self.leftBubblesFrame, 0, 0, 1, 1)

        self.centerLayout = QVBoxLayout()
        self.centerLayout.setSpacing(14)
        self.centerLayout.setObjectName(u"centerLayout")
        self.centerLayout.setContentsMargins(80, 50, 80, 50)
        self.topSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.centerLayout.addItem(self.topSpacer)

        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(40)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet(u"color: #2F5C8F; background-color: transparent;")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.centerLayout.addWidget(self.titleLabel)

        self.welcomeLabel = QLabel(self.centralwidget)
        self.welcomeLabel.setObjectName(u"welcomeLabel")
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(12)
        self.welcomeLabel.setFont(font1)
        self.welcomeLabel.setStyleSheet(u"color: #666666; background-color: transparent;")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setWordWrap(True)

        self.centerLayout.addWidget(self.welcomeLabel)

        self.middleSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.centerLayout.addItem(self.middleSpacer)

        self.loginLine = QLineEdit(self.centralwidget)
        self.loginLine.setObjectName(u"loginLine")
        self.loginLine.setMinimumSize(QSize(0, 46))

        self.centerLayout.addWidget(self.loginLine)

        self.passwrdLine = QLineEdit(self.centralwidget)
        self.passwrdLine.setObjectName(u"passwrdLine")
        self.passwrdLine.setMinimumSize(QSize(0, 46))
        self.passwrdLine.setEchoMode(QLineEdit.Password)

        self.centerLayout.addWidget(self.passwrdLine)

        self.forgotLayout = QHBoxLayout()
        self.forgotLayout.setObjectName(u"forgotLayout")
        self.forgotLeftSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.forgotLayout.addItem(self.forgotLeftSpacer)

        self.forgotPasswordBtn = QPushButton(self.centralwidget)
        self.forgotPasswordBtn.setObjectName(u"forgotPasswordBtn")
        self.forgotPasswordBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.forgotPasswordBtn.setStyleSheet(u"QPushButton { background-color: transparent; color: #2F5C8F; border: none; text-decoration: underline; font-family: \"Times New Roman\"; font-size: 12px; padding: 4px; }\n"
"QPushButton:hover { color: #1E4470; }\n"
"QPushButton:focus { outline: none; }")

        self.forgotLayout.addWidget(self.forgotPasswordBtn)

        self.forgotRightSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.forgotLayout.addItem(self.forgotRightSpacer)


        self.centerLayout.addLayout(self.forgotLayout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonLeftSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.buttonLeftSpacer)

        self.btnEnter = QPushButton(self.centralwidget)
        self.btnEnter.setObjectName(u"btnEnter")
        self.btnEnter.setMinimumSize(QSize(200, 52))
        self.btnEnter.setMaximumSize(QSize(200, 52))
        font2 = QFont()
        font2.setFamilies([u"Times New Roman"])
        font2.setPointSize(16)
        font2.setBold(True)
        self.btnEnter.setFont(font2)
        self.btnEnter.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; padding: 0px; }\n"
"QPushButton:hover { background-color: #1E4470; }\n"
"QPushButton:pressed { background-color: #163257; }\n"
"QPushButton:focus { outline: none; }")

        self.buttonLayout.addWidget(self.btnEnter)

        self.buttonRightSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.buttonRightSpacer)


        self.centerLayout.addLayout(self.buttonLayout)

        self.bottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.centerLayout.addItem(self.bottomSpacer)


        self.gridLayout.addLayout(self.centerLayout, 0, 1, 1, 1)

        self.rightBubblesFrame = QFrame(self.centralwidget)
        self.rightBubblesFrame.setObjectName(u"rightBubblesFrame")
        self.rightBubblesFrame.setMinimumSize(QSize(120, 0))
        self.rightBubblesFrame.setMaximumSize(QSize(180, 16777215))
        self.rightBubblesFrame.setStyleSheet(u"background-color: transparent; border: none;")
        self.rightBubblesLayout = QVBoxLayout(self.rightBubblesFrame)
        self.rightBubblesLayout.setObjectName(u"rightBubblesLayout")
        self.rightBubblesLayout.setContentsMargins(0, 0, 0, 0)
        self.rightBubblesLabel = QLabel(self.rightBubblesFrame)
        self.rightBubblesLabel.setObjectName(u"rightBubblesLabel")
        self.rightBubblesLabel.setAlignment(Qt.AlignCenter)

        self.rightBubblesLayout.addWidget(self.rightBubblesLabel)


        self.gridLayout.addWidget(self.rightBubblesFrame, 0, 2, 1, 1)

        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f", None))
        self.leftBubblesLabel.setText("")
        self.titleLabel.setText(QCoreApplication.translate("LoginWindow", u"\u0414\u041d\u0415\u0412\u041d\u0418\u041a\n"
"\u0422\u0415\u0420\u0410\u041f\u0418\u0418", None))
        self.welcomeLabel.setText(QCoreApplication.translate("LoginWindow", u"\u0412\u043e\u0439\u0434\u0438\u0442\u0435 \u0432 \u0441\u0438\u0441\u0442\u0435\u043c\u0443, \u0447\u0442\u043e\u0431\u044b \u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u0442\u0435\u0440\u0430\u043f\u0438\u0438", None))
        self.loginLine.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043b\u043e\u0433\u0438\u043d", None))
        self.passwrdLine.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.forgotPasswordBtn.setText(QCoreApplication.translate("LoginWindow", u"\u0417\u0430\u0431\u044b\u043b\u0438 \u043f\u0430\u0440\u043e\u043b\u044c?", None))
        self.btnEnter.setText(QCoreApplication.translate("LoginWindow", u"\u0412\u043e\u0439\u0442\u0438", None))
        self.rightBubblesLabel.setText("")
    # retranslateUi

