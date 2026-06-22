import sqlite3

DB = "database/northpos.db"


def sales_summary():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        COUNT(id),
        SUM(subtotal),
        SUM(tax),
        SUM(total)
    FROM invoices
    """)

    report = cursor.fetchone()

    print("NORTHPOS - SALES REPORT")
    print("-----------------------")
    print(f"Total Invoices: {report[0]}")
    print(f"Subtotal Sales: ${report[1]:.2f}")
    print(f"Taxes Collected: ${report[2]:.2f}")
    print(f"Total Sales: ${report[3]:.2f}")

    conn.close()


def top_products():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        products.code,
        products.name,
        SUM(invoice_details.quantity) AS units
    FROM invoice_details
    JOIN products 
    ON invoice_details.product_id = products.id
    GROUP BY products.id
    ORDER BY units DESC
    """)

    products = cursor.fetchall()

    print("")
    print("TOP SELLING PRODUCTS")
    print("--------------------")

    for product in products:
        print(product)

    conn.close()


if __name__ == "__main__":

    sales_summary()

    print()

    top_products()