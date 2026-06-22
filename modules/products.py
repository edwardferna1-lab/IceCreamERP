import sqlite3

DB = "database/northpos.db"


def add_product(code, name, category_id, sale_price, cost, stock, minimum_stock):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO products
        (code, name, category_id, sale_price, cost, stock, minimum_stock)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (code, name, category_id, sale_price, cost, stock, minimum_stock))

        conn.commit()
        print("Product added successfully.")

    except sqlite3.IntegrityError:
        print("Error: Product code already exists.")

    finally:
        conn.close()


def list_products():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, code, name, sale_price, cost, stock, minimum_stock, active
    FROM products
    ORDER BY name
    """)

    products = cursor.fetchall()

    if not products:
        print("No products found.")
    else:
        for product in products:
            print(product)

    conn.close()


def search_product(keyword):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, code, name, sale_price, stock
    FROM products
    WHERE code LIKE ? OR name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    products = cursor.fetchall()

    if not products:
        print("No matching products found.")
    else:
        for product in products:
            print(product)

    conn.close()


def update_product(product_id, name, sale_price, cost, stock, minimum_stock):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET name = ?, sale_price = ?, cost = ?, stock = ?, minimum_stock = ?
    WHERE id = ?
    """, (name, sale_price, cost, stock, minimum_stock, product_id))

    conn.commit()
    conn.close()

    print("Product updated successfully.")


def delete_product(product_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET active = 0
    WHERE id = ?
    """, (product_id,))

    conn.commit()
    conn.close()

    print("Product disabled successfully.")


if __name__ == "__main__":
    print("NORTHPOS - PRODUCTS MODULE")
    print("--------------------------")

    list_products()