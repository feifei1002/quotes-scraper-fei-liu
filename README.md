# Quotes Scraper

A small command-line Python package that logs in to [quotes.toscrape.com](https://quotes.toscrape.com), scrapes quote data and stores the results in a local CSV memory file.

The scraper supports two modes:
- `backfill`: scrape all available quotes and save any records not already stored.
- `latest`: check the website against the existing memory file and append only new quotes.

## Architecture

The project is split into small modules:

- `config.py` loads login details (username and password) from `.env` or environment variables.
- `models.py` defines the `QuoteRecord` data structure.
- `scraper.py` handles browser login and page scraping with Playwright.
- `storage.py` reads and writes the CSV memory file and prevents duplicates.
- `cli.py` provides the `quotes-scraper` command.

## Output and Memory File

```text
data/memory.csv
```
The file is created automatically when ```backfill``` or ```latest``` adds records for the first time. The CSV contains one row per quote with these columns:
quote, author, tags, page_number

## Duplicate detection

A duplicate is identified using the quote text and author name.
Before comparing records, the scraper lowercases the values and normalizes whitespace. This means small formatting differences such as extra spaces, do not create duplicate rows.
Tags are not included in the duplicate key because the quote text and author are the main identity of the record.

## Assumptions and Limitations

- The project uses Playwright with Chromium.
- The reviewer should install the Playwright Chromium browser before running the scraper.
- The target website is small, so ```latest``` scans the available pages and then appends only records not already in memory.
- CSV is used because the case study asks for data/memory.csv and CSV opens easily in Excel.

## A. Clone and Install Locally

```
git clone https://github.com/feifei1002/quotes-scraper-fei-liu.git
cd quotes-scraper-fei-liu
python -m venv .venv
```
On Windows:
```
.venv\Scripts\activate
pip install -e .
python -m playwright install chromium
```

## B. Install directly from Github

```
python -m venv .venv
.venv\Scripts\activate
pip install "git+https://github.com/feifei1002/quotes-scraper-fei-liu.git"
python -m playwright install chromium
```

## Login Details
Create a ```.env``` file in the project root:
```
QUOTES_USERNAME=test
QUOTES_PASSWORD=test
```
You can also provide these values as environment variables instead of using a ```.env``` file.

## Commands

- Run a full backfill:
```quotes-scraper backfill```
    - Example output:
        ```
        Backfill complete: found 100, added 100, skipped 0.
        Memory file: data\memory.csv
        ```

- Check for new quotes only:
```quotes-scraper latest```
    - Example output:
            ```
            No new quotes found.
            Memory file: data\memory.csv
            ```

- Run in headless mode:
```quotes-scraper backfill --headless```
    - Example output:
            ```
            Backfill complete: found 100, added 0, skipped 10.
            Memory file: data\memory.csv
            ```

- Show the browser while it runs:
```quotes-scraper latest --no-headless```
    - Example output:
            ```
            No new quotes found.
            Memory file: data\memory.csv
            ```
            A browser should pop-up.
