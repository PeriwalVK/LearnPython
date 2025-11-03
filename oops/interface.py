"""

Interface: A “can-do” Relationship

    An interface defines a pure contract
    It defines a list of methods that a class must implement, but provides no implementation itself.
    It represents a capability or behavior that multiple, possibly unrelated, classes can share.

    Key Idea:
        It is 100% abstract — it only defines what methods must exist, not how they should work.
        It enforces a common behavior contract across different implementations.

    Relationship:
        Used for a “can-do” or “has-a-capability” relationship.

    Example:
        EmailNotifier, SlackNotifier, and SMSNotifier are completely different in implementation and purpose,
        but all of them can send notifications.
        Thus, they share a common capability — “can send a notification” — defined by the Notifier interface.

    Simple Example: INotifier
        In Python, there is no interface keyword (unlike Java or C#).
        We typically define an interface by creating an abstract base class (ABC) containing only abstract methods.

"""

from abc import ABC, abstractmethod
from typing import List


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotifier(Notifier):
    def send(self, message: str):
        print(f"Sending email: {message}")


class SlackNotifier(Notifier):
    def send(self, message: str):
        print(f"Sending Slack message: {message}")


def notify_all(notifiers, message):
    for n in notifiers:
        n.send(message)


notifiers: List[Notifier] = [EmailNotifier(), SlackNotifier()]
notify_all(notifiers, "System Down Alert!")
