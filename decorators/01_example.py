import inspect

print(inspect.stack()[0][3])


def decorator1(func):
    curr_func_name = inspect.stack()[0][3]
    logger_tag = f"[{curr_func_name}]"

    def wrapper1(*args, **kwargs):
        print(f"{logger_tag} wrapper1 started, wrapping {func.__name__}, args:{args}, kwargs: {kwargs}")
        val = func(*args, **kwargs)
        print(f"{logger_tag} wrapper1 ended")
        return '#'.join(["w1", val])

    return wrapper1


def decorator2(func):
    curr_func_name = inspect.stack()[0][3]
    logger_tag = f"[{curr_func_name}]"

    def wrapper2(*args, **kwargs):
        print(f"{logger_tag} wrapper2 started, wrapping {func.__name__}, args:{args}, kwargs: {kwargs}")
        val = func(*args, **kwargs)
        print(f"{logger_tag} wrapper2 ended")
        return '#'.join(["w2", val])

    return wrapper2


@decorator1
@decorator2
def f(a):
    print(f"f called with {a}")
    return "f"

print(f("laddu"))

"""
[decorator1] wrapper1 started, wrapping wrapper2, args:('laddu',), kwargs: {}
[decorator2] wrapper2 started, wrapping f, args:('laddu',), kwargs: {}
f called with laddu
[decorator2] wrapper2 ended
[decorator1] wrapper1 ended
w1#w2#f
"""