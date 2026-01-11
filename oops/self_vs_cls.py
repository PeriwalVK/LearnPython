"""
self_vs_cls_tutorial.py

A small tutorial to explain the difference between `self` and `cls` in Python OOP.

Run with:

    python self_vs_cls_tutorial.py
"""

from __future__ import annotations  # just makes type hints with "ClassName" easier
from typing import TypeVar, Type

T = TypeVar("T")


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


# ====================================================================================================
# ################################ 1. DEMO: `self` (instance methods) ################################
# ====================================================================================================
def demo_self():
    separator("1. DEMO: `self` (instance methods)")

    class Dog:
        # class attribute (shared by all instances)
        species = "Canis familiaris"

        def __init__(self, name: str, age: int):
            # `self` is the *instance* being created
            self.name = name  # instance attribute
            self.age = age

        def describe(self) -> None:
            """Instance method: first parameter is `self`."""
            print(f"[Dog.describe] self is: {self!r}")
            print(f"My name is {self.name} and I am {self.age} years old.")

        def bark(self) -> None:
            print(f"{self.name} says: woof!")

        def celebrate_birthday(self) -> None:
            """Instance method that mutates instance state via `self`."""
            self.age += 1
            print(f"Happy birthday {self.name}! You are now {self.age}.")

    d = Dog("Rex", 5)
    print("Created Dog instance:", d)
    print("Species via class:", Dog.species)
    print("Species via instance:", d.species)

    # When you call d.describe(), Python translates it to Dog.describe(d)
    d.describe()
    d.bark()
    d.celebrate_birthday()


# ====================================================================================================
# ################################## 2. DEMO: `cls` (class methods) ##################################
# ====================================================================================================
def demo_cls():
    separator("2. DEMO: `cls` (class methods)")

    class Cat:
        # class attribute
        species = "Felis catus"
        counter = 0  # how many Cat (or subclasses) have been created

        def __init__(self, name: str):
            self.name = name

        # ---------- classmethod ----------
        @classmethod
        def increment_counter(cls) -> None:
            """
            Class method: first parameter is `cls`, the *class* itself.
            Can read/modify class-level data.
            """
            cls.counter += 1
            print(
                f"[Cat.increment_counter] cls = {cls.__name__}, counter = {cls.counter}"
            )

        @classmethod
        def from_string(cls: Type[T], data: str) -> T:
            """
            A common pattern: 'alternative constructor'.
            `cls` will be the concrete class we call this on.
            """
            name = data.strip()
            # IMPORTANT: use `cls`, not hard-coded `Cat`,
            # so subclasses calling this get instances of the *subclass*.
            instance = cls(name)  # type: ignore[call-arg]  # (simple demo, ignore typing noise)
            cls.increment_counter()
            return instance

        # ---------- regular instance method ----------
        def say_hi(self) -> None:
            print(f"{self.name} the {self.species} says hi!")

    class PersianCat(Cat):
        """Subclass of Cat to show how `cls` changes for subclasses."""

        species = "Persian cat"

    # Call classmethod on base class
    cat1 = Cat.from_string("Milo")
    cat1.say_hi()

    # Call the same classmethod on a subclass
    persian1 = PersianCat.from_string("Luna")
    persian1.say_hi()

    # Notice that cls was `PersianCat` inside from_string/increment_counter
    print("Cat.counter =", Cat.counter)
    print("PersianCat.counter =", PersianCat.counter)

    # You can also call classmethods through instances (not recommended stylistically, but valid):
    cat1.from_string("Another")  # effectively Cat.from_string(...)
    print("After calling from instance: Cat.counter =", Cat.counter)


# ====================================================================================================
# ############################### 3. DEMO: staticmethod (no self, no cls) ############################
# ====================================================================================================
def demo_staticmethod():
    separator("3. DEMO: staticmethod (no self, no cls)")

    class MathUtils:
        # static methods get *no* automatic first argument
        @staticmethod
        def add(a: int, b: int) -> int:
            return a + b

        @staticmethod
        def is_even(n: int) -> bool:
            return n % 2 == 0

    # Called on class
    print("MathUtils.add(2, 3) =", MathUtils.add(2, 3))

    # or on an instance (but it's just namespacing, no 'self', no 'cls'):
    utils = MathUtils()
    print("utils.is_even(4) =", utils.is_even(4))


# ====================================================================================================
# ############################## 4. DEMO: self vs cls in the same class ##############################
# ====================================================================================================
def demo_self_vs_cls_together():
    separator("4. DEMO: self vs cls in the same class")

    class VendingMachineState:
        """
        Very small, artificial example showing:
        - instance method uses `self`
        - classmethod uses `cls` to create new objects
        """

        def __init__(self, name: str):
            self.name = name

        def handle_input(self, user_input: str) -> None:
            """
            Instance method: acts *on this specific state object*.
            """
            print(f"[{self.name}.handle_input] Received:", user_input)

        @classmethod
        def create_default(cls) -> "VendingMachineState":
            """
            Classmethod: `cls` is the class; can be used as a 'factory'.
            """
            print(f"[{cls.__name__}.create_default] Creating default state")
            return cls("Idle")  # if subclass calls this, `cls` will be that subclass

    class MaintenanceState(VendingMachineState):
        pass

    # Using classmethod as factory
    default_state = VendingMachineState.create_default()
    default_state.handle_input("Insert coin")

    # From subclass: `cls` will be MaintenanceState
    maint_state = MaintenanceState.create_default()
    maint_state.handle_input("Tech menu")


# ====================================================================================================
# ############################################ 5. SUMMARY ############################################
# ====================================================================================================


def print_summary():
    separator("5. SUMMARY")
    print("""
- `self`:
    - Conventional name for the first parameter of an *instance method*.
    - Refers to the *object instance*.
    - Used to access/modify instance attributes and call other instance methods.
    - Python automatically passes the instance when you do: obj.method(...)

- `cls`:
    - Conventional name for the first parameter of a *class method* (decorated with @classmethod).
    - Refers to the *class itself* (e.g., Cat or PersianCat).
    - Used to access/modify class-level data and write alternative constructors/factories.
    - Python automatically passes the class when you do: Class.method(...)

- `@staticmethod`:
    - No `self`, no `cls` automatically.
    - Just a function that lives inside the class namespace for organization.

They are just *conventions* (you could name them differently), but using `self` and `cls`
is strongly recommended for readability.
""")


# ============================
# MAIN
# ============================


if __name__ == "__main__":
    demo_self()
    demo_cls()
    demo_staticmethod()
    demo_self_vs_cls_together()
    print_summary()
