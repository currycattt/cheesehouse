"""
    python demo_lab9.py discount     (Section 2.3)
    python demo_lab9.py factory      (Section 3.2)  -> crashes on purpose
    python demo_lab9.py input        (Section 5.1)  -> type: abc, then -5, then 12.50
    python demo_lab9.py csv          (Section 5.2)  -> then rename products.csv and run again
"""
import sys

from discount import BulkDiscount, PercentageDiscount
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from storage import load_products
from supplier import Supplier

supplier = Supplier("S000", "Demo Supplier", "demo@example.com")


def demo_discount() -> None:
    product = ProductFactory.create("physical", "T1", "Item", 125.0, 10, supplier, 1.0)
    order = Order("O1", BulkDiscount(200, 20))
    order.add_order_line(product, 2)                 # lines add up to 250
    print("With BulkDiscount(200, 20):       ", order.calculate_total())
    order.set_discount(PercentageDiscount(10))
    print("After set_discount(Percentage 10):", order.calculate_total())


def demo_factory() -> None:
    ProductFactory.create("service", "S1", "Installation", 30.0, 5, supplier)
    print("This line is only reached if nothing was raised.")


def demo_input() -> None:
    value = get_positive_float("Enter a price: ")
    print("Returned:", value)


def demo_csv() -> None:
    inventory = Inventory()                          # a fresh, empty inventory
    load_products("products.csv", inventory, supplier)
    print("IDs in inventory:", [p.get_product_id() for p in inventory.get_products()])


DEMOS = {"discount": demo_discount, "factory": demo_factory,
         "input": demo_input, "csv": demo_csv}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name in DEMOS:
        DEMOS[name]()
    else:
        print("Usage: python demo_lab9.py [discount | factory | input | csv]")
