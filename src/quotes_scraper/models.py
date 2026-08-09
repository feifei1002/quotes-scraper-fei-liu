from dataclasses import dataclass


# Each scraped quote will be stored as a QuoteRecord object
@dataclass
class QuoteRecord:
    quote: str
    author: str
    tags: str
    page_number: int

# This method converts the QuoteRecord object into a dictionary format, so it can be written easily to a CSV file later.
    def to_row(self) -> dict:
        return {
            "quote": self.quote,
            "author": self.author,
            "tags": self.tags,
            "page_number": self.page_number,
        }