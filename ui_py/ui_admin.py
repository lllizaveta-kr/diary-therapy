# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'admin.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_AdminAnalyticsWindow(object):
    def setupUi(self, AdminAnalyticsWindow):
        if not AdminAnalyticsWindow.objectName():
            AdminAnalyticsWindow.setObjectName(u"AdminAnalyticsWindow")
        AdminAnalyticsWindow.resize(1280, 820)
        AdminAnalyticsWindow.setStyleSheet(u"QMainWindow { background-color: #EEF3F8; }\n"
"QLabel { color: #1A1A1A; background-color: transparent; }\n"
"QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QLineEdit::placeholder { color: #999999; }\n"
"QLineEdit:focus { border: 2px solid #2F5C8F; }\n"
"QComboBox { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QComboBox::drop-down { border: none; width: 28px; }\n"
"QComboBox QAbstractItemView { background-color: #FFFFFF; color: #1A1A1A; selection-background-color: #7A9CC6; selection-color: #FFFFFF; border: 1px solid #CCCCCC; }\n"
"QTableWidget { background-color: #FFFFFF; color: #1A1A1A; gridline-color: #EEEEEE; font-family: \"Times New Roman\"; font-size: 13px; border: 1px solid #CCCCCC; border-radius: 12px; }\n"
"QTableWidget::item { color: #1A1A1A; backgrou"
                        "nd-color: #FFFFFF; padding: 8px; }\n"
"QTableWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }\n"
"QHeaderView::section { background-color: #2F5C8F; color: #FFFFFF; padding: 10px; border: none; font-family: \"Times New Roman\"; font-size: 13px; font-weight: bold; }\n"
"QTabWidget::pane { border: none; background: transparent; }\n"
"QTabBar::tab { background: #D6E3F3; color: #1A1A1A; padding: 10px 24px; margin-right: 4px; border-top-left-radius: 10px; border-top-right-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QTabBar::tab:selected { background: #2F5C8F; color: #FFFFFF; font-weight: bold; }\n"
"QPushButton { outline: none; }\n"
"QPushButton:focus { outline: none; }")
        self.centralwidget = QWidget(AdminAnalyticsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 14)
        self.topBar = QHBoxLayout()
        self.topBar.setObjectName(u"topBar")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(22)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet(u"color: #2F5C8F; background: transparent;")

        self.topBar.addWidget(self.titleLabel)

        self.topSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBar.addItem(self.topSpacer1)

        self.logoutBtn = QPushButton(self.centralwidget)
        self.logoutBtn.setObjectName(u"logoutBtn")
        self.logoutBtn.setMinimumSize(QSize(110, 38))
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(12)
        self.logoutBtn.setFont(font1)
        self.logoutBtn.setStyleSheet(u"QPushButton { background-color: #C0504D; color: #FFFFFF; border: none; border-radius: 10px; font-weight: bold; }\n"
"QPushButton:hover { background-color: #A0403D; }\n"
"QPushButton:pressed { background-color: #803533; }")

        self.topBar.addWidget(self.logoutBtn)


        self.mainLayout.addLayout(self.topBar)

        self.subtitleLabel = QLabel(self.centralwidget)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        font2 = QFont()
        font2.setFamilies([u"Times New Roman"])
        font2.setPointSize(11)
        self.subtitleLabel.setFont(font2)
        self.subtitleLabel.setStyleSheet(u"color: #666666; background: transparent;")

        self.mainLayout.addWidget(self.subtitleLabel)

        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.tabAnalytics = QWidget()
        self.tabAnalytics.setObjectName(u"tabAnalytics")
        self.analyticsLayout = QVBoxLayout(self.tabAnalytics)
        self.analyticsLayout.setSpacing(10)
        self.analyticsLayout.setObjectName(u"analyticsLayout")
        self.chartsGridLayout = QGridLayout()
        self.chartsGridLayout.setObjectName(u"chartsGridLayout")
        self.chartsGridLayout.setHorizontalSpacing(20)
        self.chartsGridLayout.setVerticalSpacing(10)
        self.barChartFrame = QFrame(self.tabAnalytics)
        self.barChartFrame.setObjectName(u"barChartFrame")
        self.barChartFrame.setMinimumSize(QSize(0, 280))
        self.barChartFrame.setStyleSheet(u"background-color: #FFFFFF; border-radius: 12px;")
        self.barChartLayout = QVBoxLayout(self.barChartFrame)
        self.barChartLayout.setObjectName(u"barChartLayout")
        self.barChartLayout.setContentsMargins(10, 10, 10, 10)

        self.chartsGridLayout.addWidget(self.barChartFrame, 0, 0, 1, 1)

        self.pieChartFrame = QFrame(self.tabAnalytics)
        self.pieChartFrame.setObjectName(u"pieChartFrame")
        self.pieChartFrame.setMinimumSize(QSize(0, 280))
        self.pieChartFrame.setStyleSheet(u"background-color: #FFFFFF; border-radius: 12px;")
        self.pieChartLayout = QVBoxLayout(self.pieChartFrame)
        self.pieChartLayout.setObjectName(u"pieChartLayout")
        self.pieChartLayout.setContentsMargins(10, 10, 10, 10)

        self.chartsGridLayout.addWidget(self.pieChartFrame, 0, 1, 1, 1)

        self.lineChartFrame = QFrame(self.tabAnalytics)
        self.lineChartFrame.setObjectName(u"lineChartFrame")
        self.lineChartFrame.setMinimumSize(QSize(0, 280))
        self.lineChartFrame.setStyleSheet(u"background-color: #FFFFFF; border-radius: 12px;")
        self.lineChartLayout = QVBoxLayout(self.lineChartFrame)
        self.lineChartLayout.setObjectName(u"lineChartLayout")
        self.lineChartLayout.setContentsMargins(10, 10, 10, 10)

        self.chartsGridLayout.addWidget(self.lineChartFrame, 0, 2, 1, 1)

        self.barChartCheckBox = QCheckBox(self.tabAnalytics)
        self.barChartCheckBox.setObjectName(u"barChartCheckBox")
        self.barChartCheckBox.setMinimumSize(QSize(0, 35))
        font3 = QFont()
        font3.setFamilies([u"Times New Roman"])
        font3.setPointSize(13)
        self.barChartCheckBox.setFont(font3)
        self.barChartCheckBox.setStyleSheet(u"QCheckBox { color: #1A1A1A; spacing: 10px; }\n"
"QCheckBox::indicator { width: 22px; height: 22px; border: 2px solid #2F5C8F; border-radius: 4px; background-color: #FFFFFF; }\n"
"QCheckBox::indicator:checked { background-color: #2F5C8F; }")

        self.chartsGridLayout.addWidget(self.barChartCheckBox, 1, 0, 1, 1)

        self.pieChartCheckBox = QCheckBox(self.tabAnalytics)
        self.pieChartCheckBox.setObjectName(u"pieChartCheckBox")
        self.pieChartCheckBox.setMinimumSize(QSize(0, 35))
        self.pieChartCheckBox.setFont(font3)
        self.pieChartCheckBox.setStyleSheet(u"QCheckBox { color: #1A1A1A; spacing: 10px; }\n"
"QCheckBox::indicator { width: 22px; height: 22px; border: 2px solid #2F5C8F; border-radius: 4px; background-color: #FFFFFF; }\n"
"QCheckBox::indicator:checked { background-color: #2F5C8F; }")

        self.chartsGridLayout.addWidget(self.pieChartCheckBox, 1, 1, 1, 1)

        self.lineChartCheckBox = QCheckBox(self.tabAnalytics)
        self.lineChartCheckBox.setObjectName(u"lineChartCheckBox")
        self.lineChartCheckBox.setMinimumSize(QSize(0, 35))
        self.lineChartCheckBox.setFont(font3)
        self.lineChartCheckBox.setStyleSheet(u"QCheckBox { color: #1A1A1A; spacing: 10px; }\n"
"QCheckBox::indicator { width: 22px; height: 22px; border: 2px solid #2F5C8F; border-radius: 4px; background-color: #FFFFFF; }\n"
"QCheckBox::indicator:checked { background-color: #2F5C8F; }")

        self.chartsGridLayout.addWidget(self.lineChartCheckBox, 1, 2, 1, 1)


        self.analyticsLayout.addLayout(self.chartsGridLayout)

        self.exportPdfButton = QPushButton(self.tabAnalytics)
        self.exportPdfButton.setObjectName(u"exportPdfButton")
        self.exportPdfButton.setMinimumSize(QSize(0, 50))
        self.exportPdfButton.setFont(font3)
        self.exportPdfButton.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: white; border: none; border-radius: 10px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }\n"
