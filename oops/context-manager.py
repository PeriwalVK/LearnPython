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


with AnyClass() as instance:
    print(f"(3) inside with block")
