import threading
import time
import random
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def print_subsection(title, l: int = 100):
    n = len(title)
    hash_len = (l - n - 2) // 2
    print(f"\n {'-' * hash_len} {title} {'-' * hash_len}\n")


def announce(msg: str):
    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


# print("--- PYTHON THREADING MASTERCLASS ---")
# print("We will go through 5 levels of complexity.\n")


# ==========================================
# LESSON 1: The Basics (Start & Join)
# ==========================================
# Goal: Run two functions at the same time.
# key concepts: .start(), .join()


@announce("LESSON 1: The Basics (Start & Join)")
def run_lesson_1():
    def heavy_calculation(name):
        print(f"[{name}] Starting calculation...")
        time.sleep(2)  # Simulates doing work
        print(f"[{name}] Calculation complete!")

    start_time = time.time()

    # 1. Create the threads
    t1 = threading.Thread(target=heavy_calculation, args=("Thread-1",))
    t2 = threading.Thread(target=heavy_calculation, args=("Thread-2",))

    # 2. Start them (This forks execution)
    t1.start()
    t2.start()

    print("[Main] Threads are running, I am waiting...")

    # 3. Join them (Wait for them to finish before continuing)
    # If we didn't do this, the script would finish before the threads were done.
    t1.join()
    t2.join()

    end_time = time.time()
    print(f"[Main] Done. Total time: {end_time - start_time:.2f}s")
    print(
        "[Main] Note: If this was sequential, it would take 4 seconds. "
        "But Because it's threaded, it takes ~2 seconds."
    )


# ==========================================
# LESSON 2: The Race Condition (The Danger Zone)
# ==========================================
# Goal: Show what happens when threads fight over shared data.
# Key concepts: Shared Memory, Data Corruption


@announce("LESSON 2: Race Conditions (Unsafe)")
def run_lesson_2():
    bank_balance = 0

    def make_transaction_unsafe():
        nonlocal bank_balance
        # We copy the value to a local variable
        current_balance = bank_balance
        # We sleep to force a "Context Switch" (simulation of the OS pausing the thread)
        time.sleep(0.0001)
        # We update the value
        bank_balance = current_balance + 1

    threads = []
    # Create 100 threads that all try to add $1 at the exact same time
    for _ in range(100):
        t = threading.Thread(target=make_transaction_unsafe)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Expected Balance: $100")
    print(f"Actual Balance:   ${bank_balance}")
    print("Why? Because threads overwrote each other's work!")


# ==========================================
# LESSON 3: Locks (The Solution)
# ==========================================
# Goal: Fix the race condition using a Lock (Mutex).
# Key concepts: threading.Lock(), acquire(), release(), context managers


@announce("LESSON 3: Locking (Safe)")
def run_lesson_3():
    safe_balance = 0
    account_lock = threading.Lock()  # Create the lock

    def make_transaction_safe():
        nonlocal safe_balance
        nonlocal account_lock

        with account_lock:
            # Only ONE thread can be inside that 'with' block at a time.
            current = safe_balance
            time.sleep(0.0001)
            safe_balance = current + 1

    threads = []
    for _ in range(100):
        t = threading.Thread(target=make_transaction_safe)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Actual Balance:   ${safe_balance} (Perfect!)")


# ==========================================
# LESSON 4: Daemon Threads
# ==========================================
# Goal: Run a background task that dies when the main program dies.
# Key concepts: daemon=True


# @announce("LESSON 4: Daemon Threads")
# def run_lesson_4():
#     def background_autosave():
#         cnt = 0
#         while True:
#             cnt+=1
#             print(f"[Autosave][{cnt}] Saving work...", end="\r")
#             time.sleep(0.5)
#             # print("here")


#     # daemon=True means: "If the main program finishes, kill this thread immediately"
#     # (Non-Daemon Thread (Default):
#     #   This is a VIP. The Python program cannot exit as long as this thread is running.
#     #   It will wait forever for it to finish.)
#     t = threading.Thread(target=background_autosave, daemon=True)
#     t.start()

#     print("[Main] Working on main task (3 seconds)...")
#     time.sleep(3)
#     print("\n[Main] Work finished. Exiting.")
#     # Notice we do NOT join the daemon thread. It dies automatically here.


# ==========================================
# LESSON 5: Producer-Consumer (Queues)
# ==========================================
# Goal: Safe communication between threads.
# Key concepts: queue.Queue, put(), get(), task_done()


@announce("LESSON 5: Thread-Safe Queues")
def run_lesson_5():
    def chef(order_queue: queue.Queue):
        while True:
            order = order_queue.get()  # Blocks until an item is available
            if order is None:
                print(f"[{threading.current_thread().name}]: Exiting...")
                break  # Poison pill to stop the thread

            print(f"[{threading.current_thread().name}] Cooking {order}...")
            time.sleep(random.uniform(0.1, 0.5))
            print(f"[{threading.current_thread().name}] {order} is ready!")

            order_queue.task_done()  # Tell queue this specific item is finished

    kitchen_queue = queue.Queue()

    # Start 2 worker threads (Chefs)
    num_threads = 2
    worker_threads = [
        threading.Thread(
            target=chef, args=(kitchen_queue,), daemon=True, name=f"Chef-{i + 1}"
        )
        for i in range(num_threads)
    ]

    for t in worker_threads:
        t.start()

    orders = ["Steak", "Pasta", "Salad", "Soup", "Burger"]

    for order in orders:
        print(f"[Waiter] Order placed: {order}")
        kitchen_queue.put(order)

    # Block the main thread until the queue is empty

    kitchen_queue.join()
    # for _ in worker_threads:
    #     kitchen_queue.put(None)

    print("[Manager] All orders served!")


