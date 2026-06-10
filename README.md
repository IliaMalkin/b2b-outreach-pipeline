# B2B Outreach Pipeline

![CI](https://github.com/IliaMalkin/b2b-outreach-pipeline/actions/workflows/ci.yml/badge.svg?branch=main)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

AI-assisted portfolio project: an end-to-end Python workflow for preparing a B2B cold-email outreach dataset.

```text
companies_seed.csv ──► personalize_from_csv.py ──► enriched CSV
        (50 B2B SaaS companies)        (fetch site, extract fact)
                                              │
                                              ▼
                              build_portfolio_outputs.py
                                              │
                              ┌───────────────┴───────────────┐
                              ▼                               ▼
              outreach_pipeline_masked.csv      outreach_pipeline_masked.xlsx
              (Google Sheets-ready)             (base data + sequence + QA summary)
```

The public repository contains a sanitized demo version. Real email addresses, personal contact names, and any private campaign data are not published.

## What It Demonstrates

- AI-agent-assisted research workflow for B2B outreach preparation;
- website-based personalization from public company pages;
- reproducible CSV -> CSV -> XLSX pipeline for Google Sheets-style work;
- masked public exports with contact and email privacy preserved;
- a three-step outreach sequence and QA summary;
- clear separation between automation, human review, and send-ready validation.

## What It Does

- starts from a CSV seed list of B2B companies;
- fetches public website pages and extracts a short personalization fact;
- keeps contact role and contact name as separate fields;
- masks email addresses for public/demo exports;
- generates Google Sheets-ready CSV and formatted XLSX output;
- includes a three-step outreach sequence and validation notes.

## AI-Agent Workflow

The project was built as an agent-assisted workflow with Claude Code / Codex-style tooling:

1. define the target segment and seed company list;
2. use an AI agent to help research public company context and outreach angles;
3. scrape/fetch public website pages for lightweight personalization signals;
4. structure the result into a consistent outreach table;
5. mask contact data before publishing;
6. generate an XLSX workbook with base data, email sequence, and QA summary;
7. review rows for hallucinated contacts, unsupported claims, and send-readiness risks.

See [docs/agent_workflow.md](docs/agent_workflow.md) for the detailed workflow.

## Example: Input Row → Output Row

Input (`data/companies_seed.csv`):

| company | site | segment |
| --- | --- | --- |
| amoCRM | https://www.amocrm.ru/ | CRM для отделов продаж |

Output (`data/outreach_pipeline_masked.csv`):

| Field | Value |
| --- | --- |
| Email | `su***@amocrm.ru` (masked for public demo) |
| Роль/отдел | Клиентский отдел |
| Персонализация | «amoCRM позиционирует себя как CRM именно для продаж, а не для всего сразу — значит ваша аудитория уже понимает ценность воронки и может оценить дополнительный канал лидов.» |
| Источник email | amocrm.ru/contacts/ |
| Статус | email найден на сайте; masked public demo |

The personalization line is grounded in the company's own public homepage copy — when a site is unreachable or exposes no public contact, the row is labeled (`[сайт недоступен]`, `not found in public demo`) instead of inventing data.

## Repository Structure

```text
data/
  companies_seed.csv              # input company list, no email addresses
  outreach_pipeline_masked.csv    # sanitized output dataset
docs/
  agent_workflow.md               # AI-agent-assisted build and QA workflow
  email_sequence.md               # neutral three-step outreach sequence
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
- SMTP validation is not included in the public demo;
- private prompts, raw scraping notes, and non-public campaign data are not published.

## Quick Start

Create a CSV with at least `company` and `website` or `site` columns, then run:

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

## Limitations

- The public dataset is masked and should not be used for real outreach.
- Email deliverability checks and SMTP validation are intentionally out of scope.
- Some companies do not expose a public decision-maker name; those rows are labeled instead of inventing a contact.
- The public demo includes the reproducible Python pipeline and sanitized outputs, not private agent logs or raw campaign data.
