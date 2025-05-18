import aiohttp
from bs4 import BeautifulSoup
import asyncio

class PageScraper:
    @staticmethod
    async def safe_request(session, url, retries=6, delay=1):
        for attempt in range(retries):
            try:
                async with session.get(url) as response:
                    if response.status in [429, 502]:
                        print(f"⚠️ {url} - Hata {response.status}, tekrar deneme {attempt+1}")
                        await asyncio.sleep(delay * (attempt + 1))
                        continue
                    elif response.status != 200:
                        print(f"❌ {url} - HTTP Hata Kodu: {response.status}")
                        return None
                    return await response.text()
            except Exception as e:
                print(f"❌ {url} - Bağlantı hatası: {e}")
                await asyncio.sleep(delay * (attempt + 1))
        return None

    @staticmethod
    async def scraping(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            html = await PageScraper.safe_request(session, url)
            if not html:
                return set()

            soup = BeautifulSoup(html, "html.parser")
            unique_products = set()

            product_containers = soup.find_all("div", class_="productItem")
            for container in product_containers:

                product = container.find("div", class_="productName")
                product_name = product.get_text(strip=True) if product else "Ürün Adı yok"

                price = container.find("span", class_="discountPriceSpan")
                product_price = price.get_text(strip=True) if price else "Fiyat bilgisi yok"

                stock_status = "In Stock"
                out_of_stock = container.find("a", class_="TukendiIco")
                if out_of_stock:
                    stock_status = "Out of Stock"

                unique_products.add(f"{product_name} = {product_price} |{stock_status}|")

            return unique_products
