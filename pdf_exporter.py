import os
from datetime import datetime
from PySide6.QtGui import (
    QPdfWriter, QPageSize, QPageLayout, QPainter,
    QFont, QColor, QPen, QFontMetrics
)
from PySide6.QtCore import Qt, QRectF

PAGE_W = 2480
PAGE_H = 3508
MARGIN = 150
FONT = "Arial"


def _setup_writer(filepath):
    writer = QPdfWriter(filepath)
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setPageOrientation(QPageLayout.Orientation.Portrait)
    writer.setResolution(300)
    return writer, QPainter(writer)


def _draw_header(painter, title, subtitle=""):
    painter.setPen(QColor("#1a1a2e"))
    f = QFont(FONT, 20, QFont.Weight.Bold)
    painter.setFont(f)
    painter.drawText(QRectF(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, 80), Qt.AlignmentFlag.AlignCenter, title)

    if subtitle:
        painter.setPen(QColor("#2F5C8F"))
        f.setPointSize(14)
        f.setBold(False)
        painter.setFont(f)
        painter.drawText(QRectF(MARGIN, MARGIN + 80, PAGE_W - 2 * MARGIN, 60), Qt.AlignmentFlag.AlignCenter, subtitle)
    return MARGIN + 220  # Чуть больше отступа от заголовка


def _draw_footer(painter, page_num):
    painter.setPen(QColor("#888888"))
    f = QFont(FONT, 10)
    painter.setFont(f)
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    painter.drawText(QRectF(MARGIN, PAGE_H - MARGIN + 20, PAGE_W - 2 * MARGIN, 50),
                     Qt.AlignmentFlag.AlignLeft, f"Сгенерировано: {date_str}")
    painter.drawText(QRectF(MARGIN, PAGE_H - MARGIN + 20, PAGE_W - 2 * MARGIN, 50),
                     Qt.AlignmentFlag.AlignRight, f"Стр. {page_num}")


def export_charts_to_pdf(filepath, charts_data):
    writer, painter = _setup_writer(filepath)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    page_num = 1
    for idx, (name, pixmap) in enumerate(charts_data):
        if idx > 0:
            _draw_footer(painter, page_num)
            writer.newPage()
            page_num += 1

        y = _draw_header(painter, "Отчёт по аналитике", name)
        img_w = PAGE_W - 2 * MARGIN
        img_h = int(pixmap.height() * (img_w / pixmap.width()))
        painter.drawPixmap(int(MARGIN), int(y), img_w, img_h, pixmap)

    _draw_footer(painter, page_num)
    painter.end()


