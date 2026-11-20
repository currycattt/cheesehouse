from discount import DiscountStrategy, NoDiscount
from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity


class Order:
    def __init__(self, discount: DiscountStrategy = None):
        self.order_lines = []
        self.discount = discount if discount is not None else NoDiscount()

    def add_line(self, product: Product, quantity: int):
        self.order_lines.append(OrderLine(product, quantity))

    def set_discount(self, discount: DiscountStrategy):
        self.discount = discount

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)   # no if/elif about discount types