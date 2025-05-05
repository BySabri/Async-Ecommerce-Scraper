import aiohttp
from bs4 import BeautifulSoup

class PageScraper:
    @staticmethod
    async def scraping(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")

                    unique_products = set()

                    product_containers = soup.find_all("div", class_="product-detail-card")
                    for container in product_containers:
                        # Marka adını çek
                        brand = container.find("a", class_="brand-title")
                        brand_name = brand.get_text(strip=True) if brand else "Marka bilgisi yok"

                        # Ürün adını çek
                        product = container.find("a", class_="product-title")
                        product_name = product.get_text(strip=True) if product else "Ürün adı yok"

                        # Fiyatı çek
                        price = container.find("span", class_="product-price")
                        product_price = price.get_text(strip=True) + " TL" if price else "Fiyat bilgisi yok"

                        # Stok durumunu kontrol et
                        stock_status = "✓"
                        out_of_stock = soup.find("span", class_="out-of-stock")
                        if out_of_stock:
                            stock_status = "X"

                        # Veriyi set'e ekle
                        unique_products.add(f"{brand_name} {product_name} = {product_price} ({stock_status})")

                    return unique_products  # Set olarak benzersiz ürünleri döndür

                else:
                    print(f"Sayfa çekilemedi! HTTP Kod: {response.status}")
                    return set()  # Boş set döndür
