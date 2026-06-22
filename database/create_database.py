import sqlite3

conn = sqlite3.connect("database/heladeria.db")
cursor = conn.cursor()

# Categorías
cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
)
""")

# Productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE,
    nombre TEXT NOT NULL,
    categoria_id INTEGER,
    precio_venta REAL NOT NULL,
    costo REAL NOT NULL,
    stock REAL DEFAULT 0,
    stock_minimo REAL DEFAULT 5,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
""")

# Clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    credito_disponible REAL DEFAULT 0
)
""")

# Proveedores
cursor.execute("""
CREATE TABLE IF NOT EXISTS proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT
)
""")

# Usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT,
    rol TEXT
)
""")

# Facturas
cursor.execute("""
CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente_id INTEGER,
    subtotal REAL,
    impuestos REAL,
    total REAL,
    metodo_pago TEXT,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")

# Detalle Factura
cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_factura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER,
    producto_id INTEGER,
    cantidad REAL,
    precio REAL,
    subtotal REAL,
    FOREIGN KEY(factura_id) REFERENCES facturas(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
""")

# Kardex
cursor.execute("""
CREATE TABLE IF NOT EXISTS kardex (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    movimiento TEXT,
    cantidad REAL,
    saldo REAL,
    observacion TEXT,
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente.")