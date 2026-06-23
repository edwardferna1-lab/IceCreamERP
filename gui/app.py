import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.sales import create_invoice

DB = "database/northpos.db"


def get_products():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, name
    FROM products
    WHERE active = 1
    ORDER BY name
    """)
    products = cursor.fetchall()
    conn.close()
    return products


class NorthPOSApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("NorthPOS - Smart Business System")
        self.geometry("1100x650")
        self.create_layout()
        self.show_dashboard()

    def create_layout(self):
        self.sidebar = tk.Frame(self, width=220, bg="#1f2937")
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="#f3f4f6")
        self.content.pack(side="right", fill="both", expand=True)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Sales", self.show_sales),
            ("Products", self.show_products),
            ("Customers", self.show_customers),
            ("Inventory", self.show_inventory),
            ("Reports", self.show_reports),
            ("Settings", self.show_settings)
        ]

        for text, command in buttons:
            tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#374151",
                fg="white",
                font=("Arial", 12),
                width=20,
                height=2
            ).pack(pady=5, padx=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM products")
        products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM invoices")
        invoices = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customers")
        customers = cursor.fetchone()[0]

        cursor.execute("SELECT IFNULL(SUM(total), 0) FROM invoices")
        sales = round(cursor.fetchone()[0], 2)

        conn.close()

        tk.Label(
            self.content,
            text="NorthPOS Dashboard",
            font=("Arial", 28, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        stats = tk.Frame(self.content, bg="#f3f4f6")
        stats.pack(pady=20)

        cards = [
            ("Products", products),
            ("Customers", customers),
            ("Invoices", invoices),
            ("Sales $", sales)
        ]

        for title, value in cards:
            card = tk.Frame(
                stats,
                bd=2,
                relief="solid",
                padx=30,
                pady=20,
                bg="white"
            )
            card.pack(side="left", padx=15)

            tk.Label(card, text=title, font=("Arial", 14, "bold"), bg="white").pack()
            tk.Label(card, text=str(value), font=("Arial", 22), bg="white").pack()

    def show_sales(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Sales Screen",
            font=("Arial", 24, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        tk.Label(self.content, text="Customer ID").pack()
        customer_entry = ttk.Entry(self.content, width=40)
        customer_entry.insert(0, "1")
        customer_entry.pack(pady=5)

        tk.Label(self.content, text="Product").pack()
        products = get_products()
        product_options = [f"{p[0]} - {p[1]}" for p in products]

        product_combo = ttk.Combobox(
            self.content,
            values=product_options,
            width=37,
            state="readonly"
        )

        if product_options:
            product_combo.current(0)

        product_combo.pack(pady=5)

        tk.Label(self.content, text="Quantity").pack()
        quantity_entry = ttk.Entry(self.content, width=40)
        quantity_entry.insert(0, "1")
        quantity_entry.pack(pady=5)

        tk.Label(self.content, text="Payment Method").pack()
        payment_combo = ttk.Combobox(
            self.content,
            values=["Cash", "Card", "Transfer", "Credit"],
            width=37,
            state="readonly"
        )
        payment_combo.current(0)
        payment_combo.pack(pady=5)

        def create_sale():
            try:
                customer_id = int(customer_entry.get())
                selected_product = product_combo.get()

                if not selected_product:
                    raise ValueError("Please select a product.")

                product_id = int(selected_product.split(" - ")[0])
                quantity = float(quantity_entry.get())
                payment_method = payment_combo.get()

                create_invoice(customer_id, [(product_id, quantity)], payment_method)

                messagebox.showinfo("Success", "Invoice created successfully.")
                self.show_sales()

            except Exception as error:
                messagebox.showerror("Error", str(error))

        ttk.Button(
            self.content,
            text="Create Invoice",
            command=create_sale
        ).pack(pady=20)

    def show_products(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Product Management",
            font=("Arial", 24, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        columns = (
            "ID", "Code", "Name", "Sale Price",
            "Cost", "Stock", "Min Stock", "Active"
        )

        table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=120)

        table.pack(fill="x", padx=20, pady=10)

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, code, name, sale_price, cost, stock, minimum_stock, active
        FROM products
        ORDER BY name
        """)

        products = cursor.fetchall()
        conn.close()

        for product in products:
            table.insert("", "end", values=product)

        ttk.Button(
            self.content,
            text="+ New Product",
            command=self.add_product_window
        ).pack(pady=5)

        ttk.Button(
            self.content,
            text="Edit Selected Product",
            command=lambda: self.edit_product_window(table)
        ).pack(pady=5)

        ttk.Button(
            self.content,
            text="Refresh",
            command=self.show_products
        ).pack(pady=10)

    def add_product_window(self):
        window = tk.Toplevel(self)
        window.title("Add Product")
        window.geometry("450x500")

        tk.Label(window, text="Code").pack(pady=5)
        code_entry = ttk.Entry(window, width=40)
        code_entry.pack()

        tk.Label(window, text="Name").pack(pady=5)
        name_entry = ttk.Entry(window, width=40)
        name_entry.pack()

        tk.Label(window, text="Sale Price").pack(pady=5)
        sale_entry = ttk.Entry(window, width=40)
        sale_entry.pack()

        tk.Label(window, text="Cost").pack(pady=5)
        cost_entry = ttk.Entry(window, width=40)
        cost_entry.pack()

        tk.Label(window, text="Stock").pack(pady=5)
        stock_entry = ttk.Entry(window, width=40)
        stock_entry.pack()

        tk.Label(window, text="Minimum Stock").pack(pady=5)
        min_stock_entry = ttk.Entry(window, width=40)
        min_stock_entry.pack()

        def save_product():
            try:
                conn = sqlite3.connect(DB)
                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO products
                (code, name, sale_price, cost, stock, minimum_stock, active)
                VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (
                    code_entry.get(),
                    name_entry.get(),
                    float(sale_entry.get()),
                    float(cost_entry.get()),
                    float(stock_entry.get()),
                    float(min_stock_entry.get())
                ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Product added successfully.")
                window.destroy()
                self.show_products()

            except Exception as error:
                messagebox.showerror("Error", str(error))

        ttk.Button(
            window,
            text="Save Product",
            command=save_product
        ).pack(pady=20)

    def edit_product_window(self, table):
        selected_item = table.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a product to edit.")
            return

        product = table.item(selected_item)["values"]

        product_id = product[0]
        code = product[1]
        name = product[2]
        sale_price = product[3]
        cost = product[4]
        stock = product[5]
        minimum_stock = product[6]

        window = tk.Toplevel(self)
        window.title("Edit Product")
        window.geometry("450x500")

        tk.Label(window, text="Code").pack(pady=5)
        code_entry = ttk.Entry(window, width=40)
        code_entry.insert(0, code)
        code_entry.pack()

        tk.Label(window, text="Name").pack(pady=5)
        name_entry = ttk.Entry(window, width=40)
        name_entry.insert(0, name)
        name_entry.pack()

        tk.Label(window, text="Sale Price").pack(pady=5)
        sale_entry = ttk.Entry(window, width=40)
        sale_entry.insert(0, sale_price)
        sale_entry.pack()

        tk.Label(window, text="Cost").pack(pady=5)
        cost_entry = ttk.Entry(window, width=40)
        cost_entry.insert(0, cost)
        cost_entry.pack()

        tk.Label(window, text="Stock").pack(pady=5)
        stock_entry = ttk.Entry(window, width=40)
        stock_entry.insert(0, stock)
        stock_entry.pack()

        tk.Label(window, text="Minimum Stock").pack(pady=5)
        min_stock_entry = ttk.Entry(window, width=40)
        min_stock_entry.insert(0, minimum_stock)
        min_stock_entry.pack()

        def save_changes():
            try:
                conn = sqlite3.connect(DB)
                cursor = conn.cursor()

                cursor.execute("""
                UPDATE products
                SET code = ?, name = ?, sale_price = ?, cost = ?, stock = ?, minimum_stock = ?
                WHERE id = ?
                """, (
                    code_entry.get(),
                    name_entry.get(),
                    float(sale_entry.get()),
                    float(cost_entry.get()),
                    float(stock_entry.get()),
                    float(min_stock_entry.get()),
                    product_id
                ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Product updated successfully.")
                window.destroy()
                self.show_products()

            except Exception as error:
                messagebox.showerror("Error", str(error))

        ttk.Button(
            window,
            text="Save Changes",
            command=save_changes
        ).pack(pady=20)

    def show_customers(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Customers",
            font=("Arial", 24, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        columns = ("ID", "Name", "Phone", "Email", "Credit")

        table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=160)

        table.pack(fill="x", padx=20, pady=10)

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, name, phone, email, available_credit
        FROM customers
        ORDER BY name
        """)

        customers = cursor.fetchall()
        conn.close()

        for customer in customers:
            table.insert("", "end", values=customer)

    def show_inventory(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Inventory Movements (Kardex)",
            font=("Arial", 24, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        columns = (
            "ID", "Code", "Product", "Movement",
            "Quantity", "Balance", "Note", "Date"
        )

        table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=120)

        table.pack(fill="both", expand=True, padx=20, pady=10)

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            im.id,
            p.code,
            p.name,
            im.movement_type,
            im.quantity,
            im.balance,
            im.note,
            im.date
        FROM inventory_movements im
        JOIN products p
            ON p.id = im.product_id
        ORDER BY im.id DESC
        """)

        movements = cursor.fetchall()
        conn.close()

        for movement in movements:
            table.insert("", "end", values=movement)

    def show_reports(self):
        self.clear_content()

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(id), IFNULL(SUM(subtotal), 0), IFNULL(SUM(tax), 0), IFNULL(SUM(total), 0)
        FROM invoices
        """)

        report = cursor.fetchone()

        cursor.execute("""
        SELECT
            products.code,
            products.name,
            SUM(invoice_details.quantity) AS units
        FROM invoice_details
        JOIN products ON invoice_details.product_id = products.id
        GROUP BY products.id
        ORDER BY units DESC
        """)

        top_products = cursor.fetchall()
        conn.close()

        tk.Label(
            self.content,
            text="Reports",
            font=("Arial", 24, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        report_text = (
            f"Total Invoices: {report[0]}\n"
            f"Subtotal Sales: ${report[1]:.2f}\n"
            f"Taxes Collected: ${report[2]:.2f}\n"
            f"Total Sales: ${report[3]:.2f}\n"
        )

        tk.Label(
            self.content,
            text=report_text,
            font=("Arial", 16),
            bg="#f3f4f6",
            justify="left"
        ).pack(pady=10)

        tk.Label(
            self.content,
            text="Top Selling Products",
            font=("Arial", 18, "bold"),
            bg="#f3f4f6"
        ).pack(pady=10)

        columns = ("Code", "Product", "Units Sold")

        table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=180)

        table.pack(pady=10)

        for product in top_products:
            table.insert("", "end", values=product)

    def show_settings(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Settings",
            font=("Arial", 24, "bold"),
            bg="#f3f4f6"
        ).pack(pady=20)

        settings_text = (
            "Business Name: NorthPOS Demo\n"
            "Tax Rate: 13%\n"
            "Currency: CAD\n"
            "Database: SQLite\n"
            "Version: 1.0"
        )

        tk.Label(
            self.content,
            text=settings_text,
            font=("Arial", 16),
            bg="#f3f4f6",
            justify="left"
        ).pack(pady=20)


if __name__ == "__main__":
    app = NorthPOSApp()
    app.mainloop()