# ==========================================
# BONUS: The Professional Way (ThreadPoolExecutor)
# ==========================================
# Goal: Do Lesson 1 but with less code and better management.


@announce("BONUS: ThreadPoolExecutor (Modern Standard)")
def run_bonus():
    def download_url(url):
        time.sleep(random.uniform(0.5, 1))
        return f"[{threading.current_thread().name}] Data from {url}"

    urls = ["google.com", "yahoo.com", "bing.com", "duckduckgo.com", "github.com"]

    # Automatically manages threads, queue, and starting/stopping
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(download_url, urls)

    for res in results:
        print(f"[Main] Received: {res}")


# ==========================================
# MAIN RUNNER
# ==========================================
def main1():
    # Uncomment the lesson you want to run, or run them all
    run_lesson_1()
    run_lesson_2()
    run_lesson_3()
    run_lesson_5()
    run_bonus()


"""
=============================================================================
PYTHON THREADING COMPLETE TUTORIAL
=============================================================================
A comprehensive guide to Python's threading library with practical examples.

Author: Threading Tutorial
Python Version: 3.7+

Table of Contents:
    1. Basic Thread Creation
    2. Creating Threads with Classes
    3. Thread Naming and Identification
    4. Daemon Threads
    5. Thread Joining and Waiting
    6. Race Conditions (The Problem)
    7. Thread Synchronization - Lock
    8. Thread Synchronization - RLock (Reentrant Lock)
    9. Thread Synchronization - Semaphore
    10. Thread Synchronization - Event
    11. Thread Synchronization - Condition
    12. Thread Synchronization - Barrier
    13. Thread-Local Data
    14. Timer Threads
    15. Thread-Safe Queue (Producer-Consumer Pattern)
    16. Thread Pool (concurrent.futures)
    17. Common Pitfalls and Best Practices

Run this script to see all examples in action!
=============================================================================
"""


# =============================================================================
# SECTION 1: BASIC THREAD CREATION
# =============================================================================


@announce("SECTION 1: BASIC THREAD CREATION")
def section_1_basic_thread_creation():
    """
    The simplest way to create a thread is using threading.Thread()
    with a target function.
    """

    # Simple function to run in a thread
    def say_hello(name):
        """A simple function that will run in a separate thread."""
        print(f"[{name}]: Hello from {name}!")
        print(f"[{name}]: Thread ID: {threading.current_thread().ident}")
        time.sleep(1)  # Simulate some work
        print(f"[{name}]: Thread finished!")

    print("Creating and starting threads...")
    print(f"Main thread: {threading.current_thread().name}\n")

    # Method 1: Create and start separately
    thread1 = threading.Thread(target=say_hello, args=("Thread-1",))
    thread1.start()

    # Method 2: Multiple threads
    thread2 = threading.Thread(target=say_hello, args=("Thread-2",))
    thread3 = threading.Thread(target=say_hello, args=("Thread-3",))

    thread2.start()
    thread3.start()

    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    print("\nAll threads completed!")

    # Show active thread count
    print(f"Active threads: {threading.active_count()}")


# =============================================================================
# SECTION 2: CREATING THREADS WITH CLASSES
# =============================================================================


@announce("SECTION 2: CREATING THREADS WITH CLASSES")
def section_2_thread_classes():
    """
    You can also create threads by subclassing threading.Thread.
    This is useful when you need to maintain state or have complex logic.
    """

    class WorkerThread(threading.Thread):
        """Custom thread class that performs a specific task."""

        def __init__(self, worker_id, iterations):
            # IMPORTANT: Always call parent __init__
            super().__init__()
            self.worker_id = worker_id
            self.iterations = iterations
            self.result = 0  # Store result

        def run(self):
            """
            Override run() method - this is what executes in the thread.
            DO NOT call run() directly! Use start() instead.
            """
            print(f"  Worker {self.worker_id} starting...")

            for i in range(self.iterations):
                self.result += i
                time.sleep(0.1)

            print(f"  Worker {self.worker_id} finished with result: {self.result}")

    # Create thread instances
    workers = [
        WorkerThread(worker_id=1, iterations=5),
        WorkerThread(worker_id=2, iterations=3),
        WorkerThread(worker_id=3, iterations=4),
    ]

    # Start all threads
    for worker in workers:
        worker.start()  # Calls run() in a new thread

    # Wait for completion and collect results
    for worker in workers:
        worker.join()

    # Access results
    total = sum(w.result for w in workers)
    print(f"\nTotal result from all workers: {total}")


# =============================================================================
# SECTION 3: THREAD NAMING AND IDENTIFICATION
# =============================================================================