"QPushButton:pressed { background-color: #5A7CA6; }")

        self.analyticsLayout.addWidget(self.exportPdfButton)

        self.tabs.addTab(self.tabAnalytics, "")
        self.tabAssign = QWidget()
        self.tabAssign.setObjectName(u"tabAssign")
        self.assignLayout = QVBoxLayout(self.tabAssign)
        self.assignLayout.setSpacing(14)
        self.assignLayout.setObjectName(u"assignLayout")
        self.label = QLabel(self.tabAssign)
        self.label.setObjectName(u"label")
        font4 = QFont()
        font4.setFamilies([u"Times New Roman"])
        font4.setPointSize(13)
        font4.setBold(True)
        self.label.setFont(font4)
        self.label.setStyleSheet(u"color: #2F5C8F;")

        self.assignLayout.addWidget(self.label)

        self.assignFormRow = QHBoxLayout()
        self.assignFormRow.setSpacing(12)
        self.assignFormRow.setObjectName(u"assignFormRow")
        self.assignPatientCombo = QComboBox(self.tabAssign)
        self.assignPatientCombo.setObjectName(u"assignPatientCombo")
        self.assignPatientCombo.setMinimumHeight(42)
        self.assignPatientCombo.setMinimumWidth(320)

        self.assignFormRow.addWidget(self.assignPatientCombo)

        self.assignDoctorCombo = QComboBox(self.tabAssign)
        self.assignDoctorCombo.setObjectName(u"assignDoctorCombo")
        self.assignDoctorCombo.setMinimumHeight(42)
        self.assignDoctorCombo.setMinimumWidth(320)

        self.assignFormRow.addWidget(self.assignDoctorCombo)

        self.assignBtn = QPushButton(self.tabAssign)
        self.assignBtn.setObjectName(u"assignBtn")
        self.assignBtn.setMinimumSize(QSize(220, 42))
        self.assignBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: white; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #1E4470; }\n"
