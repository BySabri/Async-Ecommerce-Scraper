from Database.product_database import sqLite

def save_to_sqlite(products, site):
    for product in products:
        try:

            name_price, stock_status = product.rsplit('|', 1)
            product_name, product_price = name_price.strip().rsplit('=', 1)

            product_name = product_name.strip()
            cleaned_price = product_price.replace(" TL", "").replace(".", "").replace(",", ".")
            product_price = float(cleaned_price.strip())
            stock_status = stock_status.replace("|", "").strip()
            product_stock = 0 if stock_status.lower() == "out of stock" else 1

            sqLite(product_name, product_price, product_stock, site)

        except Exception as e:
            print(f"Hata oluştu: {product} -> {e}")