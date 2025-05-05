import aiohttp
from bs4 import BeautifulSoup
from numpy.ma.extras import unique


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

                    for link in soup.select(".menu-543 a"):
                        href = link.get("href")
                        if href:
                            full_href = href + "?ps=300"
                            unique_links.add(full_href)
                            print(full_href)

                    return list(unique_links)

                else:
                    print(f"Sayfa çekilemedi! HTTP Kod: {response.status}")
                    return None
