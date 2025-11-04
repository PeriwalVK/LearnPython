# THE PROBLEM: This class is tightly coupled to other parts of the system.
# To add a new notification (e.g., an SMS alert), you MUST modify this class.

class CustomerNotificationService:
    def notify_customers(self, product_name, stock):
        pass

class InventoryDashboard:
    def update_display(self, product_name, stock):
        pass




class BadProduct:
    def __init__(self, name):
        self.name = name
        self._stock = 0
        # The Product needs to know about every single service.
        self.notification_service = CustomerNotificationService()
        self.dashboard = InventoryDashboard()

    def set_stock(self, new_stock):
        self._stock = new_stock
        print(f"Stock for {self.name} changed to {self._stock}.")

        # Manually notifying everyone. This list will grow and become unmanageable.
        self.notification_service.notify_customers(self.name, self._stock)
        self.dashboard.update_display(self.name, self._stock)

# This code violates the Single Responsibility and Open/Closed principles.
# The Product's job is to manage product data, not to manage notifications.