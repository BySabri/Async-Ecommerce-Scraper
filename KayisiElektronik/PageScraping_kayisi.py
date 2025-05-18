import aiohttp
import asyncio
from bs4 import BeautifulSoup

class PageScraper:
    @staticmethod
    async def scraping(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            retries = 5
            for attempt in range(retries):
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            text = await response.text()
                            soup = BeautifulSoup(text, "html.parser")

                            unique_products = set()

                            product_containers = soup.find_all("div", class_="showcase")
                            for container in product_containers:

                                product = container.find("div", class_="showcase-title")
                                product_name = product.get_text(strip=True) if product else "Ürün adı yok"


                                price = container.find("div", class_="showcase-price-new")
                                product_price = price.get_text(strip=True) + " TL" if price else "Fiyat bilgisi yok"


                                stock_status = "In Stock"
                                out_of_stock = soup.find("a", class_="remind-me-button")
                                if out_of_stock:
                                    stock_status = "Out of Stock"

                                unique_products.add(f"{product_name} = {product_price} |{stock_status}|")

                            return unique_products

                        elif response.status == 429:
                            wait_time = 2 ** attempt
                            print(f"⚠️ 429 Too Many Requests. {wait_time} saniye bekleniyor... ({attempt+1}. deneme)")
                            await asyncio.sleep(wait_time)

                        else:
                            print(f"Sayfa çekilemedi! HTTP Kod: {response.status}")
                            return set()

                except aiohttp.ClientError as e:
                    print(f"⚠️ İstek hatası: {e}")
                    await asyncio.sleep(2)

            print(f"❌ {url} adresi {retries} denemede de alınamadı.")
            return set()