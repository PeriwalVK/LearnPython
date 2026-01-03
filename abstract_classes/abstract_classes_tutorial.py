"""
abstract_classes_tutorial.py

A small tutorial script that demonstrates the basics of abstract classes in Python.

Topics covered:
1. What is an abstract class and why use it?
2. How to define an abstract class using abc.ABC and @abstractmethod
3. You cannot instantiate abstract classes directly
4. Mixing abstract and concrete methods
5. Abstract properties
6. Partially implemented subclasses (still abstract)
7. Default implementations in abstract methods

Run this script:
    python abstract_classes_tutorial.py
"""

from abc import ABC, abstractmethod
from math import pi
from typing import override


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


# ====================================================================================================
# ############################### 1. BASIC ABSTRACT CLASS AND SUBCLASS ###############################
# ====================================================================================================


def basic_abstract_class_and_subclass():
    separator("1. BASIC ABSTRACT CLASS AND SUBCLASS")

    class Animal(ABC):
        """
        Abstract base class.

        - Inherit from ABC to make a class abstract-capable.
        - At least one @abstractmethod makes the class abstract.
        """

        def __init__(self, name: str):
            self.name = name

        @abstractmethod
        def speak(self) -> str:
            """
            Abstract method: subclasses MUST implement this,
            otherwise they will also be abstract and cannot be instantiated.
            """
            pass

    # Trying to instantiate an abstract class -> TypeError
    try:
        print("\nTrying to create an Animal directly...")
        a = Animal("Generic animal")  # This will fail
    except TypeError as e:
        print("Cannot instantiate Animal:", e)

    class Dog(Animal):
        """Concrete subclass that implements the abstract method."""

        @override
        def speak(self) -> str:
            return f"{self.name} says: Woof!"

    class Cat(Animal):
        """Another concrete subclass."""

        @override
        def speak(self) -> str:
            return f"{self.name} says: Meow!"

    print("\nCreating concrete subclasses that implement 'speak':")
    dog = Dog("Rex")
    cat = Cat("Mittens")
    print(dog.speak())
    print(cat.speak())


# ====================================================================================================
# ############################### 2. MIXING ABSTRACT AND CONCRETE METHODS ###############################
# ====================================================================================================


def mixing_abstract_and_concrete_methods():
    separator("2. MIXING ABSTRACT AND CONCRETE METHODS")

    class AdvancedAnimal(ABC):
        """
        Abstract base class with both abstract and concrete methods.
        """

        def __init__(self, name: str):
            self.name = name

        @abstractmethod
        def speak(self) -> str:
            """Abstract method: must be implemented by subclasses."""
            pass

        def describe(self) -> str:
            """Concrete method: shared implementation for all subclasses."""
            return f"I am an animal named {self.name}."

    class Bird(AdvancedAnimal):
        @override
        def speak(self) -> str:
            return f"{self.name} says: Tweet!"

    print("\nCreating a Bird (subclass of AdvancedAnimal):")
    parrot = Bird("Polly")
    print(parrot.describe())  # concrete method from base class
    print(parrot.speak())  # overridden abstract method


# ====================================================================================================
# ############################### 3. ABSTRACT PROPERTIES ###############################
# ====================================================================================================


def abstract_properties():
    separator("3. ABSTRACT PROPERTIES")

    class Shape(ABC):
        """
        Example showing abstract properties using @property + @abstractmethod.
        """

        @property
        @abstractmethod
        def area(self) -> float:
            """Subclasses must implement this property."""
            pass

        @property
        @abstractmethod
        def perimeter(self) -> float:
            """Another abstract property."""
            pass

    class Circle(Shape):
        def __init__(self, radius: float):
            self._radius = radius

        @property
        @override
        def area(self) -> float:
            return pi * self._radius**2

        @property
        @override
        def perimeter(self) -> float:
            return 2 * pi * self._radius

    c = Circle(3)
    print("\nCircle with radius 3:")
    print("Area:", c.area)
    print("Perimeter:", c.perimeter)


# ====================================================================================================
# ######### 4. SUBCLASSES CAN STILL BE ABSTRACT IF THEY DO NOT IMPLEMENT ALL METHODS #################
# ====================================================================================================


def subclasses_can_still_be_abstract_if_they_do_not_implement_all_methods():
    separator(
        "4. SUBCLASSES CAN STILL BE ABSTRACT IF THEY DO NOT IMPLEMENT ALL METHODS"
    )

    class PaymentProcessor(ABC):
        @abstractmethod
        def pay(self, amount: float) -> None:
            pass

        @abstractmethod
        def refund(self, amount: float) -> None:
            pass

    class OnlinePaymentProcessor(PaymentProcessor):
        """
        Implements only 'pay', forgets to implement 'refund'.
        This class is STILL ABSTRACT and cannot be instantiated.
        """

        @override
        def pay(self, amount: float) -> None:
            print(f"Paying ${amount:.2f} online.")

    try:
        print("\nTrying to create OnlinePaymentProcessor (missing 'refund')...")
        opp = OnlinePaymentProcessor()  # still abstract
    except TypeError as e:
        print("Cannot instantiate OnlinePaymentProcessor:", e)

    class FullOnlinePaymentProcessor(OnlinePaymentProcessor):
        """
        Implements the remaining abstract method 'refund'.
        Now this class is concrete and can be instantiated.
        """

        @override
        def refund(self, amount: float) -> None:
            print(f"Refunding ${amount:.2f} online.")

    print("\nCreating FullOnlinePaymentProcessor (fully implemented):")
    fopp = FullOnlinePaymentProcessor()
    fopp.pay(100)
    fopp.refund(50)