@announce("SECTION 3: THREAD NAMING AND IDENTIFICATION")
def section_3_thread_naming():
    """
    Threads can be named for easier debugging and logging.
    Each thread also has a unique identifier.
    """

    def show_thread_info():
        """Display information about the current thread."""
        current = threading.current_thread()
        print(f"  Name: {current.name}")
        print(f"  ID: {current.ident}")
        print(f"  Native ID: {current.native_id}")  # Python 3.8+
        print(f"  Is Alive: {current.is_alive()}")
        print(f"  Is Daemon: {current.daemon}")
        print()

    print("Main thread info:")
    show_thread_info()

    # Create named threads
    def worker():
        print(f"Worker thread info:")
        show_thread_info()

    # Method 1: Name in constructor
    t1 = threading.Thread(target=worker, name="MyCustomThread-1")

    # Method 2: Set name after creation
    t2 = threading.Thread(target=worker)
    t2.name = "MyCustomThread-2"

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    # List all active threads
    print("All active threads:")
    for thread in threading.enumerate():
        print(f"  - {thread.name} (daemon: {thread.daemon})")


# =============================================================================
# SECTION 4: DAEMON THREADS
# =============================================================================


@announce("SECTION 4: DAEMON THREADS")
def section_4_daemon_threads():
    """
    Daemon threads are background threads that automatically terminate
    when the main program exits. They're useful for background tasks
    that shouldn't prevent program exit.

    Non-daemon (default): Program waits for thread to complete
    Daemon: Program can exit while thread is still running
    """

    def background_task(name, duration):
        """Simulates a long-running background task."""
        print(f"  {name}: Starting (will take {duration}s)")
        for i in range(duration):
            print(f"  {name}: Working... ({i + 1}/{duration})")
            time.sleep(0.3)
        print(f"  {name}: Finished!")

    # Non-daemon thread (default) - Program waits for it
    print_subsection("Non-Daemon Thread (default)")
    regular_thread = threading.Thread(
        target=background_task,
        args=("Regular", 3),
        daemon=False,  # This is the default
    )
    regular_thread.start()
    regular_thread.join()  # Wait for completion

    # Daemon thread - Would be killed if program exits
    print_subsection("Daemon Thread")
    daemon_thread = threading.Thread(
        target=background_task,
        args=("Daemon", 3),
        daemon=True,  # Set as daemon
    )

    # Alternative way to set daemon
    # daemon_thread.daemon = True  # Must be set before start()

    daemon_thread.start()

    print("  Main: Waiting 1 second then continuing...")
    time.sleep(1)
    print("  Main: If this were the end of program, daemon would be killed!")

    # We'll wait for demo purposes
    daemon_thread.join()

    print("\n  Key Takeaway:")
    print("  - Use daemon=True for background tasks (logging, monitoring)")
    print("  - Use daemon=False (default) for important tasks that must complete")


# =============================================================================
# SECTION 5: THREAD JOINING AND WAITING
# =============================================================================


@announce("SECTION 5: THREAD JOINING AND WAITING")
def section_5_thread_joining():
    """
    join() blocks the calling thread until the target thread terminates.
    You can also specify a timeout.
    """

    def slow_task(seconds):
        """A task that takes some time."""
        print(f"  Task: Starting ({seconds}s task)")
        time.sleep(seconds)
        print(f"  Task: Completed!")
        return "Success"

    # Basic join - wait indefinitely
    print_subsection("Basic join()")
    t1 = threading.Thread(target=slow_task, args=(1,))
    t1.start()
    print("  Main: Waiting for thread...")
    t1.join()  # Blocks until t1 finishes
    print("  Main: Thread finished!")

    # Join with timeout
    print_subsection("join() with timeout")
    t2 = threading.Thread(target=slow_task, args=(3,))
    t2.start()

    print("  Main: Waiting max 1 second...")
    t2.join(timeout=1.0)  # Wait at most 1 second

    if t2.is_alive():
        print("  Main: Thread still running after timeout!")
        print("  Main: Waiting for completion...")
        t2.join()  # Wait for actual completion
    else:
        print("  Main: Thread finished within timeout!")

    # Joining multiple threads
    print_subsection("Joining Multiple Threads")
    threads = []
    for i in range(3):
        t = threading.Thread(target=slow_task, args=(0.5,))
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    print("  All threads completed!")


# =============================================================================
# SECTION 6: RACE CONDITIONS (THE PROBLEM)
# =============================================================================


@announce("SECTION 6: RACE CONDITIONS (THE PROBLEM)")
def section_6_race_conditions():
    """
    Race conditions occur when multiple threads access shared data
    simultaneously, leading to unpredictable results.

    THIS IS THE PROBLEM WE NEED TO SOLVE!
    """

    print("  Race condition: When threads compete to modify shared data")
    print("  Result: Unpredictable, incorrect values\n")

    # Shared variable - THE PROBLEM
    counter = 0

    def increment_counter(times):
        """Increment shared counter - NOT THREAD SAFE!"""
        nonlocal counter
        for _ in range(times):
            # This looks atomic but it's actually:
            # 1. Read counter value
            # 2. Add 1 to value
            # 3. Write new value back
            # Another thread can interrupt between any of these steps!
            current = counter
            # Simulate slight delay (makes race condition more visible)
            time.sleep(0.0001)
            counter = current + 1

    # Create multiple threads incrementing the same counter
    threads = []
    increments_per_thread = 100
    num_threads = 5

    for i in range(num_threads):
        t = threading.Thread(target=increment_counter, args=(increments_per_thread,))
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    expected = num_threads * increments_per_thread

    print(f"  Expected result: {expected}")
    print(f"  Actual result:   {counter}")
    print(f"  Lost updates:    {expected - counter}")
    print("\n  ⚠️  This is a RACE CONDITION!")
    print("  Solution: Use Locks (see next section)")


