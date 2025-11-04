# THE PROBLEM: This class violates the Open/Closed Principle.
# To add a new shipping method (e.g., "FedEx Shipping"), you MUST modify this class.
class BadOrder:
    def __init__(self, items):
        self.items = items

    def calculate_shipping_cost(self, shipping_method: str):
        total_weight = sum(item['weight'] for item in self.items)
        if shipping_method == 'flat_rate':
            # Business logic for a flat rate
            return 10.00
        elif shipping_method == 'per_item':
            # Business logic for per-item cost
            return 5.00 * len(self.items)
        elif shipping_method == 'weight_based':
            # Business logic based on weight
            return 1.50 * total_weight
        else:
            raise ValueError(f"Unknown shipping method: {shipping_method}")

# This code is rigid, hard to test, and will become a mess as more methods are added.