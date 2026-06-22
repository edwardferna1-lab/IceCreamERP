import sqlite3

DB = "database/northpos.db"


def list_inventory_movements():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        inventory_movements.id,
        products.code,
        products.name,
        inventory_movements.movement_type,
        inventory_movements.quantity,
        inventory_movements.balance,
        inventory_movements.note,
        inventory_movements.date
    FROM inventory_movements
    JOIN products ON inventory_movements.product_id = products.id
    ORDER BY inventory_movements.id DESC
    """)

    movements = cursor.fetchall()

    print("NORTHPOS - INVENTORY MOVEMENTS")
    print("------------------------------")

    for movement in movements:
        print(movement)

    conn.close()


if __name__ == "__main__":
    list_inventory_movements()
    