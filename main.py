"""
CampusCart - main CLI application.
Wires together the inventory, cart, and logger modules into one tool.
Author: Luqman
"""

from inventory import display_catalog, verify_stock, update_stock, calc_price_quote
from cart import add_to_cart, calculate_subtotal, stream_receipt_lines
from logger import log_transaction, get_audit_summary 

# Shared data for the whole app
inventory = {
    "101": {"name": "Notebook", "price": 24.50, "stock": 21},
    "102": {"name": "Pen", "price": 12.10, "stock": 29},
}
cart = []

# Discount rule used at checkout: 10% off when the subtotal is over $20
DISCOUNT_RATE = 0.10
DISCOUNT_THRESHOLD = 20


@log_transaction
def checkout(cart, inventory):
    """Total the cart, apply discount, deduct stock, and print a receipt."""
    if not cart:
        print("Your cart is empty. Nothing to check out.")
        return

    # Print the receipt lines from the cart module's generator
    for line in stream_receipt_lines(cart, inventory):
        print(line)

    # Work out the discounted total
    subtotal = calculate_subtotal(cart)
    rate = DISCOUNT_RATE if subtotal > DISCOUNT_THRESHOLD else 0
    quote = calc_price_quote({"price": subtotal}, 1, tax_rate=0, discount_rate=rate)
    if quote["discount"] > 0:
        print(f"Discount (10%): -${quote['discount']:.2f}")
    print(f"Total amount due: ${quote['total']:.2f}")

    # Deduct the purchased quantities from stock
    for item in cart:
        update_stock(inventory, item["id"], -item["qty"])

    cart.clear()
    print("Checkout complete. Thank you!")


def main():
    while True:
        print("\n1. View catalog")
        print("2. Add to cart")
        print("3. View cart")
        print("4. Checkout")
        print("5. Exit")

        choice = input("Choose an option: ").strip().lower()

        if choice == "1":
            display_catalog(inventory)

        elif choice == "2":
            item_id = input("Enter the item ID to add to cart: ").strip()
            if item_id not in inventory:
                print("Item not found in inventory.")
                continue
            try:
                quantity = int(input(
                    f"How many of {inventory[item_id]['name']}? "
                    f"(Available: {inventory[item_id]['stock']}): "
                ))
            except ValueError:
                print("Please enter a whole number.")
                continue
            if not verify_stock(inventory, item_id, quantity):
                print("Not enough stock, or invalid quantity.")
                continue
            if add_to_cart(cart, inventory, item_id, quantity):
                print(f"Added {quantity} x {inventory[item_id]['name']} to cart.")
            else:
                print("Could not add item to cart.")

        elif choice == "3":
            if not cart:
                print("Your cart is empty.")
            else:
                for line in stream_receipt_lines(cart, inventory):
                    print(line)

        elif choice == "4":
            checkout(cart, inventory)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please pick 1-5")


if __name__ == "__main__":
    main()