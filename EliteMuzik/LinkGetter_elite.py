import aiohttp
from bs4 import BeautifulSoup


class LinkGetter:
    @staticmethod
    async def scrape_unique_links(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")

                    unique_links = set()

                    # 1. Navbar linklerini topla
                    for link in soup.select(".menu a[href]"):
                        href = link.get("href")
                        if href:
                            full_url = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                            print("🧭 Menü linki:", full_url)

                            # Sayfa numaraları için dinamik olarak gez
                            page_num = 1
                            while True:
                                page_url = f"{full_url}?pg={page_num}"
                                if page_url in unique_links:
                                    print(f"✅ {page_url} zaten var, çıkılıyor.")
                                    break

                                print(f"📄 Sayfa linki: {page_url}")
                                unique_links.add(page_url)

                                async with session.get(page_url, headers=headers) as page_response:
                                    if page_response.status != 200:
                                        print(f"❌ {page_url} yüklenemedi.")
                                        break

                                    page_html = await page_response.text()
                                    soup = BeautifulSoup(page_html, "html.parser")

                                    canonical_tag = soup.find("link", rel="canonical")
                                    if canonical_tag:
                                        canonical_url = canonical_tag.get("href")
                                        if "?pg=" not in canonical_url and page_num > 1:
                                            print(
                                                f"🔁 {page_num}. sayfa yok, {canonical_url} adresine yönlendirildi. Durduruluyor.")
                                            break

                                page_num += 1

                    return list(unique_links)
                else:
                    print(f"❌ Sayfa çekilemedi! HTTP Kod: {response.status}")
                    return None

    @staticmethod
    async def check_page_exists(session, url):
        # Sayfanın var olup olmadığını kontrol etmek için
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
                else:
                    return False
        except:
            return False
