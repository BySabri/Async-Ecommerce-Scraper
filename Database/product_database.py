import sqlite3


def sqLite(product_name, product_price, product_stock, e_commerce_site):
    try:
        conn = sqlite3.connect("../Database/products.db")

        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_price REAL,
            product_stock INTEGER,
            e_commerce_site TEXT,
            date TEXT DEFAULT CURRENT_TIMESTAMP)
        """)
        cursor.execute("""INSERT INTO products (product_name, product_price, product_stock, e_commerce_site) VALUES (?,?,?,?)""",
                       (product_name, product_price, product_stock, e_commerce_site))

        conn.commit()

        print("Veri başarıyla kaydedildi!")

    except sqlite3.Error as e:
        print(f"Bir hata oluştu: {e}")

    finally:
        # Bağlantıyı kapat
        conn.close()