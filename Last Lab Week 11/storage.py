import csv
import json
import os

from inventory import Inventory
from product_factory import ProductFactory


def load_inventory():
    inventory = Inventory()
    try:
        with open("inventory.json", "r") as file:
            saved_products = json.load(file)
    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with empty inventory.")
        return inventory
    except json.JSONDecodeError:
        print("inventory.json is not valid JSON. Starting with empty inventory.")
        return inventory

    for item in saved_products:
        try:
            # older files have no "type" key, so default to physical
            product = ProductFactory.create(
                item.get("type", "physical"), item["id"], item["name"],
                item["price"], item["stock"])
            inventory.add_product(product)
        except (ValueError, KeyError) as error:
            print("Skipping bad saved product:", error)
    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory.get_all_data(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")
    print("File location:", os.path.abspath("inventory.json"))


def load_products(path, inventory, supplier=None):
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id, name,
                        float(price), int(stock), supplier)
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")