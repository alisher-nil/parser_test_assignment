import asyncio

from playwright.async_api import async_playwright

from app.parsers import HalykParser, KaspiParser, WBParser

kaspi_url = "https://kaspi.kz/shop/p/tush-dlja-resnits-luxvisage-xxl-superob-em-effekt-nakladnyh-resnits-dlja-ob-ema-chernyi-17400245/?c=750000000"
halyk_url = "https://halykmarket.kz/category/tush/tush-dlja-resnic-luxvisage-xxl-superobem-chernaja/"
wb_url = "https://wildberries.kz/catalog/16789083/detail.aspx?size=47262700/"


async def main():
    async with async_playwright() as playwright:
        # wb and halyk do not detect headless safari, so we use webkit
        webkit_browser = await playwright.webkit.launch()

        halyk_parser = HalykParser(webkit_browser)
        kaspi_parser = KaspiParser(webkit_browser)
        wb_parser = WBParser(webkit_browser)
        # No parser for ozon, protection too strong
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
