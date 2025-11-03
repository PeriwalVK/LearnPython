"""
Abstract Class: An “is-a” Relationship

    An abstract class serves as a blueprint for a group of closely related classes
    that share common structure or behavior.
    `It cannot be instantiated directly and is meant to be inherited by subclasses.

    Key Idea:
        1. It provides partial implementation —
            combining both abstract methods (declared, but not implemented) and concrete methods (fully implemented).
        2. It allows you to enforce a common interface while sharing reusable logic across subclasses.

    Relationship:
        Used when there is an “is-a” relationship between base and derived classes.

    Example:
        A StripePayment is a PaymentGateway.
        A PayPalPayment is a PaymentGateway.

    The abstract PaymentGateway class can define:
        1. Common behavior (ex: validate_amount(), log_transaction())
        2. Abstract behaviors that must be implemented by each subclass (ex: process_payment())
"""

from abc import ABC, abstractmethod
from typing import List


class PaymentGateway(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def validate_amount(self, amount: float):
        """
        Every payment gateway (like Stripe, Razorpay) shares common logic —
            like validating amount, currency conversion, etc.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

    @abstractmethod
    def process_payment(self, amount: float, currency: str):
        pass


class StripeGateway(PaymentGateway):
    def process_payment(self, amount: float, currency: str):
        self.validate_amount(amount)
        print(f"Processing {currency} {amount} via Stripe API...")
        # actual Stripe API call here


class PayPalGateway(PaymentGateway):
    def process_payment(self, amount: float, currency: str):
        self.validate_amount(amount)
        print(f"Processing {currency} {amount} via PayPal API...")
        # actual PayPal API call here


gateways: List[PaymentGateway] = [
    StripeGateway(api_key="sk_test_123"),
    PayPalGateway(api_key="pk_test_456"),
]
for each in gateways:
    each.process_payment(100, "USD")
    # Processing USD 100 via Stripe API...
    # Processing USD 100 via PayPal API...
