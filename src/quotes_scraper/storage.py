import csv
import re
from pathlib import Path

from quotes_scraper.models import QuoteRecord

FIELDNAMES = ["quote", "author", "tags", "page_number"]

# Crate a duplicate-check key using quote text + author name. 
# This will be used to check for duplicates in the memory.csv file.
# Because the same quote text by the same author should only be stored once.
def make_key(record: QuoteRecord) -> tuple[str, str]:
    quote = re.sub(r"\s+", " ", record.quote).strip().lower()
    author = re.sub(r"\s+", " ", record.author).strip().lower()
    return quote, author

# Reads data/memory.csv if it already exists and returns a list of QuoteRecord objects. 
# If the file does not exist, it returns an empty list.
def load_memory(memory_file: Path) -> list[QuoteRecord]:
    if not memory_file.exists():
        return []

    records = []

    with memory_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append(
                QuoteRecord(
                    quote=row["quote"],
                    author=row["author"],
                    tags=row["tags"],
                    page_number=int(row["page_number"]),
                )
            )
    return records

# Compares the scraped records with the existing records in memory.csv 
# and returns a list of new records that are not already present in memory.csv.
def find_new_records(
        scraped_records: list[QuoteRecord],
        existing_records: list[QuoteRecord]
    ) -> tuple[list[QuoteRecord], int]:

    existing_keys = {make_key(record) for record in existing_records}

    new_records = []
    skipped_count = 0

    for record in scraped_records:
        key = make_key(record)

        if key in existing_keys:
            skipped_count += 1
            continue

        existing_keys.add(key)
        new_records.append(record)

    return new_records, skipped_count

# Writes only the new records to the csv file.
def append_records(memory_file: Path, records: list[QuoteRecord]) -> None:
    if not records:
        return

    memory_file.parent.mkdir(parents=True, exist_ok=True)

    should_write_header = not memory_file.exists() or memory_file.stat().st_size == 0

    with memory_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if should_write_header:
            writer.writeheader()

        for record in records:
            writer.writerow(record.to_row())