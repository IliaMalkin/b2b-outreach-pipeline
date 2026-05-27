# AI-Agent Workflow

This repository is a sanitized public version of an AI-assisted B2B outreach workflow. The goal was to turn a raw company list into a reviewable outreach workbook without publishing private contact data.

## Workflow

1. **Segment definition**
   - Define the target market: B2B SaaS, CRM, analytics, communication, low-code/no-code, and automation companies.
   - Create a seed CSV with company name, website, and segment.

2. **Agent-assisted research**
   - Use Claude Code / Codex-style agent workflows to inspect company websites and public pages.
   - Ask the agent to identify positioning, product category, outreach angle, and possible personalization signals.
   - Keep the output structured so it can be reviewed row by row.

3. **Website-based personalization**
   - Run `scripts/personalize_from_csv.py` to fetch public website pages.
   - Extract a short fact from meta description, Open Graph description, H1, or title.
   - Store the result in a `personalization` column.

4. **Table shaping**
   - Normalize columns for company, website, segment, contact role, masked email, personalization, source, and status.
   - Keep contact name and role separate so departments are not presented as people.

5. **Privacy pass**
   - Mask email addresses before publishing.
   - Replace personal contact names with public-demo labels.
   - Keep source/status fields so the data can still be evaluated.

6. **Workbook generation**
   - Run `scripts/build_portfolio_outputs.py`.
   - Generate a formatted XLSX with the outreach base, email sequence, and QA summary.

7. **QA review**
   - Check row count and required fields.
   - Review personalization for unsupported claims.
   - Mark missing public decision-maker names instead of inventing contacts.
   - Document remaining risks in `docs/validation_report.md`.

## What Was Automated

- Website fetch and extraction of basic personalization facts.
- CSV transformation and output generation.
- XLSX formatting for a portfolio-ready workbook.
- QA summary generation for the public demo.

## What Still Needs Human Review

- SMTP and deliverability validation before any real campaign.
- Final source audit for contact emails.
- Copy review against the exact target segment and offer.
- Manual approval before sending any outreach.

## Portfolio Use

This project is useful for roles involving:

- AI-assisted outreach;
- lead enrichment;
- sales/marketing operations automation;
- Google Sheets/XLSX workflows;
- Python scripting for business tasks;
- data privacy and public portfolio sanitization.
