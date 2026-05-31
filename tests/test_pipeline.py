from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_portfolio_outputs, personalize_from_csv


def test_build_workbook_creates_expected_sheets() -> None:
    rows = [
        {
            "Company": "Example Co",
            "Website": "https://example.com",
            "Email": "sa***@example.com",
            "Personalization": "Example Co sells B2B software.",
        }
    ]

    workbook = build_portfolio_outputs.build_workbook(rows)

    assert workbook.sheetnames == ["Outreach base", "Email sequence", "QA summary"]
    assert workbook["Outreach base"]["A1"].value == "Company"
    assert workbook["Outreach base"]["A2"].value == "Example Co"
    assert workbook["QA summary"]["B2"].value == 1


def test_personalize_run_adds_personalization_column(
    tmp_path: Path, monkeypatch
) -> None:
    input_path = tmp_path / "companies.csv"
    output_path = tmp_path / "out.csv"

    with input_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["company", "website"])
        writer.writeheader()
        writer.writerow({"company": "Example Co", "website": "example.com"})

    monkeypatch.setattr(
        personalize_from_csv,
        "fetch",
        lambda url: (
            "<html><head><meta name='description' "
            "content='Reliable B2B data tools'></head></html>"
        ),
    )

    personalize_from_csv.run(input_path, output_path)

    with output_path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["company"] == "Example Co"
    assert rows[0]["personalization"]
    assert "reliable B2B data tools" in rows[0]["personalization"]
