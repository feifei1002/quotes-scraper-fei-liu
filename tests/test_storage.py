from pathlib import Path
import tempfile
import unittest

from quotes_scraper.models import QuoteRecord
from quotes_scraper.storage import append_records, find_new_records, load_memory

class StorageTests(unittest.TestCase):

    def test_find_new_records_skips_existing_quote_and_author(self):
        existing_records = [
            QuoteRecord("Hello world", "Alice", "test", 1)
        ]

        scraped_records = [
            QuoteRecord("Hello  world", "ALICE", "different-tag", 1),
            QuoteRecord("New quote", "Bob", "new", 2),
        ]

        new_records, skipped_count = find_new_records(
            scraped_records=scraped_records,
            existing_records=existing_records,
        )

        self.assertEqual(skipped_count, 1)
        self.assertEqual(
            new_records, [QuoteRecord("New quote", "Bob", "new", 2)]
        )

    def test_append_records_creates_csv_that_can_be_loaded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            memory_file = Path(temp_dir) / "data" / "memory.csv"

            records = [QuoteRecord("Quote 1", "Author 1", "tag-one, tag-two", 3)]

            append_records(memory_file, records)
            loaded_records = load_memory(memory_file)
            self.assertEqual(loaded_records, records)

if __name__ == "__main__":
    unittest.main()