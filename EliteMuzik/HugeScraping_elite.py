import asyncio
from ScrapingUtils.scraping_utils import ScrapingUtils
from PageScraping_elite import PageScraper
from LinkGetter_elite import LinkGetter
from ScrapingUtils.save_to_sqlite import save_to_sqlite

class SiteScraper:
    @staticmethod
    async def huge_scraper():
        base_url = "https://www.elitmuzik.com.tr"

        category_links = set(await LinkGetter.scrape_unique_links(base_url))
        unique_products = set()

        if category_links:
            await ScrapingUtils.process_category_links(
                category_links,
                base_url,
                unique_products,
                SiteScraper.scrape_category
            )

        save_to_sqlite(unique_products, "elitmuzik.com.tr")

    @staticmethod
    async def scrape_category(url, unique_products):
        try:
            products = await PageScraper.scraping(url)
            if products:
                for product in products:
                    unique_products.add(product)
        except Exception as e:
            print(f"⚠️ {url} adresine bağlanırken hata oluştu: {e}")

if __name__ == "__main__":
    asyncio.run(SiteScraper.huge_scraper())

