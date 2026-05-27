# Validation Report

## Checked

- `data/outreach_pipeline_masked.csv`: 50 rows, 11 columns, no empty required fields in the public demo.
- `outputs/outreach_pipeline_masked.xlsx`: 3 sheets — `Outreach base`, `Email sequence`, `QA summary`.
- Email values are masked in the public repository.
- Contact names are redacted in the public repository.
- `Имя контакта` and `Роль/отдел` are separate columns, so a department is not presented as a person.
- Personalization is filled for every row.
- The email sequence has 3 steps and avoids unsupported case-study claims.
- `scripts/personalize_from_csv.py` runs the CSV -> CSV personalization step.
- `scripts/build_portfolio_outputs.py` rebuilds the XLSX portfolio artifact from the masked CSV.

## Remaining Risks

- SMTP validation is not included in the public demo. A real campaign would need deliverability validation before launch.
- Some emails in the original private workflow may belong to a parent brand or company group rather than exactly matching the website domain. The public demo preserves source/status fields to make this reviewable.
- Not every company exposes a public decision-maker name. Those rows are labeled instead of inventing a person.
- Personalization is based on public website data and public research notes. A real campaign should keep source URLs/screenshots for auditability.
- The public repository includes sanitized outputs, not private prompt logs or raw contact data.

## What Makes The Workflow Useful

- The XLSX is not just a flat export: it includes base data, an email sequence, and QA notes.
- Status/source columns make it clear where data came from and what needs review.
- The pipeline can be rerun from CSV inputs instead of being a one-off spreadsheet.
- The public version shows data hygiene: masking, no invented contacts, and explicit limitations.
