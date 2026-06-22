from products import add_product

products = [
    ("ICE001", "Vanilla Ice Cream", None, 4.50, 2.00, 100, 10),
    ("ICE002", "Chocolate Ice Cream", None, 4.50, 2.00, 100, 10),
    ("ICE003", "Strawberry Ice Cream", None, 4.50, 2.00, 100, 10),
    ("ICE004", "Mango Ice Cream", None, 4.75, 2.25, 100, 10),
    ("TOP001", "Chocolate Chips", None, 0.75, 0.25, 200, 20),
    ("TOP002", "Caramel Syrup", None, 0.75, 0.30, 200, 20),
    ("DRK001", "Coca Cola", None, 2.50, 1.00, 50, 10),
    ("DRK002", "Sprite", None, 2.50, 1.00, 50, 10)
]

for product in products:
    add_product(*product)

print("Sample products loaded successfully.")