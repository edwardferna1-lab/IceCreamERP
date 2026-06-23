import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.sales import create_invoice

DB = "database/northpos.db"


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
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#374151",
                fg="white",
                font=("Arial", 12),
                width=20,
                height=2
            )
            btn.pack(pady=5, padx=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="NorthPOS Dashboard",
            font=("Arial", 28, "bold"),
            bg="#f3f4f6"
        ).pack(pady=30)

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
        customer_entry.pack(pady=5)

        tk.Label(self.content, text="Product ID").pack()
        product_entry = ttk.Entry(self.content, width=40)
        product_entry.pack(pady=5)

        tk.Label(self.content, text="Quantity").pack()
        quantity_entry = ttk.Entry(self.content, width=40)
        quantity_entry.pack(pady=5)

        tk.Label(self.content, text="Payment Method").pack()
        payment_entry = ttk.Entry(self.content, width=40)
        payment_entry.pack(pady=5)

        def create_sale():
            try:
                customer_id = int(customer_entry.get())
                product_id = int(product_entry.get())
                quantity = float(quantity_entry.get())
                payment_method = payment_entry.get()

                create_invoice(
                    customer_id,
                    [(product_id, quantity)],
                    payment_method
                )

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
            text="Refresh",
            command=self.show_products
        ).pack(pady=10)

    def show_customers(self):
        self.clear_content()
        tk.Label(self.content, text="Customers Screen", font=("Arial", 24), bg="#f3f4f6").pack(pady=30)

    def show_inventory(self):
        self.clear_content()
        tk.Label(self.content, text="Inventory / Kardex Screen", font=("Arial", 24), bg="#f3f4f6").pack(pady=30)

    def show_reports(self):
        self.clear_content()
        tk.Label(self.content, text="Reports Screen", font=("Arial", 24), bg="#f3f4f6").pack(pady=30)

    def show_settings(self):
        self.clear_content()
        tk.Label(self.content, text="Settings Screen", font=("Arial", 24), bg="#f3f4f6").pack(pady=30)


if __name__ == "__main__":
    app = NorthPOSApp()
    app.mainloop()