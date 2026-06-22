import tkinter as tk
from tkinter import ttk


class NorthPOSApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("NorthPOS - Smart Business System")
        self.geometry("1100x650")

        self.create_layout()


    def create_layout(self):

        title = tk.Label(
            self,
            text="NorthPOS Dashboard",
            font=("Arial", 24)
        )

        title.pack(pady=20)


        frame = tk.Frame(self)
        frame.pack()


        buttons = [
            "Sales",
            "Products",
            "Customers",
            "Inventory",
            "Reports",
            "Settings"
        ]


        for text in buttons:

            btn = ttk.Button(
                frame,
                text=text,
                width=25
            )

            btn.pack(pady=8)



if __name__ == "__main__":

    app = NorthPOSApp()
    app.mainloop()