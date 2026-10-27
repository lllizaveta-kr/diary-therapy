"""Кабинет врача."""
from datetime import date, datetime
from PySide6.QtCore import QDate, Qt, QTime, QTimer
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFileDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QMainWindow, QPushButton, QScrollArea, QTextEdit, QTimeEdit,
    QVBoxLayout, QWidget,
)
import db
import pdf_exporter
from validators import validate_birth_date, validate_name, validate_phone, validate_policy
from windows import common
from windows.common import DiaryCard, MoodTrend, RxCard, human_date
from windows import msgbox as mb
from windows import widgets as w

TAB_COLORS = ["#1E4470", "#2F5C8F", "#5A7CA6", "#7A9CC6"]
FREQUENCIES = ["1 раз в день", "2 раза в день", "3 раза в день", "4 раза в день", "через день", "1 раз в неделю",
               "при боли", "при приступе"]


class TimeChip(QFrame):
    def __init__(self, text, on_remove):
        super().__init__()
        pl = w.pal()
        self.text = text
        self.setObjectName("timeChip")
        self.setStyleSheet(
            f"QFrame#timeChip {{ background: {pl['accent']}; border-radius: 15px; }} QLabel {{ color: white; background: transparent; }}")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 4, 4, 4)
        lay.setSpacing(4)
        lay.addWidget(w.label(text, 10, bold=True, color="#FFFFFF"))
        close = QPushButton("✕")
        close.setFixedSize(22, 22)
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.setStyleSheet(
            "QPushButton { background: rgba(255,255,255,0.18); color: white; border: none; border-radius: 11px; } QPushButton:hover { background: rgba(255,255,255,0.35); }")
        close.clicked.connect(lambda: on_remove(self))
        lay.addWidget(close)


class PatientCard(w.AnimatedCard):
    def __init__(self, p, active_rx):
        mood, mood_color = w.mood_of(p["last_wellbeing"])
        super().__init__(width=310, accent=mood_color)
        pl = w.pal()
        top = QHBoxLayout()
        top.setSpacing(12)
        top.addWidget(w.Avatar(p["full_name"], 52))
        col = QVBoxLayout()
        col.setSpacing(2)
        col.addWidget(w.label(p["full_name"], 11, bold=True, wrap=True))
        col.addWidget(w.label(common.patient_meta(p["birth_date"], p["gender"]), 9, color=pl["muted"]))
        top.addLayout(col, 1)
        self.body_layout.addLayout(top)

        mood_row = QHBoxLayout()
        mood_row.setSpacing(8)
        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background: {mood_color}; border-radius: 5px;")
        mood_row.addWidget(dot)
        when = p["last_entry"].strftime("%d.%m") if p["last_entry"] else ""
        mood_row.addWidget(w.label(f"{mood} · {when}" if when else "Дневник пока пуст", 9))
        mood_row.addStretch()
        self.body_layout.addLayout(mood_row)

        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet(f"background: {pl['line']};")
        self.body_layout.addWidget(line)

        pills = QHBoxLayout()
        pills.setSpacing(6)
        if active_rx:
            for r in active_rx[:4]:
                icon = w.PillIcon(r["form"], r["name_med"], 30)
                icon.setToolTip(f"{r['name_med']} {r['dosage']} — {r['frequency']}")
                pills.addWidget(icon)
            if len(active_rx) > 4:
                pills.addWidget(w.label(f"+{len(active_rx) - 4}", 9, bold=True, color=pl["accent"]))
            names = ", ".join(r["name_med"] for r in active_rx[:2])
            more = "…" if len(active_rx) > 2 else ""
            pills.addWidget(w.label(names + more, 9, color=pl["muted"]), 1)
        else:
            pills.addWidget(w.label("Нет активных назначений", 9, color=pl["muted"]))
            pills.addStretch()
        self.body_layout.addLayout(pills)

        stats = QHBoxLayout()
        stats.setSpacing(6)
        stats.addWidget(
            w.chip(w.plural(len(active_rx), "назначение", "назначения", "назначений"), pl["accent_soft"], pl["accent"]))
        stats.addWidget(w.chip(w.plural(p["diary_count"], "запись", "записи", "записей"), pl["card_alt"], pl["muted"]))
        stats.addStretch()
        self.body_layout.addLayout(stats)


class MedTile(w.AnimatedCard):
    def __init__(self, m):
        super().__init__(width=126)
        pl = w.pal()
        self.data = m
        self.setToolTip(" · ".join(x for x in (m["name_med"], m["dosage"], m["form"], m["manufacturer"]) if x))
        self.body_layout.setContentsMargins(8, 12, 8, 12)
        self.body_layout.setSpacing(4)
        self.pill = w.PillIcon(m["form"], m["name_med"], 50)
        self.body_layout.addWidget(self.pill, 0, Qt.AlignmentFlag.AlignHCenter)
        title = m["name_med"] if len(m["name_med"]) <= 12 else m["name_med"][:10].rstrip() + "…"
        name = w.label(title, 9, bold=True, wrap=True)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(name)
        sub = w.label(" · ".join(x for x in (m["dosage"], m["form"]) if x), 8, color=pl["muted"], wrap=True)
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(sub)


