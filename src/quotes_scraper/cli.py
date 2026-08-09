import argparse
from pathlib import Path

from quotes_scraper.config import load_credentials
from quotes_scraper.scraper import QuotesScraper
from quotes_scraper.storage import append_records, find_new_records, load_memory

DEFAULT_BASE_URL = "https://quotes.toscrape.com"
DEFAULT_MEMORY_FILE = Path("data/memory.csv")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quotes_scraper",
        description="Scrape quotes.toscrape.com into a local CSV memory file.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ["backfill", "latest"]:
        command_parser = subparsers.add_parser(command)

        command_parser.add_argument(
            "--memory-file",
            type=Path,
            default=DEFAULT_MEMORY_FILE,
            help="CSV file used for output and local memory.",
        )

        command_parser.add_argument(
            "--headless",
            action=argparse.BooleanOptionalAction,
            default=True,
            help="Run browser hidden by default. Use --no-headless to show it.",
        )

    return parser

def run(command: str, memory_file: Path, headless: bool) -> None:
    credentials = load_credentials()
    scraper = QuotesScraper(
        base_url=DEFAULT_BASE_URL,
        credentials=credentials,
        headless=headless,
    )

    existing_records = load_memory(memory_file)
    scraped_records = scraper.scrape()

    new_records, skipped_count = find_new_records(
        scraped_records=scraped_records,
        existing_records=existing_records,
    )

    append_records(memory_file, new_records)

    if command == "latest" and not new_records:
        print("No new quotes found.")
    else:
        print(
            f"{command.capitalize()} complete: "
            f"found {len(scraped_records)}, "
            f"added {len(new_records)}, "
            f"skipped {skipped_count}."
        )
    print(f"Memory file: {memory_file}")

    return 0

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    return run(
        command=args.command,
        memory_file=args.memory_file,
        headless=args.headless,
    )
    