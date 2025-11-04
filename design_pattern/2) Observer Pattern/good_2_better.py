from __future__ import annotations  # to break circular dependencies
from abc import ABC, abstractmethod
from typing import List

# =====================================================================================
# STEP 1: DEFINE THE OBSERVER INTERFACE
#
# This is the contract for all "subscribers". It declares an `update` method
# that the Subject will call when its state changes.
# =====================================================================================


class IStockObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    # Read-only abstract field
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # # Read-write abstract field
    # @property
    # @abstractmethod
    # def price(self) -> float: ...

    # @price.setter
    # @abstractmethod
    # def price(self, value: float) -> None: ...

    @abstractmethod
    def update(self, subject: IStockSubject) -> None:
        """Receive update from subject."""
        pass


# =====================================================================================
# STEP 2: DEFINE THE SUBJECT (PUBLISHER) INTERFACE/BASE CLASS
#
# This defines the subscription management methods. A concrete Subject will use
# these to manage its list of subscribers.
# =====================================================================================


class IStockSubject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    

    @abstractmethod
    def attach(self, observer: IStockObserver) -> None:
        """Attach an observer to the subject."""
        pass

    @abstractmethod
    def detach(self, observer: IStockObserver) -> None:
        """Detach an observer from the subject."""
        pass

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about an event."""
        pass


# =====================================================================================
# STEP 3: CREATE THE CONCRETE SUBJECT CLASS
#
# This is the object that has the interesting state. It implements the subscription
# management methods and notifies its observers when its state changes.
# =====================================================================================


class Product(IStockSubject):
    """
    The Concrete Subject owns some important state and notifies observers when the
    state changes.
    """

    _stock: int = 0
    _name: str = ""
    _observers: List[IStockObserver] = []

    def __init__(self, name: str, stock: int = 0):
        self._stock = stock
        self._name = name
        self._observers = []

    def attach(self, observer: IStockObserver) -> None:
        print(f"Product '{self._name}': Attached an observer: [{observer.name}].")
        self._observers.append(observer)

    def detach(self, observer: IStockObserver) -> None:
        print(f"Product '{self._name}': Detached an observer: [{observer.name}].")
        self._observers.remove(observer)

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """
        print(f"Product '{self._name}': Notifying {len(self._observers)} observers...")
        for observer in self._observers:
            observer.update(self)

    def set_stock(self, new_stock: int) -> None:
        """
        This is the core business logic. When the state changes, we notify.
        """
        print(f"\n---> Setting stock for '{self._name}' to {new_stock}.")
        if self._stock == 0 and new_stock > 0:
            print(f"'{self._name}' is now back in stock!")

        self._stock = new_stock
        self.notify()  # The magic happens here!

    def getStock(self) -> int:
        return self._stock

    def getName(self) -> str:
        return self._name


# =====================================================================================
# STEP 4: CREATE CONCRETE OBSERVER CLASSES
#
# These are the objects that want to be notified. They are completely decoupled
# from each other and from the concrete Subject. They only know about the Observer interface.
# =====================================================================================


class CustomerNotifier(IStockObserver):
    """
    A Concrete Observer that emails customers when a product is back in stock.
    """

    # _product: Product
    _name = "Customer Notifier"

    @property
    def name(self) -> str:
        """
        The getter for the name. It simply returns the value of the
        internal _name variable. This fulfills the abstract getter requirement.
        """
        return self._name


    # def __init__(self, product: Product) -> None:
    #     self._product = product

    def update(self, subject: IStockSubject) -> None:
        if subject.getStock() > 0:
            print(
                f"[{self.name}]: Sending 'back in stock' emails for '{subject.getName()}'."
            )


class InventoryDashboard(IStockObserver):
    """
    A Concrete Observer that updates a management dashboard display.
    """

    # _product: Product
    _name = "Inventory Dashboard"

    @property
    def name(self) -> str:
        """
        The getter for the name. It simply returns the value of the
        internal _name variable. This fulfills the abstract getter requirement.
        """
        return self._name

    def update(self, subject: IStockSubject) -> None:
        print(
            f"[{self.name}]: Display for '{subject.getName()}' updated. New stock: {subject.getStock()}."
        )


class LowStockAlert(IStockObserver):
    """
    A Concrete Observer that alerts the purchasing team if stock is low.
    """

    _alert_threshold = 5
    _name = "Low Stock Alert"
    
    @property
    def name(self) -> str:
        """
        The getter for the name. It simply returns the value of the
        internal _name variable. This fulfills the abstract getter requirement.
        """
        return self._name

    def update(self, subject: IStockSubject) -> None:
        if 0 < subject.getStock() <= self._alert_threshold:
            print(
                f"[{self.name}]: WARNING! Stock for '{subject.getName()}' is low ({subject.getStock()}). Alerting purchasing team."
            )


# =====================================================================================
# STEP 5: CLIENT CODE (HOW TO USE IT)
# =====================================================================================

if __name__ == "__main__":
    # Create the Subject (the product we are tracking)
    ps5 = Product("PlayStation 5")

    # Create our Observers (the services that need to know about stock changes)
    customer_emailer = CustomerNotifier()
    dashboard = InventoryDashboard()
    purchasing_alerter = LowStockAlert()

    # --- Subscribe the observers to the subject ---
    ps5.attach(customer_emailer)
    ps5.attach(dashboard)
    ps5.attach(purchasing_alerter)

    # --- Simulate a state change: The product comes back in stock! ---
    # The set_stock method will call notify(), which will update all attached observers.
    ps5.set_stock(3)  # Stock is now low, so all three observers should react.

    # --- Simulate detaching an observer ---
    print("\nCustomer notifications are getting too spammy. Detaching the emailer.")
    ps5.detach(customer_emailer)

    # --- Simulate another state change ---
    ps5.set_stock(
        50
    )  # Now only the dashboard and low-stock alert (which won't fire) are listening.

    
    
    # =================================================================================
    # THE BIG WIN: Add a NEW observer type without touching ANY existing code.
    # The system is OPEN for extension, but CLOSED for modification.
    # =================================================================================
    class SlackAlerter(IStockObserver):
        """A new observer that sends a message to a Slack channel."""

        # _product: Product
        _name = "Slack Alerter"

        @property
        def name(self) -> str:
            """
            The getter for the name. It simply returns the value of the
            internal _name variable. This fulfills the abstract getter requirement.
            """
            return self._name

        def update(self, subject: IStockSubject) -> None:
            if subject.getStock() > 0:
                print(
                    f"[{self.name}]: Posting to #general: '{subject.getName()}' is back in stock! ({subject.getStock()} units)."
                )

    
    
    
    print("\n--- A new feature is added: Slack notifications! ---")
    slack_bot = SlackAlerter()
    ps5.attach(slack_bot)

    # Simulate one more state change to see the new observer in action
    ps5.set_stock(49)
