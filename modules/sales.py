import sqlite3

DB = "database/northpos.db"
TAX_RATE = 0.13


def create_invoice(customer_id, items, payment_method):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    subtotal = 0

    # Calculate subtotal
    for product_id, quantity in items:
        cursor.execute(
            "SELECT sale_price FROM products WHERE id=?",
            (product_id,)
        )

        price = cursor.fetchone()[0]
        subtotal += price * quantity

    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)
    subtotal = round(subtotal, 2)

    # Create invoice
    cursor.execute("""
    INSERT INTO invoices
    (customer_id, subtotal, tax, total, payment_method)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        customer_id,
        subtotal,
        tax,
        total,
        payment_method
    ))

    invoice_id = cursor.lastrowid

    # Save invoice details and update inventory
    for product_id, quantity in items:
        cursor.execute(
            "SELECT sale_price, stock FROM products WHERE id=?",
            (product_id,)
        )

        product = cursor.fetchone()

        price = product[0]
        stock = product[1]
        item_subtotal = round(price * quantity, 2)

        cursor.execute("""
        INSERT INTO invoice_details
        (invoice_id, product_id, quantity, price, subtotal)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            invoice_id,
            product_id,
            quantity,
            price,
            item_subtotal
        ))

        # Reduce inventory
        new_stock = stock - quantity

        cursor.execute("""
        UPDATE products
        SET stock=?
        WHERE id=?
        """,
        (
            new_stock,
            product_id
        ))

        # Register inventory movement / Kardex
        cursor.execute("""
        INSERT INTO inventory_movements
        (product_id, movement_type, quantity, balance, note)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            product_id,
            "SALE",
            -quantity,
            new_stock,
            f"Invoice #{invoice_id}"
        ))

    conn.commit()
    conn.close()

    print("Invoice created successfully.")
    print("-----------------------------")
    print(f"Invoice ID: {invoice_id}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Total: ${total:.2f}")


if __name__ == "__main__":
    create_invoice(
        1,
        [
            (1, 2),
            (2, 1)
        ],
        "Cash"
    )