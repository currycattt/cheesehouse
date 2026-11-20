import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from discount import (NoDiscount, PercentageDiscount, BulkDiscount,
                      StudentDiscount, DiscountStrategy)
from inventory import Inventory
from input_helpers import get_positive_float
from order import Order, OrderLine
from product import PhysicalProduct, DigitalProduct
from product_factory import ProductFactory
from storage import load_products


def make_order(discount=None):
    order = Order(discount)
    order.add_line(ProductFactory.create("physical", "P1", "Lamp", 50.0, 10), 5)  # 250
    return order


class TestDiscounts(unittest.TestCase):
    def test_default_is_no_discount(self):
        self.assertEqual(make_order().calculate_total(), 250)

    def test_bulk(self):
        self.assertEqual(make_order(BulkDiscount(200, 20)).calculate_total(), 230)

    def test_set_discount_changes_strategy(self):
        order = make_order(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_new_strategy_needs_no_order_change(self):
        self.assertIsInstance(StudentDiscount(), DiscountStrategy)
        self.assertAlmostEqual(make_order(StudentDiscount()).calculate_total(), 237.5)


class TestFactory(unittest.TestCase):
    def test_creates_correct_types(self):
        self.assertIsInstance(ProductFactory.create("physical", "a", "A", 1, 1), PhysicalProduct)
        self.assertIsInstance(ProductFactory.create("digital", "b", "B", 1, 1), DigitalProduct)

    def test_unknown_type(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "s", "S", 1, 1)
        self.assertIn("Unknown product type", str(ctx.exception))


class TestValidation(unittest.TestCase):
    def test_bad_price(self):
        for price in (0, -1):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "a", "A", price, 1)

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "a", "A", 1, -1)
        product = ProductFactory.create("digital", "a", "A", 1, 1)
        with self.assertRaises(ValueError):
            product.update_stock(-5)

    def test_bad_order_quantity(self):
        product = ProductFactory.create("physical", "a", "A", 1, 1)
        for qty in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(product, qty)


class TestInputAndFiles(unittest.TestCase):
    def test_get_positive_float_retries(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            self.assertEqual(get_positive_float("Price: "), 12.5)

    def test_missing_file(self):
        inventory = Inventory()
        load_products("does_not_exist.csv", inventory)  # must not crash
        self.assertEqual(inventory.get_all_data(), [])

    def test_bad_rows_skipped(self):
        csv_text = ("product_type,product_id,name,price,stock_quantity\n"
                    "physical,P001,Desk Lamp,25.00,10\n"
                    "digital,D001,Photo Editor,49.90,100\n"
                    "service,S001,Installation,30.00,5\n"
                    "physical,P002,Office Chair,abc,3\n"
                    "physical,P003,Monitor Stand,39.50,7\n")
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write(csv_text)
        try:
            inventory = Inventory()
            load_products(f.name, inventory)
            self.assertEqual(len(inventory.get_all_data()), 3)
        finally:
            os.remove(f.name)


if __name__ == "__main__":
    unittest.main()