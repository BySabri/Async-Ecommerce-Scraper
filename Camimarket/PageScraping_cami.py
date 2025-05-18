from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep


class PageScraper:
    @staticmethod
    def scraping(url):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        unique_products = set()

        try:
            for _ in range(4):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(0.8)

            while True:
                try:
                    button = driver.find_element(By.CLASS_NAME, "ias-trigger-next")
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    sleep(1)
                    button.click()
                    print("🔄 Butona tıklandı.")
                    sleep(0.7)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(0.6)

                except NoSuchElementException:
                    print("✅ Tüm ürünler yüklendi.")
                    break
                except ElementClickInterceptedException:
                    print("⚠️ Butona tıklanamadı, tekrar deneniyor...")
                    sleep(1)

            product_containers = driver.find_elements(By.CLASS_NAME, "product-thumb")
            for container in product_containers:
                try:
                    product = container.find_element(By.CLASS_NAME, "name").text.strip()

                    price_container = container.find_element(By.CLASS_NAME, "price")
                    if price_container.find_elements(By.CLASS_NAME, "price-new"):
                        price = price_container.find_element(By.CLASS_NAME, "price-new").text.strip()
                    else:
                        price = price_container.text.strip()

                    stock_status = "In Stock"
                    if container.find_elements(By.CLASS_NAME, "label-outofstock"):
                        stock_status = "Out of Stock"


                    unique_products.add(f"{product} = {price} |{stock_status}|")

                    print(f"{product} = {price} ({stock_status})")
                except Exception as e:
                    print(f"⚠️ Ürün okunurken hata: {e}")

        finally:
            driver.quit()

        return unique_products
