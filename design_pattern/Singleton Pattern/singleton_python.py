"""
singleton_tutorial.py

Minimal tutorial-style examples of common ways to create singletons in Python.

Covered patterns:
  1) Module-as-singleton (idiomatic Python)
  2) Overriding __new__
  3) Decorator
  4) Metaclass
  5) Borg / Monostate (shared state, not a strict singleton)
"""

from threading import Lock, Thread


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def announce(msg: str):
    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


# ---------------------------------------------------------
# 1. Module-as-singleton (most Pythonic, no special code)
# ---------------------------------------------------------
"""
Python modules are already singletons by design. 
Put shared state in a module, then import that module everywhere.

Example:

  # file: config.py
  value = 42

  # file: app.py
  import config
  print(config.value)  # same object/config everywhere

The module itself acts like a singleton.
"""

# ---------------------------------------------------------
# 2. Singleton via __new__
# ---------------------------------------------------------


@announce("2. Singleton via __new__")
def _2_singleton_via_new():
    """
    This is the standard Object-Oriented approach.
    We override the __new__ method, which is responsible for creating memory for the object.
    We simply tell it: 'If we already made one, just return that one.

    Simple and effective. However, be careful—
        if you have an __init__ method, Python will run it every time you call SingletonNew(),
        potentially resetting your data (last assignment wins).
        To solve that, we move to Method 3 (Singleton via decorator)
    """

    class SingletonNew:
        """Singleton implemented by overriding __new__."""

        _instance = None

        def __new__(cls, *args, **kwargs):
            """
            Why doesn't it loop infinitely?
                It does not loop because super().__new__(cls) calls the __new__ method of the `object` class,
                not the __new__ method of your SingletonNew class.

                >>> class SingletonNew:
                >>>    pass

                IS SAME AS

                >>> class SingletonNew(object):
                >>>    pass
            """
            if cls._instance is None:
                cls._instance = super().__new__(cls)  # object.__new__(SingletonNew)
            return cls._instance

        def __init__(self, value):
            # __init__ runs on every call; last assignment wins
            self.value = value

    n1 = SingletonNew(1)
    n2 = SingletonNew(2)
    print("  n1 is n2:", n1 is n2)  # True
    print("  n1.value, n2.value:", n1.value, n2.value)
    # 2 2 (only last assignment wins bcz __init__ runs on every call)
    """
    ### => What is happening here

    Call chain:
        SingletonNew(...)
            -> type.__call__
                -> SingletonNew.__new__ (returns same instance every time)
                -> SingletonNew.__init__ (runs EVERY time: last value wins)

    So you get:
        - Same instance
        - `value` overwritten each call
    """


# ---------------------------------------------------------
# 3. Singleton via decorator (The flexible way)
# ---------------------------------------------------------


@announce("3. Singleton via decorator")
def _3_singleton_via_decorator():
    """
    The Decorator pattern allows us to hide the singleton logic outside of the class.
    This is great because your class looks clean,
    and the 'singleton' behavior is just a tag you add on top.

    This is very popular because it separates concerns.
    The Logger class focuses on logging,
    and the @singleton decorator focuses on object creation.
    """

    def singleton(cls):
        """
        Class decorator that turns a class into a singleton.

        Note: after decoration, the name refers to a factory function,
        not a real class object (but you can usually ignore that).
        """
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)  # <-- __init__ called here
            return instances[cls]

        return get_instance

    @singleton
    class SingletonDecor:
        def __init__(self, value):
            self.value = value

    d1 = SingletonDecor(1)
    d2 = SingletonDecor(2)
    print("  d1 is d2:", d1 is d2)  # True
    print(
        "  d1.value, d2.value:", d1.value, d2.value
    )  # 1 1 (bcz __init__ called only once)
    """
    ### => What is happening here

    After decoration:

    - `SingletonDecor` is now `get_instance`, a **function**, not a class.
    - First call: `get_instance(1)` constructs the instance, runs `__init__(1)`. (or say __call__)
    - Second call: `get_instance(2)` returns cached instance, no `__init__`.

    So:

    - Same instance
    - `__init__` runs only first time: first value wins

    """


# ---------------------------------------------------------
# 4. Singleton via metaclass
# ---------------------------------------------------------