# =============================================================================
# SECTION 7: THREAD SYNCHRONIZATION - LOCK
# =============================================================================


@announce("SECTION 7: THREAD SYNCHRONIZATION - LOCK")
def section_7_lock():
    """
    A Lock (mutex) ensures only one thread can access a resource at a time.
    This solves the race condition problem.
    """

    counter = 0
    lock = threading.Lock()

    def increment_with_lock(times):
        """Thread-safe increment using Lock."""
        nonlocal counter
        for _ in range(times):
            # Method 1: Explicit acquire/release
            # lock.acquire()
            # try:
            #     counter += 1
            # finally:
            #     lock.release()  # ALWAYS release in finally!

            # Method 2: Context manager (RECOMMENDED)
            with lock:  # Automatically acquires and releases
                current = counter
                time.sleep(0.0001)  # Same delay as race condition example
                counter = current + 1

    print_subsection("Safe Counter with Lock")

    threads = []
    increments_per_thread = 100
    num_threads = 5

    for i in range(num_threads):
        t = threading.Thread(target=increment_with_lock, args=(increments_per_thread,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    expected = num_threads * increments_per_thread

    print(f"  Expected result: {expected}")
    print(f"  Actual result:   {counter}")
    print(f"  ✓ No lost updates!")

    # Lock methods
    print_subsection("Lock Methods")

    demo_lock = threading.Lock()

    # Try to acquire without blocking
    print(f"  Lock acquired: {demo_lock.acquire(blocking=False)}")  # True
    print(f"  Lock is held (locked): {demo_lock.locked()}")  # True
    print(f"  Try acquire again: {demo_lock.acquire(blocking=False)}")  # False
    demo_lock.release()
    print(f"  After release, locked: {demo_lock.locked()}")  # False

    # Acquire with timeout
    print(f"\n  Acquire with timeout:")
    demo_lock.acquire()

    def try_acquire():
        result = demo_lock.acquire(timeout=0.5)
        print(f"    Thread acquired lock: {result}")

    t = threading.Thread(target=try_acquire)
    t.start()
    t.join()
    demo_lock.release()


# =============================================================================
# SECTION 8: THREAD SYNCHRONIZATION - RLOCK (REENTRANT LOCK)
# =============================================================================


@announce("SECTION 8: THREAD SYNCHRONIZATION - RLOCK (REENTRANT LOCK)")
def section_8_rlock():
    """
    RLock (Reentrant Lock) can be acquired multiple times by the SAME thread.
    Regular Lock would cause deadlock if same thread tries to acquire twice.

    Use RLock when:
    - You have nested function calls that need the lock
    - Recursive functions that need synchronization
    """

    print_subsection("Problem with Regular Lock in Nested Calls")
    print("  If a function holding a lock calls another function")
    print("  that also needs the lock → DEADLOCK with regular Lock!\n")

    # RLock example
    print_subsection("Solution: RLock")

    rlock = threading.RLock()

    class BankAccount:
        """Bank account with nested locking needs."""

        def __init__(self, balance):
            self.balance = balance
            self.lock = threading.RLock()  # Use RLock for nested calls

        def withdraw(self, amount):
            with self.lock:
                if self.balance >= amount:
                    self.balance -= amount
                    return True
                return False

        def deposit(self, amount):
            with self.lock:
                self.balance += amount

        def transfer_to(self, other_account, amount):
            """Transfer needs to call withdraw and deposit."""
            with self.lock:  # First acquisition
                # withdraw() will acquire the SAME lock again
                # With regular Lock: DEADLOCK
                # With RLock: Works fine!
                if self.withdraw(amount):  # Second acquisition
                    other_account.deposit(amount)
                    print(f"  Transferred ${amount}")
                    return True
                print(f"  Transfer failed: insufficient funds")
                return False

    account1 = BankAccount(100)
    account2 = BankAccount(50)

    print(f"  Before: Account1=${account1.balance}, Account2=${account2.balance}")
    account1.transfer_to(account2, 30)
    print(f"  After:  Account1=${account1.balance}, Account2=${account2.balance}")

    # Show RLock can be acquired multiple times by same thread
    print_subsection("RLock Acquisition Count")

    rlock = threading.RLock()

    print("  Acquiring RLock 3 times in same thread...")
    rlock.acquire()
    print("    Acquired once")
    rlock.acquire()
    print("    Acquired twice")
    rlock.acquire()
    print("    Acquired three times")

    print("  Releasing 3 times...")
    rlock.release()
    rlock.release()
    rlock.release()
    print("  ✓ All released!")


# =============================================================================
# SECTION 9: THREAD SYNCHRONIZATION - SEMAPHORE
# =============================================================================


@announce("SECTION 9: THREAD SYNCHRONIZATION - SEMAPHORE")
def section_9_semaphore():
    """
    Semaphore allows a LIMITED number of threads to access a resource.
    Think of it as a counter that allows N threads through.

    Use cases:
    - Connection pooling
    - Rate limiting
    - Limiting concurrent access to a resource
    """

    print("  Semaphore: Allows N threads to access resource simultaneously")
    print("  Lock is like Semaphore(1)\n")

    # Simulate a connection pool with max 3 connections
    print_subsection("Connection Pool Simulation (max 3 connections)")

    # Allow max 3 concurrent connections
    connection_pool = threading.Semaphore(3)

    # BoundedSemaphore prevents releasing more than acquired
    # bounded_pool = threading.BoundedSemaphore(3)

    def access_database(thread_id):
        """Simulate database access with limited connections."""
        print(f"  Thread {thread_id}: Waiting for connection...")

        with connection_pool:  # Acquire a "connection"
            print(f"  Thread {thread_id}: ✓ Got connection! Working...")
            time.sleep(random.uniform(0.5, 1.5))  # Simulate work
            print(f"  Thread {thread_id}: Done, releasing connection")

    # Create 7 threads competing for 3 connections
    threads = []
    for i in range(7):
        t = threading.Thread(target=access_database, args=(i,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n  ✓ All threads completed using only 3 concurrent connections!")

    # BoundedSemaphore
    print_subsection("BoundedSemaphore (Safer)")
    print("  BoundedSemaphore raises error if you release too many times")
    print("  Use it to catch programming errors!\n")

    bounded = threading.BoundedSemaphore(2)
    bounded.acquire()
    bounded.acquire()
    bounded.release()
    bounded.release()

    try:
        bounded.release()  # This will raise an error!
    except ValueError as e:
        print(f"  ✓ Caught error: {e}")


# =============================================================================
# SECTION 10: THREAD SYNCHRONIZATION - EVENT
# =============================================================================


@announce("SECTION 10: THREAD SYNCHRONIZATION - EVENT")
def section_10_event():
    """
    Event is a simple signaling mechanism between threads.
    One thread signals an event, other threads wait for it.

    Methods:
    - set(): Set the internal flag to True
    - clear(): Reset the internal flag to False
    - wait(): Block until the flag is True
    - is_set(): Check if the flag is True
    """

    print("  Event: Simple thread signaling mechanism")
    print("  One thread signals, others wait for the signal\n")

    print_subsection("Server Startup Simulation")

    server_ready = threading.Event()

    def start_server():
        """Simulate server startup."""
        print("  Server: Starting up...")
        time.sleep(2)  # Startup takes time
        print("  Server: ✓ Ready to accept connections!")
        server_ready.set()  # Signal that server is ready

    def client(client_id):
        """Client that waits for server to be ready."""
        print(f"  Client {client_id}: Waiting for server...")

        # Wait for server to be ready (with optional timeout)
        is_ready = server_ready.wait(timeout=5)

        if is_ready:
            print(f"  Client {client_id}: ✓ Connected to server!")
        else:
            print(f"  Client {client_id}: ✗ Timeout waiting for server")

    # Start server thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Start multiple client threads
    client_threads = []
    for i in range(3):
        t = threading.Thread(target=client, args=(i,))
        client_threads.append(t)
        t.start()

    # Wait for all
    server_thread.join()
    for t in client_threads:
        t.join()

    # Reset example
    print_subsection("Event Reset (clear)")

    event = threading.Event()
    print(f"  Initial state - is_set(): {event.is_set()}")

    event.set()
    print(f"  After set() - is_set(): {event.is_set()}")

    event.clear()
    print(f"  After clear() - is_set(): {event.is_set()}")


# =============================================================================
# SECTION 11: THREAD SYNCHRONIZATION - CONDITION
# =============================================================================


@announce("SECTION 11: THREAD SYNCHRONIZATION - CONDITION")
def section_11_condition():
    """
    Condition allows threads to wait for a certain condition to become true.
    More flexible than Event - allows complex waiting conditions.

    Methods:
    - acquire()/release(): Lock the condition
    - wait(): Release lock and wait to be notified
    - notify(): Wake up one waiting thread
    - notify_all(): Wake up all waiting threads
    """

    print("  Condition: Wait for complex conditions to become true")
    print("  More powerful than Event for producer-consumer patterns\n")

    print_subsection("Producer-Consumer with Condition")

    buffer = []
    MAX_SIZE = 5
    condition = threading.Condition()

    def producer():
        """Produce items when buffer has space."""
        for i in range(10):
            with condition:
                # Wait while buffer is full
                while len(buffer) >= MAX_SIZE:
                    print(f"  Producer: Buffer full, waiting...")
                    condition.wait()

                # Produce item
                item = f"item-{i}"
                buffer.append(item)
                print(f"  Producer: Added {item}, buffer size: {len(buffer)}")

                # Notify consumers that item is available
                condition.notify()

            time.sleep(random.uniform(0.1, 0.3))

    def consumer(consumer_id):
        """Consume items when buffer has items."""
        consumed = 0
        while consumed < 5:  # Each consumer takes 5 items
            with condition:
                # Wait while buffer is empty
                while len(buffer) == 0:
                    print(f"  Consumer {consumer_id}: Buffer empty, waiting...")
                    condition.wait()

                # Consume item
                item = buffer.pop(0)
                consumed += 1
                print(
                    f"  Consumer {consumer_id}: Got {item}, buffer size: {len(buffer)}"
                )

                # Notify producer that space is available
                condition.notify()

            time.sleep(random.uniform(0.1, 0.4))

    # Start threads
    producer_thread = threading.Thread(target=producer)
    consumer_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(2)]

    producer_thread.start()
    for t in consumer_threads:
        t.start()

    producer_thread.join()
    for t in consumer_threads:
        t.join()

    print("\n  ✓ All items produced and consumed!")


# =============================================================================
# SECTION 12: THREAD SYNCHRONIZATION - BARRIER
# =============================================================================


@announce("SECTION 12: THREAD SYNCHRONIZATION - BARRIER")
def section_12_barrier():
    """
    Barrier blocks threads until a specified number of threads are waiting.
    Then all threads are released simultaneously.

    Use cases:
    - Parallel algorithms where threads must sync at checkpoints
    - Phased computations
    - Starting multiple threads at the same time
    """

    print("  Barrier: Sync point where threads wait for each other")
    print("  All threads must reach barrier before any can proceed\n")

    print_subsection("Race Start Simulation")

    NUM_RACERS = 5
    start_barrier = threading.Barrier(NUM_RACERS)

    def racer(name):
        """A racer that waits at the starting line."""
        print(f"  {name}: Getting ready...")
        time.sleep(random.uniform(0.5, 1.5))  # Preparation time varies

        print(f"  {name}: Ready! Waiting at start line...")

        # Wait for all racers to be ready
        start_barrier.wait()

        # All racers start at the same time!
        print(f"  {name}: GO! 🏃")

        # Race
        time.sleep(random.uniform(0.5, 1.0))
        print(f"  {name}: Finished!")

    threads = []
    for i in range(NUM_RACERS):
        t = threading.Thread(target=racer, args=(f"Racer-{i}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Barrier with action
    print_subsection("Barrier with Action Callback")

    def barrier_action():
        """Called when all threads reach barrier, before releasing."""
        print("\n  >>> All threads reached barrier! Starting countdown... <<<")
        for i in range(3, 0, -1):
            print(f"  >>> {i}...")
            time.sleep(0.3)
        print("  >>> GO! <<<\n")

    barrier_with_action = threading.Barrier(3, action=barrier_action)

    def worker(worker_id):
        print(f"  Worker {worker_id}: Approaching barrier...")
        barrier_with_action.wait()
        print(f"  Worker {worker_id}: Passed barrier!")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# =============================================================================
# SECTION 13: THREAD-LOCAL DATA
# =============================================================================


@announce("SECTION 13: THREAD-LOCAL DATA")
def section_13_thread_local():
    """
    Thread-local data is data that is unique to each thread.
    Each thread sees its own version of the variable.

    Use cases:
    - Database connections per thread
    - Request context in web apps
    - User session data
    """

    print("  Thread-local: Each thread has its own copy of the data")
    print("  No need for locks - each thread has isolated data\n")

    # Create thread-local storage
    thread_local_data = threading.local()

    def worker(worker_id):
        """Each thread sets and uses its own data."""
        # Set thread-local data
        thread_local_data.worker_id = worker_id
        thread_local_data.request_id = f"REQ-{worker_id}-{random.randint(1000, 9999)}"

        # Simulate some work
        time.sleep(random.uniform(0.1, 0.3))

        # Read thread-local data - each thread sees its OWN values
        print(f"  Thread {threading.current_thread().name}:")
        print(f"    worker_id = {thread_local_data.worker_id}")
        print(f"    request_id = {thread_local_data.request_id}")

    threads = []
    for i in range(4):
        t = threading.Thread(target=worker, args=(i,), name=f"Worker-{i}")
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Show that main thread doesn't have the data
    print(f"\n  Main thread trying to access thread-local data:")
    try:
        print(f"    worker_id = {thread_local_data.worker_id}")
    except AttributeError:
        print("    ✓ AttributeError - data doesn't exist in main thread!")


# =============================================================================
# SECTION 14: TIMER THREADS
# =============================================================================


@announce("SECTION 14: TIMER THREADS")
def section_14_timer():
    """
    Timer threads execute a function after a specified delay.
    Can be cancelled before execution.
    """

    print("  Timer: Execute function after a delay")
    print("  Can be cancelled before execution\n")

    print_subsection("Basic Timer")

    def delayed_message(message):
        print(f"  ⏰ Timer fired: {message}")

    # Create a timer (2 second delay)
    timer = threading.Timer(1.0, delayed_message, args=("Hello from the future!",))

    print("  Starting timer (1 second delay)...")
    timer.start()

    print("  Waiting for timer...")
    timer.join()  # Wait for timer to complete

    print_subsection("Cancellable Timer")

    def important_action():
        print("  ⚠️ This should NOT print if cancelled!")

    timer = threading.Timer(2.0, important_action)
    timer.start()

    print("  Timer started (2 second delay)")
    print("  Cancelling timer after 0.5 seconds...")
    time.sleep(0.5)
    timer.cancel()  # Cancel before it fires
    print("  ✓ Timer cancelled!")

    # Repeating timer (not built-in, but easy to create)
    print_subsection("Repeating Timer (Custom)")

    class RepeatingTimer:
        """A timer that repeats at a fixed interval."""

        def __init__(self, interval, function, *args, **kwargs):
            self.interval = interval
            self.function = function
            self.args = args
            self.kwargs = kwargs
            self.running = False
            self.timer = None

        def _run(self):
            if self.running:
                self.function(*self.args, **self.kwargs)
                self.timer = threading.Timer(self.interval, self._run)
                self.timer.start()

        def start(self):
            self.running = True
            self.timer = threading.Timer(self.interval, self._run)
            self.timer.start()

        def stop(self):
            self.running = False
            if self.timer:
                self.timer.cancel()

    counter = 0

    def tick():
        nonlocal counter
        counter += 1
        print(f"  Tick {counter}!")

    repeating = RepeatingTimer(0.3, tick)
    repeating.start()

    print("  Repeating timer started...")
    time.sleep(1.5)  # Let it tick a few times

    repeating.stop()
    print("  Repeating timer stopped!")


# =============================================================================
# SECTION 15: THREAD-SAFE QUEUE (PRODUCER-CONSUMER)
# =============================================================================


@announce("SECTION 15: THREAD-SAFE QUEUE (PRODUCER-CONSUMER)")
def section_15_queue():
    """
    queue.Queue is a thread-safe queue for communication between threads.
    Perfect for producer-consumer patterns.

    Types:
    - Queue: FIFO (First In, First Out)
    - LifoQueue: LIFO (Last In, First Out) - Stack
    - PriorityQueue: Items sorted by priority
    """

    print("  queue.Queue is thread-safe - no external locks needed!")
    print("  Built-in blocking for full/empty conditions\n")

    print_subsection("Producer-Consumer Pattern")

    work_queue = queue.Queue(maxsize=5)  # Max 5 items

    def producer(producer_id, num_items):
        """Produce items and put them in the queue."""
        for i in range(num_items):
            item = f"P{producer_id}-Item{i}"
            work_queue.put(item)  # Blocks if queue is full
            print(f"  Producer {producer_id}: Added {item}")
            time.sleep(random.uniform(0.1, 0.3))

        print(f"  Producer {producer_id}: Done producing")

    def consumer(consumer_id):
        """Consume items from the queue."""
        while True:
            try:
                # Block for at most 1 second
                item = work_queue.get(timeout=1.0)
                print(f"  Consumer {consumer_id}: Processing {item}")
                time.sleep(random.uniform(0.2, 0.4))
                work_queue.task_done()  # Signal that item is processed
            except queue.Empty:
                print(f"  Consumer {consumer_id}: No more items, exiting")
                break

    # Start producers
    producers = [threading.Thread(target=producer, args=(i, 3)) for i in range(2)]

    # Start consumers
    consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(2)]

    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    for p in producers:
        p.join()
    for c in consumers:
        c.join()

    # Queue methods
    print_subsection("Queue Methods")

    q = queue.Queue(maxsize=3)

    print("  Queue operations:")
    print(f"  empty(): {q.empty()}")

    q.put("a")
    q.put("b")
    print(f"  After adding 2 items, qsize(): {q.qsize()}")
    print(f"  full(): {q.full()}")

    q.put("c")
    print(f"  After adding 3rd item, full(): {q.full()}")

    # Non-blocking operations
    try:
        q.put("d", block=False)  # Would block, so raises Full
    except queue.Full:
        print("  put(block=False) raised Full exception")

    item = q.get()
    print(f"  get() returned: {item}")

    # Other queue types
    print_subsection("Queue Types")

    # LIFO Queue (Stack)
    lifo = queue.LifoQueue()
    lifo.put(1)
    lifo.put(2)
    lifo.put(3)
    print(f"  LifoQueue: {lifo.get()}, {lifo.get()}, {lifo.get()}")  # 3, 2, 1

    # Priority Queue
    pq = queue.PriorityQueue()
    pq.put((3, "low priority"))
    pq.put((1, "high priority"))
    pq.put((2, "medium priority"))
    print(f"  PriorityQueue:")
    while not pq.empty():
        print(f"    {pq.get()}")


# =============================================================================
# SECTION 16: THREAD POOL (CONCURRENT.FUTURES)
# =============================================================================


@announce("SECTION 16: THREAD POOL (CONCURRENT.FUTURES)")
def section_16_thread_pool():
    """
    ThreadPoolExecutor provides a high-level interface for thread pools.
    Manages thread creation/destruction automatically.
    """

    print("  ThreadPoolExecutor: High-level, managed thread pool")
    print("  Recommended over raw threading for most use cases\n")

    def fetch_url(url):
        """Simulate fetching a URL."""
        time.sleep(random.uniform(0.5, 1.5))
        return f"Content from {url}"

    urls = [f"https://example.com/page{i}" for i in range(5)]

    # Method 1: map()
    print_subsection("Using map() - Ordered Results")

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_url, urls))

    for url, result in zip(urls, results):
        print(f"  {url}: {result[:30]}...")

    # Method 2: submit() + as_completed()
    print_subsection("Using submit() + as_completed() - Results as They Finish")

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}

        # Process results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                print(f"  ✓ {url}: {result[:30]}...")
            except Exception as e:
                print(f"  ✗ {url}: Error - {e}")

    # Exception handling
    print_subsection("Exception Handling")

    def risky_operation(x):
        if x == 2:
            raise ValueError(f"Error processing {x}")
        return x * 10

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(risky_operation, i) for i in range(4)]

        for future in as_completed(futures):
            try:
                result = future.result()
                print(f"  Result: {result}")
            except ValueError as e:
                print(f"  Caught exception: {e}")


