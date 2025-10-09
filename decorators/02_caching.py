import functools
import inspect


"""
The Magic of Closures
The behavior you're observing is a core concept in Python called a closure. 
A closure occurs when a nested function (like wrapper) remembers and has access to the variables from the enclosing scope 
(the cache function's scope), even after the outer function has finished executing.

The @cache syntax is just a shortcut for sum = cache(sum). 
This operation happens only one time when the Python interpreter first defines the sum function.

So, when the script is loaded:

1. The sum function is defined.
2. The decorator @cache is immediately applied. This means cache(sum) is called.
3. Inside cache(sum), the cache dictionary is created, and print("inside decorator...") is executed.
4. The cache function finishes and returns the wrapper function. The name sum is now pointing to this wrapper function.

From this point on, the cache function itself is never called again for sum.

As we established, after the decoration process, the variable sum no longer holds your original sum function. It holds the wrapper function that was created and returned by the cache decorator.
So, every time you execute print(sum(1,2)), you are actually calling wrapper(1, 2). Since the print statement is inside wrapper, it gets executed on every call.

3. How did the cache dictionary work?
This is the closure in action!

Even though the cache function finished executing (the "inside decorator" print proves this), the wrapper function maintains a reference to the environment where it was created. This environment includes the cache = dict() variable.

It's not a local variable to wrapper: It's not re-created every time wrapper is called.
It's not a global variable: It's private to this specific decorator instance. If you decorated another function with @cache, that function would get its own, separate cache dictionary.
The wrapper function "closes over" the cache dictionary. This means it can read from and write to that dictionary across multiple calls.



"""

def cache(func):
    cache = dict()
    print(f"inside decorator of {func.__name__}, cache is {cache}")

    """
        without this @functools.wraps(func)
        wrapper.__name__ = "wrapper"

        but with this
        wrapper.__name__ = wrapped.__name__
        wrapper.__doc__ = wrapped.__doc__
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"inside wrapper of {wrapper.__name__}, cache is {cache}")

        key = tuple(sorted([*args, *kwargs.values()]))

        if key not in cache:
            cache[key] = func(*args, **kwargs)
            print(f"added new cache for key {key}")
        else:
            print(f"cache hit for key {key}")
        return cache[key]
    
    return wrapper

@cache
def add(x,y):
    return x+y



"""
>>> add = cache(lambda x,y: x+y)
>>> print(add.__name__)  # '<lambda>'
hence override the name manually
>>> add.__name__ = 'add'
or can use a named decoprator, (search online)
"""


@cache
def diff(x,y):
    return abs(x-y)



print(add(1,2))
print(add(3,4))
print(add(2,3))
print(add(1,3))
print(add(4,1))
print(add(y=5, x=10))

print("----------NOW SEEING THE CACHE EFFECT---------")
print(add(3,2))
print(add(1,2))
print(add(10,5))
print(add(1, x=4))
print(add(1, y=4))
print(add(y=3, x=1))
print(add(x=10, y=5))






print("###############################")
print(diff(1,2))
print(diff(3,4))
print(diff(2,3))
print(diff(1,3))
print(diff(4,1))
print(diff(y=5, x=10))

print("----------NOW SEEING THE CACHE EFFECT---------")
print(diff(3,2))
print(diff(1,2))
print(diff(10,5))
print(diff(1, x=4))
print(diff(1, y=4))
print(diff(y=3, x=1))
print(diff(x=10, y=5))

print("----------SHOULD HIT ORIGINAL FUNCTION WITHOUT HITTING THE CACHE ---------")
"""
These will refer to original functions without any wrapper
my_func.__wrapped__.__wrapped__ in case of double decorators
if no wrapper, then throws error

a helper of the same is 
>>> original = inspect.unwrap(my_func)
it will not throw error and returns the original function itself if there is no wrapper 
"""
print(add.__wrapped__(x=10,y=5))
print(diff.__wrapped__(x=10,y=5))

print(inspect.unwrap(add)(x=10,y=5))
print(inspect.unwrap(diff)(x=10,y=5))

print(add.__wrapped__ == inspect.unwrap(add))
print(diff.__wrapped__ == inspect.unwrap(diff))



mult = lambda x,y: x*y

print(mult == inspect.unwrap(mult))