@announce("4. Singleton via metaclass")
def _4_singleton_via_metaclass():
    """
        Metaclass creates the Class.
        Class creates the Instance (Object).

        >>> class Dog(metaclass=SingletonMeta):
        >>>    pass

        Relationship: Dog is an instance of SingletonMeta.
        Effect: SingletonMeta controls how the class Dog is constructed and how it behaves when you call Dog().
        Analogy: You aren't editing the blueprint. You are changing the machine that prints the blueprint.

        >>> class SingletonParent:
        >>>     pass
        >>>
        >>> class MyClass(SingletonParent):
        >>>     pass


        When you write MyClass(), you are calling the class.
        The class itself doesn't have a __call__ method (classes have __new__ and __init__).
        The __call__ method belongs to the type of the class.

        If you want to intercept the moment someone writes MyClass(), you have to change the type of the class.

        By default, the type of every class is type.
        By using metaclass=SingletonMeta, you change the type of MyClass to SingletonMeta.
        Now, when you write MyClass(), Python executes SingletonMeta.__call__.




        DEFAULT meta class `type` looks like below

        >>> class type:
        >>>     def __call__(cls, *args, **kwargs):
        >>>         obj = cls.__new__(cls, *args, **kwargs)
        >>>         if isinstance(obj, cls):
        >>>             cls.__init__(obj, *args, **kwargs)
        >>>         return obj




        ## 1.
        >>> obj = MyClass(1, 2)
        The actual sequence is:

            1. `MyClass` is a **class object**.
            2. A class object is an instance of a **metaclass** (usually `type`).
            3. Calling `MyClass(...)` is effectively:
                >>> MyClass.__call__(1, 2)
            4. since `MyClass.__call__` is inherited from its metaclass, so this is actually:
                >>> type.__call__(MyClass, 1, 2)   # when the metaclass is 'type'


        So the detailed chain is:


            MyClass(...)
                -> type.__call__(MyClass, ...)
                    -> MyClass.__new__(MyClass, ...)
                    -> MyClass.__init__(instance, ...)

        So basically calling `MyClass()` calls `__new__`, then `__init__`”,
        and the metaclass `__call__` in between is orchestrating it.



        ## 2. class SingletonMeta(type): is basically overriding __call__ method of metaclass `type`


        The new chain is:

            SingletonWithMeta(...)
                -> SingletonMeta.__call__(SingletonWithMeta, ...)
                    -> (maybe) super().__call__(SingletonWithMeta, ...)
                        -> type.__call__(SingletonWithMeta, ...)
                            -> SingletonWithMeta.__new__(SingletonWithMeta, ...)
                            -> SingletonWithMeta.__init__(instance, ...)


    ## 4. Your mental model can safely be:

    > “`MyClass(...)` → metaclass `__call__` → `__new__` → `__init__`.”

    Overriding `__new__` changes the “creation” step.
    Overriding the metaclass `__call__` changes *whether / when* creation happens at all.
    """

    class SingletonMeta(type):
        """Metaclass that makes any class using it a singleton."""

        _instances = {}

        def __call__(cls, *args, **kwargs):
            # The 'cls' argument will be the specific class being instantiated. 
            # (Ex: SingletonWithMeta)
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]

    class SingletonWithMeta(metaclass=SingletonMeta):
        def __init__(self, value):
            self.value = value

        def some_business_logic(self):
            pass

    m1 = SingletonWithMeta(1)
    m2 = SingletonWithMeta(2)
    if id(m1) == id(m2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
    print(f"  m1 is m2: {m1 is m2}")  # True
    print(f"  m1.value, m2.value: {m1.value}, {m2.value}")
    # 1 1 (bcz __init__ called only once (when __call__ was called))
    """
    ### => What is happening here

    Call chain:

        SingletonWithMeta(...)
            -> SingletonMeta.__call__
                -> (first time) type.__call__
                    -> __new__ then __init__
                -> (later) return cached instance, no __new__/__init__

    So:

    - Same instance
    - `__init__` runs only once (first call): first value wins
    - And `SingletonWithMeta` stays a “real” class, unlike the decorator version
    
    """


# ---------------------------------------------------------
# 4.1 Thread-Safe Singleton via metaclass
# ---------------------------------------------------------


@announce("4.1 Thread-Safe Singleton via metaclass")
def _4_1_thread_safe_singleton_via_metaclass():
    class SingletonMeta(type):
        """
        This is a thread-safe implementation of Singleton.
        """

        _instances = {}

        _lock: Lock = Lock()
        """
        We now have a lock object that will be used to synchronize threads during
        first access to the Singleton.
        """

        def __call__(cls, *args, **kwargs):
            """
            Possible changes to the value of the `__init__` argument do not affect
            the returned instance.
            """
            # Now, imagine that the program has just been launched. Since there's no
            # Singleton instance yet, multiple threads can simultaneously pass the
            # previous conditional and reach this point almost at the same time. The
            # first of them will acquire lock and will proceed further, while the
            # rest will wait here.

            if cls not in cls._instances:
                with cls._lock:
                    # The first thread to acquire the lock, reaches this conditional,
                    # goes inside and creates the Singleton instance. Once it leaves the
                    # lock block, a thread that might have been waiting for the lock
                    # release may then enter this section. But since the Singleton field
                    # is already initialized, the thread won't create a new object.
                    if cls not in cls._instances:
                        instance = super().__call__(*args, **kwargs)
                        cls._instances[cls] = instance

            return cls._instances[cls]

    class Singleton(metaclass=SingletonMeta):
        value: str = None
        """
        We'll use this property to prove that our Singleton really works.
        """

        def __init__(self, value: str) -> None:
            self.value = value

        def some_business_logic(self):
            pass

    def test_singleton(value: str) -> None:
        singleton = Singleton(value)
        print(f"input: {value} -> got: {singleton.value}")

    # The client code.

    print(
        "If you see the same value, then singleton was reused (yay!)\n"
        "If you see different values, "
        "then 2 singletons were created (booo!!)\n\n"
        "RESULT:\n"
    )

    process1 = Thread(target=test_singleton, args=("FOO",))
    process2 = Thread(target=test_singleton, args=("BAR",))
    process3 = Thread(target=test_singleton, args=("COCO",))
    process4 = Thread(target=test_singleton, args=("MOCO",))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()


# ---------------------------------------------------------
# 5. Borg / Monostate (shared state, many instances)
# ---------------------------------------------------------


@announce("5. Borg / Monostate pattern")
def _5_borg_or_monostate():
    class Borg:
        """
        Borg / Monostate pattern:
        - Many instances
        - All share the same state (attributes)
        """

        _shared_state = {}

        def __init__(self, value):
            # All instances share the same __dict__
            self.__dict__ = self._shared_state
            self.value = value

    b1 = Borg(1)
    b2 = Borg(2)
    print("  b1 is b2:", b1 is b2)  # False
    print("  b1.value, b2.value:", b1.value, b2.value)  # 2 2


# ---------------------------------------------------------
# Demo of all patterns
# ---------------------------------------------------------
if __name__ == "__main__":
    _2_singleton_via_new()
    _3_singleton_via_decorator()
    _4_singleton_via_metaclass()
    _4_1_thread_safe_singleton_via_metaclass()
    _5_borg_or_monostate()