class PatientPicker(QScrollArea):
    def __init__(self, on_pick):
        super().__init__()
        self.on_pick = on_pick
        self._buttons = {}
        self.setWidgetResizable(True)
        self.setFixedHeight(66)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(
            "QScrollArea { background: transparent; border: none; } QScrollArea > QWidget > QWidget { background: transparent; }")
        self.inner = QWidget()
        self.row = QHBoxLayout(self.inner)
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.setSpacing(8)
        self.setWidget(self.inner)

    def set_patients(self, patients):
        while self.row.count():
            item = self.row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons = {}
        pl = w.pal()
        for p in patients:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(52)
            btn.setStyleSheet(
                f"QPushButton {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 26px; padding: 0 14px 0 4px; text-align: left; }} QPushButton:hover {{ border-color: {pl['accent']}; }} QPushButton:checked {{ background: {pl['accent_soft']}; border: 2px solid {pl['accent']}; }}")
            lay = QHBoxLayout(btn)
            lay.setContentsMargins(4, 4, 14, 4)
            lay.setSpacing(8)
            _, color = w.mood_of(p["last_wellbeing"])
            lay.addWidget(w.Avatar(p["full_name"], 42, ring=color))
            lay.addWidget(w.label(w.short_name(p["full_name"]), 10, bold=True))
            btn.setMinimumWidth(60 + btn.fontMetrics().horizontalAdvance(w.short_name(p["full_name"])) + 40)
            btn.clicked.connect(lambda _=False, i=p["id_patient"]: self.select(i, notify=True))
            self.row.addWidget(btn)
            self._buttons[p["id_patient"]] = btn
        self.row.addStretch()

    def select(self, id_patient, notify=False):
        for i, b in self._buttons.items():
            b.setChecked(i == id_patient)
        if notify:
            self.on_pick(id_patient)


