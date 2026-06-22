import sqlite3

DB = "database/northpos.db"


def add_product(code, name, category_id, sale_price, cost, stock, minimum_stock):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products
    (code, name, category_id, sale_price, cost, stock, minimum_stock)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (code, name, category_id, sale_price, cost, stock, minimum_stock))

    conn.commit()
    conn.close()

    print("Product added successfully.")


def list_products():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, code, name, sale_price, stock
    FROM products
    """)

    products = cursor.fetchall()

    if len(products) == 0:
        print("No products found.")
    else:
        for product in products:
            print(product)

    conn.close()


def add_test_product():
    try:
        add_product(
            "ICE001",
            "Vanilla Ice Cream",
            None,
            4.50,
            2.00,
            100,
            10
        )
    except sqlite3.IntegrityError:
        print("Product already exists.")


if __name__ == "__main__":
    add_test_product()
    list_products()