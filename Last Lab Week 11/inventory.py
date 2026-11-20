from product import Product

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_id()) is not None:
            print("Error: Product ID already exists.")
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_id() == product_id:
                return product
        return None

    def display_all(self):
        print()
        print("Current Inventory")
        print("------------------------------------------------")
        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("------------------------------------------------")
        print()

    def get_all_data(self):
        return [product.to_dictionary() for product in self.__products]
    def get_products(self) -> list[Product]:
        return self.__products

    def get_total_units(self) -> int:
        return sum(p.get_stock() for p in self.__products)

    def exceeds_limits(self, extra_units) -> bool:
        return self.get_total_units() + extra_units > self.MAX_UNITS

    def calculate_tax(self) -> float:
        return self.TAX_RATE * self.get_total_units()