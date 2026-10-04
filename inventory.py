def display_catalog(inventory):
	print("\n+----------------------------------------------+")
	print("  |	CAMPUS CART CATALOG			|")
	print("  +----------------------------------------------+")
	for items_id, item in inventory.items():
		print(
			f"ID: {items_id} | "
			f"Name: {item['name']} |"
			f"Price: ${item['price']:.2f} |"
			f"Stock: {item['stock']}"
		)
	print("================================================")


def verify_stock(inventory,items_id,requested_qty):
	"""Check whether the requested quantity is available."""
	if items_id not in inventory:
		return False
	if requested_qty <= 0:
		return False
	return requested_qty <= inventory[items_id]["stock"]

def update_stock(inventory, items_id, quantity):
	"""Make sure stock is up to date"""
	if items_id not in inventory:
		return False
	stock_update = inventory[items_id]["stock"] + quantity
	if stock_update < 0:
		return False
	inventory[items_id]["stock"] = stock_update
	return True

def calc_price_quote(item, quantity, tax_rate=0, discount_rate=0):
	"""Calculate subtotal, discount, tax and final price"""

	if quantity <= 0:
		return None

	subtotal = item['price'] * quantity
	discount = subtotal * discount_rate
	taxable_amount = subtotal - discount
	tax = taxable_amount * tax_rate
	total = taxable_amount + tax

	return {
		"subtotal": subtotal,
		"discount": discount,
		"tax": tax,
		"total": total
	}

def filter_available_products(inventory):
	available_products = filter(
		lambda item: item["stock"] > 0,
		inventory.values()
	)
	return list(available_products)

def sort_product_by_price(inventory):
	return sorted(
		inventory.values(),
		key=lambda item: item["price"]
	)


if __name__ == "__main__":
	test_inventory = {
		"101": {"name": "Notebook", "price": 2.50, "stock": 21},
		"102": {"name": "Pen", "price": 1.50, "stock": 15},
		"103": {"name": "Water Bottle", "price": 5.00, "stock": 12},
		"104": {"name": "Shirt", "price": 8.00, "stock": 25}
	}
	print("Testing stock availability:")
	print(verify_stock(test_inventory, "102", 5))

	print("\nTesting price quote:")
	quote = calc_price_quote(test_inventory["102"], 5, tax_rate=0.08, discount_rate=0.10)
	print(quote)

	print("\nTesting stock update:")
	print(update_stock(test_inventory, "102", -5))
	print(test_inventory["102"]["stock"])

	print("\nTesting available products:")
	print(filter_available_products(test_inventory))

	print("\nTesting price sorting:")
	print(sort_product_by_price(test_inventory))
