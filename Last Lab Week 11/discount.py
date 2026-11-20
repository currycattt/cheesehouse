from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        self.__threshold = threshold
        self.__amount = amount

    def apply(self, total: float) -> float:
        return total - self.__amount if total >= self.__threshold else total


# Section 2.4: a fourth strategy, added WITHOUT touching Order
class StudentDiscount(PercentageDiscount):
    def __init__(self):
        super().__init__(5)