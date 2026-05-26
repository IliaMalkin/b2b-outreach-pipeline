# B2B Outreach Pipeline

Portfolio project: an end-to-end Python workflow for preparing a B2B cold-email outreach dataset.

The public repository contains a sanitized demo version. Real email addresses and personal contact names are not published.

## What It Does

- starts from a CSV seed list of B2B companies;
- enriches rows with website-based personalization;
- keeps contact role and contact name as separate fields;
- masks email addresses for public/demo exports;
- generates Google Sheets-ready CSV and formatted XLSX output;
- includes a three-step outreach sequence and QA summary.

## Repository Structure

```text
data/
  companies_seed.csv              # input company list, no email addresses
  outreach_pipeline_masked.csv    # sanitized output dataset
docs/
  email_sequence.md               # three-step outreach sequence
  validation_report.md            # QA notes and remaining risks
outputs/
  outreach_pipeline_masked.xlsx   # formatted workbook demo
scripts/
  build_portfolio_outputs.py      # CSV/XLSX export from masked data
  personalize_from_csv.py         # CSV -> CSV with personalization column
```

## Data Privacy

This repository is intentionally sanitized:

- emails are masked, for example `sa***@example.com`;
- personal contact names are replaced with `public contact found` / `not found in public demo`;
- the workbook is a demonstration artifact, not a ready-to-send contact list;
- SMTP validation is not included in the public demo.

## Quick Start

Create a CSV with at least `company` and `website` columns, then run:

```bash
python scripts/personalize_from_csv.py data/companies_seed.csv data/companies_personalized_demo.csv
```

Build the formatted portfolio outputs:

```bash
python scripts/build_portfolio_outputs.py
```

The generated files are written to:

```text
data/outreach_pipeline_masked.csv
outputs/outreach_pipeline_masked.xlsx
```

## Output Columns

- `Компания`
- `Сайт`
- `Сегмент`
- `Имя контакта`
- `Роль/отдел`
- `Email`
- `Персонализация`
- `Источник персонализации`
- `Источник контакта`
- `Источник email`
- `Статус`

## Implementation Notes

- Language: Python 3.11+
- XLSX generation: `openpyxl`
- Website fetch: Python standard library (`urllib`)
- No paid APIs are required for the public demo.

## Portfolio Framing

This project demonstrates:

- practical data wrangling for outbound operations;
- safe handling of contact data in public artifacts;
- website-based personalization;
- export automation for CSV/XLSX/Google Sheets workflows;
- QA thinking: row counts, masked data, status labels, and validation notes.

## Limitations

- The public dataset is masked and should not be used for real outreach.
- Email deliverability checks and SMTP validation are intentionally out of scope.
- Some companies do not expose a public decision-maker name; those rows are labeled instead of inventing a contact.
