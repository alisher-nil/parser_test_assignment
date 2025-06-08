import string
from abc import ABC, abstractmethod

from playwright.async_api import Browser, Page


class BaseParser(ABC):
    def __init__(self, url: str, browser: Browser, timeout: int = 5000) -> None:
        self.url = url
        self.browser = browser
        self.timeout = timeout

    @abstractmethod
    async def fetch_price(self) -> int: ...

    async def get_page(self) -> Page:
        page = await self.browser.new_page()
        page.set_default_timeout(self.timeout)
        await page.goto(self.url)
        await page.wait_for_timeout(self.timeout)
        return page

    def parse_price_from_text(self, price_text: str) -> int:
        digits = "".join(filter(lambda c: c in string.digits, price_text))
        if not digits:
            return 0
        return int(digits)
