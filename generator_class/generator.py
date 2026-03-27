"""

When the generator function is called, it does not execute the function body immediately.
Instead, it returns a generator object that can be iterated over to produce the values.


def generator_name(arg):
    yield something
    # similar to defining a normal function,
    # but instead of the return statement we use the yield statement.

"""

import time


def my_generator(n):

    print(
        "first line inside generator function"
    )  # will be executed when first next() is called

    # initialize counter
    value = 0

    # loop until counter is less than n
    while value < n:
        # produce the current value of the counter
        print(f"Just before yielding {value}")
        yield value  # Returns the value and pause execution till next() is called
        print(f"Just after yielding {value}")

        # increment the counter
        value += 1


# # iterate over the generator object produced by my_generator
# for value in my_generator(3):

#     # print each value produced by generator
#     print(value)

gen = my_generator(3)

print("just before calling first next on my generator obj")

print(next(gen))
"""
first line inside generator function
Just before yielding 0
0
"""

print(next(gen))
"""
Just after yielding 0
Just before yielding 1
1
"""
print(next(gen))
"""
Just after yielding 1
Just before yielding 2
2
"""
# print(next(gen))
try:
    print(next(gen))
except StopIteration as e:
    print("end achieved")
    # e.traceback()


##################### fibonacci generator #####################


def fibonacci_generator():
    """Generates an infinite sequence of Fibonacci numbers."""
    a, b = 0, 1
    while True:
        yield a  # Return 'a' and pause execution
        a, b = b, a + b  # Update a and b for the next number


gen = fibonacci_generator()

# printing first 10 fibonacci numbers
for i in range(10):
    print(f"fib[{i}] = {next(gen)}")

# for each in gen:
#     print(each)
#     time.sleep(0.2)
#     if each > 100:
#         break
#     # This keeps printing fibomnacci number infinitely


####################################################################


def is_armstrong(num_: int, digits: int):
    sum_ = 0
    curr = num_
    while curr:
        sum_ += (curr % 10) ** digits
        curr //= 10
    return sum_ == num_


def armstrong():

    # while True:
    digits = 1
    while True:
        for num in range(10 ** (digits - 1), 10 ** (digits)):
            if is_armstrong(num, digits):
                yield num
        digits += 1


g = armstrong()

# printing first 20 armstrong numbers
for i in range(20):
    print(f"Armstrong[{i+1}]: {next(g)}")


# print(is_armstrong(115132219018763992565095597973971522400, 39))
# print(is_armstrong(115132219018763992565095597973971522401, 39))
