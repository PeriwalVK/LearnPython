"""
Walrus operator (x := 1)
introduced in Python 3.8.
lets you assign a value to a variable as part of an expression.
Basically, it combines assignment and evaluation in one step.
"""

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# Without walrus operator
n = len(my_list)
if n > 10:
    print(f"List is too long ({n} elements)")

# With walrus operator
if (n := len(my_list)) > 10:
    print(f"List is too long ({n} elements)")


# Read input until user types 'quit'
while (
    line := input("Enter something (won't stop until you enter nullstring): ")
) != "":
    print(f"not quitting since you entered: {line}")

# line is also available outside if block
print(f"Now quitting since you entered: '{line}' which is nothing")


# Only keep squares of numbers if square is > 10
numbers = [1, 2, 3, 4, 5]
squares = [y for x in numbers if (y := x**2) > 10]
print(squares)  # Output: [16, 25]


# Instead of calling len(my_list) twice
if (n := len(my_list)) > 5:
    print(f"Length is {n}")


x = [0, 1, 2, 3, 4, 5]

i = -1
while (i := i + 1) < (n := len(x)):
    print(x[i])
    # i+=1

print(f"outside while since i is {i} and n is {n}")
