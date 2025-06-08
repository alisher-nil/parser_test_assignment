from typing import Optional, override

from playwright.async_api import Page

from app.parsers.base import BaseParser
from app.parsers.exceptions import InvalidSelectionException


class HalykParser(BaseParser):
    @override
    async def fetch_price(self, url) -> Optional[int]:
        try:
            page = await self.get_page(url)
            return await self.parse_price(page)

        except InvalidSelectionException as e:
            # there should be a logger instead of print in production code
            print(f"Error during price fetching: {e}")
            return None

    async def parse_price(self, page: Page) -> int:
        price_locator = page.locator(".desc-price-value")
        if await price_locator.count() == 0:
            raise InvalidSelectionException("Price section not found")

        price_text = await price_locator.text_content()
        if price_text is None:
            raise InvalidSelectionException("Price text is empty")

        price = self.parse_price_from_text(price_text)
        return price
