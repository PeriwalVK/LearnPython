"""
Python Generics Tutorial (Beginner Friendly)
===========================================

Goal:
- Understand what "generics" are in Python type hints
- Learn how to write generic functions and classes using typing.TypeVar + Generic
- Learn common patterns: constraints, bounds, variance
- Understand what is checked by type checkers (mypy/pyright) vs what happens at runtime

Requires:
- Python 3.10+ recommended (3.11+ even better)
- A type checker (optional but recommended): mypy or pyright
"""

from __future__ import annotations

from dataclasses import dataclass
from re import I
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Optional,
    TypeVar,
    Protocol,
    runtime_checkable,
)

from numpy import double


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def announce(msg: str):
    """
    A decorator to announce a message before calling a function.
    """

    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


# ---------------------------------------------------------------------------
# 1) Why generics?
# ---------------------------------------------------------------------------
# A generic type lets you write code "once" but keep precise types.
#
# Example: A function that returns "the first element" should return the same
# type as the elements of the list. If the list is list[int], return int.
# If it's list[str], return str.
#
# Without generics, you'd likely return Any and lose type information.


# ---------------------------------------------------------------------------
# 2) Built-in generics: list[int], dict[str, int], etc.
# ---------------------------------------------------------------------------


@announce("(2) Built-in generics: list[int], dict[str, int], etc.")
def _2_demo_builtin_generics() -> None:
    numbers: list[int] = [1, 2, 3]
    names: list[str] = ["Ada", "Linus"]

    mapping: dict[str, int] = {"alice": 10, "bob": 20}

    print("numbers:", numbers)
    print("names:", names)
    print("mapping:", mapping)

    # These annotations help tools (mypy/pyright/IDE) catch mistakes:
    # numbers.append("oops")  # type checker would flag this


# ---------------------------------------------------------------------------
# 3) Generic functions with TypeVar
# ---------------------------------------------------------------------------
T = TypeVar("T")  # T is a "type variable": it stands for a type.


def first(items: list[T]) -> T:
    """
    Return the first element of a list, preserving its element type.

    If items is list[int], return type is int.
    If items is list[str], return type is str.
    """
    if not items:
        raise ValueError("items must not be empty")
    return items[0]


@announce("(3) Generic functions with TypeVar")
def _3_demo_generic_function() -> None:
    a = first([10, 20, 30])  # inferred type: int
    b = first(["x", "y", "z"])  # inferred type: str
    print(f"first str: {b} and type: {type(b)}")
    print(f"first int: {a} and type: {type(a)}")


# ---------------------------------------------------------------------------
# 4) Generic classes with Generic[T]
# ---------------------------------------------------------------------------
class Box(Generic[T]):
    """
    A Box[T] holds a value of type T.
    Box[int] holds an int, Box[str] holds a str, etc.
    """

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value


@announce("(4) Generic classes with Generic[T]")
def _4_demo_generic_class() -> None:
    int_box = Box[int](123)
    print("int_box.get():", int_box.get())

    str_box = Box("hello")  # type checker can infer Box[str]
    print("str_box.get():", str_box.get())

    # str_box.set(999)  # type checker would flag this (expecting str)


# ---------------------------------------------------------------------------
# 5) Optional + generics: a "maybe" result
# ---------------------------------------------------------------------------
def find_first_match(items: Iterable[T], predicate) -> Optional[T]:
    """
    Return the first item that matches predicate, or None.
    Note: predicate isn't typed here (to keep beginner-friendly).
    """
    for x in items:
        if predicate(x):
            return x
    return None


@announce("""(5) Optional + generics: a "maybe" result""")
def _5_demo_optional_generic() -> None:
    match = find_first_match([1, 2, 3, 4], lambda n: n > 2)  # Optional[int]
    print("match:", match)


# ---------------------------------------------------------------------------
# 6) TypeVar constraints and bounds
# ---------------------------------------------------------------------------
# Constraints: T can only be one of a few types.
NumberOrStr = TypeVar("NumberOrStr", int, float, str)


def stringify(x: NumberOrStr) -> str:
    # x can be int, float, or str (only those)
    return str(x)


# Bound: T must be a subtype of some base type (e.g., must be comparable)
ComparableT = TypeVar("ComparableT", bound="SupportsLessThan")


@runtime_checkable
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def min_value(a: ComparableT, b: ComparableT) -> ComparableT:
    return a if a < b else b


@announce("(6) TypeVar constraints and bounds")
def _6_demo_constraints_bounds() -> None:
    print("stringify(10):", stringify(10))
    print("stringify('x'):", stringify("x"))
    # stringify([])  # type checker would flag this

    print("min_value(3, 7):", min_value(3, 7))
    print("min_value('a', 'b'):", min_value("a", "b"))


# ---------------------------------------------------------------------------
# 7) A more realistic generic container: a Stack[T]
# ---------------------------------------------------------------------------
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._data: list[T] = []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        # iterate from bottom to top
        return iter(self._data)


@announce("(7) A more realistic generic container: a Stack[T]")
def _7_demo_stack() -> None:
    s = Stack[int]()
    s.push(1)
    s.push(2)
    print("stack len:", len(s))
    print("stack pop:", s.pop())
    # s.push("x")  # type checker would flag this


# ---------------------------------------------------------------------------
# 8) Variance (intro): covariance and invariance
# ---------------------------------------------------------------------------
# Beginners often ask:
#   "If Dog is an Animal, is list[Dog] a list[Animal]?"

# In Python typing: list is INVARIANT.
# - list[Dog] is NOT a subtype of list[Animal]

# Reason: if it were allowed, you could do:
#   animals: list[Animal] = dogs
#   animals.append(Cat())  # now dogs list has a Cat (bad!)