# =============================================================================
# SECTION 17: COMMON PITFALLS AND BEST PRACTICES
# =============================================================================


@announce("SECTION 17: COMMON PITFALLS AND BEST PRACTICES")
def section_17_best_practices():
    """
    Common pitfalls to avoid and best practices to follow.
    """

    # Pitfall 1: Forgetting to release locks
    print_subsection("Pitfall 1: Forgetting to Release Locks")
    print("""
    # ❌ BAD - Lock might not be released if exception occurs
    lock.acquire()
    do_something()  # If this raises, lock is never released!
    lock.release()
    
    # ✓ GOOD - Use context manager
    with lock:
        do_something()
    
    # ✓ GOOD - Or use try/finally
    lock.acquire()
    try:
        do_something()
    finally:
        lock.release()
    """)

    # Pitfall 2: Deadlocks
    print_subsection("Pitfall 2: Deadlocks")
    print("""
    # ❌ DEADLOCK - Thread 1 and Thread 2 wait for each other
    # Thread 1:
    lock_a.acquire()
    lock_b.acquire()  # Waiting for Thread 2 to release
    
    # Thread 2:
    lock_b.acquire()
    lock_a.acquire()  # Waiting for Thread 1 to release
    
    # ✓ SOLUTION - Always acquire locks in the same order
    # Both threads: lock_a first, then lock_b
    """)

    # Pitfall 3: Race condition with check-then-act
    print_subsection("Pitfall 3: Check-Then-Act Race Condition")
    print("""
    # ❌ BAD - Race condition between check and action
    if not queue.empty():
        item = queue.get()  # Another thread might get it first!
    
    # ✓ GOOD - Use exception handling or blocking
    try:
        item = queue.get(block=False)
    except queue.Empty:
        pass
    """)

    # Best practices summary
    print_subsection("Best Practices Summary")
    print("""
    1. Use `with` statement for locks (context managers)
    
    2. Prefer `ThreadPoolExecutor` over raw `threading` for most cases
    
    3. Use `queue.Queue` for thread communication
    
    4. Use `Event` for simple signaling between threads
    
    5. Keep critical sections (locked code) as short as possible
    
    6. Avoid shared mutable state when possible
    
    7. Use `threading.local()` for thread-specific data
    
    8. Remember: threading is for I/O-bound tasks
       Use multiprocessing for CPU-bound tasks (GIL limitation)
    
    9. Always handle exceptions in threads
    
    10. Use timeouts to prevent indefinite blocking:
        - lock.acquire(timeout=5)
        - queue.get(timeout=5)
        - event.wait(timeout=5)
    """)

    # GIL reminder
    print_subsection("Remember: The GIL")
    print("""
    Python has a Global Interpreter Lock (GIL).
    This means:
    
    ✓ Threading works great for I/O-bound tasks:
      - Network requests
      - File operations
      - Database queries
      - User input
    
    ✗ Threading does NOT speed up CPU-bound tasks:
      - Mathematical computations
      - Image processing
      - Data crunching
    
    For CPU-bound tasks, use:
      - multiprocessing
      - ProcessPoolExecutor
      - Or libraries like NumPy that release the GIL
    """)


