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


    tax = subtotal * TAX_RATE
    total = subtotal + tax


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


    # Save invoice details

    for product_id, quantity in items:

        cursor.execute(
            "SELECT sale_price, stock FROM products WHERE id=?",
            (product_id,)
        )

        product = cursor.fetchone()

        price = product[0]
        stock = product[1]

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
            price * quantity
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


    conn.commit()
    conn.close()


    print("Invoice created successfully.")
    print("Subtotal:", subtotal)
    print("Tax:", tax)
    print("Total:", total)



if __name__ == "__main__":

    create_invoice(
        1,
        [
            (1,2),
            (2,1)
        ],
        "Cash"
    )