# Some containers are covariant, e.g. Sequence[T] (read-only view).

# We won't implement variance here, but it's useful to know the concept.


# ---------------------------------------------------------------------------
# 9) Important: Type hints are mostly NOT enforced at runtime
# ---------------------------------------------------------------------------
@announce("(9) Important: Type hints are mostly NOT enforced at runtime")
def _9_demo_runtime_behavior() -> None:
    b = Box[int](10)
    # Python will let you do this at runtime (type hints not enforced):
    b.set("oops")  # type: ignore
    print("runtime allowed wrong type in Box[int]:", b.get())
    print("=> use a type checker to catch this during development.")


# ==============================================================================
#  (10) MULTIPLE GENERICS [Example: A Pair (Tuple wrapper)]
# ==============================================================================

K = TypeVar("K")  # Key
V = TypeVar("V")  # Value


class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"Pair({self.key}, {self.value})"

    def __str__(self) -> str:
        return f"({self.key}, {self.value})"

    # __str__: "Make it pretty."
    # __repr__: "Make it precise." (And make it look like the constructor if possible).
    # Debuggers use __repr__.
    # Lists/Dicts use __repr__ for their items.


def swap(pair: Pair[K, V]) -> Pair[V, K]:
    """
    Takes a Pair<K, V> and returns a Pair<V, K>
    """
    return Pair(pair.value, pair.key)


@announce("(10) MULTIPLE GENERICS [Example: A Pair (Tuple wrapper)]")
def _10_demo_multiple_generics() -> None:
    # --- Usage ---
    my_pair = Pair("ID", 555)  # Pair[str, int]
    swapped = swap(my_pair)  # Pair[int, str]
    print("my_pair:", my_pair)
    print("swapped:", swapped)


# ==============================================================================
#  (11) BOUNDED GENERIC
# ==============================================================================

N = TypeVar("N", bound=int | float)
#  "N" can be anything, BUT it must be a subclass of (int or float).


def add_five(value: N) -> N:
    return value + 5


@announce("(11) BOUNDED GENERIC")
def _11_demo_bounded_generic() -> None:
    # --- Usage ---
    print(add_five(10))  # ✅ OK (int)
    print(add_five(10.5))  # ✅ OK (float)

    # print(add_five("A")) # ❌ TYPE ERROR
    # Even though Generics usually accept anything,
    # 'bound' stops the String at the door.


# ==============================================================================
#  (12) MODERN PYTHON GENERICS (PEP 695)
#  New in Python 3.12+
# ==============================================================================
#  Look how clean this is!
#  We declare the Generic [T] inside brackets right before the definition.
# ==============================================================================

print("""
# Old Way:
# T = TypeVar("T")
# def first(l: List[T]) -> T: ...
      
# New Way:
def first_modern[T](items: list[T]) -> T:
    return items[0]

class ModernBox[T]:
    def __init__(self, item: T):
        self.item = item

# With Constraints:
def double_val[T: (int, float)](value: T) -> T:
    return value * 2
""")


# New Way:
def first_modern[T](items: list[T]) -> T:
    return items[0]


class ModernBox[T]:
    def __init__(self, item: T):
        self.item = item


class ModernMirror[T]:
    def __init__(self):
        pass

    def mirror(self, obj: T) -> T:
        return obj


# With Constraints:
def double_val[T: (int, float)](value: T) -> T:
    return value * 2


@announce("(12) MODERN PYTHON GENERICS (PEP 695) - [New in Python 3.12+]")
def _12_demo_modern_python_generics() -> None:
    # --- Usage ---
    int_ex = first_modern([1, 2, 3])
    str_ex = first_modern(["A", "B", "C"])
    print(f"first_modern([1, 2, 3]): {int_ex} and type: {type(int_ex)}")
    print(f"""first_modern(["A", "B", "C"]): {str_ex} and type: {type(str_ex)}""")
    print()

    box = ModernBox("Hello")
    print(f"""box.item: {box.item} and type: {type(box.item)}""")
    print()

    mirror_ = ModernMirror()
    mirror_hello = mirror_.mirror("Hello")
    mirror_123 = mirror_.mirror(123)
    print(f"""mirror_.mirror("Hello"): {mirror_hello} and type: {type(mirror_hello)}""")
    print(f"""mirror_.mirror(123): {mirror_123} and type: {type(mirror_123)}""")
    print()

    Imirror = ModernMirror[int]()
    Imirror_hello = Imirror.mirror("Hello")
    Imirror_123 = Imirror.mirror(123)
    print(
        f"""int_mirror.mirror("Hello"): {Imirror_hello} and type: {type(Imirror_hello)}"""
    )
    print("❌ violated intent, But didn't fail as generics are erased at runtime")
    print(f"""int_mirror.mirror(123): {Imirror_123} and type: {type(Imirror_123)}""")
    print()

    double_ex_10 = double_val(10)
    double_ex_10_5 = double_val(10.5)
    print(f"double_val(10): {double_ex_10} and type: {type(double_ex_10)}")
    print(f"double_val(10.5): {double_ex_10_5} and type: {type(double_ex_10_5)}")


# ---------------------------------------------------------------------------
# Run all demos
# ---------------------------------------------------------------------------
def main() -> None:
    _2_demo_builtin_generics()
    _3_demo_generic_function()
    _4_demo_generic_class()
    _5_demo_optional_generic()
    _6_demo_constraints_bounds()
    _7_demo_stack()
    _9_demo_runtime_behavior()
    _10_demo_multiple_generics()
    _11_demo_bounded_generic()
    _12_demo_modern_python_generics()


if __name__ == "__main__":
    main()
