# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'doctor.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_DoctorWindow(object):
    def setupUi(self, DoctorWindow):
        if not DoctorWindow.objectName():
            DoctorWindow.setObjectName(u"DoctorWindow")
        DoctorWindow.resize(1280, 800)
        DoctorWindow.setStyleSheet(u"QMainWindow { background-color: #EEF3F8; }\n"
"QLabel { color: #1A1A1A; background-color: transparent; }\n"
"QLineEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QLineEdit::placeholder { color: #999999; }\n"
"QLineEdit:focus { border: 2px solid #2F5C8F; }\n"
"QTextEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QTextEdit::placeholder { color: #999999; }\n"
"QComboBox { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QComboBox::drop-down { border: none; width: 28px; }\n"
"QComboBox QAbstractItemView { background-color: #FFFFFF; color: #1A1A1A; selection-background-color: #7A9CC6; selection-color: #FFFFFF; border: 1px solid #CCCCCC; }\n"
"QDateE"
                        "dit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px 14px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QDateEdit::drop-down { border: none; width: 24px; }\n"
"QTableWidget { background-color: #FFFFFF; color: #1A1A1A; gridline-color: #EEEEEE; font-family: \"Times New Roman\"; font-size: 13px; border: 1px solid #CCCCCC; border-radius: 12px; }\n"
"QTableWidget::item { color: #1A1A1A; background-color: #FFFFFF; padding: 8px; }\n"
"QTableWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }\n"
"QHeaderView::section { background-color: #2F5C8F; color: #FFFFFF; padding: 10px; border: none; font-family: \"Times New Roman\"; font-size: 13px; font-weight: bold; }\n"
"QStackedWidget > QWidget { background-color: #EEF3F8; }\n"
"QListWidget { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; padding: 4px; }\n"
"QListWidget::item { padding: 8px; bor"
                        "der-radius: 6px; }\n"
"QListWidget::item:selected { background-color: #7A9CC6; color: #FFFFFF; }\n"
"QListWidget::item:hover { background-color: #E8EFF8; }\n"
"QPushButton { outline: none; }\n"
"QPushButton:focus { outline: none; }")
        self.centralwidget = QWidget(DoctorWindow)
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

        self.navPatients = QPushButton(self.sidebar)
        self.navPatients.setObjectName(u"navPatients")
        self.navPatients.setCheckable(True)

        self.sidebarLayout.addWidget(self.navPatients)

        self.navAddPatient = QPushButton(self.sidebar)
        self.navAddPatient.setObjectName(u"navAddPatient")
        self.navAddPatient.setCheckable(True)

        self.sidebarLayout.addWidget(self.navAddPatient)

        self.navPrescriptions = QPushButton(self.sidebar)
        self.navPrescriptions.setObjectName(u"navPrescriptions")
        self.navPrescriptions.setCheckable(True)

        self.sidebarLayout.addWidget(self.navPrescriptions)

        self.navDiaries = QPushButton(self.sidebar)
        self.navDiaries.setObjectName(u"navDiaries")
        self.navDiaries.setCheckable(True)

        self.sidebarLayout.addWidget(self.navDiaries)

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

        self.cardPatients = QFrame(self.homePage)
        self.cardPatients.setObjectName(u"cardPatients")
        self.cardPatients.setMinimumSize(QSize(0, 170))
        self.cardPatients.setStyleSheet(u"QFrame#cardPatients { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#cardPatients QLabel { color: #1A1A1A; background: transparent; }")
        self.cardPatientsLayout = QVBoxLayout(self.cardPatients)
        self.cardPatientsLayout.setSpacing(10)
        self.cardPatientsLayout.setObjectName(u"cardPatientsLayout")
        self.cardPatientsLayout.setContentsMargins(24, 18, 24, 18)
        self.patientsHead = QHBoxLayout()
        self.patientsHead.setObjectName(u"patientsHead")
        self.label = QLabel(self.cardPatients)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setFamilies([u"Times New Roman"])
        font6.setPointSize(14)
        font6.setBold(True)
        self.label.setFont(font6)
        self.label.setStyleSheet(u"color: #2F5C8F;")

        self.patientsHead.addWidget(self.label)

        self.patientsHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.patientsHead.addItem(self.patientsHeadSpacer)

        self.patientsCountLabel = QLabel(self.cardPatients)
        self.patientsCountLabel.setObjectName(u"patientsCountLabel")
        self.patientsCountLabel.setFont(font5)
        self.patientsCountLabel.setStyleSheet(u"color: #7A9CC6;")

        self.patientsHead.addWidget(self.patientsCountLabel)


        self.cardPatientsLayout.addLayout(self.patientsHead)

        self.patientsListLabel = QLabel(self.cardPatients)
        self.patientsListLabel.setObjectName(u"patientsListLabel")
        self.patientsListLabel.setFont(font3)
        self.patientsListLabel.setWordWrap(True)

        self.cardPatientsLayout.addWidget(self.patientsListLabel)

        self.btnOpenPatientsFromHome = QPushButton(self.cardPatients)
        self.btnOpenPatientsFromHome.setObjectName(u"btnOpenPatientsFromHome")
        self.btnOpenPatientsFromHome.setMinimumSize(QSize(180, 38))
        self.btnOpenPatientsFromHome.setMaximumSize(QSize(180, 38))
        self.btnOpenPatientsFromHome.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.cardPatientsLayout.addWidget(self.btnOpenPatientsFromHome)


        self.homePageLayout.addWidget(self.cardPatients)

        self.cardsRow = QHBoxLayout()
        self.cardsRow.setSpacing(16)
        self.cardsRow.setObjectName(u"cardsRow")
        self.cardPrescrHome = QFrame(self.homePage)
        self.cardPrescrHome.setObjectName(u"cardPrescrHome")
        self.cardPrescrHome.setMinimumSize(QSize(0, 150))
        self.cardPrescrHome.setStyleSheet(u"QFrame#cardPrescrHome { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#cardPrescrHome QLabel { color: #1A1A1A; background: transparent; }")
        self.cardPrescrHomeLayout = QVBoxLayout(self.cardPrescrHome)
        self.cardPrescrHomeLayout.setObjectName(u"cardPrescrHomeLayout")
        self.cardPrescrHomeLayout.setContentsMargins(22, 18, 22, 18)
        self.label1 = QLabel(self.cardPrescrHome)
        self.label1.setObjectName(u"label1")
        self.label1.setFont(font6)
        self.label1.setStyleSheet(u"color: #2F5C8F;")

        self.cardPrescrHomeLayout.addWidget(self.label1)

        self.label2 = QLabel(self.cardPrescrHome)
        self.label2.setObjectName(u"label2")
        self.label2.setFont(font5)
        self.label2.setWordWrap(True)

        self.cardPrescrHomeLayout.addWidget(self.label2)

        self.btnOpenPrescrFromHome = QPushButton(self.cardPrescrHome)
        self.btnOpenPrescrFromHome.setObjectName(u"btnOpenPrescrFromHome")
        self.btnOpenPrescrFromHome.setMinimumHeight(36)
        self.btnOpenPrescrFromHome.setMaximumSize(QSize(160, 36))
        self.btnOpenPrescrFromHome.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }")

        self.cardPrescrHomeLayout.addWidget(self.btnOpenPrescrFromHome)


        self.cardsRow.addWidget(self.cardPrescrHome)

        self.cardDiaryHome = QFrame(self.homePage)
        self.cardDiaryHome.setObjectName(u"cardDiaryHome")
        self.cardDiaryHome.setMinimumSize(QSize(0, 150))
        self.cardDiaryHome.setStyleSheet(u"QFrame#cardDiaryHome { background-color: #FFFFFF; border: none; border-radius: 16px; }\n"
"QFrame#cardDiaryHome QLabel { color: #1A1A1A; background: transparent; }")
        self.cardDiaryHomeLayout = QVBoxLayout(self.cardDiaryHome)
        self.cardDiaryHomeLayout.setObjectName(u"cardDiaryHomeLayout")
        self.cardDiaryHomeLayout.setContentsMargins(22, 18, 22, 18)
        self.label3 = QLabel(self.cardDiaryHome)
        self.label3.setObjectName(u"label3")
        self.label3.setFont(font6)
        self.label3.setStyleSheet(u"color: #2F5C8F;")

        self.cardDiaryHomeLayout.addWidget(self.label3)

        self.label4 = QLabel(self.cardDiaryHome)
        self.label4.setObjectName(u"label4")
        self.label4.setFont(font5)
        self.label4.setWordWrap(True)

        self.cardDiaryHomeLayout.addWidget(self.label4)

        self.btnOpenDiariesFromHome = QPushButton(self.cardDiaryHome)
        self.btnOpenDiariesFromHome.setObjectName(u"btnOpenDiariesFromHome")
        self.btnOpenDiariesFromHome.setMinimumHeight(36)
        self.btnOpenDiariesFromHome.setMaximumSize(QSize(160, 36))
        self.btnOpenDiariesFromHome.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }")

        self.cardDiaryHomeLayout.addWidget(self.btnOpenDiariesFromHome)


        self.cardsRow.addWidget(self.cardDiaryHome)


        self.homePageLayout.addLayout(self.cardsRow)

        self.homeBottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.homePageLayout.addItem(self.homeBottomSpacer)

        self.pages.addWidget(self.homePage)
        self.patientsPage = QWidget()
        self.patientsPage.setObjectName(u"patientsPage")
        self.patientsPageLayout = QVBoxLayout(self.patientsPage)
        self.patientsPageLayout.setObjectName(u"patientsPageLayout")
        self.patientsTable = QTableWidget(self.patientsPage)
        self.patientsTable.setObjectName(u"patientsTable")

        self.patientsPageLayout.addWidget(self.patientsTable)

        self.pages.addWidget(self.patientsPage)
        self.addPatientPage = QWidget()
        self.addPatientPage.setObjectName(u"addPatientPage")
        self.addPatientLayout = QVBoxLayout(self.addPatientPage)
        self.addPatientLayout.setSpacing(14)
        self.addPatientLayout.setObjectName(u"addPatientLayout")
        self.label5 = QLabel(self.addPatientPage)
        self.label5.setObjectName(u"label5")
        font7 = QFont()
        font7.setFamilies([u"Times New Roman"])
        font7.setPointSize(13)
        font7.setBold(True)
        self.label5.setFont(font7)
        self.label5.setStyleSheet(u"color: #2F5C8F;")

        self.addPatientLayout.addWidget(self.label5)

        self.newPatientFullName = QLineEdit(self.addPatientPage)
        self.newPatientFullName.setObjectName(u"newPatientFullName")
        self.newPatientFullName.setMinimumHeight(42)

        self.addPatientLayout.addWidget(self.newPatientFullName)

        self.genderRow = QHBoxLayout()
        self.genderRow.setObjectName(u"genderRow")
        self.label6 = QLabel(self.addPatientPage)
        self.label6.setObjectName(u"label6")
        self.label6.setFont(font3)

        self.genderRow.addWidget(self.label6)

        self.newPatientGender = QComboBox(self.addPatientPage)
        self.newPatientGender.addItem("")
        self.newPatientGender.addItem("")
        self.newPatientGender.setObjectName(u"newPatientGender")
        self.newPatientGender.setMinimumHeight(42)
        self.newPatientGender.setMinimumWidth(200)

        self.genderRow.addWidget(self.newPatientGender)

        self.genderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.genderRow.addItem(self.genderSpacer)


        self.addPatientLayout.addLayout(self.genderRow)

        self.newPatientPolicy = QLineEdit(self.addPatientPage)
        self.newPatientPolicy.setObjectName(u"newPatientPolicy")
        self.newPatientPolicy.setMinimumHeight(42)

        self.addPatientLayout.addWidget(self.newPatientPolicy)

        self.newPatientPhone = QLineEdit(self.addPatientPage)
        self.newPatientPhone.setObjectName(u"newPatientPhone")
        self.newPatientPhone.setMinimumHeight(42)

        self.addPatientLayout.addWidget(self.newPatientPhone)

        self.birthRow = QHBoxLayout()
        self.birthRow.setObjectName(u"birthRow")
        self.label7 = QLabel(self.addPatientPage)
        self.label7.setObjectName(u"label7")

        self.birthRow.addWidget(self.label7)

        self.newPatientBirthDate = QDateEdit(self.addPatientPage)
        self.newPatientBirthDate.setObjectName(u"newPatientBirthDate")
        self.newPatientBirthDate.setMinimumHeight(42)
        self.newPatientBirthDate.setCalendarPopup(True)

        self.birthRow.addWidget(self.newPatientBirthDate)

        self.birthSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.birthRow.addItem(self.birthSpacer)


        self.addPatientLayout.addLayout(self.birthRow)

        self.addPatientBtnRow = QHBoxLayout()
        self.addPatientBtnRow.setObjectName(u"addPatientBtnRow")
        self.addPatientBtnSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.addPatientBtnRow.addItem(self.addPatientBtnSpacer)

        self.createPatientBtn = QPushButton(self.addPatientPage)
        self.createPatientBtn.setObjectName(u"createPatientBtn")
        self.createPatientBtn.setMinimumSize(QSize(260, 46))
        self.createPatientBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 14px; font-weight: bold; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.addPatientBtnRow.addWidget(self.createPatientBtn)


        self.addPatientLayout.addLayout(self.addPatientBtnRow)

        self.addPatientBottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.addPatientLayout.addItem(self.addPatientBottomSpacer)

        self.pages.addWidget(self.addPatientPage)
        self.prescrPage = QWidget()
        self.prescrPage.setObjectName(u"prescrPage")
        self.prescrPageLayout = QVBoxLayout(self.prescrPage)
        self.prescrPageLayout.setSpacing(12)
        self.prescrPageLayout.setObjectName(u"prescrPageLayout")
        self.label8 = QLabel(self.prescrPage)
        self.label8.setObjectName(u"label8")
        self.label8.setFont(font7)
        self.label8.setStyleSheet(u"color: #2F5C8F;")

        self.prescrPageLayout.addWidget(self.label8)

        self.patientCombo = QComboBox(self.prescrPage)
        self.patientCombo.setObjectName(u"patientCombo")
        self.patientCombo.setMinimumHeight(42)

        self.prescrPageLayout.addWidget(self.patientCombo)

        self.medRow1 = QHBoxLayout()
        self.medRow1.setSpacing(8)
        self.medRow1.setObjectName(u"medRow1")
        self.medicationSearch = QLineEdit(self.prescrPage)
        self.medicationSearch.setObjectName(u"medicationSearch")
        self.medicationSearch.setMinimumHeight(42)

        self.medRow1.addWidget(self.medicationSearch)

        self.addMedicationBtn = QPushButton(self.prescrPage)
        self.addMedicationBtn.setObjectName(u"addMedicationBtn")
        self.addMedicationBtn.setMinimumSize(QSize(170, 42))
        self.addMedicationBtn.setStyleSheet(u"QPushButton { background-color: #7A9CC6; color: white; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #6A8CB6; }")

        self.medRow1.addWidget(self.addMedicationBtn)


        self.prescrPageLayout.addLayout(self.medRow1)

        self.medicationList = QListWidget(self.prescrPage)
        self.medicationList.setObjectName(u"medicationList")
        self.medicationList.setMaximumHeight(140)

        self.prescrPageLayout.addWidget(self.medicationList)

        self.prescrFormRow1 = QHBoxLayout()
        self.prescrFormRow1.setSpacing(12)
        self.prescrFormRow1.setObjectName(u"prescrFormRow1")
        self.dosageLine = QLineEdit(self.prescrPage)
        self.dosageLine.setObjectName(u"dosageLine")
        self.dosageLine.setMinimumHeight(42)

        self.prescrFormRow1.addWidget(self.dosageLine)

        self.freqLine = QLineEdit(self.prescrPage)
        self.freqLine.setObjectName(u"freqLine")
        self.freqLine.setMinimumHeight(42)

        self.prescrFormRow1.addWidget(self.freqLine)


        self.prescrPageLayout.addLayout(self.prescrFormRow1)

        self.prescrDateRow = QHBoxLayout()
        self.prescrDateRow.setSpacing(12)
        self.prescrDateRow.setObjectName(u"prescrDateRow")
        self.label9 = QLabel(self.prescrPage)
        self.label9.setObjectName(u"label9")

        self.prescrDateRow.addWidget(self.label9)

        self.startDate = QDateEdit(self.prescrPage)
        self.startDate.setObjectName(u"startDate")
        self.startDate.setMinimumHeight(42)

        self.prescrDateRow.addWidget(self.startDate)

        self.label10 = QLabel(self.prescrPage)
        self.label10.setObjectName(u"label10")

        self.prescrDateRow.addWidget(self.label10)

        self.endDate = QDateEdit(self.prescrPage)
        self.endDate.setObjectName(u"endDate")
        self.endDate.setMinimumHeight(42)

        self.prescrDateRow.addWidget(self.endDate)

        self.prescrDateSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.prescrDateRow.addItem(self.prescrDateSpacer)


        self.prescrPageLayout.addLayout(self.prescrDateRow)

        self.commentText = QTextEdit(self.prescrPage)
        self.commentText.setObjectName(u"commentText")
        self.commentText.setMaximumHeight(60)

        self.prescrPageLayout.addWidget(self.commentText)

        self.prescrBtnRow = QHBoxLayout()
        self.prescrBtnRow.setObjectName(u"prescrBtnRow")
        self.prescrBtnSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.prescrBtnRow.addItem(self.prescrBtnSpacer)

        self.addPrescrBtn = QPushButton(self.prescrPage)
        self.addPrescrBtn.setObjectName(u"addPrescrBtn")
        self.addPrescrBtn.setMinimumSize(QSize(240, 44))
        self.addPrescrBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 14px; font-weight: bold; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.prescrBtnRow.addWidget(self.addPrescrBtn)


        self.prescrPageLayout.addLayout(self.prescrBtnRow)

        self.prescrBottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.prescrPageLayout.addItem(self.prescrBottomSpacer)

        self.pages.addWidget(self.prescrPage)
        self.diariesPage = QWidget()
        self.diariesPage.setObjectName(u"diariesPage")
        self.diariesPageLayout = QVBoxLayout(self.diariesPage)
        self.diariesPageLayout.setSpacing(12)
        self.diariesPageLayout.setObjectName(u"diariesPageLayout")
        self.label11 = QLabel(self.diariesPage)
        self.label11.setObjectName(u"label11")
        self.label11.setFont(font7)
        self.label11.setStyleSheet(u"color: #2F5C8F;")

        self.diariesPageLayout.addWidget(self.label11)

        self.diaryTopRow = QHBoxLayout()
        self.diaryTopRow.setSpacing(12)
        self.diaryTopRow.setObjectName(u"diaryTopRow")
        self.diaryPatientCombo = QComboBox(self.diariesPage)
        self.diaryPatientCombo.setObjectName(u"diaryPatientCombo")
        self.diaryPatientCombo.setMinimumHeight(42)
        self.diaryPatientCombo.setMinimumWidth(320)

        self.diaryTopRow.addWidget(self.diaryPatientCombo)

        self.viewDiaryBtn = QPushButton(self.diariesPage)
        self.viewDiaryBtn.setObjectName(u"viewDiaryBtn")
        self.viewDiaryBtn.setMinimumSize(QSize(200, 42))
        self.viewDiaryBtn.setStyleSheet(u"QPushButton { background-color: #2F5C8F; color: #FFFFFF; border: none; border-radius: 10px; font-family: \"Times New Roman\"; font-size: 13px; }\n"
"QPushButton:hover { background-color: #1E4470; }")

        self.diaryTopRow.addWidget(self.viewDiaryBtn)

        self.diaryTopSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.diaryTopRow.addItem(self.diaryTopSpacer)


        self.diariesPageLayout.addLayout(self.diaryTopRow)

        self.diarySummaryLabel = QLabel(self.diariesPage)
        self.diarySummaryLabel.setObjectName(u"diarySummaryLabel")
        self.diarySummaryLabel.setFont(font5)
        self.diarySummaryLabel.setStyleSheet(u"color: #666666;")

        self.diariesPageLayout.addWidget(self.diarySummaryLabel)

        self.diaryListWidget = QWidget(self.diariesPage)
        self.diaryListWidget.setObjectName(u"diaryListWidget")
        self.diaryListWidget.setMinimumSize(QSize(0, 400))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.diaryListWidget.sizePolicy().hasHeightForWidth())
        self.diaryListWidget.setSizePolicy(sizePolicy)
        self.diaryListWidget.setStyleSheet(u"background: transparent;")
        self.diaryListLayout = QVBoxLayout(self.diaryListWidget)
        self.diaryListLayout.setSpacing(12)
        self.diaryListLayout.setObjectName(u"diaryListLayout")
        self.diaryListLayout.setContentsMargins(0, 0, 0, 0)

        self.diariesPageLayout.addWidget(self.diaryListWidget)

        self.pages.addWidget(self.diariesPage)
        self.helpPage = QWidget()
        self.helpPage.setObjectName(u"helpPage")
        self.helpLayout = QVBoxLayout(self.helpPage)
        self.helpLayout.setSpacing(14)
        self.helpLayout.setObjectName(u"helpLayout")
        self.label12 = QLabel(self.helpPage)
        self.label12.setObjectName(u"label12")
        self.label12.setFont(font4)
        self.label12.setStyleSheet(u"color: #2F5C8F;")

        self.helpLayout.addWidget(self.label12)

        self.helpText = QTextEdit(self.helpPage)
        self.helpText.setObjectName(u"helpText")
        self.helpText.setReadOnly(True)
        self.helpText.setStyleSheet(u"QTextEdit { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CCCCCC; border-radius: 10px; padding: 16px; font-family: \"Times New Roman\"; font-size: 13px; }")

        self.helpLayout.addWidget(self.helpText)

        self.pages.addWidget(self.helpPage)

        self.contentLayout.addWidget(self.pages)


        self.mainLayout.addWidget(self.contentWidget)

        DoctorWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DoctorWindow)

        QMetaObject.connectSlotsByName(DoctorWindow)
    # setupUi

    def retranslateUi(self, DoctorWindow):
        DoctorWindow.setWindowTitle(QCoreApplication.translate("DoctorWindow", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0432\u0440\u0430\u0447\u0430", None))
        self.avatarLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0412", None))
        self.nameLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0424\u0418\u041e \u0432\u0440\u0430\u0447\u0430", None))
        self.roleLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0412\u0440\u0430\u0447-\u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442", None))
        self.navHome.setText(QCoreApplication.translate("DoctorWindow", u"  \u0413\u043b\u0430\u0432\u043d\u0430\u044f", None))
        self.navPatients.setText(QCoreApplication.translate("DoctorWindow", u"  \u041c\u043e\u0438 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u044b", None))
        self.navAddPatient.setText(QCoreApplication.translate("DoctorWindow", u"  \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.navPrescriptions.setText(QCoreApplication.translate("DoctorWindow", u"  \u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f", None))
        self.navDiaries.setText(QCoreApplication.translate("DoctorWindow", u"  \u0414\u043d\u0435\u0432\u043d\u0438\u043a\u0438", None))
        self.navHelp.setText(QCoreApplication.translate("DoctorWindow", u"  \u041f\u043e\u043c\u043e\u0449\u044c (F1)", None))
        self.pageTitleLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0413\u043b\u0430\u0432\u043d\u0430\u044f", None))
        self.logoutBtn.setText(QCoreApplication.translate("DoctorWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.greetingLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0414\u043e\u0431\u0440\u044b\u0439 \u0434\u0435\u043d\u044c!", None))
        self.subGreetingLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u044f\u0439\u0442\u0435 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430\u043c\u0438 \u0438 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f\u043c\u0438", None))
        self.label.setText(QCoreApplication.translate("DoctorWindow", u"\u041c\u041e\u0418 \u041f\u0410\u0426\u0418\u0415\u041d\u0422\u042b", None))
        self.patientsCountLabel.setText(QCoreApplication.translate("DoctorWindow", u"0 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u043e\u0432", None))
        self.patientsListLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0423 \u0432\u0430\u0441 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442 \u043f\u0440\u0438\u043a\u0440\u0435\u043f\u043b\u0451\u043d\u043d\u044b\u0445 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u043e\u0432", None))
        self.btnOpenPatientsFromHome.setText(QCoreApplication.translate("DoctorWindow", u"\u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u043e\u0432", None))
        self.label1.setText(QCoreApplication.translate("DoctorWindow", u"\u041d\u0410\u0417\u041d\u0410\u0427\u0415\u041d\u0418\u042f", None))
        self.label2.setText(QCoreApplication.translate("DoctorWindow", u"\u0421\u043e\u0437\u0434\u0430\u0432\u0430\u0439\u0442\u0435 \u0438 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u0438\u0440\u0443\u0439\u0442\u0435 \u0441\u0445\u0435\u043c\u044b \u043b\u0435\u0447\u0435\u043d\u0438\u044f", None))
        self.btnOpenPrescrFromHome.setText(QCoreApplication.translate("DoctorWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
        self.label3.setText(QCoreApplication.translate("DoctorWindow", u"\u0414\u041d\u0415\u0412\u041d\u0418\u041a\u0418 \u041f\u0410\u0426\u0418\u0415\u041d\u0422\u041e\u0412", None))
        self.label4.setText(QCoreApplication.translate("DoctorWindow", u"\u041f\u0440\u043e\u0441\u043c\u0430\u0442\u0440\u0438\u0432\u0430\u0439\u0442\u0435 \u0437\u0430\u043f\u0438\u0441\u0438 \u0441\u0430\u043c\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u0438\u044f \u0438 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438", None))
        self.btnOpenDiariesFromHome.setText(QCoreApplication.translate("DoctorWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
        self.label5.setText(QCoreApplication.translate("DoctorWindow", u"\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u043d\u043e\u0432\u043e\u0433\u043e \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.newPatientFullName.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u0424\u0418\u041e \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.label6.setText(QCoreApplication.translate("DoctorWindow", u"\u041f\u043e\u043b:", None))
        self.newPatientGender.setItemText(0, QCoreApplication.translate("DoctorWindow", u"\u043c\u0443\u0436\u0441\u043a\u043e\u0439", None))
        self.newPatientGender.setItemText(1, QCoreApplication.translate("DoctorWindow", u"\u0436\u0435\u043d\u0441\u043a\u0438\u0439", None))

        self.newPatientPolicy.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u043e\u043b\u0438\u0441\u0430", None))
        self.newPatientPhone.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u0422\u0435\u043b\u0435\u0444\u043e\u043d", None))
        self.label7.setText(QCoreApplication.translate("DoctorWindow", u"\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f:", None))
        self.newPatientBirthDate.setDisplayFormat(QCoreApplication.translate("DoctorWindow", u"dd.MM.yyyy", None))
        self.createPatientBtn.setText(QCoreApplication.translate("DoctorWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.label8.setText(QCoreApplication.translate("DoctorWindow", u"\u041d\u043e\u0432\u043e\u0435 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435", None))
        self.medicationSearch.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u0440\u0435\u043f\u0430\u0440\u0430\u0442\u0430 \u0438\u043b\u0438 \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u043e\u0432\u044b\u0439", None))
        self.addMedicationBtn.setText(QCoreApplication.translate("DoctorWindow", u"+ \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0440\u0435\u043f\u0430\u0440\u0430\u0442", None))
        self.dosageLine.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u0414\u043e\u0437\u0438\u0440\u043e\u0432\u043a\u0430 (\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, 10 \u043c\u0433)", None))
        self.freqLine.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u041a\u0440\u0430\u0442\u043d\u043e\u0441\u0442\u044c (\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, 2 \u0440\u0430\u0437\u0430 \u0432 \u0434\u0435\u043d\u044c)", None))
        self.label9.setText(QCoreApplication.translate("DoctorWindow", u"\u041d\u0430\u0447\u0430\u043b\u043e:", None))
        self.label10.setText(QCoreApplication.translate("DoctorWindow", u"\u041a\u043e\u043d\u0435\u0446:", None))
        self.commentText.setPlaceholderText(QCoreApplication.translate("DoctorWindow", u"\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043a \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044e", None))
        self.addPrescrBtn.setText(QCoreApplication.translate("DoctorWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435", None))
        self.label11.setText(QCoreApplication.translate("DoctorWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430, \u0447\u0442\u043e\u0431\u044b \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0435\u0433\u043e \u0434\u043d\u0435\u0432\u043d\u0438\u043a", None))
        self.viewDiaryBtn.setText(QCoreApplication.translate("DoctorWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0434\u043d\u0435\u0432\u043d\u0438\u043a", None))
        self.diarySummaryLabel.setText(QCoreApplication.translate("DoctorWindow", u"\u0417\u0430\u043f\u0438\u0441\u0438 \u043d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u044b", None))
        self.label12.setText(QCoreApplication.translate("DoctorWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.helpText.setHtml(QCoreApplication.translate("DoctorWindow", u"<h2 style=\"color:#2F5C8F;\">\u041f\u0430\u043d\u0435\u043b\u044c \u0432\u0440\u0430\u0447\u0430</h2><p><b>\u041c\u043e\u0438 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u044b</b> \u2014 \u0441\u043f\u0438\u0441\u043e\u043a \u0432\u0430\u0448\u0438\u0445 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u043e\u0432.</p><p><b>\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430</b> \u2014 \u0441\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430 \u0441 \u0424\u0418\u041e, \u043f\u043e\u043b\u043e\u043c \u0438 \u0434\u0430\u043d\u043d\u044b\u043c\u0438.</p><p><b>\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f</b> \u2014 \u043f\u043e\u0438\u0441\u043a \u043f\u0440\u0435\u043f\u0430\u0440\u0430\u0442\u0430 \u0438\u043b\u0438 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0433\u043e.</p><p><b>\u0414\u043d\u0435\u0432\u043d\u0438\u043a\u0438</b> \u2014 \u0437\u0430\u043f\u0438\u0441\u0438"
                        " \u0441\u0430\u043c\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u0438\u044f \u0438 \u043f\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u0434\u0438\u0430\u0433\u043d\u043e\u0437\u0430 \u043f\u043e \u041c\u041a\u0411-10.</p><h3 style=\"color:#2F5C8F;\">\u0413\u043e\u0440\u044f\u0447\u0438\u0435 \u043a\u043b\u0430\u0432\u0438\u0448\u0438</h3><p><b>F1</b> \u2014 \u0441\u043f\u0440\u0430\u0432\u043a\u0430<br><b>Ctrl+Q</b> \u2014 \u0432\u044b\u0439\u0442\u0438<br><b>Ctrl+1\u20265</b> \u2014 \u0440\u0430\u0437\u0434\u0435\u043b\u044b</p>", None))
    # retranslateUi

