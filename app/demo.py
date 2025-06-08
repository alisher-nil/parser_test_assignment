import asyncio
import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from app.parsers import HalykParser, KaspiParser, WBParser

load_dotenv()
kaspi_url = os.getenv("KASPI_URL", "")
wb_url = os.getenv("WB_URL", "")
halyk_url = os.getenv("HALYK_URL", "")


async def main():
    async with async_playwright() as playwright:
        # Kaspi does not protect itself from scraping.
        # Wb and halyk do, but they do not detect headless safari.
        # Ozon does not allow scraping at all, and it's protection is quite robust,
        # can't bypass it yet
        webkit_browser = await playwright.webkit.launch()

        halyk_parser = HalykParser(webkit_browser)
        kaspi_parser = KaspiParser(webkit_browser)
        wb_parser = WBParser(webkit_browser)
        tasks = [
            kaspi_parser.fetch_price(kaspi_url),
            wb_parser.fetch_price(wb_url),
            halyk_parser.fetch_price(halyk_url),
        ]
        results = await asyncio.gather(*tasks)
        results = [result for result in results if result is not None]
        print("minimum price:", min(results))
        print("maximum price:", max(results))
        print(
            f"average price: {sum(results) / len(results):.2f}",
        )
        print("mean price:", sorted(results)[len(results) // 2])
        print(results)


if __name__ == "__main__":
    asyncio.run(main())
