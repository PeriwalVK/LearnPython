import threading
from functools import wraps

def synchronized(lock):
    """ A decorator that mimics Java's synchronized block """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator

# --- Usage ---

my_lock = threading.Lock()

@synchronized(my_lock)
def thread_safe_function():
    print("I am running safely!")

# Or inside a class
class BankAccount:
    def __init__(self):
        self._lock = threading.RLock()

    # You can apply the lock from 'self' manually, 
    # but explicit 'with' inside the method is usually preferred in Python.
    def deposit(self, amount):
        with self._lock:
            print(f"Depositing {amount}")



# class BankAccountWithDecorator:
#     def __init__(self):
#         self._lock = threading.RLock()

#     # You can apply the lock from 'self' manually, 
#     # but explicit 'with' inside the method is usually preferred in Python.
#     @synchronized(self._lock)
#     def deposit(self, amount):
        
#         print(f"Depositing {amount}")
