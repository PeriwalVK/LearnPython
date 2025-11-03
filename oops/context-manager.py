# from utils.common_utils import separator

# from boolean.any_all import separator
def separator(msg: str, l: int = 120):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print("=" * l)
    print(f"{'#'*hash_len} {msg} {'#'*hash_len}")
    print("=" * l)

class AnyClass:
    def __init__(self):
        print(f"(1) inside __init__")

    def __enter__(self):
        # Called at the start of the with block
        print(f"(2) inside __enter__")
        return self  # becomes `instance` in `with AnyClass() as instance:`

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"(4) inside __exit__")
        # Called at the end of the with block (even if an exception occurs)
        # Here you can clean up resources


separator("With Context manager")

with AnyClass() as instance:
    print(f"(3) inside with block")


separator("Without Context manager")
instance = AnyClass()
print(f"(3) After initialization of object")