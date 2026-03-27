print(-10 // 3)  # -4
print(10.0 // 3)  # 3.0
print(10 // 3.0)  # 3.0

x = 2e3  # or 2e3
print(type(x), x)  # float, 2000.0

n1 = "Vilas"
n2 = "Vila"

print(n1 == n2)  # False
print(n1 > n2)  # True, bcz ascending order me phle vila then vilas; hence vilas > vila


n1 = "Vilas"
n2 = "Virat"

print(n1 == n2)  # False
print(n1 > n2)  # False, jo ascenduing order me baad me aaye wo bada


n1 = "Vilas"
n2 = "vilas"

print(n1 == n2)  # False
print(n1 > n2)  # False, bcz ord("V") < ord ("v")


x = [1, 2, 3]
a, b, c = x

print(b)

# x = 9999999999999999999999999999999999999999999999999999999999999
# y = 9999999999999999999999999999999999999999999999999999999999999

# x = "9999999999999999999999999999999999999999999999999999999999999".split()
# y = "9999999999999999999999999999999999999999999999999999999999999".split()

x = int(
    "".join("9999999999999999999999999999999999999999999999999999999999999".split())
)
y = int(
    "".join("9999999999999999999999999999999999999999999999999999999999999".split())
)
z = 9999999999999999999999999999999999999999999999999999999999999
w = 9999999999999999999999999999999999999999999999999999999999999
print(id(x))
print(id(y))
print(id(z))
print(id(w))


x = [1, 2, 3]
print(isinstance(x, list))  # True


# sorting string such that first alphabets then numeric
x = "Z1A7B4"  # expected "ABZ147"


def comp(x: str, y: str):
    x_is_digit = x.isdigit()
    y_is_digit = y.isdigit()

    if x_is_digit ^ y_is_digit:  # if one is digit and other is not
        return -1 if not x_is_digit else 1  # digit should come after alphabet
    else:
        return -1 if x < y else 1


from functools import cmp_to_key

print("".join(sorted(list(x), key=cmp_to_key(comp))))

