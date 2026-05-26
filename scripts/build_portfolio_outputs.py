from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "outreach_pipeline_masked.csv"
OUT_XLSX = ROOT / "outputs" / "outreach_pipeline_masked.xlsx"
EMAIL_SEQUENCE = ROOT / "docs" / "email_sequence.md"


def read_rows() -> list[dict[str, str]]:
    with DATA_CSV.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_workbook(rows: list[dict[str, str]]) -> Workbook:
    workbook = Workbook()
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    wrap = Alignment(wrap_text=True, vertical="top")

    sheet = workbook.active
    sheet.title = "Outreach base"
    headers = list(rows[0])
    sheet.append(headers)
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
    for row in rows:
        sheet.append([row[column] for column in headers])

    widths = [24, 32, 28, 24, 22, 26, 72, 32, 30, 32, 34]
    for index, width in enumerate(widths[: len(headers)], start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = wrap
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions

    sequence = workbook.create_sheet("Email sequence")
    sequence.append(["Step", "Subject", "Body"])
    for cell in sequence[1]:
        cell.fill = header_fill
        cell.font = header_font
    sequence_rows = [
        (
            "Email 1",
            "{{Компания}} и холодные письма",
            "{{Имя}}, привет.\n\n{{персонализация}}\n\n"
            "Мы запускаем холодный email для B2B: база, письма, домены и первые ответы. "
            "Для {{Компания}} я бы начал с короткого пилота на 2-3 сегмента.\n\n"
            "Хотите, покажу, как это может выглядеть у вас?",
        ),
        (
            "Email 2",
            "Re: {{Компания}} и холодные письма",
            "{{Имя}}, вдогонку коротко.\n\n"
            "Часто проблема не в канале, а в запуске: база собрана не по ICP, домен холодный, "
            "письма читаются как спам.\n\n"
            "Если интересно, давайте 15 минут, покажу механику запуска.",
        ),
        (
            "Email 3",
            "Re: {{Компания}} и холодные письма",
            "{{Имя}}, всё, последнее.\n\n"
            "Холодный email нормально работает, когда это серия маленьких тестов: "
            "сегмент, оффер, письмо, ответ.\n\n"
            "Если тема всплывёт позже, ответьте на это письмо. Договоримся.",
        ),
    ]
    for row in sequence_rows:
        sequence.append(row)
    sequence.column_dimensions["A"].width = 20
    sequence.column_dimensions["B"].width = 40
    sequence.column_dimensions["C"].width = 96
    for row in sequence.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = wrap

    qa = workbook.create_sheet("QA summary")
    qa_rows = [
        ["Metric", "Value"],
        ["Rows", len(rows)],
        ["Email visibility", "all emails masked in public portfolio"],
        ["Personalization", "filled for every row"],
        ["Contact names", "redacted in public portfolio"],
        ["SMTP validation", "not included in public demo"],
    ]
    for row in qa_rows:
        qa.append(row)
    for cell in qa[1]:
        cell.fill = header_fill
        cell.font = header_font
    qa.column_dimensions["A"].width = 34
    qa.column_dimensions["B"].width = 70

    return workbook


def main() -> int:
    rows = read_rows()
    if not rows:
        raise RuntimeError("No rows found in masked CSV")
    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    workbook = build_workbook(rows)
    workbook.save(OUT_XLSX)
    print(f"saved {OUT_XLSX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