class NewPatientDialog(QDialog):
    def __init__(self, parent, id_doctor):
        super().__init__(parent)
        pl = w.pal()
        self.id_doctor = id_doctor
        self.result_data = None
        self.setWindowTitle("Новый пациент")
        self.setMinimumWidth(500)
        self.setStyleSheet(f"QDialog {{ background: {pl['bg']}; }}" + w.input_qss())

        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 22, 26, 22)
        lay.setSpacing(8)
        head = QHBoxLayout()
        self.avatar = w.Avatar("", 56)
        head.addWidget(self.avatar)
        col = QVBoxLayout()
        col.addWidget(w.label("Новый пациент", 15, bold=True))
        col.addWidget(w.label("Логин и пароль будут созданы автоматически", 9, color=pl["muted"]))
        head.addLayout(col, 1)
        lay.addLayout(head)

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Фамилия Имя Отчество")
        self.full_name.textChanged.connect(self._on_name)
        self.birth = QDateEdit(QDate(1990, 1, 1))
        self.birth.setCalendarPopup(True)
        self.birth.setDisplayFormat("dd.MM.yyyy")
        self.gender = QComboBox()
        self.gender.addItems(["мужской", "женский"])
        self.policy = QLineEdit()
        self.policy.setPlaceholderText("16 цифр")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("+7XXXXXXXXXX")
        self.login_hint = w.label("", 9, color=pl["muted"])

        lay.addWidget(w.label("ФИО", 9, color=pl["muted"]))
        lay.addWidget(self.full_name)
        lay.addWidget(self.login_hint)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(4)
        for i, (cap, field) in enumerate((("Дата рождения", self.birth), ("Пол", self.gender),
                                          ("Полис ОМС", self.policy), ("Телефон", self.phone))):
            grid.addWidget(w.label(cap, 9, color=pl["muted"]), (i // 2) * 2, i % 2)
            grid.addWidget(field, (i // 2) * 2 + 1, i % 2)
        lay.addLayout(grid)

        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel = w.ghost_button("Отмена")
        cancel.clicked.connect(self.reject)
        create = w.primary_button("Зарегистрировать")
        create.clicked.connect(self._create)
        buttons.addWidget(cancel)
        buttons.addWidget(create)
        lay.addSpacing(8)
        lay.addLayout(buttons)

    def _on_name(self, text):
        self.avatar.full_name = text
        self.avatar.update()
        self.login_hint.setText(f"Логин: {db.generate_login(text)}" if text.strip() else "")

    def _create(self):
        full_name = self.full_name.text().strip()
        birth = self.birth.date().toString("yyyy-MM-dd")
        for (ok, err), title in (
                (validate_name(full_name), "Ошибка в ФИО"), (validate_birth_date(birth), "Ошибка в дате рождения"),
                (validate_policy(self.policy.text()), "Ошибка в полисе"),
                (validate_phone(self.phone.text()), "Ошибка в телефоне")):
            if not ok:
                mb.warning(self, title, err)
                return
        login = db.find_free_login(db.generate_login(full_name))
        password = db.generate_password()
        id_user = db.create_patient_by_doctor(self.id_doctor, full_name, birth, self.gender.currentText(),
                                              self.policy.text().strip(), self.phone.text().strip(), login, password)
        if id_user is None:
            mb.critical(self, "Ошибка", "Не удалось создать пациента.")
            return
        self.result_data = {"id_user": id_user, "login": login, "password": password}
        self.accept()


class DoctorWindow(QMainWindow):
    def __init__(self, user_data, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.id_user = user_data["id_user"]
        self.full_name = user_data["full_name"]

        doctor = db.get_doctor_by_user(self.id_user)
        if not doctor:
            mb.critical(self, "Ошибка", "Профиль врача не найден")
            self.close()
            return
        self.id_doctor = doctor[0]
        self.profile = db.get_doctor_crm(self.id_doctor) or {}
        self._selected_med = None
        self._med_tiles = []
        self._times = []
        self._diary_patient = None

        pl = w.pal()
        self.setWindowTitle("Дневник терапии — кабинет врача")
        self.resize(1400, 900)
        self.setMinimumSize(1150, 740)

        central = QWidget()
        central.setObjectName("docRoot")
        central.setStyleSheet(f"QWidget#docRoot {{ background: {pl['bg']}; }}" + w.input_qss())
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(26, 18, 26, 14)
        root.setSpacing(14)
        root.addLayout(self._build_header())

        self.kpi_row = QHBoxLayout()
        self.kpi_row.setSpacing(8)
        root.addLayout(self.kpi_row)

        self.tabs = w.FolderTabs()
        self.tabs.add_tab(self._build_patients(), "Мои пациенты", "users", TAB_COLORS[0])
        self.tabs.add_tab(self._build_prescriptions(), "Назначения", "pill", TAB_COLORS[1])
        self.tabs.add_tab(self._build_diaries(), "Дневники", "book", TAB_COLORS[2])
        self.tabs.add_tab(self._build_help(), "Справка", "file", TAB_COLORS[3])
        self.tabs.currentChanged.connect(lambda _: self.panel.close_panel())
        root.addWidget(self.tabs, 1)

        self.panel = w.SidePanel(central)

        QShortcut(QKeySequence("F1"), self, lambda: self.tabs.set_current(3))
        QShortcut(QKeySequence("Ctrl+Q"), self, self.on_logout)
        QShortcut(QKeySequence("Ctrl+N"), self, self.on_new_patient)
        QShortcut(QKeySequence("Ctrl+F"), self, self._focus_search)
        for i in range(4):
            QShortcut(QKeySequence(f"Ctrl+{i + 1}"), self, lambda i=i: self.tabs.set_current(i))

        QTimer.singleShot(50, self.refresh_all)

    def _build_header(self):
        pl = w.pal()
        row = QHBoxLayout()
        row.setSpacing(14)
        logo = QLabel("ДТ")
        logo.setFixedSize(44, 44)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont(w.FONT, 13, QFont.Weight.Bold))
        logo.setStyleSheet(
            "color: white; border-radius: 13px; background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #2F5C8F, stop:1 #163257);")
        row.addWidget(logo)

        titles = QVBoxLayout()
        titles.setSpacing(0)
        hour = datetime.now().hour
        greeting = (
            "Доброе утро" if 5 <= hour < 12 else "Добрый день" if hour < 18 else "Добрый вечер" if hour < 23 else "Доброй ночи")
        parts = self.full_name.split()
        name = " ".join(parts[1:3]) if len(parts) > 1 else self.full_name
        titles.addWidget(w.label(f"{greeting}, {name}!", 15, bold=True))
        titles.addWidget(w.label("Кабинет врача · Дневник терапии", 9, color=pl["muted"]))
        row.addLayout(titles)
        row.addStretch()

        add = w.primary_button("+  Новый пациент")
        add.setToolTip("Ctrl+N")
        add.clicked.connect(self.on_new_patient)
        row.addWidget(add)

        self.me_btn = QPushButton()
        self.me_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.me_btn.setToolTip("Мой профиль и фото")
        self.me_btn.setMinimumHeight(56)
        self.me_btn.setStyleSheet(
            f"QPushButton {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 28px; }} QPushButton:hover {{ border-color: {pl['accent']}; }}")
        me = QHBoxLayout(self.me_btn)
        me.setContentsMargins(5, 4, 16, 4)
        me.setSpacing(10)
        self.me_avatar = w.Avatar(self.full_name, 46, w.doctor_photo_path(self.profile.get("photo")), ring=pl["accent"])
        me.addWidget(self.me_avatar)
        me_col = QVBoxLayout()
        me_col.setSpacing(0)
        me_col.addWidget(w.label(w.short_name(self.full_name), 10, bold=True))
        me_col.addWidget(w.label(self.profile.get("specialty") or "врач", 8, color=pl["muted"]))
        me.addLayout(me_col)
        self.me_btn.setMinimumWidth(110 + self.me_btn.fontMetrics().horizontalAdvance(w.short_name(self.full_name)))
        self.me_btn.clicked.connect(self.open_profile)
        row.addWidget(self.me_btn)

        logout = w.ghost_button("Выйти")
        logout.setToolTip("Ctrl+Q")
        logout.clicked.connect(self.on_logout)
        row.addWidget(logout)
        return row

    def _build_patients(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        bar = QHBoxLayout()
        bar.setSpacing(10)
        self.patient_search = w.search_line("Поиск по ФИО, полису, телефону")
        self.patient_search.textChanged.connect(self._render_patients)
        self.patient_filter = w.SegmentedFilter(
            [("all", "Все"), ("attention", "Требуют внимания"), ("no_rx", "Без назначений")])
        self.patient_filter.changed.connect(self._render_patients)
        export_btn = w.ghost_button("Выгрузить список PDF")
        export_btn.clicked.connect(self.export_my_patients_pdf)
        bar.addWidget(self.patient_search, 1)
        bar.addWidget(self.patient_filter)
        bar.addWidget(export_btn)
        lay.addLayout(bar)

        self.patients_count = w.label("", 9, color=w.pal()["muted"])
        lay.addWidget(self.patients_count)
        self.patients_grid = w.CardGrid("Пациенты не найдены")
        lay.addWidget(self.patients_grid, 1)
        return page

    def _build_prescriptions(self):
        pl = w.pal()
        page = QWidget()
        lay = QHBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(18)

        form_inner = QWidget()
        form_inner.setStyleSheet("background: transparent;")
        form = QVBoxLayout(form_inner)
        form.setContentsMargins(0, 0, 8, 0)
        form.setSpacing(6)
        form.addWidget(w.label("Новое назначение", 13, bold=True))
        form.addWidget(w.label("Пациент", 9, color=pl["muted"]))
        self.rx_patient = QComboBox()
        form.addWidget(self.rx_patient)

        med_head = QHBoxLayout()
        med_head.addWidget(w.label("Препарат", 9, color=pl["muted"]))
        med_head.addStretch()
        add_med = QPushButton("+ свой препарат")
        add_med.setCursor(Qt.CursorShape.PointingHandCursor)
        add_med.setStyleSheet(
            f"QPushButton {{ color: {pl['accent']}; background: transparent; border: none; font-family: '{w.FONT}'; font-size: 9pt; font-weight: 600; }} QPushButton:hover {{ text-decoration: underline; }}")
        add_med.clicked.connect(self.on_new_medication)
        med_head.addWidget(add_med)
        form.addLayout(med_head)

        self.med_search = w.search_line("Название препарата")
        self.med_search.textChanged.connect(self._render_meds)
        form.addWidget(self.med_search)
        self.med_grid = w.CardGrid("Препарат не найден — добавьте свой")
        self.med_grid.setFixedHeight(250)
        form.addWidget(self.med_grid)
        self.med_selected = w.label("Препарат не выбран", 9, color=pl["muted"])
        form.addWidget(self.med_selected)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(4)
        self.rx_dosage = QLineEdit()
        self.rx_dosage.setPlaceholderText("10 мг")
        self.rx_freq = QComboBox()
        self.rx_freq.setEditable(True)
        self.rx_freq.addItems(FREQUENCIES)
        self.rx_start = QDateEdit(QDate.currentDate())
        self.rx_end = QDateEdit(QDate.currentDate().addDays(30))
        for d in (self.rx_start, self.rx_end):
            d.setCalendarPopup(True)
            d.setDisplayFormat("dd.MM.yyyy")
        for i, (cap, field) in enumerate((("Дозировка", self.rx_dosage), ("Кратность", self.rx_freq),
                                          ("Начало", self.rx_start), ("Окончание", self.rx_end))):
            grid.addWidget(w.label(cap, 9, color=pl["muted"]), (i // 2) * 2, i % 2)
            grid.addWidget(field, (i // 2) * 2 + 1, i % 2)
        form.addLayout(grid)

        quick = QHBoxLayout()
        quick.setSpacing(6)
        quick.addWidget(w.label("Курс:", 9, color=pl["muted"]))
        for days in (7, 14, 30, 90):
            b = self._small_button(f"{days} дн.")
            b.clicked.connect(lambda _=False, d=days: self.rx_end.setDate(self.rx_start.date().addDays(d)))
            quick.addWidget(b)
        quick.addStretch()
        form.addLayout(quick)

        form.addWidget(w.label("Время приёма (пациенту придут напоминания)", 9, color=pl["muted"]))
        times = QHBoxLayout()
        times.setSpacing(6)
        self.rx_time = QTimeEdit(QTime(8, 0))
        self.rx_time.setDisplayFormat("HH:mm")
        add_time = self._small_button("Добавить")
        add_time.clicked.connect(lambda: self._add_time(self.rx_time.time().toString("HH:mm")))
        times.addWidget(self.rx_time)
        times.addWidget(add_time)
        for t in ("08:00", "14:00", "20:00"):
            b = self._small_button(t)
            b.clicked.connect(lambda _=False, t=t: self._add_time(t))
            times.addWidget(b)
        times.addStretch()
        form.addLayout(times)

        self.times_box = QWidget()
        self.times_box.setStyleSheet("background: transparent;")
        self.times_flow = w.FlowLayout(self.times_box, spacing=6)
        self.times_flow.setContentsMargins(0, 0, 0, 0)
        form.addWidget(self.times_box)

        form.addWidget(w.label("Комментарий для пациента", 9, color=pl["muted"]))
        self.rx_comment = QTextEdit()
        self.rx_comment.setPlaceholderText("Например: после еды, запивать водой")
        self.rx_comment.setFixedHeight(64)
        form.addWidget(self.rx_comment)

        create = w.primary_button("Назначить")
        create.clicked.connect(self.on_create_prescription)
        form.addSpacing(4)
        form.addWidget(create)
        form.addStretch()

        form_card = w.AnimatedCard(clickable=False)
        form_card.setFixedWidth(500)
        form_card.body_layout.setContentsMargins(18, 16, 10, 16)
        form_card.body_layout.addWidget(w.make_scroll(form_inner))
        lay.addWidget(form_card)

        right = QVBoxLayout()
        right.setSpacing(10)
        head = QHBoxLayout()
        head.addWidget(w.label("Мои назначения", 13, bold=True))
        head.addStretch()
        self.rx_filter = w.SegmentedFilter([("active", "Активные"), ("completed", "Завершённые"), ("all", "Все")])
        self.rx_filter.changed.connect(self._render_rx)
        head.addWidget(self.rx_filter)
        right.addLayout(head)

        self.rx_patient_filter = QComboBox()
        self.rx_patient_filter.currentIndexChanged.connect(self._render_rx)
        right.addWidget(self.rx_patient_filter)
        self.rx_grid = w.CardGrid("Назначений нет")
        right.addWidget(self.rx_grid, 1)
        lay.addLayout(right, 1)
        return page

    def _small_button(self, text):
        pl = w.pal()
        b = QPushButton(text)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setMinimumHeight(32)
        b.setStyleSheet(
            f"QPushButton {{ background: {pl['accent_soft']}; color: {pl['accent']}; border: none; border-radius: 9px; padding: 4px 10px; font-family: '{w.FONT}'; font-size: 9pt; font-weight: 600; }} QPushButton:hover {{ background: {pl['accent']}; color: white; }}")
        return b

    def _build_diaries(self):
        pl = w.pal()
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        self.picker = PatientPicker(self.show_diary)
        lay.addWidget(self.picker)

        self.diary_inner = QWidget()
        self.diary_inner.setStyleSheet("background: transparent;")
        self.diary_layout = QVBoxLayout(self.diary_inner)
        self.diary_layout.setContentsMargins(0, 0, 8, 0)
        self.diary_layout.setSpacing(4)
        self.diary_layout.addWidget(w.label("Выберите пациента", 11, color=pl["muted"]))
        lay.addWidget(w.make_scroll(self.diary_inner), 1)
        return page

    def _build_help(self):
        pl = w.pal()
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        flow = w.FlowLayout(inner, spacing=12)
        sections = [
            ("users", "Мои пациенты",
             "Карточки прикреплённых к вам пациентов. Цвет точки — последнее самочувствие из дневника. Фильтр «Требуют внимания» оставляет тех, кому плохо. Клик по карточке — карта пациента с назначениями и динамикой."),
            ("pill", "Назначения",
             "Выберите пациента и препарат плиткой, укажите дозировку и курс. Время приёма добавляется чипами — пациенту в эти часы придёт напоминание. Клик по назначению справа позволяет завершить или возобновить курс."),
            ("book", "Дневники",
             "Лента записей пациента с графиком самочувствия. Кнопка «Диагноз и комментарий» открывает справочник МКБ-10 и поле для рекомендаций."),
            ("user", "Профиль",
             "Нажмите на своё фото в шапке, чтобы загрузить или заменить фотографию. Специальность, кабинет и график меняет администратор."),
        ]
        for icon, title, text in sections:
            card = w.AnimatedCard(width=330, clickable=False)
            head = QHBoxLayout()
            head.addWidget(w.Icon(icon, 40, pl["accent"], pl["accent_soft"], 12))
            head.addWidget(w.label(title, 11, bold=True), 1)
            card.body_layout.addLayout(head)
            card.body_layout.addWidget(w.label(text, 9, color=pl["muted"], wrap=True))
            flow.addWidget(card)

        keys = w.AnimatedCard(width=330, clickable=False)
        keys.body_layout.addWidget(w.label("Горячие клавиши", 11, bold=True))
        for k, d in (("Ctrl+1…4", "переключение вкладок"), ("Ctrl+N", "новый пациент"), ("Ctrl+F", "поиск"),
                     ("Esc", "закрыть боковую панель"), ("F1", "справка"), ("Ctrl+Q", "выйти")):
            r = QHBoxLayout()
            key = w.label(k, 9, bold=True, color=pl["accent"])
            key.setMinimumWidth(80)
            r.addWidget(key)
            r.addWidget(w.label(d, 9, color=pl["muted"]), 1)
            keys.body_layout.addLayout(r)
        flow.addWidget(keys)
        return w.make_scroll(inner)

    def refresh_all(self):
        self.patients = [p for p in db.get_patients_crm() if p["id_doctor"] == self.id_doctor]
        self.rx = db.get_prescriptions_by_doctor(self.id_doctor)
        self.meds = db.get_medications_full()
        self._fill_patient_combos()
        self._render_kpi()
        self._render_patients()
        self._render_meds()
        self._render_rx()
        self.picker.set_patients(self.patients)
        if self._diary_patient:
            self.picker.select(self._diary_patient)
            self.show_diary(self._diary_patient)
        elif self.patients:
            self.picker.select(self.patients[0]["id_patient"], notify=True)

    def _active_rx(self, id_patient):
        return [r for r in self.rx if r["id_patient"] == id_patient and r["status"] == "active"]

    def _fill_patient_combos(self):
        for combo, first in ((self.rx_patient, None), (self.rx_patient_filter, "Все пациенты")):
            current = combo.currentData()
            combo.blockSignals(True)
            combo.clear()
            if first:
                combo.addItem(first, None)
            for p in self.patients:
                combo.addItem(p["full_name"], p["id_patient"])
            idx = combo.findData(current)
            combo.setCurrentIndex(idx if idx >= 0 else 0)
            combo.blockSignals(False)

    def _render_kpi(self):
        while self.kpi_row.count():
            item = self.kpi_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        week_ago = date.today().toordinal() - 6
        attention = [p for p in self.patients if w.mood_of(p["last_wellbeing"])[0] in ("Плохо", "Очень плохо")]
        recent = sum(1 for p in self.patients if p["last_entry"] and p["last_entry"].toordinal() >= week_ago)
        tiles = [
            w.KpiTile("users", "моих пациентов", len(self.patients), "#2F5C8F"),
            w.KpiTile("pill", "активных назначений", sum(1 for r in self.rx if r["status"] == "active"), "#2F5C8F"),
            w.KpiTile("book", "пациентов вели дневник за неделю", recent, "#2F5C8F"),
            w.KpiTile("stethoscope", "требуют внимания", len(attention), "#2F5C8F",
                      "по последней записи" if attention else ""),
        ]
        for i, t in enumerate(tiles):
            self.kpi_row.addWidget(t)
            t.appear(i * 70)

    def _render_patients(self, *_):
        text = self.patient_search.text().strip().lower()
        mode = self.patient_filter.value()
        cards = []
        for p in self.patients:
            hay = " ".join(str(p[k] or "") for k in ("full_name", "policy_number", "phone", "login")).lower()
            if text and text not in hay:
                continue
            active = self._active_rx(p["id_patient"])
            if mode == "attention" and w.mood_of(p["last_wellbeing"])[0] not in ("Плохо", "Очень плохо"):
                continue
            if mode == "no_rx" and active:
                continue
            card = PatientCard(p, active)
            card.clicked.connect(lambda i=p["id_patient"]: self.open_patient(i))
            cards.append(card)
        self.patients_grid.set_cards(cards)
        self.patients_count.setText(f"Показано {len(cards)} из {len(self.patients)}")

    def _render_meds(self, *_):
        text = self.med_search.text().strip().lower()
        tiles = []
        for m in self.meds:
            if text and text not in f"{m['name_med']} {m['form'] or ''}".lower():
                continue
            tile = MedTile(m)
            tile.set_selected(m["id_medication"] == self._selected_med)
            tile.clicked.connect(lambda m=m: self._select_med(m))
            tiles.append(tile)
        self._med_tiles = tiles
        self.med_grid.set_cards(tiles)

    def _select_med(self, m):
        self._selected_med = m["id_medication"]
        for t in self._med_tiles:
            t.set_selected(t.data["id_medication"] == self._selected_med)
            if t.data["id_medication"] == self._selected_med:
                t.pill.wobble()
        self.med_selected.setText(f"Выбран: {m['name_med']} {m['dosage'] or ''}".strip())
        self.med_selected.setStyleSheet(f"color: {w.pal()['accent']}; background: transparent; font-weight: 600;")
        if m["dosage"]:
            self.rx_dosage.setText(m["dosage"])

    def _render_rx(self, *_):
        mode = self.rx_filter.value()
        id_patient = self.rx_patient_filter.currentData()
        cards = []
        for r in self.rx:
            if mode != "all" and r["status"] != mode:
                continue
            if id_patient and r["id_patient"] != id_patient:
                continue
            card = RxCard(r)
            card.clicked.connect(lambda r=r: self.open_prescription(r))
            cards.append(card)
        self.rx_grid.set_cards(cards)

    def _add_time(self, t):
        if t in self._times:
            return
        self._times.append(t)
        self._times.sort()
        self._render_times()

    def _remove_time(self, chip):
        if chip.text in self._times:
            self._times.remove(chip.text)
        self._render_times()

    def _render_times(self):
        self.times_flow.clear()
        for t in self._times:
            self.times_flow.addWidget(TimeChip(t, self._remove_time))
        self.times_box.updateGeometry()

    def on_new_patient(self):
        dlg = NewPatientDialog(self, self.id_doctor)
        if dlg.exec() and dlg.result_data:
            r = dlg.result_data
            db.log_action(self.id_user, "create_user", "users", r["id_user"])
            self.refresh_all()
            common.CredentialsDialog(self, r["login"], r["password"], "Пациент зарегистрирован",
                                     "Пациент прикреплён к вам. Передайте ему логин и пароль для входа.").exec()
            self.tabs.set_current(0)

    def on_new_medication(self):
        dlg = common.NewMedicationDialog(self, self.med_search.text().strip())
        if dlg.exec() and dlg.id_medication:
            self.meds = db.get_medications_full()
            self.med_search.clear()
            m = next((x for x in self.meds if x["id_medication"] == dlg.id_medication), None)
            self._selected_med = dlg.id_medication
            self._render_meds()
            if m:
                self._select_med(m)

    def on_create_prescription(self):
        if self.rx_patient.count() == 0:
            mb.warning(self, "Нет пациентов", "Сначала зарегистрируйте пациента.")
            return
        if not self._selected_med:
            mb.warning(self, "Не выбран препарат", "Выберите препарат из списка или добавьте свой.")
            self.med_search.setFocus()
            return
        dosage = self.rx_dosage.text().strip()
        freq = self.rx_freq.currentText().strip()
        if not dosage or not freq:
            mb.warning(self, "Не заполнено", "Укажите дозировку и кратность приёма.")
            return
        if self.rx_end.date() < self.rx_start.date():
            mb.warning(self, "Даты", "Дата окончания раньше даты начала.")
            return
        id_rx = db.create_prescription(self.rx_patient.currentData(), self.id_doctor, self._selected_med, dosage, freq,
                                       self.rx_start.date().toString("yyyy-MM-dd"),
                                       self.rx_end.date().toString("yyyy-MM-dd"), self.rx_comment.toPlainText().strip())
        if not id_rx:
            mb.critical(self, "Ошибка", "Не удалось создать назначение")
            return
        for t in self._times:
            db.create_prescription_schedule(id_rx, f"{t}:00", dosage, "")
        db.log_action(self.id_user, "create_prescription", "prescriptions", id_rx)

        patient = self.rx_patient.currentText()
        times = f"\nВремя приёма: {', '.join(self._times)}" if self._times else ""
        self._selected_med = None
        self._times = []
        self._render_times()
        self.rx_dosage.clear()
        self.rx_comment.clear()
        self.med_search.clear()
        self.med_selected.setText("Препарат не выбран")
        self.med_selected.setStyleSheet(f"color: {w.pal()['muted']}; background: transparent;")
        self.rx_filter.set_value("active")
        self.refresh_all()
        mb.info(self, "Готово", f"Назначение для «{patient}» создано.{times}")

    def _focus_search(self):
        line = {0: self.patient_search, 1: self.med_search}.get(self.tabs.bar.current())
        if line:
            line.setFocus()
            line.selectAll()

    def on_logout(self):
        if self.login_window:
            self.login_window.return_from_child()
        self.close()

    def open_patient(self, id_patient):
        p = next((x for x in self.patients if x["id_patient"] == id_patient), None)
        if not p:
            return
        pl = w.pal()
        self.panel.open_panel("Карта пациента")
        lay = self.panel.content_layout

        mood, color = w.mood_of(p["last_wellbeing"])
        head = QHBoxLayout()
        head.setSpacing(14)
        head.addWidget(w.Avatar(p["full_name"], 72, ring=color))
        col = QVBoxLayout()
        col.setSpacing(4)
        col.addWidget(w.label(p["full_name"], 14, bold=True, wrap=True))
        col.addWidget(w.label(common.patient_meta(p["birth_date"], p["gender"]), 9, color=pl["muted"]))
        col.addWidget(w.chip(f"Самочувствие: {mood}", color))
        head.addLayout(col, 1)
        lay.addLayout(head)

        exp_diary = w.ghost_button("Выгрузить дневник в PDF")
        exp_diary.clicked.connect(lambda: self.export_diary_pdf(id_patient, p["full_name"]))
        lay.addWidget(exp_diary)

        actions = QHBoxLayout()
        give = w.primary_button("Назначить препарат")
        give.clicked.connect(lambda: self._goto_prescribe(id_patient))
        diary = w.ghost_button("Открыть дневник")
        diary.clicked.connect(lambda: self._goto_diary(id_patient))
        actions.addWidget(give)
        actions.addWidget(diary)
        lay.addLayout(actions)

        lay.addWidget(w.info_block(
            [("Дата рождения", common.fmt_date(p["birth_date"])), ("Полис ОМС", p["policy_number"]),
             ("Телефон", p["phone"]), ("Логин", p["login"])]))

        entries = db.get_diary_full(id_patient)
        lay.addWidget(w.section_title("Динамика самочувствия"))
        trend_box = QFrame()
        trend_box.setObjectName("trendBox")
        trend_box.setStyleSheet(
            f"QFrame#trendBox {{ background: {pl['card']}; border-radius: 14px; border: 1px solid {pl['line']}; }}")
        tl = QVBoxLayout(trend_box)
        tl.setContentsMargins(8, 8, 8, 4)
        tl.addWidget(MoodTrend(entries, 120))
        lay.addWidget(trend_box)

        rx = db.get_prescriptions_full(id_patient)
        lay.addWidget(w.section_title(f"Назначения · {len(rx)}"))
        if not rx:
            lay.addWidget(w.label("Назначений пока нет", 9, color=pl["muted"]))
        for r in rx:
            lay.addWidget(common.rx_row(r))
        lay.addStretch()

    def _goto_prescribe(self, id_patient):
        self.panel.close_panel()
        self.rx_patient.setCurrentIndex(max(0, self.rx_patient.findData(id_patient)))
        self.tabs.set_current(1)
        self.med_search.setFocus()

    def _goto_diary(self, id_patient):
        self.panel.close_panel()
        self.tabs.set_current(2)
        self.picker.select(id_patient, notify=True)

    def open_prescription(self, r):
        pl = w.pal()
        self.panel.open_panel("Назначение")
        lay = self.panel.content_layout

        head = QHBoxLayout()
        head.setSpacing(14)
        pill = w.PillIcon(r["form"], r["name_med"], 84)
        head.addWidget(pill)
        QTimer.singleShot(350, pill.wobble)
        col = QVBoxLayout()
        col.addWidget(w.label(r["name_med"], 15, bold=True, wrap=True))
        col.addWidget(w.label(f"{r['dosage']} · {r['form'] or ''}", 10, color=pl["muted"]))
        col.addWidget(common.status_chip(r["status"]))
        head.addLayout(col, 1)
        lay.addLayout(head)

        lay.addWidget(w.info_block(
            [("Пациент", r["patient_name"]), ("Кратность", r["frequency"]), ("Время приёма", r["times"] or "не задано"),
             ("Начало", common.fmt_date(r["start_date"])), ("Окончание", common.fmt_date(r["end_date"]))]))

        if r["comment"]:
            lay.addWidget(w.section_title("Комментарий"))
            lay.addWidget(w.label(r["comment"], 10, wrap=True))
        lay.addWidget(w.section_title("Курс"))

        if r["status"] == "active":
            btn = w.danger_button("Завершить курс")
            btn.clicked.connect(lambda: self._set_status(r, "completed"))
        else:
            btn = w.ghost_button("Возобновить курс")
            btn.clicked.connect(lambda: self._set_status(r, "active"))
        lay.addWidget(btn)
        lay.addStretch()

    def _set_status(self, r, status):
        text = "Завершить курс" if status == "completed" else "Возобновить курс"
        if not mb.confirm(self, text, f"{text} «{r['name_med']}» у пациента {r['patient_name']}?"):
            return
        if db.set_prescription_status(r["id_prescription"], status):
            self.panel.close_panel()
            self.refresh_all()

    def show_diary(self, id_patient):
        self._diary_patient = id_patient
        pl = w.pal()
        while self.diary_layout.count():
            item = self.diary_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        p = next((x for x in self.patients if x["id_patient"] == id_patient), None)
        if not p:
            return
        entries = db.get_diary_full(id_patient)

        summary = w.AnimatedCard(clickable=False)
        sl = QHBoxLayout()
        sl.setSpacing(16)
        info = QVBoxLayout()
        info.setSpacing(4)
        info.addWidget(w.label(p["full_name"], 13, bold=True))
        info.addWidget(w.label(common.patient_meta(p["birth_date"], p["gender"]), 9, color=pl["muted"]))
        info.addWidget(
            w.label(w.plural(len(entries), "запись", "записи", "записей") + " в дневнике", 9, color=pl["muted"]))
        diagnosed = sum(1 for e in entries if e["disease_code"] or e["doctor_diagnosis"])
        info.addWidget(w.chip(f"с диагнозом: {diagnosed}", pl["accent_soft"], pl["accent"]))
        info.addStretch()
        sl.addLayout(info)
        trend = MoodTrend(entries, 120)
        sl.addWidget(trend, 1)
        summary.body_layout.addLayout(sl)
        self.diary_layout.addWidget(summary)
        summary.appear(0)

        if not entries:
            self.diary_layout.addWidget(w.label("Пациент пока не делал записей", 10, color=pl["muted"]))
        for i, e in enumerate(entries):
            card = DiaryCard(e, self.open_diagnosis)
            self.diary_layout.addWidget(card)
            card.appear(60 + min(i, 10) * 50)
        self.diary_layout.addStretch()

    def open_diagnosis(self, e):
        pl = w.pal()
        mood, color = w.mood_of(e["well_being_text"])
        self.panel.open_panel("Диагноз и комментарий")
        lay = self.panel.content_layout

        head = QHBoxLayout()
        head.addWidget(w.label(human_date(e["entry_date"]), 12, bold=True))
        head.addWidget(w.chip(mood, color))
        head.addStretch()
        lay.addLayout(head)

        symptoms = e["symptoms"] if e["symptoms"] and e["symptoms"] != "нет" else "без симптомов"
        lay.addWidget(w.label(symptoms, 9, color=pl["muted"], wrap=True))

        lay.addWidget(w.section_title("Болезнь по МКБ-10"))
        search = w.search_line("Код или название: I10, диабет, мигрень")
        lay.addWidget(search)

        lst = QListWidget()
        lst.setFixedHeight(190)
        lst.setWordWrap(True)
        lst.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        lst.setStyleSheet(
            f"QListWidget {{ background: {pl['card']}; border: 1px solid {pl['line']}; border-radius: 12px; padding: 4px; font-family: '{w.FONT}'; font-size: 9pt; color: {pl['text']}; outline: none; }} QListWidget::item {{ padding: 7px 8px; border-radius: 8px; }} QListWidget::item:hover {{ background: {pl['accent_soft']}; }} QListWidget::item:selected {{ background: {pl['accent']}; color: white; }}" + w.scroll_qss().replace(
                "QScrollArea", "QListWidget"))
        lay.addWidget(lst)

        chosen = w.label("", 9, bold=True, color=pl["accent"], wrap=True)
        lay.addWidget(chosen)

        diseases = db.get_all_diseases()
        state = {"id": e["id_disease"], "shown": []}
        if e["disease_code"]:
            chosen.setText(f"Выбрано: {e['disease_code']} — {e['disease_name']}")

        def fill(text=""):
            t = text.strip().lower()
            lst.clear()
            state["shown"] = [d for d in diseases if not t or t in f"{d[1]} {d[2]}".lower()]
            for d in state["shown"]:
                lst.addItem(f"{d[1]}  —  {d[2]}")
                if d[0] == state["id"]:
                    lst.setCurrentRow(lst.count() - 1)

        def pick(row):
            if 0 <= row < len(state["shown"]):
                d = state["shown"][row]
                state["id"] = d[0]
                chosen.setText(f"Выбрано: {d[1]} — {d[2]}")

        search.textChanged.connect(fill)
        lst.currentRowChanged.connect(pick)
        fill()

        lay.addWidget(w.section_title("Уточнения и рекомендации"))
        diag = QLineEdit(e["doctor_diagnosis"] or "")
        diag.setPlaceholderText("Например: подбор терапии, контроль давления")
        lay.addWidget(diag)

        lay.addWidget(w.section_title("Комментарий пациенту"))
        comment = QTextEdit()
        comment.setPlaceholderText("Пациент увидит комментарий в своём дневнике")
        comment.setFixedHeight(90)
        lay.addWidget(comment)

        save = w.primary_button("Сохранить")

        def do_save():
            text = diag.text().strip()
            note = comment.toPlainText().strip()
            if not state["id"] and not text and not note:
                mb.warning(self, "Пусто", "Выберите болезнь, напишите уточнение или комментарий.")
                return
            if state["id"] or text:
                if not db.set_diary_diagnosis_full(e["id_diary"], text, state["id"], self.id_doctor):
                    mb.critical(self, "Ошибка", "Не удалось сохранить диагноз")
                    return
                db.log_action(self.id_user, "set_diagnosis", "diary_entries", e["id_diary"])
            if note:
                db.add_doctor_comment(e["id_diary"], self.id_doctor, note)
            self.panel.close_panel()
            self.show_diary(self._diary_patient)

        save.clicked.connect(do_save)
        lay.addWidget(save)
        lay.addStretch()

    def open_profile(self):
        pl = w.pal()
        d = db.get_doctor_crm(self.id_doctor) or {}
        self.panel.open_panel("Мой профиль")
        lay = self.panel.content_layout

        photo = w.Avatar(self.full_name, 240, w.doctor_photo_path(d.get("photo")), shape="rounded", height=260)
        lay.addWidget(photo, 0, Qt.AlignmentFlag.AlignHCenter)
        if not photo.has_photo():
            hint = w.label("Загрузите фотографию — её увидят пациенты и администратор", 9, color=pl["accent_light"],
                           wrap=True)
            hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(hint)

        upload = w.primary_button("Заменить фото" if d.get("photo") else "Загрузить фото")

        def do_upload():
            path, _ = QFileDialog.getOpenFileName(self, "Моё фото", "", "Изображения (*.png *.jpg *.jpeg *.bmp *.webp)")
            if not path:
                return
            name = common.save_doctor_photo(self.id_doctor, path, d.get("photo"))
            if not name or name == d.get("photo"):
                mb.warning(self, "Фото", "Не удалось открыть изображение.")
                return
            db.update_doctor_profile(self.id_doctor, d.get("specialty"), d.get("office"), d.get("schedule"),
                                     d.get("phone"), d.get("email"), name)
            db.log_action(self.id_user, "doctor_photo", "doctors", self.id_doctor)
            self.profile = db.get_doctor_crm(self.id_doctor) or {}
            self.me_avatar.set_photo(w.doctor_photo_path(name))
            self.open_profile()

        upload.clicked.connect(do_upload)
        lay.addWidget(upload)

        lay.addWidget(w.label(self.full_name, 14, bold=True, wrap=True))
        lay.addWidget(w.info_block(
            [("Специальность", d.get("specialty")), ("Кабинет", d.get("office")), ("График приёма", d.get("schedule")),
             ("Телефон", d.get("phone")), ("E-mail", d.get("email")), ("Логин", d.get("login"))]))

        lay.addWidget(
            w.label("Специальность, кабинет и контакты меняет администратор.", 8, color=pl["muted"], wrap=True))

        # --- Кнопка смены пароля ---
        change_pass_btn = w.ghost_button("Сменить пароль")
        change_pass_btn.clicked.connect(lambda: common.ChangePasswordDialog(self, self.id_user).exec())
        lay.addWidget(change_pass_btn)
        # ---------------------------

        lay.addStretch()

    def export_my_patients_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить список", "my_patients.pdf", "PDF (*.pdf)")
        if not path:
            return
        if not path.endswith(".pdf"):
            path += ".pdf"
        try:
            pdf_exporter.export_patients_to_pdf(path, self.patients, f"Пациенты врача: {self.full_name}")
            mb.info(self, "Готово", "Список пациентов выгружен.")
        except Exception as e:
            mb.critical(self, "Ошибка", f"Не удалось: {e}")

    def export_diary_pdf(self, id_patient, patient_name):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить дневник", f"diary_{patient_name}.pdf", "PDF (*.pdf)")
        if not path:
            return
        if not path.endswith(".pdf"):
            path += ".pdf"
        entries = db.get_diary_full(id_patient)
        try:
            pdf_exporter.export_diary_to_pdf(path, patient_name, entries, db.get_indicators_for_diary)
            mb.info(self, "Готово", "Дневник пациента выгружен.")
        except Exception as e:
            mb.critical(self, "Ошибка", f"Не удалось: {e}")