"QPushButton:pressed { background-color: #163257; }")

        self.assignFormRow.addWidget(self.assignBtn)

        self.assignSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.assignFormRow.addItem(self.assignSpacer)


        self.assignLayout.addLayout(self.assignFormRow)

        self.label1 = QLabel(self.tabAssign)
        self.label1.setObjectName(u"label1")
        self.label1.setFont(font1)

        self.assignLayout.addWidget(self.label1)

        self.assignTable = QTableWidget(self.tabAssign)
        self.assignTable.setObjectName(u"assignTable")

        self.assignLayout.addWidget(self.assignTable)

        self.tabs.addTab(self.tabAssign, "")
        self.tabUsers = QWidget()
        self.tabUsers.setObjectName(u"tabUsers")
        self.usersLayout = QVBoxLayout(self.tabUsers)
        self.usersLayout.setSpacing(12)
        self.usersLayout.setObjectName(u"usersLayout")
        self.formLayout = QHBoxLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName(u"formLayout")
        self.loginLine = QLineEdit(self.tabUsers)
        self.loginLine.setObjectName(u"loginLine")
        self.loginLine.setMinimumHeight(40)

        self.formLayout.addWidget(self.loginLine)

        self.passwordLine = QLineEdit(self.tabUsers)
        self.passwordLine.setObjectName(u"passwordLine")
        self.passwordLine.setMinimumHeight(40)

        self.formLayout.addWidget(self.passwordLine)

        self.fullNameLine = QLineEdit(self.tabUsers)
        self.fullNameLine.setObjectName(u"fullNameLine")
        self.fullNameLine.setMinimumHeight(40)

        self.formLayout.addWidget(self.fullNameLine)

        self.roleCombo = QComboBox(self.tabUsers)
        self.roleCombo.addItem("")
        self.roleCombo.addItem("")
        self.roleCombo.addItem("")
        self.roleCombo.setObjectName(u"roleCombo")
        self.roleCombo.setMinimumHeight(40)

        self.formLayout.addWidget(self.roleCombo)

        self.addBtn = QPushButton(self.tabUsers)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMinimumSize(QSize(130, 40))
        self.addBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: white; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #1E4470; }\n"
"QPushButton:pressed { background-color: #163257; }")

        self.formLayout.addWidget(self.addBtn)


        self.usersLayout.addLayout(self.formLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setSpacing(10)
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.generateBtn = QPushButton(self.tabUsers)
        self.generateBtn.setObjectName(u"generateBtn")
        self.generateBtn.setMinimumSize(QSize(240, 40))
        self.generateBtn.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: white; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }\n"
