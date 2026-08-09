from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from quotes_scraper.config import Credentials
from quotes_scraper.models import QuoteRecord

class QuotesScraper:
    def __init__(self, base_url: str, credentials: Credentials, headless: bool = True):
        self.base_url = base_url.rstrip("/")
        self.credentials = credentials
        self.headless = headless

# Open Chromium, logs in, scrapes the pages, then closes the browser.
    def scrape(self) -> list[QuoteRecord]:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.headless)
            page = browser.new_page()

            try:
                self._login(page)
                return self._scrape_pages(page)
            finally:
                browser.close()

# Goes to /login, fills the form, submits it, and checks for a logout link.
    def _login(self, page) -> None:
        login_url = urljoin(self.base_url, "/login")
        page.goto(login_url)

        page.fill('input[name="username"]', self.credentials.username)
        page.fill('input[name="password"]', self.credentials.password)
        page.click('input[type="submit"]')

        if page.locator('a[href="/logout"]').count() == 0:
            raise RuntimeError("Login failed. Logout link was not found.")

# Loops through each page until there is no “next” button.
# Each quote becomes a QuoteRecord.
    def _scrape_pages(self, page) -> list[QuoteRecord]:
        records = []
        page_number = 1
        next_url = f"{self.base_url}/page/1"

        while next_url:
            page.goto(next_url)

            quote_blocks = page.locator(".quote")

            for index in range(quote_blocks.count()):
                block = quote_blocks.nth(index)

                quote = block.locator(".text").inner_text().strip()
                author = block.locator(".author").inner_text().strip()
                tags = block.locator(".tags .tag").all_inner_texts()

                records.append(
                    QuoteRecord(
                        quote=quote,
                        author=author,
                        tags=", ".join(tags),
                        page_number=page_number,
                    )
                )

            next_link = page.locator('li.next a')

            if next_link.count() > 0:
                next_url = ""
            else:
                href = next_link.first.get_attribute("href")
                next_url = urljoin(self.base_url, href)
                page_number += 1

        return records