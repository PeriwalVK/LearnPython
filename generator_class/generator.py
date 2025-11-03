"""

When the generator function is called, it does not execute the function body immediately.
Instead, it returns a generator object that can be iterated over to produce the values.


def generator_name(arg):
    yield something
    # similar to defining a normal function,
    # but instead of the return statement we use the yield statement.

"""


def my_generator(n):

    # initialize counter
    value = 0

    # loop until counter is less than n
    while value < n:

        # produce the current value of the counter
        print(f"Just before yielding {value}")
        yield value
        print(f"Just after yielding {value}")

        # increment the counter
        value += 1


# # iterate over the generator object produced by my_generator
# for value in my_generator(3):

#     # print each value produced by generator
#     print(value)

gen = my_generator(3)

print(next(gen))
"""
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

try:
    print(next(gen))
except Exception as e:
    e.traceback()