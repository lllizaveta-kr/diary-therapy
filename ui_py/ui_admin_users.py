# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'admin_users.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_AdminUsersWindow(object):
    def setupUi(self, AdminUsersWindow):
        if not AdminUsersWindow.objectName():
            AdminUsersWindow.setObjectName(u"AdminUsersWindow")
        AdminUsersWindow.resize(1000, 600)
        AdminUsersWindow.setStyleSheet(u"QMainWindow { background-color: #F5F5F5; }\n"
"QLabel { color: #1A1A1A; background-color: transparent; }\n"
"QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QLineEdit::placeholder { color: #888888; }\n"
"QComboBox { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QComboBox::drop-down { border: none; width: 24px; }\n"
"QComboBox QAbstractItemView { background-color: #FFFFFF; color: #1A1A1A; selection-background-color: #7A9CC6; selection-color: #FFFFFF; border: 1px solid #CCCCCC; outline: none; }\n"
"QComboBox QAbstractItemView::item { color: #1A1A1A; background-color: #FFFFFF; padding: 6px 10px; }\n"
"QComboBox QAbstractItemView::item:selected { background-color: #7A9CC6; color: #FFFFFF; }\n"
"QTableWidget { background-color: #FFFFFF; color: #1A1A1A; gridline-color: #"
                        "DDDDDD; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QTableWidget::item { color: #1A1A1A; background-color: #FFFFFF; }\n"
"QTableWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }\n"
"QHeaderView::section { background-color: #2F5C8F; color: #FFFFFF; padding: 6px; border: none; }")
        self.centralwidget = QWidget(AdminUsersWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(18)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet(u"color: #2F5C8F; background-color: transparent;")

        self.mainLayout.addWidget(self.titleLabel)

        self.formLayout = QHBoxLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.loginLine = QLineEdit(self.centralwidget)
        self.loginLine.setObjectName(u"loginLine")
        self.loginLine.setMinimumHeight(35)

        self.formLayout.addWidget(self.loginLine)

        self.passwordLine = QLineEdit(self.centralwidget)
        self.passwordLine.setObjectName(u"passwordLine")
        self.passwordLine.setMinimumHeight(35)

        self.formLayout.addWidget(self.passwordLine)

        self.fullNameLine = QLineEdit(self.centralwidget)
        self.fullNameLine.setObjectName(u"fullNameLine")
        self.fullNameLine.setMinimumHeight(35)

        self.formLayout.addWidget(self.fullNameLine)

        self.roleCombo = QComboBox(self.centralwidget)
        self.roleCombo.addItem("")
        self.roleCombo.addItem("")
        self.roleCombo.addItem("")
        self.roleCombo.setObjectName(u"roleCombo")
        self.roleCombo.setMinimumHeight(35)

        self.formLayout.addWidget(self.roleCombo)

        self.addBtn = QPushButton(self.centralwidget)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMinimumSize(QSize(120, 35))
        self.addBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: white; border: none; border-radius: 6px; } QPushButton:hover { background-color: #1E4470; }")

        self.formLayout.addWidget(self.addBtn)


        self.mainLayout.addLayout(self.formLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.generateBtn = QPushButton(self.centralwidget)
        self.generateBtn.setObjectName(u"generateBtn")
        self.generateBtn.setMinimumSize(QSize(220, 35))
        self.generateBtn.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: white; border: none; border-radius: 6px; } QPushButton:hover { background-color: #6A8CB6; }")

        self.buttonsLayout.addWidget(self.generateBtn)

        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonsLayout.addItem(self.spacer1)

        self.deleteBtn = QPushButton(self.centralwidget)
        self.deleteBtn.setObjectName(u"deleteBtn")
        self.deleteBtn.setMinimumSize(QSize(160, 35))
        self.deleteBtn.setStyleSheet(u"QPushButton { background-color: #C0504D; color: white; border: none; border-radius: 6px; } QPushButton:hover { background-color: #A0403D; }")

        self.buttonsLayout.addWidget(self.deleteBtn)


        self.mainLayout.addLayout(self.buttonsLayout)

        self.usersTable = QTableWidget(self.centralwidget)
        self.usersTable.setObjectName(u"usersTable")

        self.mainLayout.addWidget(self.usersTable)

        AdminUsersWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AdminUsersWindow)

        QMetaObject.connectSlotsByName(AdminUsersWindow)
    # setupUi

    def retranslateUi(self, AdminUsersWindow):
        AdminUsersWindow.setWindowTitle(QCoreApplication.translate("AdminUsersWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c\u0438", None))
        self.titleLabel.setText(QCoreApplication.translate("AdminUsersWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c\u0438", None))
        self.loginLine.setPlaceholderText(QCoreApplication.translate("AdminUsersWindow", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.passwordLine.setPlaceholderText(QCoreApplication.translate("AdminUsersWindow", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.fullNameLine.setPlaceholderText(QCoreApplication.translate("AdminUsersWindow", u"\u0424\u0418\u041e", None))
        self.roleCombo.setItemText(0, QCoreApplication.translate("AdminUsersWindow", u"doctor", None))
        self.roleCombo.setItemText(1, QCoreApplication.translate("AdminUsersWindow", u"patient", None))
        self.roleCombo.setItemText(2, QCoreApplication.translate("AdminUsersWindow", u"admin", None))

        self.addBtn.setText(QCoreApplication.translate("AdminUsersWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.generateBtn.setText(QCoreApplication.translate("AdminUsersWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043b\u043e\u0433\u0438\u043d \u0438 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.deleteBtn.setText(QCoreApplication.translate("AdminUsersWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0433\u043e", None))
    # retranslateUi

