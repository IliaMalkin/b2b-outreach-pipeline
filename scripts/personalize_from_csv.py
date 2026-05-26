from __future__ import annotations

import argparse
import csv
import html
import re
import ssl
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def normalize_url(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith(("http://", "https://")):
        return [value]
    return [f"https://{value}", f"http://{value}"]


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl.create_default_context()
    with urlopen(request, timeout=15, context=context) as response:
        raw = response.read(1_500_000)
        encoding = response.headers.get_content_charset() or "utf-8"
    try:
        "".encode(encoding)
    except LookupError:
        encoding = "utf-8"
    return raw.decode(encoding, errors="ignore")


def clean_html(value: str) -> str:
    value = re.sub(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def first_match(patterns: list[str], text: str) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.S)
        if match:
            value = clean_html(match.group(1))
            if value:
                return value
    return ""


def extract_fact(company: str, site: str, body: str) -> str:
    description = first_match(
        [
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']',
            r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
            r'<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']og:description["\']',
        ],
        body,
    )
    h1 = first_match([r"<h1[^>]*>(.*?)</h1>"], body)
    title = first_match([r"<title[^>]*>(.*?)</title>"], body)

    source = description or h1 or title
    if not source:
        return "[сайт недоступен]"

    source = re.sub(r"\s+", " ", source).strip(" .")
    source = source[:210].rstrip(" ,.;:-")
    if company.lower() in source.lower():
        return f"На главной {site} указано: {source}."
    return f"На главной {company} пишет про {source[0].lower() + source[1:]}."


def personalize_row(row: dict[str, str]) -> dict[str, str]:
    company = row.get("company") or row.get("Компания") or ""
    site = row.get("website") or row.get("site") or row.get("Сайт") or ""
    for url in normalize_url(site):
        try:
            body = fetch(urljoin(url, "/"))
            row["personalization"] = extract_fact(company, site, body)
            return row
        except Exception:  # noqa: BLE001 - fallback is recorded in the output.
            continue
    row["personalization"] = "[сайт недоступен]"
    return row


def run(input_path: Path, output_path: Path) -> None:
    with input_path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise RuntimeError("Input CSV is empty")

    output_rows = [personalize_row(dict(row)) for row in rows]
    fieldnames = list(rows[0])
    if "personalization" not in fieldnames:
        fieldnames.append("personalization")

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a personalization column to a company CSV.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    run(args.input_csv, args.output_csv)
    print(f"saved {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
