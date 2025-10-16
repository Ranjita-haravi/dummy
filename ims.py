from database import setup_database
from product_manager import add_product, view_products, edit_product, delete_product

def main_menu():
    while True:
        print("\n=== Inventory Management System ===")
        print("1. Add Product")
        print("2. View Products")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            edit_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            print("Exiting IMS. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    setup_database()
    main_menu()
