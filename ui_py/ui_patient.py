# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'patient.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_PatientWindow(object):
    def setupUi(self, PatientWindow):
        if not PatientWindow.objectName():
            PatientWindow.setObjectName(u"PatientWindow")
        PatientWindow.resize(1280, 800)
        PatientWindow.setStyleSheet(u"QMainWindow { background-color: #EEF3F8; }\n"
"QLabel { color: #1A1A1A; background-color: transparent; }\n"
"QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QLineEdit::placeholder { color: #999999; }\n"
"QLineEdit:focus { border: 2px solid #2F5C8F; }\n"
"QTextEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QTextEdit::placeholder { color: #999999; }\n"
"QComboBox { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QComboBox::drop-down { border: none; width: 28px; }\n"
"QComboBox QAbstractItemView { background-color: #FFFFFF; color: #1A1A1A; selection-background-color: #7A9CC6; selection-color: #FFFFFF; border: 1px solid #CCCCCC; }\n"
"QTable"
                        "Widget { background-color: #FFFFFF; color: #1A1A1A; gridline-color: #EEEEEE; font-family: \"Times New Roman\"; font-size: 13px; border: 1px solid #CCCCCC; border-radius: 12px; }\n"
"QTableWidget::item { color: #1A1A1A; background-color: #FFFFFF; padding: 8px; }\n"
"QTableWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }\n"
"QHeaderView::section { background-color: #2F5C8F; color: #FFFFFF; padding: 10px; border: none; font-family: \"Times New Roman\"; font-size: 13px; font-weight: bold; }\n"
"QStackedWidget > QWidget { background-color: #EEF3F8; }\n"
"QCheckBox { color: #1A1A1A; font-family: \"Times New Roman\"; font-size: 13px; spacing: 8px; background: transparent; }\n"
"QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #2F5C8F; border-radius: 4px; background-color: #FFFFFF; }\n"
"QCheckBox::indicator:checked { background-color: #2F5C8F; }\n"
"QSlider::groove:horizontal { height: 8px; background: #D6E3F3; border-radius: 4px; }\n"
"QSlider::handle:horizontal { background: #"
                        "2F5C8F; width: 20px; margin: -7px 0; border-radius: 10px; }\n"
"QSlider::sub-page:horizontal { background: #2F5C8F; border-radius: 4px; }\n"
"QPushButton { outline: none; }\n"
"QPushButton:focus { outline: none; }")
        self.centralwidget = QWidget(PatientWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(220, 0))
        self.sidebar.setMaximumSize(QSize(220, 16777215))
        self.sidebar.setStyleSheet(u"QFrame#sidebar { background-color: #2F5C8F; border: none; }\n"
"QLabel { color: #FFFFFF; background-color: transparent; }\n"
"QPushButton { color: #FFFFFF; background-color: transparent; border: none; text-align: left; padding: 12px 20px; font-family: \"Times New Roman\"; font-size: 14px; border-radius: 10px; }\n"
"QPushButton:hover { background-color: #1E4470; }\n"
"QPushButton:checked { background-color: #1E4470; font-weight: bold; }\n"
"QPushButton:focus { outline: none; }")
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(6)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(16, 24, 16, 20)
        self.avatarLabel = QLabel(self.sidebar)
        self.avatarLabel.setObjectName(u"avatarLabel")
        self.avatarLabel.setMinimumSize(QSize(70, 70))
        self.avatarLabel.setMaximumSize(QSize(70, 70))
        self.avatarLabel.setStyleSheet(u"background-color: #FFFFFF; color: #2F5C8F; border-radius: 35px; font-size: 28px; font-weight: bold;")
        self.avatarLabel.setAlignment(Qt.AlignCenter)

        self.sidebarLayout.addWidget(self.avatarLabel)

        self.nameLabel = QLabel(self.sidebar)
        self.nameLabel.setObjectName(u"nameLabel")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(12)
        font.setBold(True)
        self.nameLabel.setFont(font)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setWordWrap(True)

        self.sidebarLayout.addWidget(self.nameLabel)

        self.roleLabel = QLabel(self.sidebar)
        self.roleLabel.setObjectName(u"roleLabel")
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(9)
        self.roleLabel.setFont(font1)
        self.roleLabel.setStyleSheet(u"color: #D6E3F3;")
        self.roleLabel.setAlignment(Qt.AlignCenter)

        self.sidebarLayout.addWidget(self.roleLabel)

        self.sidebarTopSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarTopSpacer)

        self.navHome = QPushButton(self.sidebar)
        self.navHome.setObjectName(u"navHome")
        self.navHome.setCheckable(True)
        self.navHome.setChecked(True)

        self.sidebarLayout.addWidget(self.navHome)

        self.navPrescr = QPushButton(self.sidebar)
        self.navPrescr.setObjectName(u"navPrescr")
        self.navPrescr.setCheckable(True)

        self.sidebarLayout.addWidget(self.navPrescr)

        self.navDiary = QPushButton(self.sidebar)
        self.navDiary.setObjectName(u"navDiary")
        self.navDiary.setCheckable(True)

        self.sidebarLayout.addWidget(self.navDiary)

        self.navHistory = QPushButton(self.sidebar)
        self.navHistory.setObjectName(u"navHistory")
        self.navHistory.setCheckable(True)

        self.sidebarLayout.addWidget(self.navHistory)

        self.navProfile = QPushButton(self.sidebar)
        self.navProfile.setObjectName(u"navProfile")
        self.navProfile.setCheckable(True)

        self.sidebarLayout.addWidget(self.navProfile)

        self.navHelp = QPushButton(self.sidebar)
        self.navHelp.setObjectName(u"navHelp")
        self.navHelp.setCheckable(True)

        self.sidebarLayout.addWidget(self.navHelp)

        self.sidebarBottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarBottomSpacer)


        self.mainLayout.addWidget(self.sidebar)

        self.contentWidget = QWidget(self.centralwidget)
        self.contentWidget.setObjectName(u"contentWidget")
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setSpacing(20)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(30, 24, 30, 24)
        self.topBar = QHBoxLayout()
        self.topBar.setObjectName(u"topBar")
        self.pageTitleLabel = QLabel(self.contentWidget)
        self.pageTitleLabel.setObjectName(u"pageTitleLabel")
        font2 = QFont()
        font2.setFamilies([u"Times New Roman"])
        font2.setPointSize(20)
        font2.setBold(True)
        self.pageTitleLabel.setFont(font2)
        self.pageTitleLabel.setStyleSheet(u"color: #2F5C8F; background-color: transparent;")

        self.topBar.addWidget(self.pageTitleLabel)

        self.topSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBar.addItem(self.topSpacer1)

        self.logoutBtn = QPushButton(self.contentWidget)
        self.logoutBtn.setObjectName(u"logoutBtn")
        self.logoutBtn.setMinimumSize(QSize(110, 38))
        font3 = QFont()
        font3.setFamilies([u"Times New Roman"])
        font3.setPointSize(12)
        self.logoutBtn.setFont(font3)
        self.logoutBtn.setStyleSheet(u"QPushButton { background-color: #C0504D; color: #FFFFFF; border: none; border-radius: 10px; font-weight: bold; }\n"
"QPushButton:hover { background-color: #A0403D; }\n"
"QPushButton:pressed { background-color: #803533; }")

        self.topBar.addWidget(self.logoutBtn)


        self.contentLayout.addLayout(self.topBar)

        self.pages = QStackedWidget(self.contentWidget)
        self.pages.setObjectName(u"pages")
        self.pages.setStyleSheet(u"QStackedWidget { background: transparent; border: none; }\n"
"QStackedWidget > QWidget { background-color: #EEF3F8; }")
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.homePageLayout = QVBoxLayout(self.homePage)
        self.homePageLayout.setSpacing(16)
        self.homePageLayout.setObjectName(u"homePageLayout")
        self.greetingLabel = QLabel(self.homePage)
        self.greetingLabel.setObjectName(u"greetingLabel")
        font4 = QFont()
        font4.setFamilies([u"Times New Roman"])
        font4.setPointSize(18)
        font4.setBold(True)
        self.greetingLabel.setFont(font4)

        self.homePageLayout.addWidget(self.greetingLabel)

        self.subGreetingLabel = QLabel(self.homePage)
        self.subGreetingLabel.setObjectName(u"subGreetingLabel")
        font5 = QFont()
        font5.setFamilies([u"Times New Roman"])
        font5.setPointSize(11)
        self.subGreetingLabel.setFont(font5)
        self.subGreetingLabel.setStyleSheet(u"color: #666666;")

        self.homePageLayout.addWidget(self.subGreetingLabel)

        self.cardToday = QFrame(self.homePage)
        self.cardToday.setObjectName(u"cardToday")
        self.cardToday.setMinimumSize(QSize(0, 170))
        self.cardToday.setStyleSheet(u"QFrame#cardToday { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#cardToday QLabel { color: #1A1A1A; background: transparent; }")
        self.cardTodayLayout = QVBoxLayout(self.cardToday)
        self.cardTodayLayout.setSpacing(10)
        self.cardTodayLayout.setObjectName(u"cardTodayLayout")
        self.cardTodayLayout.setContentsMargins(24, 18, 24, 18)
        self.todayHead = QHBoxLayout()
        self.todayHead.setObjectName(u"todayHead")
        self.label = QLabel(self.cardToday)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setFamilies([u"Times New Roman"])
        font6.setPointSize(14)
        font6.setBold(True)
        self.label.setFont(font6)
        self.label.setStyleSheet(u"color: #2F5C8F; background: transparent;")

        self.todayHead.addWidget(self.label)

        self.todayHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.todayHead.addItem(self.todayHeadSpacer)

        self.todayCountLabel = QLabel(self.cardToday)
        self.todayCountLabel.setObjectName(u"todayCountLabel")
        self.todayCountLabel.setFont(font5)
        self.todayCountLabel.setStyleSheet(u"color: #7A9CC6; background: transparent;")

        self.todayHead.addWidget(self.todayCountLabel)


        self.cardTodayLayout.addLayout(self.todayHead)

        self.todayListLabel = QLabel(self.cardToday)
        self.todayListLabel.setObjectName(u"todayListLabel")
        self.todayListLabel.setFont(font3)
        self.todayListLabel.setWordWrap(True)

        self.cardTodayLayout.addWidget(self.todayListLabel)

        self.btnOpenPrescrFromHome = QPushButton(self.cardToday)
        self.btnOpenPrescrFromHome.setObjectName(u"btnOpenPrescrFromHome")
        self.btnOpenPrescrFromHome.setMinimumSize(QSize(180, 38))
        self.btnOpenPrescrFromHome.setMaximumSize(QSize(180, 38))
        self.btnOpenPrescrFromHome.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.cardTodayLayout.addWidget(self.btnOpenPrescrFromHome)


        self.homePageLayout.addWidget(self.cardToday)

        self.cardsRow = QHBoxLayout()
        self.cardsRow.setSpacing(16)
        self.cardsRow.setObjectName(u"cardsRow")
        self.cardDiaryHome = QFrame(self.homePage)
        self.cardDiaryHome.setObjectName(u"cardDiaryHome")
        self.cardDiaryHome.setMinimumSize(QSize(0, 150))
        self.cardDiaryHome.setStyleSheet(u"QFrame#cardDiaryHome { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#cardDiaryHome QLabel { color: #1A1A1A; background: transparent; }")
        self.cardDiaryHomeLayout = QVBoxLayout(self.cardDiaryHome)
        self.cardDiaryHomeLayout.setObjectName(u"cardDiaryHomeLayout")
        self.cardDiaryHomeLayout.setContentsMargins(22, 18, 22, 18)
        self.label1 = QLabel(self.cardDiaryHome)
        self.label1.setObjectName(u"label1")
        self.label1.setFont(font6)
        self.label1.setStyleSheet(u"color: #2F5C8F; background: transparent;")

        self.cardDiaryHomeLayout.addWidget(self.label1)

        self.label2 = QLabel(self.cardDiaryHome)
        self.label2.setObjectName(u"label2")
        self.label2.setFont(font5)
        self.label2.setWordWrap(True)

        self.cardDiaryHomeLayout.addWidget(self.label2)

        self.btnOpenDiaryFromHome = QPushButton(self.cardDiaryHome)
        self.btnOpenDiaryFromHome.setObjectName(u"btnOpenDiaryFromHome")
        self.btnOpenDiaryFromHome.setMinimumHeight(36)
        self.btnOpenDiaryFromHome.setMaximumSize(QSize(160, 36))
        self.btnOpenDiaryFromHome.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }")

        self.cardDiaryHomeLayout.addWidget(self.btnOpenDiaryFromHome)


        self.cardsRow.addWidget(self.cardDiaryHome)

        self.cardHistoryHome = QFrame(self.homePage)
        self.cardHistoryHome.setObjectName(u"cardHistoryHome")
        self.cardHistoryHome.setMinimumSize(QSize(0, 150))
        self.cardHistoryHome.setStyleSheet(u"QFrame#cardHistoryHome { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#cardHistoryHome QLabel { color: #1A1A1A; background: transparent; }")
        self.cardHistoryHomeLayout = QVBoxLayout(self.cardHistoryHome)
        self.cardHistoryHomeLayout.setObjectName(u"cardHistoryHomeLayout")
        self.cardHistoryHomeLayout.setContentsMargins(22, 18, 22, 18)
        self.label3 = QLabel(self.cardHistoryHome)
        self.label3.setObjectName(u"label3")
        self.label3.setFont(font6)
        self.label3.setStyleSheet(u"color: #2F5C8F; background: transparent;")

        self.cardHistoryHomeLayout.addWidget(self.label3)

        self.label4 = QLabel(self.cardHistoryHome)
        self.label4.setObjectName(u"label4")
        self.label4.setFont(font5)
        self.label4.setWordWrap(True)

        self.cardHistoryHomeLayout.addWidget(self.label4)

        self.btnOpenHistoryFromHome = QPushButton(self.cardHistoryHome)
        self.btnOpenHistoryFromHome.setObjectName(u"btnOpenHistoryFromHome")
        self.btnOpenHistoryFromHome.setMinimumHeight(36)
        self.btnOpenHistoryFromHome.setMaximumSize(QSize(160, 36))
        self.btnOpenHistoryFromHome.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }")

        self.cardHistoryHomeLayout.addWidget(self.btnOpenHistoryFromHome)


        self.cardsRow.addWidget(self.cardHistoryHome)


        self.homePageLayout.addLayout(self.cardsRow)

        self.homeBottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.homePageLayout.addItem(self.homeBottomSpacer)

        self.pages.addWidget(self.homePage)
        self.prescrPage = QWidget()
        self.prescrPage.setObjectName(u"prescrPage")
        self.prescrPageLayout = QVBoxLayout(self.prescrPage)
        self.prescrPageLayout.setObjectName(u"prescrPageLayout")
        self.prescrTable = QTableWidget(self.prescrPage)
        self.prescrTable.setObjectName(u"prescrTable")

        self.prescrPageLayout.addWidget(self.prescrTable)

        self.prescrBottomLayout = QHBoxLayout()
        self.prescrBottomLayout.setObjectName(u"prescrBottomLayout")
        self.prescrBottomSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.prescrBottomLayout.addItem(self.prescrBottomSpacer)

        self.refreshPrescrBtn = QPushButton(self.prescrPage)
        self.refreshPrescrBtn.setObjectName(u"refreshPrescrBtn")
        self.refreshPrescrBtn.setMinimumSize(QSize(160, 38))
        self.refreshPrescrBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.prescrBottomLayout.addWidget(self.refreshPrescrBtn)


        self.prescrPageLayout.addLayout(self.prescrBottomLayout)

        self.pages.addWidget(self.prescrPage)
        self.diaryPage = QWidget()
        self.diaryPage.setObjectName(u"diaryPage")
        self.diaryPageLayout = QVBoxLayout(self.diaryPage)
        self.diaryPageLayout.setSpacing(14)
        self.diaryPageLayout.setObjectName(u"diaryPageLayout")
        self.label5 = QLabel(self.diaryPage)
        self.label5.setObjectName(u"label5")
        self.label5.setFont(font6)
        self.label5.setStyleSheet(u"color: #2F5C8F;")

        self.diaryPageLayout.addWidget(self.label5)

        self.wellBeingLayout = QHBoxLayout()
        self.wellBeingLayout.setObjectName(u"wellBeingLayout")
        self.wellBeingCombo = QComboBox(self.diaryPage)
        self.wellBeingCombo.addItem("")
        self.wellBeingCombo.addItem("")
        self.wellBeingCombo.addItem("")
        self.wellBeingCombo.addItem("")
        self.wellBeingCombo.addItem("")
        self.wellBeingCombo.setObjectName(u"wellBeingCombo")
        self.wellBeingCombo.setMinimumHeight(42)
        self.wellBeingCombo.setMinimumWidth(300)

        self.wellBeingLayout.addWidget(self.wellBeingCombo)

        self.wellBeingSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.wellBeingLayout.addItem(self.wellBeingSpacer)


        self.diaryPageLayout.addLayout(self.wellBeingLayout)

        self.label6 = QLabel(self.diaryPage)
        self.label6.setObjectName(u"label6")
        self.label6.setFont(font6)
        self.label6.setStyleSheet(u"color: #2F5C8F;")

        self.diaryPageLayout.addWidget(self.label6)

        self.intensityLayout = QHBoxLayout()
        self.intensityLayout.setObjectName(u"intensityLayout")
        self.label7 = QLabel(self.diaryPage)
        self.label7.setObjectName(u"label7")

        self.intensityLayout.addWidget(self.label7)

        self.intensitySlider = QSlider(self.diaryPage)
        self.intensitySlider.setObjectName(u"intensitySlider")
        self.intensitySlider.setOrientation(Qt.Horizontal)
        self.intensitySlider.setMinimum(0)
        self.intensitySlider.setMaximum(10)
        self.intensitySlider.setValue(0)
        self.intensitySlider.setTickPosition(QSlider.TicksBelow)
        self.intensitySlider.setTickInterval(1)

        self.intensityLayout.addWidget(self.intensitySlider)

        self.label8 = QLabel(self.diaryPage)
        self.label8.setObjectName(u"label8")

        self.intensityLayout.addWidget(self.label8)

        self.intensityValueLabel = QLabel(self.diaryPage)
        self.intensityValueLabel.setObjectName(u"intensityValueLabel")
        self.intensityValueLabel.setMinimumSize(QSize(40, 0))
        font7 = QFont()
        font7.setFamilies([u"Times New Roman"])
        font7.setPointSize(13)
        font7.setBold(True)
        self.intensityValueLabel.setFont(font7)
        self.intensityValueLabel.setStyleSheet(u"color: #2F5C8F;")
        self.intensityValueLabel.setAlignment(Qt.AlignCenter)

        self.intensityLayout.addWidget(self.intensityValueLabel)


        self.diaryPageLayout.addLayout(self.intensityLayout)

        self.label9 = QLabel(self.diaryPage)
        self.label9.setObjectName(u"label9")
        self.label9.setFont(font6)
        self.label9.setStyleSheet(u"color: #2F5C8F;")

        self.diaryPageLayout.addWidget(self.label9)

        self.symptomsGrid = QGridLayout()
        self.symptomsGrid.setObjectName(u"symptomsGrid")
        self.symptomsGrid.setHorizontalSpacing(16)
        self.symptomsGrid.setVerticalSpacing(8)
        self.chkHeadache = QCheckBox(self.diaryPage)
        self.chkHeadache.setObjectName(u"chkHeadache")

        self.symptomsGrid.addWidget(self.chkHeadache, 0, 0, 1, 1)

        self.chkWeakness = QCheckBox(self.diaryPage)
        self.chkWeakness.setObjectName(u"chkWeakness")

        self.symptomsGrid.addWidget(self.chkWeakness, 0, 1, 1, 1)

        self.chkNausea = QCheckBox(self.diaryPage)
        self.chkNausea.setObjectName(u"chkNausea")

        self.symptomsGrid.addWidget(self.chkNausea, 0, 2, 1, 1)

        self.chkDizzy = QCheckBox(self.diaryPage)
        self.chkDizzy.setObjectName(u"chkDizzy")

        self.symptomsGrid.addWidget(self.chkDizzy, 0, 3, 1, 1)

        self.chkHeart = QCheckBox(self.diaryPage)
        self.chkHeart.setObjectName(u"chkHeart")

        self.symptomsGrid.addWidget(self.chkHeart, 1, 0, 1, 1)

        self.chkBreath = QCheckBox(self.diaryPage)
        self.chkBreath.setObjectName(u"chkBreath")

        self.symptomsGrid.addWidget(self.chkBreath, 1, 1, 1, 1)

        self.chkPressureUp = QCheckBox(self.diaryPage)
        self.chkPressureUp.setObjectName(u"chkPressureUp")

        self.symptomsGrid.addWidget(self.chkPressureUp, 1, 2, 1, 1)

        self.chkSleep = QCheckBox(self.diaryPage)
        self.chkSleep.setObjectName(u"chkSleep")

        self.symptomsGrid.addWidget(self.chkSleep, 1, 3, 1, 1)

        self.chkAppetite = QCheckBox(self.diaryPage)
        self.chkAppetite.setObjectName(u"chkAppetite")

        self.symptomsGrid.addWidget(self.chkAppetite, 2, 0, 1, 1)

        self.chkTremor = QCheckBox(self.diaryPage)
        self.chkTremor.setObjectName(u"chkTremor")

        self.symptomsGrid.addWidget(self.chkTremor, 2, 1, 1, 1)

        self.chkSweat = QCheckBox(self.diaryPage)
        self.chkSweat.setObjectName(u"chkSweat")

        self.symptomsGrid.addWidget(self.chkSweat, 2, 2, 1, 1)

        self.chkOtherSymptom = QCheckBox(self.diaryPage)
        self.chkOtherSymptom.setObjectName(u"chkOtherSymptom")

        self.symptomsGrid.addWidget(self.chkOtherSymptom, 2, 3, 1, 1)


        self.diaryPageLayout.addLayout(self.symptomsGrid)

        self.label10 = QLabel(self.diaryPage)
        self.label10.setObjectName(u"label10")
        self.label10.setFont(font6)
        self.label10.setStyleSheet(u"color: #2F5C8F;")

        self.diaryPageLayout.addWidget(self.label10)

        self.triggersGrid = QGridLayout()
        self.triggersGrid.setObjectName(u"triggersGrid")
        self.triggersGrid.setHorizontalSpacing(16)
        self.triggersGrid.setVerticalSpacing(8)
        self.trigStress = QCheckBox(self.diaryPage)
        self.trigStress.setObjectName(u"trigStress")

        self.triggersGrid.addWidget(self.trigStress, 0, 0, 1, 1)

        self.trigWeather = QCheckBox(self.diaryPage)
        self.trigWeather.setObjectName(u"trigWeather")

        self.triggersGrid.addWidget(self.trigWeather, 0, 1, 1, 1)

        self.trigFood = QCheckBox(self.diaryPage)
        self.trigFood.setObjectName(u"trigFood")

        self.triggersGrid.addWidget(self.trigFood, 0, 2, 1, 1)

        self.trigPhysical = QCheckBox(self.diaryPage)
        self.trigPhysical.setObjectName(u"trigPhysical")

        self.triggersGrid.addWidget(self.trigPhysical, 0, 3, 1, 1)

        self.trigSleep = QCheckBox(self.diaryPage)
        self.trigSleep.setObjectName(u"trigSleep")

        self.triggersGrid.addWidget(self.trigSleep, 1, 0, 1, 1)

        self.trigSkipMed = QCheckBox(self.diaryPage)
        self.trigSkipMed.setObjectName(u"trigSkipMed")

        self.triggersGrid.addWidget(self.trigSkipMed, 1, 1, 1, 1)

        self.trigAlcohol = QCheckBox(self.diaryPage)
        self.trigAlcohol.setObjectName(u"trigAlcohol")

        self.triggersGrid.addWidget(self.trigAlcohol, 1, 2, 1, 1)

        self.trigOtherTrigger = QCheckBox(self.diaryPage)
        self.trigOtherTrigger.setObjectName(u"trigOtherTrigger")

        self.triggersGrid.addWidget(self.trigOtherTrigger, 1, 3, 1, 1)


        self.diaryPageLayout.addLayout(self.triggersGrid)

        self.label11 = QLabel(self.diaryPage)
        self.label11.setObjectName(u"label11")
        self.label11.setFont(font6)
        self.label11.setStyleSheet(u"color: #2F5C8F;")

        self.diaryPageLayout.addWidget(self.label11)

        self.indicatorsLayout = QHBoxLayout()
        self.indicatorsLayout.setSpacing(12)
        self.indicatorsLayout.setObjectName(u"indicatorsLayout")
        self.pressureLine = QLineEdit(self.diaryPage)
        self.pressureLine.setObjectName(u"pressureLine")
        self.pressureLine.setMinimumHeight(42)

        self.indicatorsLayout.addWidget(self.pressureLine)

        self.pulseLine = QLineEdit(self.diaryPage)
        self.pulseLine.setObjectName(u"pulseLine")
        self.pulseLine.setMinimumHeight(42)

        self.indicatorsLayout.addWidget(self.pulseLine)

        self.sugarLine = QLineEdit(self.diaryPage)
        self.sugarLine.setObjectName(u"sugarLine")
        self.sugarLine.setMinimumHeight(42)

        self.indicatorsLayout.addWidget(self.sugarLine)

        self.tempLine = QLineEdit(self.diaryPage)
        self.tempLine.setObjectName(u"tempLine")
        self.tempLine.setMinimumHeight(42)

        self.indicatorsLayout.addWidget(self.tempLine)


        self.diaryPageLayout.addLayout(self.indicatorsLayout)

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.setSpacing(12)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.heightLine = QLineEdit(self.diaryPage)
        self.heightLine.setObjectName(u"heightLine")
        self.heightLine.setMinimumHeight(42)

        self.bodyLayout.addWidget(self.heightLine)

        self.weightLine = QLineEdit(self.diaryPage)
        self.weightLine.setObjectName(u"weightLine")
        self.weightLine.setMinimumHeight(42)

        self.bodyLayout.addWidget(self.weightLine)

        self.bodySpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bodyLayout.addItem(self.bodySpacer)


        self.diaryPageLayout.addLayout(self.bodyLayout)

        self.label12 = QLabel(self.diaryPage)
        self.label12.setObjectName(u"label12")
        self.label12.setFont(font6)
        self.label12.setStyleSheet(u"color: #2F5C8F;")

        self.diaryPageLayout.addWidget(self.label12)

        self.notesText = QTextEdit(self.diaryPage)
        self.notesText.setObjectName(u"notesText")
        self.notesText.setMaximumHeight(70)

        self.diaryPageLayout.addWidget(self.notesText)

        self.saveLayout = QHBoxLayout()
        self.saveLayout.setObjectName(u"saveLayout")
        self.saveSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.saveLayout.addItem(self.saveSpacer)

        self.saveDiaryBtn = QPushButton(self.diaryPage)
        self.saveDiaryBtn.setObjectName(u"saveDiaryBtn")
        self.saveDiaryBtn.setMinimumSize(QSize(240, 46))
        self.saveDiaryBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 14px; font-weight: bold; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.saveLayout.addWidget(self.saveDiaryBtn)


        self.diaryPageLayout.addLayout(self.saveLayout)

        self.diaryBottomSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.diaryPageLayout.addItem(self.diaryBottomSpacer)

        self.pages.addWidget(self.diaryPage)
        self.historyPage = QWidget()
        self.historyPage.setObjectName(u"historyPage")
        self.historyPageLayout = QVBoxLayout(self.historyPage)
        self.historyPageLayout.setObjectName(u"historyPageLayout")
        self.historyTable = QTableWidget(self.historyPage)
        self.historyTable.setObjectName(u"historyTable")

        self.historyPageLayout.addWidget(self.historyTable)

        self.pages.addWidget(self.historyPage)
        self.profilePage = QWidget()
        self.profilePage.setObjectName(u"profilePage")
        self.profilePageLayout = QVBoxLayout(self.profilePage)
        self.profilePageLayout.setSpacing(14)
        self.profilePageLayout.setObjectName(u"profilePageLayout")
        self.label13 = QLabel(self.profilePage)
        self.label13.setObjectName(u"label13")
        self.label13.setFont(font6)
        self.label13.setStyleSheet(u"color: #2F5C8F;")

        self.profilePageLayout.addWidget(self.label13)

        self.profileCard = QFrame(self.profilePage)
        self.profileCard.setObjectName(u"profileCard")
        self.profileCard.setMinimumSize(QSize(0, 280))
        self.profileCard.setStyleSheet(u"QFrame#profileCard { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#profileCard QLabel { color: #1A1A1A; background: transparent; font-family: \"Times New Roman\"; }")
        self.profileForm = QFormLayout(self.profileCard)
        self.profileForm.setObjectName(u"profileForm")
        self.profileForm.setHorizontalSpacing(20)
        self.profileForm.setVerticalSpacing(14)
        self.profileForm.setContentsMargins(24, 24, 24, 24)
        self.label14 = QLabel(self.profileCard)
        self.label14.setObjectName(u"label14")
        self.label14.setFont(font)
        self.label14.setStyleSheet(u"color: #666666;")

        self.profileForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label14)

        self.profFullName = QLabel(self.profileCard)
        self.profFullName.setObjectName(u"profFullName")
        font8 = QFont()
        font8.setFamilies([u"Times New Roman"])
        font8.setPointSize(13)
        self.profFullName.setFont(font8)

        self.profileForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.profFullName)

        self.label15 = QLabel(self.profileCard)
        self.label15.setObjectName(u"label15")
        self.label15.setFont(font)
        self.label15.setStyleSheet(u"color: #666666;")

        self.profileForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label15)

        self.profBirthDate = QLabel(self.profileCard)
        self.profBirthDate.setObjectName(u"profBirthDate")
        self.profBirthDate.setFont(font8)

        self.profileForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.profBirthDate)

        self.label16 = QLabel(self.profileCard)
        self.label16.setObjectName(u"label16")
        self.label16.setFont(font)
        self.label16.setStyleSheet(u"color: #666666;")

        self.profileForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label16)

        self.profGender = QLabel(self.profileCard)
        self.profGender.setObjectName(u"profGender")
        self.profGender.setFont(font8)

        self.profileForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.profGender)

        self.label17 = QLabel(self.profileCard)
        self.label17.setObjectName(u"label17")
        self.label17.setFont(font)
        self.label17.setStyleSheet(u"color: #666666;")

        self.profileForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label17)

        self.profPolicy = QLabel(self.profileCard)
        self.profPolicy.setObjectName(u"profPolicy")
        self.profPolicy.setFont(font8)

        self.profileForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.profPolicy)

        self.label18 = QLabel(self.profileCard)
        self.label18.setObjectName(u"label18")
        self.label18.setFont(font)
        self.label18.setStyleSheet(u"color: #666666;")

        self.profileForm.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label18)

        self.profPhone = QLabel(self.profileCard)
        self.profPhone.setObjectName(u"profPhone")
        self.profPhone.setFont(font8)

        self.profileForm.setWidget(4, QFormLayout.ItemRole.FieldRole, self.profPhone)

        self.label19 = QLabel(self.profileCard)
        self.label19.setObjectName(u"label19")
        self.label19.setFont(font)
        self.label19.setStyleSheet(u"color: #666666;")

        self.profileForm.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label19)

        self.profDoctor = QLabel(self.profileCard)
        self.profDoctor.setObjectName(u"profDoctor")
        self.profDoctor.setFont(font8)

        self.profileForm.setWidget(5, QFormLayout.ItemRole.FieldRole, self.profDoctor)


        self.profilePageLayout.addWidget(self.profileCard)

        self.profileSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.profilePageLayout.addItem(self.profileSpacer)

        self.pages.addWidget(self.profilePage)
        self.helpPage = QWidget()
        self.helpPage.setObjectName(u"helpPage")
        self.helpLayout = QVBoxLayout(self.helpPage)
        self.helpLayout.setSpacing(14)
        self.helpLayout.setObjectName(u"helpLayout")
        self.label20 = QLabel(self.helpPage)
        self.label20.setObjectName(u"label20")
        self.label20.setFont(font4)
        self.label20.setStyleSheet(u"color: #2F5C8F;")

        self.helpLayout.addWidget(self.label20)

        self.helpText = QTextEdit(self.helpPage)
        self.helpText.setObjectName(u"helpText")
        self.helpText.setReadOnly(True)
        self.helpText.setStyleSheet(u"QTextEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 16px; font-family: \"Times New Roman\"; font-size: 13px; }")

        self.helpLayout.addWidget(self.helpText)

        self.pages.addWidget(self.helpPage)

        self.contentLayout.addWidget(self.pages)


        self.mainLayout.addWidget(self.contentWidget)

        PatientWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PatientWindow)

        QMetaObject.connectSlotsByName(PatientWindow)
    # setupUi

    def retranslateUi(self, PatientWindow):
        PatientWindow.setWindowTitle(QCoreApplication.translate("PatientWindow", u"\u0414\u043d\u0435\u0432\u043d\u0438\u043a \u0437\u0434\u043e\u0440\u043e\u0432\u044c\u044f", None))
        self.avatarLabel.setText(QCoreApplication.translate("PatientWindow", u"?", None))
        self.nameLabel.setText(QCoreApplication.translate("PatientWindow", u"\u0424\u0418\u041e", None))
        self.roleLabel.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u0430\u0446\u0438\u0435\u043d\u0442", None))
        self.navHome.setText(QCoreApplication.translate("PatientWindow", u"  \u0413\u043b\u0430\u0432\u043d\u0430\u044f", None))
        self.navPrescr.setText(QCoreApplication.translate("PatientWindow", u"  \u041c\u043e\u0438 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f", None))
        self.navDiary.setText(QCoreApplication.translate("PatientWindow", u"  \u0414\u043d\u0435\u0432\u043d\u0438\u043a \u0441\u0430\u043c\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u0438\u044f", None))
        self.navHistory.setText(QCoreApplication.translate("PatientWindow", u"  \u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0437\u0430\u043f\u0438\u0441\u0435\u0439", None))
        self.navProfile.setText(QCoreApplication.translate("PatientWindow", u"  \u041c\u043e\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.navHelp.setText(QCoreApplication.translate("PatientWindow", u"  \u041f\u043e\u043c\u043e\u0449\u044c (F1)", None))
        self.pageTitleLabel.setText(QCoreApplication.translate("PatientWindow", u"\u0413\u043b\u0430\u0432\u043d\u0430\u044f", None))
        self.logoutBtn.setText(QCoreApplication.translate("PatientWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.greetingLabel.setText(QCoreApplication.translate("PatientWindow", u"\u0414\u043e\u0431\u0440\u044b\u0439 \u0434\u0435\u043d\u044c!", None))
        self.subGreetingLabel.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 \u0441\u0432\u043e\u0438 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0438 \u0437\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u0435 \u0434\u043d\u0435\u0432\u043d\u0438\u043a", None))
        self.label.setText(QCoreApplication.translate("PatientWindow", u"\u041b\u0415\u041a\u0410\u0420\u0421\u0422\u0412\u0410 \u041d\u0410 \u0421\u0415\u0413\u041e\u0414\u041d\u042f", None))
        self.todayCountLabel.setText(QCoreApplication.translate("PatientWindow", u"0 \u043f\u0440\u0438\u0451\u043c\u043e\u0432", None))
        self.todayListLabel.setText(QCoreApplication.translate("PatientWindow", u"\u0423 \u0432\u0430\u0441 \u043d\u0435\u0442 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0439", None))
        self.btnOpenPrescrFromHome.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f", None))
        self.label1.setText(QCoreApplication.translate("PatientWindow", u"\u0414\u041d\u0415\u0412\u041d\u0418\u041a \u0421\u0410\u041c\u041e\u0427\u0423\u0412\u0421\u0422\u0412\u0418\u042f", None))
        self.label2.setText(QCoreApplication.translate("PatientWindow", u"\u041e\u0442\u043c\u0435\u0442\u044c\u0442\u0435 \u0441\u0430\u043c\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u0438\u0435, \u0441\u0438\u043c\u043f\u0442\u043e\u043c\u044b \u0438 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438", None))
        self.btnOpenDiaryFromHome.setText(QCoreApplication.translate("PatientWindow", u"\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c", None))
        self.label3.setText(QCoreApplication.translate("PatientWindow", u"\u0418\u0421\u0422\u041e\u0420\u0418\u042f \u0417\u0410\u041f\u0418\u0421\u0415\u0419", None))
        self.label4.setText(QCoreApplication.translate("PatientWindow", u"\u0412\u0441\u0435 \u043f\u0440\u043e\u0448\u043b\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438 \u0434\u043d\u0435\u0432\u043d\u0438\u043a\u0430", None))
        self.btnOpenHistoryFromHome.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c", None))
        self.refreshPrescrBtn.setText(QCoreApplication.translate("PatientWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.label5.setText(QCoreApplication.translate("PatientWindow", u"\u041e\u0431\u0449\u0435\u0435 \u0441\u0430\u043c\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u0438\u0435", None))
        self.wellBeingCombo.setItemText(0, QCoreApplication.translate("PatientWindow", u"\u041e\u0442\u043b\u0438\u0447\u043d\u043e", None))
        self.wellBeingCombo.setItemText(1, QCoreApplication.translate("PatientWindow", u"\u0425\u043e\u0440\u043e\u0448\u043e", None))
        self.wellBeingCombo.setItemText(2, QCoreApplication.translate("PatientWindow", u"\u0423\u0434\u043e\u0432\u043b\u0435\u0442\u0432\u043e\u0440\u0438\u0442\u0435\u043b\u044c\u043d\u043e", None))
        self.wellBeingCombo.setItemText(3, QCoreApplication.translate("PatientWindow", u"\u041f\u043b\u043e\u0445\u043e", None))
        self.wellBeingCombo.setItemText(4, QCoreApplication.translate("PatientWindow", u"\u041e\u0447\u0435\u043d\u044c \u043f\u043b\u043e\u0445\u043e", None))

        self.label6.setText(QCoreApplication.translate("PatientWindow", u"\u0418\u043d\u0442\u0435\u043d\u0441\u0438\u0432\u043d\u043e\u0441\u0442\u044c \u0441\u0438\u043c\u043f\u0442\u043e\u043c\u043e\u0432", None))
        self.label7.setText(QCoreApplication.translate("PatientWindow", u"\u041d\u0435\u0442", None))
        self.label8.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u0438\u043b\u044c\u043d\u043e", None))
        self.intensityValueLabel.setText(QCoreApplication.translate("PatientWindow", u"0", None))
        self.label9.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u0438\u043c\u043f\u0442\u043e\u043c\u044b (\u043e\u0442\u043c\u0435\u0442\u044c\u0442\u0435 \u0432\u0441\u0435 \u043f\u043e\u0434\u0445\u043e\u0434\u044f\u0449\u0438\u0435)", None))
        self.chkHeadache.setText(QCoreApplication.translate("PatientWindow", u"\u0413\u043e\u043b\u043e\u0432\u043d\u0430\u044f \u0431\u043e\u043b\u044c", None))
        self.chkWeakness.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u043b\u0430\u0431\u043e\u0441\u0442\u044c", None))
        self.chkNausea.setText(QCoreApplication.translate("PatientWindow", u"\u0422\u043e\u0448\u043d\u043e\u0442\u0430", None))
        self.chkDizzy.setText(QCoreApplication.translate("PatientWindow", u"\u0413\u043e\u043b\u043e\u0432\u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u0435", None))
        self.chkHeart.setText(QCoreApplication.translate("PatientWindow", u"\u0411\u043e\u043b\u044c \u0432 \u0441\u0435\u0440\u0434\u0446\u0435", None))
        self.chkBreath.setText(QCoreApplication.translate("PatientWindow", u"\u041e\u0434\u044b\u0448\u043a\u0430", None))
        self.chkPressureUp.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u044f", None))
        self.chkSleep.setText(QCoreApplication.translate("PatientWindow", u"\u041d\u0430\u0440\u0443\u0448\u0435\u043d\u0438\u0435 \u0441\u043d\u0430", None))
        self.chkAppetite.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u0442\u0435\u0440\u044f \u0430\u043f\u043f\u0435\u0442\u0438\u0442\u0430", None))
        self.chkTremor.setText(QCoreApplication.translate("PatientWindow", u"\u0422\u0440\u0435\u043c\u043e\u0440 \u0440\u0443\u043a", None))
        self.chkSweat.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u0432\u044b\u0448\u0435\u043d\u043d\u0430\u044f \u043f\u043e\u0442\u043b\u0438\u0432\u043e\u0441\u0442\u044c", None))
        self.chkOtherSymptom.setText(QCoreApplication.translate("PatientWindow", u"\u0414\u0440\u0443\u0433\u043e\u0435", None))
        self.label10.setText(QCoreApplication.translate("PatientWindow", u"\u0412\u043e\u0437\u043c\u043e\u0436\u043d\u044b\u0435 \u0442\u0440\u0438\u0433\u0433\u0435\u0440\u044b", None))
        self.trigStress.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u0442\u0440\u0435\u0441\u0441", None))
        self.trigWeather.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u043c\u0435\u043d\u0430 \u043f\u043e\u0433\u043e\u0434\u044b", None))
        self.trigFood.setText(QCoreApplication.translate("PatientWindow", u"\u0415\u0434\u0430", None))
        self.trigPhysical.setText(QCoreApplication.translate("PatientWindow", u"\u0424\u0438\u0437. \u043d\u0430\u0433\u0440\u0443\u0437\u043a\u0430", None))
        self.trigSleep.setText(QCoreApplication.translate("PatientWindow", u"\u041d\u0435\u0434\u043e\u0441\u044b\u043f", None))
        self.trigSkipMed.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u0440\u043e\u043f\u0443\u0441\u043a \u043b\u0435\u043a\u0430\u0440\u0441\u0442\u0432\u0430", None))
        self.trigAlcohol.setText(QCoreApplication.translate("PatientWindow", u"\u0410\u043b\u043a\u043e\u0433\u043e\u043b\u044c", None))
        self.trigOtherTrigger.setText(QCoreApplication.translate("PatientWindow", u"\u0414\u0440\u0443\u0433\u043e\u0435", None))
        self.label11.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438 \u0437\u0434\u043e\u0440\u043e\u0432\u044c\u044f", None))
        self.pressureLine.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u0414\u0430\u0432\u043b\u0435\u043d\u0438\u0435 (120/80)", None))
        self.pulseLine.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u041f\u0443\u043b\u044c\u0441 (72)", None))
        self.sugarLine.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u0421\u0430\u0445\u0430\u0440 (5.5)", None))
        self.tempLine.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430 (36.6)", None))
        self.heightLine.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u0420\u043e\u0441\u0442 (\u0441\u043c)", None))
        self.weightLine.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u0412\u0435\u0441 (\u043a\u0433)", None))
        self.label12.setText(QCoreApplication.translate("PatientWindow", u"\u0417\u0430\u043c\u0435\u0442\u043a\u0438", None))
        self.notesText.setPlaceholderText(QCoreApplication.translate("PatientWindow", u"\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u044f", None))
        self.saveDiaryBtn.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.label13.setText(QCoreApplication.translate("PatientWindow", u"\u041b\u0438\u0447\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
        self.label14.setText(QCoreApplication.translate("PatientWindow", u"\u0424\u0418\u041e:", None))
        self.profFullName.setText(QCoreApplication.translate("PatientWindow", u"\u2014", None))
        self.label15.setText(QCoreApplication.translate("PatientWindow", u"\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f:", None))
        self.profBirthDate.setText(QCoreApplication.translate("PatientWindow", u"\u2014", None))
        self.label16.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u043b:", None))
        self.profGender.setText(QCoreApplication.translate("PatientWindow", u"\u2014", None))
        self.label17.setText(QCoreApplication.translate("PatientWindow", u"\u041f\u043e\u043b\u0438\u0441 \u041e\u041c\u0421:", None))
        self.profPolicy.setText(QCoreApplication.translate("PatientWindow", u"\u2014", None))
        self.label18.setText(QCoreApplication.translate("PatientWindow", u"\u0422\u0435\u043b\u0435\u0444\u043e\u043d:", None))
        self.profPhone.setText(QCoreApplication.translate("PatientWindow", u"\u2014", None))
        self.label19.setText(QCoreApplication.translate("PatientWindow", u"\u041b\u0435\u0447\u0430\u0449\u0438\u0439 \u0432\u0440\u0430\u0447:", None))
        self.profDoctor.setText(QCoreApplication.translate("PatientWindow", u"\u2014", None))
        self.label20.setText(QCoreApplication.translate("PatientWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.helpText.setHtml(QCoreApplication.translate("PatientWindow", u"<h2 style=\"color:#2F5C8F;\">\u041b\u0438\u0447\u043d\u044b\u0439 \u043a\u0430\u0431\u0438\u043d\u0435\u0442 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430</h2><p><b>\u0413\u043b\u0430\u0432\u043d\u0430\u044f</b> \u2014 \u043f\u0440\u0438\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0435 \u0438 \u043b\u0435\u043a\u0430\u0440\u0441\u0442\u0432\u0430 \u043d\u0430 \u0441\u0435\u0433\u043e\u0434\u043d\u044f.</p><p><b>\u041c\u043e\u0438 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f</b> \u2014 \u043f\u043b\u0430\u043d \u043b\u0435\u0447\u0435\u043d\u0438\u044f \u043e\u0442 \u0432\u0440\u0430\u0447\u0430.</p><p><b>\u0414\u043d\u0435\u0432\u043d\u0438\u043a \u0441\u0430\u043c\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u0438\u044f</b> \u2014 \u0435\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u0430\u044f \u0437\u0430\u043f\u0438\u0441\u044c \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f, \u0441\u0438\u043c\u043f\u0442\u043e\u043c\u043e\u0432, \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0435"
                        "\u0439.</p><p><b>\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0437\u0430\u043f\u0438\u0441\u0435\u0439</b> \u2014 \u0432\u0441\u0435 \u043f\u0440\u043e\u0448\u043b\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438.</p><p><b>\u041c\u043e\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c</b> \u2014 \u0432\u0430\u0448\u0438 \u0434\u0430\u043d\u043d\u044b\u0435 \u0438 \u043b\u0435\u0447\u0430\u0449\u0438\u0439 \u0432\u0440\u0430\u0447.</p><h3 style=\"color:#2F5C8F;\">\u0413\u043e\u0440\u044f\u0447\u0438\u0435 \u043a\u043b\u0430\u0432\u0438\u0448\u0438</h3><p><b>F1</b> \u2014 \u0441\u043f\u0440\u0430\u0432\u043a\u0430<br><b>Ctrl+Q</b> \u2014 \u0432\u044b\u0439\u0442\u0438</p>", None))
    # retranslateUi