def export_patients_to_pdf(filepath, patients, header_title="Список пациентов"):
    writer, painter = _setup_writer(filepath)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    y = _draw_header(painter, header_title, f"Всего записей: {len(patients)}")
    page_num = 1

    # ИСПРАВЛЕНИЕ: Уменьшили ширину колонок, чтобы всё влезло в лист (сумма = 2180)
    cols = [("ФИО", 750), ("Дата рожд.", 350), ("Телефон", 400), ("Лечащий врач", 680)]

    def draw_table_header(y_pos):
        x = MARGIN
        painter.setFont(QFont(FONT, 12, QFont.Weight.Bold))
        painter.setPen(QPen(QColor("#2F5C8F")))
        for name, width in cols:
            painter.drawText(QRectF(x, y_pos, width, 50), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             name)
            x += width
        painter.setPen(QPen(QColor("#CCCCCC")))
        painter.drawLine(int(MARGIN), int(y_pos + 50), int(PAGE_W - MARGIN), int(y_pos + 50))
        return y_pos + 70

    y = draw_table_header(y)
    painter.setFont(QFont(FONT, 10))
    painter.setPen(QPen(QColor("#1A1A1A")))

    for p in patients:
        if y > PAGE_H - MARGIN - 100:
            _draw_footer(painter, page_num)
            writer.newPage()
            page_num += 1
            y = draw_table_header(MARGIN)
            painter.setFont(QFont(FONT, 10))
            painter.setPen(QPen(QColor("#1A1A1A")))

        x = MARGIN
        fio = str(p.get("full_name") or (p[1] if isinstance(p, tuple) else ""))
        bdate = str(p.get("birth_date") or (p[2] if isinstance(p, tuple) else ""))
        phone = str(p.get("phone") or (p[4] if isinstance(p, tuple) else "—"))
        doctor = str(p.get("doctor_name") or "—")

        values = [fio, bdate, phone, doctor]
        for (col_name, width), val in zip(cols, values):
            text = painter.fontMetrics().elidedText(str(val), Qt.TextElideMode.ElideRight, width - 10)
            painter.drawText(QRectF(x, y, width, 50), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
            x += width

        y += 50
        painter.setPen(QPen(QColor("#EEEEEE")))
        painter.drawLine(int(MARGIN), int(y), int(PAGE_W - MARGIN), int(y))
        y += 10
        painter.setPen(QPen(QColor("#1A1A1A")))

    _draw_footer(painter, page_num)
    painter.end()


def export_diary_to_pdf(filepath, patient_name, entries, indicators_func):
    writer, painter = _setup_writer(filepath)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    y = _draw_header(painter, "Дневник самочувствия", f"Пациент: {patient_name}")
    page_num = 1

    for e in entries:
        if y > PAGE_H - MARGIN - 500:
            _draw_footer(painter, page_num)
            writer.newPage()
            page_num += 1
            y = MARGIN

        if isinstance(e, dict):
            id_diary = e["id_diary"];
            date_val = e["entry_date"];
            time_val = e.get("entry_time", "")
            well_being = e["well_being_text"];
            symptoms = e.get("symptoms", "");
            diagnosis = e.get("doctor_diagnosis", "")
        else:
            id_diary = e[0];
            date_val = e[1];
            time_val = e[2];
            well_being = e[3];
            symptoms = e[4];
            diagnosis = ""

        date_str = date_val.strftime("%d.%m.%Y") if hasattr(date_val, 'strftime') else str(date_val)
        time_str = time_val.strftime("%H:%M") if hasattr(time_val, 'strftime') else str(time_val)

        # 1. Дата и время (Увеличили высоту до 100, чтобы ничего не перечеркивалось)
        painter.setPen(QColor("#2F5C8F"))
        painter.setFont(QFont(FONT, 14, QFont.Weight.Bold))
        painter.drawText(QRectF(MARGIN, y, PAGE_W - 2 * MARGIN, 100),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, f"{date_str}  ·  {time_str}")
        y += 120

        painter.setPen(QColor("#1A1A1A"))
        painter.setFont(QFont(FONT, 11))

        # Создаем метрики для расчета высоты текста
        metrics = QFontMetrics(painter.font())

        # 2. Самочувствие
        text_wb = f"Самочувствие: {well_being}"
        rect_wb = metrics.boundingRect(0, 0, int(PAGE_W - 2 * MARGIN), 5000, Qt.TextFlag.TextWordWrap, text_wb)
        painter.drawText(QRectF(MARGIN, y, PAGE_W - 2 * MARGIN, rect_wb.height()),
                         Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap, text_wb)
        y += rect_wb.height() + 20

        # 3. Симптомы
        if symptoms and str(symptoms).lower() != "нет":
            text_sym = f"Симптомы: {symptoms}"
            rect_sym = metrics.boundingRect(0, 0, int(PAGE_W - 2 * MARGIN), 5000, Qt.TextFlag.TextWordWrap, text_sym)
            painter.drawText(QRectF(MARGIN, y, PAGE_W - 2 * MARGIN, rect_sym.height()),
                             Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap, text_sym)
            y += rect_sym.height() + 20

        # 4. Диагноз
        if diagnosis:
            text_diag = f"Диагноз: {diagnosis}"
            rect_diag = metrics.boundingRect(0, 0, int(PAGE_W - 2 * MARGIN), 5000, Qt.TextFlag.TextWordWrap, text_diag)
            painter.drawText(QRectF(MARGIN, y, PAGE_W - 2 * MARGIN, rect_diag.height()),
                             Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap, text_diag)
            y += rect_diag.height() + 20

        # 5. Показатели
        try:
            inds = indicators_func(id_diary)
            if inds:
                ind_text = " | ".join(f"{i[0]}: {i[1]} {i[2]}" for i in inds)
                text_ind = f"Показатели: {ind_text}"
                painter.setPen(QColor("#444444"))
                rect_ind = metrics.boundingRect(0, 0, int(PAGE_W - 2 * MARGIN), 5000, Qt.TextFlag.TextWordWrap,
                                                text_ind)
                painter.drawText(QRectF(MARGIN, y, PAGE_W - 2 * MARGIN, rect_ind.height()),
                                 Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap, text_ind)
                y += rect_ind.height() + 20
        except:
            pass

        # Разделительная линия
        y += 30
        painter.setPen(QPen(QColor("#EEEEEE")))
        painter.drawLine(int(MARGIN), int(y), int(PAGE_W - MARGIN), int(y))
        y += 50  # Отступ перед следующей записью

    _draw_footer(painter, page_num)
    painter.end()