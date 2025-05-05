class ScrapingUtils:
    @staticmethod
    async def process_category_links(category_links, base_url, unique_products, scrape_func):
        import asyncio
        tasks = []

        for category_url in category_links:
            if not category_url or " " in category_url or len(category_url) < 5:
                print(f"⚠️ Hatalı kategori linki atlandı: {category_url}")
                continue

            full_url = category_url if category_url.startswith("http") else base_url.rstrip("/") + "/" + category_url.lstrip("/")

            if not any(domain in full_url for domain in [".com", ".net", ".org"]):
                print(f"⚠️ Geçersiz domain, atlandı: {full_url}")
                continue

            print(f"\n### Kategori: {full_url} ###\n")
            tasks.append(scrape_func(full_url, unique_products))

        await asyncio.gather(*tasks)
