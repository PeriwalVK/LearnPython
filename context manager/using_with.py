from contextlib import contextmanager
import os
import time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def process(file):
    print(f"Processed {file.name}")


try:
    file = open(f"{BASE_DIR}/requirements.txt")
    try:
        process(file)
    except OSError as e:
        print("OSError:", e)
    finally:
        file.close()
except Exception as e:
    print("Generic Error:", e)
else:
    # runs only when no error block is executed
    print("No error occured")
finally:
    print("End of program")





print("=== PYTHON CONTEXT MANAGER TUTORIAL ===\n")

# ==============================================================================
# LEVEL 1: The Class-Based Context Manager
# This shows exactly how the 'with' statement works under the hood.
# ==============================================================================


class SimpleManager:
    def __init__(self, name):
        self.name = name
        print(f"[{self.name}] __init__: Object created.")

    def __enter__(self):
        # This runs immediately when you enter the 'with' block.
        print(f"[{self.name}] __enter__: Setting up resources...")

        # What you return here is assigned to the variable after 'as'
        return f"Resource({self.name})"

    def __exit__(self, exc_type, exc_val, exc_tb):
        # This runs guaranteed when the block ends (even if it crashes).
        print(f"[{self.name}] __exit__: Cleaning up resources...")

        if exc_type:
            print(f"[{self.name}] !! An error occurred: {exc_val}")
            # return True  <-- If you uncomment this, the error is suppressed/ignored.
            # return False <-- (Default) The error will crash the app after cleanup.


print("--- 1. Normal Usage ---")
with SimpleManager("Demo1") as res:
    print(f"    Inside the block. Variable 'res' is: {res}")
    print("    Doing work...")

print("\n--- 2. Handling Exceptions ---")
try:
    with SimpleManager("Demo2") as res:
        print("    Inside block. About to crash...")
        raise ValueError("Something went wrong!")
except ValueError:
    print("    (Caught the error outside the block)")


# ==============================================================================
# LEVEL 2: The 'contextlib' Shortcut
# Writing a class is verbose. Python provides a decorator to turn a
# generator function into a context manager effortlessly.
# ==============================================================================


@contextmanager
def my_generator_manager(name):
    print(f"[{name}] (Setup) Opening connection...")
    resource = ["Data1", "Data2"]

    try:
        # yield gives control back to the code inside the 'with' block
        yield resource
    except Exception as e:
        # You can handle exceptions here if you want
        print(f"[{name}] Error handled inside generator: {e}")
        raise  # Re-raise it if you don't want to silence it
    finally:
        # Code here runs when the block exits (like __exit__)
        print(f"[{name}] (Teardown) Closing connection...")


print("\n--- 3. Using the @contextmanager Decorator ---")
with my_generator_manager("GenDemo") as data:
    print(f"    Processing data: {data}")


# ==============================================================================
# LEVEL 3: A Real World Example (Performance Timer)
# A very common pattern: Measure how long a block of code takes.
# ==============================================================================


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self  # We return 'self' so the user can access properties if needed

    def __exit__(self, *args):
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"    >> Execution took: {self.duration:.4f} seconds")


print("\n--- 4. Practical Example: Timing Code ---")
with Timer():
    print("    Running heavy calculation...")
    # Simulate work
    time.sleep(0.5)

print("\n=== TUTORIAL COMPLETE ===")
