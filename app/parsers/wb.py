from typing import Optional, override

from playwright.async_api import Page

from app.parsers.base import BaseParser
from app.parsers.exceptions import InvalidSelectionException


class WBParser(BaseParser):
    currency = "KZT"
    short_timeout = 1000

    @override
    async def fetch_price(self, url) -> Optional[int]:
        try:
            page = await self.get_page(url)
            await self.change_currency(page, self.currency)
            return await self.parse_price(page)
        except InvalidSelectionException as e:
            # there should be a logger instead of print in production code
            print(f"Error during price fetching: {e}")
            return None

    async def change_currency(self, page: Page, currency: str):
        if await self.validate_current_currency(page, currency):
            print(f"Currency is already set to {currency}. No change needed.")
            return
        currency_element = page.locator("css=.simple-menu__currency")
        if currency_element is None:
            raise InvalidSelectionException("Currency element not found")
        await currency_element.hover(force=True)
        await page.wait_for_timeout(
            self.short_timeout
        )  # Wait for the currency menu to appear
        tenge_element = page.locator(
            f"label.radio-with-text:has(input.j-currency-item[value='{currency}'])"
        )
        if tenge_element is None:
            raise InvalidSelectionException("Tenge currency element not found")
        await tenge_element.click()
        await page.wait_for_timeout(
            self.short_timeout
        )  # Wait for the currency change to take effect

    async def parse_price(self, page: Page) -> int:
        selector = "css=.product-page .price-block"
        price_locator = page.locator(selector)
        if await price_locator.count() > 1:
            price_locator = price_locator.first
        price_text = await price_locator.text_content()
        if price_text is None:
            raise InvalidSelectionException("Price text is empty")
        price = self.parse_price_from_text(price_text.strip())
        return price

    async def validate_current_currency(
        self, page: Page, expected_currency: str
    ) -> bool:
        currency_element = page.locator("css=.simple-menu__currency")
        if currency_element is None:
            raise InvalidSelectionException("Currency element not found")
        current_currency = await currency_element.text_content()
        if current_currency is None:
            raise InvalidSelectionException("Currency text is empty")
        return expected_currency in current_currency.strip()
