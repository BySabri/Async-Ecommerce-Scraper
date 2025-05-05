import aiohttp
import asyncio
from bs4 import BeautifulSoup

class LinkGetter:
    @staticmethod
    async def scrape_unique_links(url):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        unique_links = set()

        async with aiohttp.ClientSession(headers=headers) as session:

            # Menü linklerini çek
            async def get_menu_links():
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"❌ Ana sayfa yüklenemedi: {response.status}")
                        return []

                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    links = []
                    for link in soup.select("div.altmenuSol a"):
                        href = link.get("href")
                        if href:
                            full_url = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                            links.append(full_url)
                    return links

            # Menüdeki bir linkin max sayfa sayısını bul
            async def get_max_page(full_url):
                try:
                    async with session.get(full_url) as response:
                        if response.status != 200:
                            return 1
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        numbers = [int(a.get_text()) for a in soup.select(".pageBorder a") if a.get_text().isdigit()]
                        return max(numbers) if numbers else 1
                except Exception as e:
                    print(f"❌ Hata: {e}")
                    return 1

            # Menüleri gez, her biri için sayfa linklerini oluştur
            menu_links = await get_menu_links()
            for menu_link in menu_links:
                print("🧭 Menü:", menu_link)
                max_page = await get_max_page(menu_link)
                print(f"🔢 Sayfa sayısı: {max_page}")
                for i in range(1, max_page + 1):
                    page_url = f"{menu_link}?sayfa={i}"
                    unique_links.add(page_url)

        return list(unique_links)
