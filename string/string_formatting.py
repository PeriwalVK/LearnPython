def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


name = "Alice"
age = 10
annual_income = 500.125


separator("1. Using F-Strings")


"""
Format Specifiers: 
    A colon : used within the braces to apply formatting options, 
    (ex: for number precision or alignment, using the Format Specification Mini-Language)
Debugging with =: 
    Python 3.8+ allows the use of = within an f-string 
    to automatically display the expression and its result, 
    (great for debugging)
"""
print(
    f"name: {name}, age: {age}, annual income: {annual_income:.2f} [comma separated: {annual_income:,}], Net worth: {annual_income * age}"
)
print(
    f"{name=}, {age=}, {annual_income=:.2f}, [comma separated {annual_income=:,}], {annual_income*age=}"
)


separator("2. using str.format()")

"""
Positional Arguments: 
    Values inserted into {} placeholders (in the order they are provided).
Indexed Arguments: 
    use index numbers to specify which argument goes where (allowing for reordering or reuse)
Keyword Arguments: 
    use named placeholders and pass values as keyword arguments.
"""

print("name: {}, age: {}".format(name, age))
print("name: {1}, age: {0}".format(age, name))
print("name: {name_}, age: {age_}".format(name_=name, age_=age))


separator("3. The Modulo Operator (%)")

"""
The original C-style formatting method (generally not recommended for new code), 
but you may encounter it in legacy systems. 
It uses format specifiers like 
    %s for strings
    %d for integers
    %f for floats
    %.2f for floats with 2 decimal places 
"""
print("name: %s, age: %d, annual income: %.2f" % (name, age, annual_income))