# =============================================================================
# MAIN - RUN ALL SECTIONS
# =============================================================================


def main():
    """Run all tutorial sections."""
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║              PYTHON THREADING COMPLETE TUTORIAL                      ║
    ║                                                                      ║
    ║  This tutorial covers all important aspects of Python threading.    ║
    ║  Each section builds on the previous one.                           ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    sections = [
        ("Basic Thread Creation", section_1_basic_thread_creation),
        ("Creating Threads with Classes", section_2_thread_classes),
        ("Thread Naming and Identification", section_3_thread_naming),
        ("Daemon Threads", section_4_daemon_threads),
        ("Thread Joining and Waiting", section_5_thread_joining),
        ("Race Conditions (The Problem)", section_6_race_conditions),
        ("Thread Synchronization - Lock", section_7_lock),
        ("Thread Synchronization - RLock", section_8_rlock),
        ("Thread Synchronization - Semaphore", section_9_semaphore),
        ("Thread Synchronization - Event", section_10_event),
        ("Thread Synchronization - Condition", section_11_condition),
        ("Thread Synchronization - Barrier", section_12_barrier),
        ("Thread-Local Data", section_13_thread_local),
        ("Timer Threads", section_14_timer),
        ("Thread-Safe Queue", section_15_queue),
        ("Thread Pool (concurrent.futures)", section_16_thread_pool),
        ("Best Practices", section_17_best_practices),
    ]

    print("  Available sections:")
    for i, (name, _) in enumerate(sections, 1):
        print(f"    {i}. {name}")

    print("\n  Options:")
    print("    - Enter section number (1-17) to run specific section")
    print("    - Enter 'all' to run all sections")
    print("    - Enter 'q' to quit\n")

    while True:
        choice = input("  Your choice: ").strip().lower()

        if choice == "q":
            print("\n  Thanks for learning Python threading! 👋\n")
            break
        elif choice == "all":
            for name, func in sections:
                func()
                print("\n  Press Enter to continue...")
                input()
            print("\n  🎉 Tutorial complete!")
            break
        else:
            try:
                section_num = int(choice)
                if 1 <= section_num <= len(sections):
                    sections[section_num - 1][1]()
                else:
                    print(f"  Please enter a number between 1 and {len(sections)}")
            except ValueError:
                print("  Invalid input. Enter a number, 'all', or 'q'")


if __name__ == "__main__":
    # main1()
    main()
