import string
from abc import ABC, abstractmethod
from typing import Optional

from playwright.async_api import Browser, Page


class BaseParser(ABC):
    timeout = 2000

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    @abstractmethod
    async def fetch_price(self, url: str) -> Optional[int]: ...

    async def get_page(self, url: str) -> Page:
        page = await self.browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(self.timeout)
        return page

    def parse_price_from_text(self, price_text: str) -> int:
        digits = "".join(filter(lambda c: c in string.digits, price_text))
        if not digits:
            return 0
        return int(digits)
