"""
cart.py - CampusCart cart and receipt module.
Handles adding items to the cart, calculating totals,
and streaming receipt lines.
Author: Luqman
"""


def add_to_cart(cart, inventory, item_id, quantity):
    """Add an item to the cart if it exists and has enough stock."""
    if item_id not in inventory:
        return False
    if quantity <= 0:
        return False
    if quantity > inventory[item_id]["stock"]:
        return False
    subtotal = inventory[item_id]["price"] * quantity
    cart.append({"id": item_id, "qty": quantity, "subtotal": subtotal})
    return True


def calculate_subtotal(cart):
    """Add up all the subtotals in the cart and return the total."""
    total = 0
    for item in cart:
        total += item["subtotal"]
    return total


def stream_receipt_lines(cart, inventory):
    """Yield one formatted receipt line at a time for each cart item."""
    if not cart:
        yield "Your cart is empty."
        return

    yield "--- Receipt ---"

    for item in cart:
        item_id = item["id"]
        name = inventory[item_id]["name"]
        price = inventory[item_id]["price"]
        quantity = item["qty"]
        subtotal = item["subtotal"]
        yield f"{name}: {quantity} x ${price:.2f} = ${subtotal:.2f}"

    yield f"Subtotal: ${calculate_subtotal(cart):.2f}"
    yield "---------------"