"QPushButton:pressed { background-color: #5A7CA6; }")

        self.buttonsLayout.addWidget(self.generateBtn)

        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonsLayout.addItem(self.spacer1)

        self.resetPasswordBtn = QPushButton(self.tabUsers)
        self.resetPasswordBtn.setObjectName(u"resetPasswordBtn")
        self.resetPasswordBtn.setMinimumSize(QSize(180, 40))
        self.resetPasswordBtn.setStyleSheet(u"QPushButton { background-color: #F2994A; color: white; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #E0842F; }\n"
"QPushButton:pressed { background-color: #C07020; }")

        self.buttonsLayout.addWidget(self.resetPasswordBtn)

        self.deleteBtn = QPushButton(self.tabUsers)
        self.deleteBtn.setObjectName(u"deleteBtn")
        self.deleteBtn.setMinimumSize(QSize(160, 40))
        self.deleteBtn.setStyleSheet(u"QPushButton { background-color: #C0504D; color: white; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #A0403D; }\n"
"QPushButton:pressed { background-color: #803533; }")

        self.buttonsLayout.addWidget(self.deleteBtn)


        self.usersLayout.addLayout(self.buttonsLayout)

        self.usersTable = QTableWidget(self.tabUsers)
        self.usersTable.setObjectName(u"usersTable")

        self.usersLayout.addWidget(self.usersTable)

        self.tabs.addTab(self.tabUsers, "")

        self.mainLayout.addWidget(self.tabs)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        font5 = QFont()
        font5.setFamilies([u"Times New Roman"])
        font5.setPointSize(10)
        self.statusLabel.setFont(font5)
        self.statusLabel.setStyleSheet(u"color: #666666; padding: 4px 8px; background: transparent;")

        self.mainLayout.addWidget(self.statusLabel)

        AdminAnalyticsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AdminAnalyticsWindow)

        QMetaObject.connectSlotsByName(AdminAnalyticsWindow)
    # setupUi

    def retranslateUi(self, AdminAnalyticsWindow):
        AdminAnalyticsWindow.setWindowTitle(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041e\u043a\u043d\u043e \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u0430", None))
        self.titleLabel.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u0430", None))
        self.logoutBtn.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.subtitleLabel.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041e\u0431\u0437\u043e\u0440 \u043a\u043b\u044e\u0447\u0435\u0432\u044b\u0445 \u043c\u0435\u0442\u0440\u0438\u043a \u0432 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u0432\u0440\u0435\u043c\u0435\u043d\u0438", None))
        self.barChartCheckBox.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0441\u0442\u043e\u043b\u0431\u0447\u0430\u0442\u0443\u044e", None))
        self.pieChartCheckBox.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043a\u0440\u0443\u0433\u043e\u0432\u0443\u044e", None))
        self.lineChartCheckBox.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043b\u0438\u043d\u0435\u0439\u043d\u0443\u044e", None))
        self.exportPdfButton.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0432 PDF", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabAnalytics), QCoreApplication.translate("AdminAnalyticsWindow", u"\u0410\u043d\u0430\u043b\u0438\u0442\u0438\u043a\u0430", None))
        self.label.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430 \u0438 \u0432\u0440\u0430\u0447\u0430 \u0434\u043b\u044f \u043f\u0440\u0438\u043a\u0440\u0435\u043f\u043b\u0435\u043d\u0438\u044f", None))
        self.assignBtn.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041f\u0440\u0438\u043a\u0440\u0435\u043f\u0438\u0442\u044c \u043a \u0432\u0440\u0430\u0447\u0443", None))
        self.label1.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0422\u0435\u043a\u0443\u0449\u0435\u0435 \u0440\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435:", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabAssign), QCoreApplication.translate("AdminAnalyticsWindow", u"\u041f\u0440\u0438\u043a\u0440\u0435\u043f\u043b\u0435\u043d\u0438\u0435 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u043e\u0432", None))
        self.loginLine.setPlaceholderText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.passwordLine.setPlaceholderText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.fullNameLine.setPlaceholderText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0424\u0418\u041e", None))
        self.roleCombo.setItemText(0, QCoreApplication.translate("AdminAnalyticsWindow", u"doctor", None))
        self.roleCombo.setItemText(1, QCoreApplication.translate("AdminAnalyticsWindow", u"patient", None))
        self.roleCombo.setItemText(2, QCoreApplication.translate("AdminAnalyticsWindow", u"admin", None))

        self.addBtn.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.generateBtn.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043b\u043e\u0433\u0438\u043d \u0438 \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.resetPasswordBtn.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.deleteBtn.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0433\u043e", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabUsers), QCoreApplication.translate("AdminAnalyticsWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c\u0438", None))
        self.statusLabel.setText(QCoreApplication.translate("AdminAnalyticsWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f...", None))
    # retranslateUi

