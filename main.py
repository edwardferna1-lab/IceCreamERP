from modules.products import list_products
from modules.customers import list_customers
from modules.sales import create_invoice
from modules.inventory import list_inventory_movements
from modules.reports import sales_summary, top_products
from modules.users import login


def show_menu():
    print("")
    print("================================")
    print("        NORTHPOS SYSTEM")
    print("================================")
    print("1. Products")
    print("2. Customers")
    print("3. New Sale")
    print("4. Inventory / Kardex")
    print("5. Reports")
    print("6. Login Test")
    print("7. Exit")


def main():
    while True:
        show_menu()
        option = input("Select option: ")

        if option == "1":
            list_products()

        elif option == "2":
            list_customers()

        elif option == "3":
            create_invoice(
                1,
                [
                    (1, 1),
                    (2, 1)
                ],
                "Cash"
            )

        elif option == "4":
            list_inventory_movements()

        elif option == "5":
            sales_summary()
            print()
            top_products()

        elif option == "6":
            username = input("Username: ")
            password = input("Password: ")
            login(username, password)

        elif option == "7":
            print("Exiting NorthPOS...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()