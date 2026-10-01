# FUNCTION 1: Load previous inventory
def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            orders = []

            for line in lines:
                line = line.strip()

                if line != "":
                    parts = line.split(",")

                    order_id = int(parts[0])
                    product_name = parts[1]
                    quantity = int(parts[2])

                    orders.append([order_id, product_name, quantity])

            return orders

    except FileNotFoundError:
        return []


# FUNCTION 2: Save inventory
def save_inventory(orders):
    with open("inventory.txt", "w") as file:

        for order in orders:
            file.write(
                str(order[0]) + "," +
                order[1] + "," +
                str(order[2]) + "\n"
            )

    print("Order successfully saved to inventory.txt")


# FUNCTION 3: Get valid quantity
def get_valid_quantity():
    quantity = input("Enter Quantity: ")

    if quantity.startswith("-"):
        print("Error: negative quantity is not allowed")
        return None

    elif not quantity.isdigit():
        print("Error: Please enter valid integer")
        return None

    else:
        return int(quantity)


# Load old orders
orders = load_inventory()


# Show current orders
print("Current Orders:")
print()

for order in orders:
    print(order[0], ",", order[1], ",", order[2])

print()


# Main program
while True:

    product_name = input("Enter Product Name or 'quit' to exit: ")

    if product_name.lower() == "quit":
        save_inventory(orders)
        break

    quantity = get_valid_quantity()

    if quantity is None:
        continue


    # Generate order ID
    if len(orders) == 0:
        order_id = 1001

    else:
        order_id = orders[-1][0] + 1


    # Add new order to list
    new_order = [order_id, product_name, quantity]

    orders.append(new_order)


    print()
    print("New Order Added:")
    print(order_id, ",", product_name, ",", quantity)
    print()