# ====================================================================================================
# ########################## 5. DEFAULT IMPLEMENTATIONS IN ABSTRACT METHODS ##########################
# ====================================================================================================


def default_implementations_in_abstract_methods():
    separator("5. DEFAULT IMPLEMENTATIONS IN ABSTRACT METHODS")

    class Logger(ABC):
        """
        You can provide a default implementation in an abstract method.
        Subclasses MUST override it, but can call super() to reuse logic.
        """

        @abstractmethod
        def log(self, message: str) -> None:
            print("[DEFAULT LOG]", message)

    class ConsoleLogger(Logger):
        @override
        def log(self, message: str) -> None:
            # Reuse the default log behavior, then add more
            super().log(message)
            print("[CONSOLE]", message)

    print("\nUsing ConsoleLogger (inherits from abstract Logger):")
    logger = ConsoleLogger()
    logger.log("Hello from abstract class tutorial!")


# ====================================================================================================
# ##################### 6. ABSTRACT CLASS AS AN 'INTERFACE' vs NORMAL INHERITANCE ####################
# ====================================================================================================


def abstract_class_as_an_interface_vs_normal_inheritance():
    separator("6. ABSTRACT CLASS AS AN 'INTERFACE' vs NORMAL INHERITANCE")

    class Flyable(ABC):
        """
        This looks like an 'interface': it only specifies behavior, no state.
        """

        @abstractmethod
        def fly(self) -> None:
            pass

    class Bird2(Flyable):
        @override
        def fly(self) -> None:
            print("Bird is flying.")

    class Airplane(Flyable):
        @override
        def fly(self) -> None:
            print("Airplane is flying.")

    print("\nBoth Bird2 and Airplane implement Flyable:")
    for obj in (Bird2(), Airplane()):
        obj.fly()
        print("Is instance of Flyable?", isinstance(obj, Flyable))


# ====================================================================================================
# ########################## 7. CONSTRUCTOR AS ABSTRACT METHOD ########################################
# ====================================================================================================


def constructor_as_abstract_method():
    separator("7. CONSTRUCTOR AS ABSTRACT METHOD")

    class DatabaseConnector(ABC):
        @abstractmethod
        def __init__(self, connection_string):
            """
            I am forcing any child class to create a constructor!
            """
            self.connection_string = connection_string

    class MySQL(DatabaseConnector):
        # This class works because it defines its own __init__
        @override
        def __init__(self, connection_string):
            self.connection_string = connection_string
            print("MySQL connected.")

    class PostgreSQL(DatabaseConnector):
        # This class fails because it relies on the parent's abstract __init__
        pass

    # --- TEST ---

    # 1. Works
    db = MySQL("mysql://localhost:3306")

    # 2. Fails
    try:
        pg = PostgreSQL("pg://localhost:5432")
    except TypeError as e:
        print(f"Error: {e}")


# ====================================================================================================
# ########################## 8. DEFINING ABSTRACT CLASS METHOD #######################################
# ====================================================================================================


def defining_abstract_class_method():
    separator("8. DEFINING ABSTRACT CLASS METHOD")

    """
    To define an abstract class method today, 
    you simply stack the @classmethod and @abstractmethod decorators. 
    The order matters: 
        @abstractmethod should be the innermost decorator (closest to the def), and 
        @classmethod should be on top.
    """

    class Base(ABC):
        @classmethod
        @abstractmethod
        def from_config(cls, config):
            """This is an abstract class method."""
            pass

    class Concrete(Base):
        @classmethod
        def from_config(cls, config):
            return cls()

    # This works
    c = Concrete.from_config({})
    print("Concrete.from_config() worked\n")

    # This would raise a TypeError because Base cannot be instantiated
    try:
        print("Instantiating Base directly...")
        b = Base()
    except TypeError as e:
        print(f"Raised a TypeError because Base cannot be instantiated: {e}")


# ====================================================================================================
# ########################################### SUMMARY ################################################
# ====================================================================================================


def summary():
    separator("SUMMARY")

    print(
        """
    Key points:
    - Inherit from 'abc.ABC' to define an abstract class.
    - Use '@abstractmethod' (and '@property' + '@abstractmethod' for properties).
    - You CANNOT instantiate a class that has unimplemented abstract methods.
    - Subclasses must implement all abstract methods/properties to be concrete.
    - Abstract classes can have normal (concrete) methods and state.
    - Abstract methods can even contain default logic that subclasses can reuse.
    """
    )


if __name__ == "__main__":
    basic_abstract_class_and_subclass()
    mixing_abstract_and_concrete_methods()
    abstract_properties()
    subclasses_can_still_be_abstract_if_they_do_not_implement_all_methods()
    default_implementations_in_abstract_methods()
    abstract_class_as_an_interface_vs_normal_inheritance()
    constructor_as_abstract_method()
    defining_abstract_class_method()
    summary()
