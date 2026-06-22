import sqlite3

DB = "database/northpos.db"


def add_customer(name, phone, email, address, available_credit):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO customers
    (name, phone, email, address, available_credit)
    VALUES (?, ?, ?, ?, ?)
    """, (name, phone, email, address, available_credit))

    conn.commit()
    conn.close()

    print("Customer added successfully.")


def list_customers():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, phone, email, available_credit
    FROM customers
    ORDER BY name
    """)

    customers = cursor.fetchall()

    if not customers:
        print("No customers found.")
    else:
        for customer in customers:
            print(customer)

    conn.close()


def search_customer(keyword):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, phone, email, available_credit
    FROM customers
    WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    customers = cursor.fetchall()

    if not customers:
        print("No matching customers found.")
    else:
        for customer in customers:
            print(customer)

    conn.close()


def update_customer(customer_id, name, phone, email, address, available_credit):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE customers
    SET name = ?, phone = ?, email = ?, address = ?, available_credit = ?
    WHERE id = ?
    """, (name, phone, email, address, available_credit, customer_id))

    conn.commit()
    conn.close()

    print("Customer updated successfully.")


def delete_customer(customer_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM customers
    WHERE id = ?
    """, (customer_id,))

    conn.commit()
    conn.close()

    print("Customer deleted successfully.")


if __name__ == "__main__":
    print("NORTHPOS - CUSTOMERS MODULE")
    print("---------------------------")

    add_customer(
        "Walk-in Customer",
        "N/A",
        "N/A",
        "N/A",
        0
    )

    list_customers()