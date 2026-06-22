import sqlite3

DB = "database/northpos.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    name TEXT NOT NULL,
    category_id INTEGER,
    sale_price REAL NOT NULL,
    cost REAL NOT NULL,
    stock REAL DEFAULT 0,
    minimum_stock REAL DEFAULT 5,
    active INTEGER DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    available_credit REAL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    customer_id INTEGER,
    subtotal REAL,
    tax REAL,
    total REAL,
    payment_method TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoice_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    product_id INTEGER,
    quantity REAL,
    price REAL,
    subtotal REAL,
    FOREIGN KEY(invoice_id) REFERENCES invoices(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    movement_type TEXT,
    quantity REAL,
    balance REAL,
    note TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

conn.commit()
conn.close()

print("NorthPOS database created successfully.")