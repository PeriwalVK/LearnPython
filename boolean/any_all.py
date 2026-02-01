def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def f1(out: bool) -> bool:
    print(f"f1 called with {out}")
    return out


def f2(out: bool) -> bool:
    print(f"f2 called with {out}")
    return out


def f3(out: bool) -> bool:
    print(f"f3 called with {out}")
    return out


def f4(out: bool) -> bool:
    print(f"f4 called with {out}")
    return out


separator("THUMB RULE")

print("""
    Thumb Rule ==>
        1. Square Brackets [...] (Lists) ==> EAGER
            - Everything inside is calculated immediately, before doing anything else.
            - No short-circuit possible.
        2. Round Brackets (...) (Generators) & and/or ==> LAZY
            - Items are calculated one by one.
            - Stops if answer is found early (short-circuit).

    Simple:
        Brackets []  =  Build everything first
        No brackets  =  Lazy, can short-circuit
""")


# ====================================================================================================
# ################################ EAGER ==> All Functions Run First ################################
# ====================================================================================================

separator("EAGER ==> All Functions Run First")
print("""
Python sees a list. It says: "Okay, I need to build this list first."
It executes f1(), f2(), f3(), f4() and creates the list BEFORE any()/all() even starts.
""")

print("Example 1: any([f1(True), f2(True), f3(True), f4(True)])")
result = any([f1(True), f2(True), f3(True), f4(True)])
print(f"Result: {result}\n")

print("Example 2: all([f1(False), f2(False), f3(True), f4(False)])")
result = all([f1(False), f2(False), f3(True), f4(False)])
print(f"Result: {result}\n")


# ====================================================================================================
# ################################ TRICKY CASE - Looks Lazy But Is Eager! ############################
# ====================================================================================================

separator("TRICKY CASE - Looks Lazy But Is Eager!")
print("""
This LOOKS like a generator, but the inner list is built first!
    any(f for f in [f1(True), f2(True), f3(True), f4(True)])
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    This list is built EAGERLY first!
""")

print("Example: any(f for f in [f1(True), f2(True), f3(True), f4(True)])")
result = any(f for f in [f1(True), f2(True), f3(True), f4(True)])
print(f"Result: {result}")
print("  -> All 4 functions ran even though generator syntax was used!")


# ====================================================================================================
# ################################ LAZY ==> Short-circuits at First Match ############################
# ====================================================================================================

separator("LAZY ==> Short-circuits at First Match")
print("""
Python sees a generator. It pulls values ONE AT A TIME.
Stops as soon as it finds the answer.
""")

print("Example 1: any(f(True) for f in [f1, f2, f3, f4])")
print("  -> Stops at f1 because True found immediately")
result = any(f(True) for f in [f1, f2, f3, f4])  # <class 'generator'>
print(f"Result: {result}\n")


print("Example 2: all(f(False) for f in [f1, f2, f3, f4])")
print("  -> Stops at f1 because False found immediately")
result = all(f(False) for f in [f1, f2, f3, f4])
print(f"Result: {result}\n")


print("Example 3: f1(True) or f2(True) or f3(True) or f4(True)")
print("  -> Stops at f1 because True found immediately")
result = f1(True) or f2(True) or f3(True) or f4(True)
print(f"Result: {result}\n")


print("Example 4: f1(False) and f2(False) and f3(False) and f4(False)")
print("  -> Stops at f1 because False found immediately")
result = f1(False) and f2(False) and f3(False) and f4(False)
print(f"Result: {result}\n")
