from abc import ABC, abstractmethod
from typing import List, Dict

# =====================================================================================
# STEP 1: DEFINE THE STRATEGY INTERFACE
#
# This is the contract for all our algorithms (strategies). It declares a method
# that the "Context" (our Order class) will use to execute a strategy.
# It defines WHAT a strategy does, but not HOW.
# =====================================================================================

class IShippingCostStrategy(ABC):
    """
    The Strategy Interface declares operations common to all supported versions
    of some algorithm. The Context uses this interface to call the algorithm
    defined by a Concrete Strategy.
    """
    @abstractmethod
    def calculate(self, items: List[Dict]) -> float:
        """Calculates the shipping cost for a list of items."""
        pass


# =====================================================================================
# STEP 2: CREATE THE CONCRETE STRATEGY CLASSES
#
# These classes implement the actual algorithms. Each class provides a different
# way to calculate the shipping cost. They all follow the same contract defined
# by the IShippingCostStrategy interface.
# =====================================================================================

class FlatRateStrategy(IShippingCostStrategy):
    """
    A Concrete Strategy for a simple flat shipping rate.
    """
    def calculate(self, items: List[Dict]) -> float:
        print("Calculating cost using: Flat Rate Strategy")
        return 10.00


class PerItemStrategy(IShippingCostStrategy):
    """
    A Concrete Strategy that charges a fixed amount per item in the order.
    """
    def calculate(self, items: List[Dict]) -> float:
        print("Calculating cost using: Per Item Strategy")
        cost_per_item = 5.00
        return cost_per_item * len(items)


class WeightBasedStrategy(IShippingCostStrategy):
    """
    A Concrete Strategy that charges based on the total weight of all items.
    """
    def calculate(self, items: List[Dict]) -> float:
        print("Calculating cost using: Weight Based Strategy")
        total_weight = sum(item.get('weight', 0) for item in items)
        cost_per_kg = 1.50
        return total_weight * cost_per_kg


# =====================================================================================
# STEP 3: CREATE THE CONTEXT CLASS
#
# The Context is the class whose behavior we want to change. In our case, it's
# the Order class. It holds a reference to a strategy object, but it is completely
# decoupled from the concrete strategy classes. It only knows about the interface.
# =====================================================================================

class Order:
    """
    The Context class. It contains the business data (items) and holds a
    reference to one of the strategy objects. It doesn't know the concrete
    class of a strategy. It works with all strategies via the strategy interface.
    """
    def __init__(self, items: List[Dict], shipping_strategy: IShippingCostStrategy):
        self.items = items
        # The Order is configured with a strategy object when it's created.
        self._shipping_strategy = shipping_strategy

    def set_shipping_strategy(self, shipping_strategy: IShippingCostStrategy):
        """Allows the client to change the strategy at runtime."""
        self._shipping_strategy = shipping_strategy

    def get_shipping_cost(self) -> float:
        """
        The Context delegates the work to its current strategy object instead of
        executing the logic itself. This is the core of the pattern.
        """
        return self._shipping_strategy.calculate(self.items)


# =====================================================================================
# STEP 4: CLIENT CODE (HOW TO USE IT)
#
# The client code is responsible for creating a strategy object and passing it
# to the context (the Order). The client can change the strategy at any time.
# =====================================================================================

if __name__ == "__main__":
    # Sample order data
    my_items = [
        {'name': 'Book', 'weight': 1.0},
        {'name': 'Laptop', 'weight': 2.5},
    ]

    print("--- SCENARIO 1: Customer chooses standard (flat rate) shipping ---")
    # The client creates a specific strategy object.
    flat_rate_shipping = FlatRateStrategy()
    # The client creates an order and injects the chosen strategy.
    order1 = Order(my_items, flat_rate_shipping)
    # The client asks for the shipping cost. The Order object uses the strategy it was given.
    cost1 = order1.get_shipping_cost()
    print(f"Shipping Cost: ${cost1:.2f}\n")


    print("--- SCENARIO 2: Customer changes mind and wants shipping based on weight ---")
    # The client creates a different strategy object.
    weight_based_shipping = WeightBasedStrategy()
    # We can use the same order object and just switch its strategy.
    order1.set_shipping_strategy(weight_based_shipping)
    cost2 = order1.get_shipping_cost()
    print(f"Shipping Cost: ${cost2:.2f}\n")


    print("--- SCENARIO 3: A different order with per-item shipping ---")
    # This demonstrates creating an order with a different initial strategy.
    per_item_shipping = PerItemStrategy()
    order2 = Order(my_items, per_item_shipping)
    cost3 = order2.get_shipping_cost()
    print(f"Shipping Cost: ${cost3:.2f}\n")

    # =================================================================================
    # THE BIG WIN: Adding a NEW strategy requires ZERO changes to the Order class.
    # We are following the Open/Closed Principle. The system is open for extension
    # (by adding new strategy classes) but closed for modification.
    # =================================================================================

    class FedExStrategy(IShippingCostStrategy):
        """A new shipping strategy from a third-party partner."""
        def calculate(self, items: List[Dict]) -> float:
            print("Calculating cost using: FedEx API Strategy")
            # In a real app, this would make an API call to FedEx
            # with the item details and return the cost.
            total_weight = sum(item.get('weight', 0) for item in items)
            base_rate = 15.00
            extra_weight_charge = 2.00 * total_weight
            return base_rate + extra_weight_charge

    print("--- SCENARIO 4: The business adds a new FedEx shipping option ---")
    fedex_shipping = FedExStrategy()
    order1.set_shipping_strategy(fedex_shipping)
    cost4 = order1.get_shipping_cost()
    print(f"Shipping Cost: ${cost4:.2f}\n")