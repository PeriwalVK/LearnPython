"""
PYTHON VARIABLE SCOPE TUTORIAL
=============================

Python follows LEGB rule to resolve variable names:

L → Local
E → Enclosing (outer function)
G → Global (module-level)
B → Built-in

This script demonstrates:
1. Local scope
2. Global scope
3. Reading vs modifying globals
4. Nested functions
5. global keyword
6. nonlocal keyword
7. Common pitfalls
"""

from os import sep


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


# --------------------------------------------------
# 1️⃣ LOCAL SCOPE
# --------------------------------------------------
separator("1️⃣  LOCAL SCOPE")


def local_example():
    x = 10  # Local Variable → function only
    print("Inside local_example(): x  =", x, "(local wala)")  # 10


local_example()
print("x not accessible outside the function")
# print(x)  # ❌ Error: x not accessible outside the function


# --------------------------------------------------
# 2️⃣ GLOBAL SCOPE
# --------------------------------------------------

separator("2️⃣  GLOBAL SCOPE")
y = 100  # Global variables → file-level


def read_global():
    print("Reading global y:", y, "(global wala)")  # 100
    # allowed without 'global'


read_global()
print("Outside function y:", y, "(able to read global wala)")  # 100


# --------------------------------------------------
# 3️⃣ MODIFYING GLOBAL VARIABLE (WITHOUT global)
# --------------------------------------------------

separator("3️⃣  MODIFYING GLOBAL VARIABLE (WITHOUT global)")
z = 100  # global


def modify_without_global():
    z = 10  # local
    print("Inside modify_without_global(): z =", z, "(local wala got modified)")  # 10


modify_without_global()
print("Outside function call z =", z, "(global wala still same)")  # 100
# Global z remains unchanged


# --------------------------------------------------
# 4️⃣ MODIFYING GLOBAL VARIABLE (WITH global)
# --------------------------------------------------

separator("4️⃣  MODIFYING GLOBAL VARIABLE (WITH global)")
a = 100  # global


def modify_with_global():
    global a  # `global`` → module-level variable
    a = 10  # modified global variable
    print("Inside modify_with_global(): a =", a, "(global wala got modified)")  # 10


modify_with_global()
print("Outside function call a =", a, "(global wala got modified)")  # 10


# --------------------------------------------------
# 5️⃣ NESTED FUNCTIONS (ENCLOSING SCOPE)
# --------------------------------------------------

separator("5️⃣  NESTED FUNCTIONS (ENCLOSING SCOPE)")
b = 100  # global


def outer_function():
    b = 10  # enclosing

    def inner_function():
        print("Inner reads enclosing b:", b, "(enclosing wala)")
        # L - NO
        # E - YES
        # G - ...
        # B - ...

    inner_function()


outer_function()


# --------------------------------------------------
# 6️⃣ global INSIDE NESTED FUNCTION
# --------------------------------------------------

separator("6️⃣  global INSIDE NESTED FUNCTION")
c = 100  # global


def outer():
    c = 10  # enclosing

    def inner():
        global c  # `global` → module-level variable
        c = 1  # global got modified
        print("Inside inner(): c =", c, "(global wala got modified to 1)")

    inner()
    print("Inside outer(): c =", c, "(enclosing remained unchanged)")


outer()
print("At module level c =", c, "(global wala got modified to 1)")

# global ALWAYS refers to module-level scope


# --------------------------------------------------
# 7️⃣ nonlocal KEYWORD
# --------------------------------------------------

separator("7️⃣  nonlocal KEYWORD")
d = 100  # global


def outer_nonlocal():
    d = 10  # enclosing

    def inner():
        nonlocal d  # `nonlocal`` → nearest enclosing variable, yaani d=10 wala
        d = 1  # hence enclosing got modified
        print("Inside inner(): d =", d, "(enclosing wala got modified to 1)")

    inner()
    print("Inside outer(): d =", d, "(bcz enclosing wala got modified to 1)")


outer_nonlocal()
print("At module level d =", d, "(bcz global wala unchanged)")


# --------------------------------------------------
# 8️⃣ MULTI-LEVEL NESTING (LEGB IN ACTION)
# --------------------------------------------------

separator("8️⃣  MULTI-LEVEL NESTING (LEGB IN ACTION)")
x = "GLOBAL"


def level_one():
    x = "ENCLOSING-1"

    def level_two():
        x = "ENCLOSING-2"

        def level_three():
            print(
                "inside_level_three(), Resolved x =",
                x,
                "(iske nearest enclosing wala yaani ENCLOSING-2)",
            )  # nearest enclosing

        level_three()

    level_two()


level_one()


# --------------------------------------------------
# 9️⃣ COMMON PITFALL
# --------------------------------------------------

separator("9️⃣  COMMON PITFALL")
k = 100  # global


def pitfall():
    # print(k)  # ❌ UnboundLocalError
    print(
        "inside pitfall(): print(k)  will give error : ❌ UnboundLocalError: "
        "cannot access local variable 'k' where it is not associated with a value"
    )
    k = 5  # Python thinks k is local because of assignment


pitfall()


# --------------------------------------------------
# 🔟 BEST PRACTICE EXAMPLE (NO global/nonlocal)
# --------------------------------------------------

separator("🔟  BEST PRACTICE EXAMPLE (NO global/nonlocal)")

print(
    "Best practice is to Prefer passing arguments and return values and then reassign"
)


num = 10  # global


def add_one(value):
    print("Inside add_one(): passed value=", value, "returning=", value + 1)
    return value + 1


print("Doing below\n>>> num = add_one(num)")
print("RESULT:")
num = add_one(num)
print("Best practice result: num is now ", num)


"""
SUMMARY
=======

- Local variables → function only
- Global variables → file-level
- global → modifies module-level variable
- nonlocal → modifies nearest enclosing variable
- Prefer passing arguments and return values
"""
