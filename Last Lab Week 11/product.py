from abc import ABC, abstractmethod


class Supplier:
    def __init__(self, name: str):
        self.name = name


class Product(ABC):
    def __init__(self, product_id, name, price, stock, supplier=None):
        # Validation lives in the class that owns the rule
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier = supplier

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    @abstractmethod
    def get_type(self) -> str:
        pass

    def update_stock(self, quantity):
        # Subclasses inherit this rule unchanged (LSP)
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(
            "ID:", self.__product_id,
            "| Type:", self.get_type(),
            "| Name:", self.__name,
            "| Price: $" + format(self.__price, ".2f"),
            "| Stock:", self.__stock
        )

    def to_dictionary(self):
        return {
            "type": self.get_type(),
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


class PhysicalProduct(Product):
    def get_type(self) -> str:
        return "physical"


class DigitalProduct(Product):
    def get_type(self) -> str:
        return "digital"