from __future__ import annotations
from contextlib import contextmanager
import threading
import time
import random
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, override


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)
    print(" ")


def print_subsection(title, l: int = 100):
    n = len(title)
    hash_len = (l - n - 2) // 2
    print(f"\n{'-' * hash_len} {title} {'-' * hash_len}\n")


def announce(msg: str):
    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


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
# SECTION 1: BASIC THREAD CREATION (Start & Join)
# =============================================================================


@announce("SECTION 1: BASIC THREAD CREATION (Start & Join)")
def section_1_basic_thread_creation():
    """
    The simplest way to create a thread is using threading.Thread()
    with a target function.
    """

    # Simple function to run in a thread
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
    print(f"Active threads: {threading.active_count()}")

    print(
        "[Main] Note: If this was sequential, it would take 4 seconds. "
        "But Because it's threaded, it takes ~2 seconds."
    )


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

        @override
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
        WorkerThread(worker_id=1, iterations=6),
        WorkerThread(worker_id=2, iterations=5),
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
        print(f"   Name: {current.name}")
        print(f"   ID: {current.ident}")
        print(f"   Native ID: {current.native_id}")  # Python 3.8+
        print(f"   Is Alive: {current.is_alive()}")
        print(f"   Is Daemon: {current.daemon}")
        print()

    print("Main thread info:")
    show_thread_info()

    # Create named threads
    def worker():
        print("Worker thread info:")
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
        print(f"  [{name}]: Starting (will take {duration}s)")
        for i in range(duration):
            print(f"  [{name}]: Working... ({i + 1}/{duration})")
            time.sleep(1)
        print(f"  [{name}]: Finished!")

    # Non-daemon thread (default) - Program waits for it
    print_subsection("Non-Daemon Thread (default)")
    regular_thread = threading.Thread(
        target=background_task,
        args=("Regular", 3),
        daemon=False,  # This is the default
    )
    # Alternative way to set daemon
    # daemon_thread.daemon = True  # Must be set before start()

    regular_thread.start()
    regular_thread.join()  # Wait for completion

    # Daemon thread - Would be killed if program exits
    print_subsection("Daemon Thread")
    daemon_thread = threading.Thread(
        target=background_task,
        args=("Daemon", 3),
        daemon=True,  # Set as daemon
    )

    daemon_thread.start()

    print("  [FUNC]: Waiting 1 second then continuing...")
    time.sleep(1)
    print("  [FUNC]: If this were the end of main program, daemon would be killed!")
    print(
        "  [FUNC]: But here it will continue as I have written it in a function, "
        "so the function will end but main thread will still be running other functions..."
    )
    print(
        "  [FUNC]: If it were the last function the main is calling and after this, main is exiting, then daemon would be killed. "
        "You can try editing program for this to observe the result"
    )

    # We'll wait for demo purposes, so that print statements don't mix up
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
        print(
            f"  [{threading.current_thread().name}]: Task: Starting (this will take {seconds} seconds...)"
        )
        time.sleep(seconds)
        print(f"  [{threading.current_thread().name}]: Task: Completed!")
        return f"[{threading.current_thread().name}]: Success"

    # Basic join - wait indefinitely
    print_subsection("Basic join()")
    t1_name = "Thread-1"
    t1 = threading.Thread(target=slow_task, args=(1,), name=t1_name)
    t1.start()
    print(f"  [Main]: Waiting for {t1_name} to finish...")
    t1.join()  # Blocks until t1 finishes
    print(f"  [Main]: {t1_name} finished!")

    # Join with timeout
    print_subsection("join() with timeout")
    thread_list = []
    for i in range(1, 3):
        thread_list.append(
            threading.Thread(
                target=slow_task, args=(i * i - 0.2,), name=f"Thread-{i + 1}"
            )
        )  # threads-2,3

    for t in thread_list:
        t.start()

    for t in thread_list:
        print(f"  [Main]: Waiting for {t.name} to finish within max 1 seconds...")
        t.join(
            timeout=1
        )  # Wait at most 1 second, then just unblocks (but doesn't kill)

        if t.is_alive():
            print(f"  [Main]: {t.name} unblocked after 1 second (not killed)!")
            print(f"  [Main]: {t.name} still running even after 1 second!")
            print(f"  [Main]: Now let {t.name} complete...")
        else:
            print(f"  [Main]: {t.name} finished within timeout!")

    for t in thread_list:
        t.join()  # Wait for actual completion


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

    # -------------------------------------- Safe Counter with Lock --------------------------------------
    print_subsection("Safe Counter with Lock")

    threads_list = []
    increments_per_thread = 100
    num_threads = 5

    for i in range(num_threads):
        t = threading.Thread(target=increment_with_lock, args=(increments_per_thread,))
        threads_list.append(t)

    for t in threads_list:
        t.start()

    for t in threads_list:
        t.join()

    expected = num_threads * increments_per_thread

    print(f"  Expected result: {expected}")
    print(f"  Actual result:   {counter}")
    print("  ✓ No lost updates!")

    # --------------------------- manually Lock/unlock and Non-Blocking locks ---------------------------
    # Lock methods
    print_subsection("manually Lock/unlock and Non-Blocking locks")

    demo_lock = threading.Lock()

    # Try to acquire without blocking
    print(f"  Lock acquired: {demo_lock.acquire(blocking=False)}")
    # True (bcz lock was available)

    print(f"  Lock is held (locked): {demo_lock.locked()}")  # True

    print(f"  Try acquire again: {demo_lock.acquire(blocking=False)}")
    # False (bcz lock not available, returned false without waiting)

    demo_lock.release()
    print(f"  After release, locked: {demo_lock.locked()}")  # False

    # ----------------------------- Non-Blocking lock using context manager -----------------------------
    print_subsection("Non-Blocking lock using context manager")

    @contextmanager
    def non_blocking_lock(lock: threading.Lock):
        acquired = lock.acquire(blocking=False)
        print(f"  lock.acquire(blocking=False) returned: {acquired}")
        try:
            if acquired:
                print(f"  After acquiring,lock.locked(): {lock.locked()}")  # True
                yield  # Lock acquired, proceed
            else:
                print("  Lock not acquired, skipping block")
        finally:
            if acquired:
                lock.release()
                print(f"  After release, lock.locked(): {lock.locked()}")  # False

    # Usage
    with non_blocking_lock(demo_lock):
        print("  Inside the block (That means non-blocking lock has been acquired)")
        # This runs only if the lock was acquired

    # --------------------------------------- Acquire with timeout ---------------------------------------
    print_subsection("Acquire with timeout")
    with demo_lock:

        def try_acquire():
            result = demo_lock.acquire(timeout=0.5)
            print(f"    Thread acquired lock: {result}")
            # False (since already acquired, hence crossed the timeout and returned False)

        t = threading.Thread(target=try_acquire)
        t.start()
        t.join()


# =============================================================================
# SECTION 8: THREAD SYNCHRONIZATION - RLOCK (REENTRANT LOCK)
# =============================================================================


@announce("SECTION 8: THREAD SYNCHRONIZATION - RLOCK (REENTRANT LOCK)")
def section_8_rlock():
    """
    RLock (Reentrant Lock) can be acquired multiple times by the SAME thread.
    Regular Lock would cause deadlock if same thread tries to acquire twice.

    Internally, an RLock tracks two things:
        The Owner: The ID of the thread that currently holds the lock.
        The Recursion Level: A counter indicating how many times the owner has acquired the lock.

    Use RLock when:
        - nested function calls that need the lock
        - Recursive functions that need synchronization
    """

    print_subsection("Problem with Regular Lock in Nested Calls")
    print(
        "  A function holding a regular lock calls another function "
        "that also needs the same lock → DEADLOCK!\n"
    )

    # RLock example
    print_subsection("Solution: threading.RLock")

    # rlock = threading.RLock()

    class BankAccount:
        """Bank account with nested locking needs."""

        def __init__(self, balance):
            self.balance = balance
            self.rlock = threading.RLock()  # Use RLock for nested calls

        def withdraw(self, amount):
            with self.rlock:
                if self.balance >= amount:
                    self.balance -= amount
                    return True
                return False

        def deposit(self, amount):
            with self.rlock:
                self.balance += amount

        def transfer_to(self, other_account: BankAccount, amount):
            """Transfer needs to call withdraw and deposit."""
            with self.rlock:  # First acquisition
                # withdraw() will acquire the SAME lock again
                # With regular Lock: DEADLOCK
                # With RLock: Works fine!
                if self.withdraw(amount):  # Second acquisition
                    other_account.deposit(amount)
                    print(f"  Transferred ${amount}")
                    return True
                print("  Transfer failed: insufficient funds")
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

    print("  Has to Release 3 times...")
    rlock.release()
    print("    1st release")
    rlock.release()
    print("    2nd release")
    rlock.release()
    print("    3rd release")
    print("  ✓ All released!")

    print_subsection("Methods to acquire Rlocks")

    print("  Method 1: acquire() and release()")
    rlock.acquire()
    # ... critical section ...
    rlock.release()

    print("  Method 2: Context manager (recommended)")
    with rlock:
        # ... critical section ...
        pass

    print("  Method 3: Non-blocking acquire")
    if rlock.acquire(blocking=False):
        try:
            # ... critical section ...
            pass
        finally:
            rlock.release()
    else:
        print("    Could not acquire lock")

    print("  Method 4: Timeout")
    if rlock.acquire(timeout=5.0):
        try:
            # ... critical section ...
            pass
        finally:
            rlock.release()

    print_subsection("Multiple Threads Example: Counter with RLock")

    # Counter with RLock
    class Counter:
        def __init__(self):
            self._rlock = threading.RLock()
            self._value = 0

        def increment(self):
            with self._rlock:
                self._value += 1

        def add(self, n):
            with self._rlock:  # Lock acquired here
                for i in range(n):
                    self.increment()
                    if i == 50:
                        print(f"Thread A: halfway done, value = {self._value}")
                        time.sleep(0.1)  # Simulate slow operation
                # Lock released here (when exiting 'with' block)

        @property
        def value(self):
            with self._rlock:
                return self._value

    common_counter = Counter()

    def add_100():
        print(f"[{threading.current_thread().name}]: Starting add(100)")
        common_counter.add(100)
        print(f"[{threading.current_thread().name}]: Finished add(100)")

    def read_value():
        time.sleep(0.05)  # Start slightly after A
        print(f"[{threading.current_thread().name}]: Trying to read value...")
        val = common_counter.value  # Will BLOCK until A is done!
        print(f"[{threading.current_thread().name}]: Got value = {val}")

    t1 = threading.Thread(target=add_100, name="WRITER-THREAD")
    t2 = threading.Thread(target=read_value, name="READER-THREAD")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(
        "=>  Reader will never get an intermidiate value\n"
        "=>  because lock will never allow Reader to acquire while it is acquired by Writer,\n"
        "=>  RLock allows re-entry only for the SAME thread. Other threads must still wait!"
    )


# =============================================================================
# SECTION 9: THREAD SYNCHRONIZATION - SEMAPHORE
# =============================================================================


@announce("SECTION 9: THREAD SYNCHRONIZATION - SEMAPHORE - [threading.Semaphore(n)]")
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
    mutex = threading.Lock()
    # I'll use it just to see how many conenction has been acquired

    # BoundedSemaphore prevents releasing more than acquired
    # bounded_pool = threading.BoundedSemaphore(3)

    def access_database(thread_id):
        """Simulate database access with limited connections."""
        print(f"  Thread {thread_id}: Waiting for connection...")

        with connection_pool:  # Acquire a "connection"
            with mutex:
                print(
                    f"  Thread {thread_id}: ✓ Got connection! Working..."
                    f"{connection_pool._value} more connections available..."
                )
            time.sleep(random.uniform(0.5, 1.5))  # Simulate work
            print(f"  Thread {thread_id}: Done, releasing connection")

        with mutex:
            print(
                f"  Thread {thread_id}: after releasing..."
                f"Now {connection_pool._value} connections available..."
            )

    print(f"At start {connection_pool._value} connections available...")
    # Create 7 threads competing for 3 connections
    threads: List[threading.Thread] = []
    for i in range(7):
        t = threading.Thread(target=access_database, args=(i,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n  ✓ All threads completed using only 3 concurrent connections!")

    # Simulate a connection pool with max 3 connections- Class Version
    print_subsection("Connection Pool Simulation (max 3 connections) - Class version")

    class ConnectionPool:
        def __init__(self):
            self._connection_pool = threading.Semaphore(3)
            self._mutex = threading.Lock()

        def _acquire_connection(self):
            print(f"  {threading.current_thread().name}: Waiting for connection...")
            self._connection_pool.acquire()
            with self._mutex:
                print(
                    f"  {threading.current_thread().name}: ✓ Got connection! Working..."
                    f"{self._connection_pool._value} more connections available..."
                )

        def release_connection(self):
            print(f"  {threading.current_thread().name}: Done, releasing connection")
            self._connection_pool.release()
            with mutex:
                print(
                    f"  {threading.current_thread().name}: after releasing..."
                    f"Now {self._connection_pool._value} connections available..."
                )

        def access_database(self):
            """Simulate database access with limited connections."""

            self._acquire_connection()
            time.sleep(random.uniform(0.5, 1.5))  # Simulate work
            self.release_connection()

    # Allow max 3 concurrent connections
    connection_pool_obj = ConnectionPool()

    print(
        f"At start {connection_pool_obj._connection_pool._value} connections available..."
    )
    # Create 7 threads competing for 3 connections
    threads: List[threading.Thread] = []
    for i in range(7):
        t = threading.Thread(
            target=connection_pool_obj.access_database, name=f"Thread {i}"
        )
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
        print("SHOCKKKKING!!!! It Shouldn't have happened...")
    except ValueError as e:
        print(f"  ✓ Caught error [as expected]: {e}")


# =============================================================================
# SECTION 10: THREAD SYNCHRONIZATION - EVENT
# =============================================================================


@announce("SECTION 10: THREAD SYNCHRONIZATION - EVENT - [threading.Event()]")
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
        print(
            f"  [{threading.current_thread().name}]: Starting up...(will take 3 seconds)"
        )
        time.sleep(3)  # Startup takes time
        print(f"  [{threading.current_thread().name}]: ✓ Ready to accept connections!")
        server_ready.set()  # Signal that server is ready

    def client(timeout: int):
        """Client that waits for server to be ready."""
        print(
            f"  [{threading.current_thread().name}]: Waiting for server...(timeout={timeout} seconds)"
        )

        # Wait for server to be ready (with optional timeout)
        is_ready = server_ready.wait(timeout=timeout)

        if is_ready:
            print(f"  [{threading.current_thread().name}]: ✓ Connected to server!")
        else:
            print(
                f"  [{threading.current_thread().name}]: ✗ Timeout waiting for server"
            )

    all_threads: List[threading.Thread] = []

    # server thread
    all_threads.append(threading.Thread(target=start_server, name="Server"))

    # multiple client threads
    for i in range(3):
        t = threading.Thread(
            target=client, args=(i + 2,), name=f"Client-with-timeout-{i + 2}"
        )
        all_threads.append(t)

    for t in all_threads:
        t.start()

    for t in all_threads:
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


@announce("SECTION 11: THREAD SYNCHRONIZATION - CONDITION - [threading.Condition()]")
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
    MAX_SIZE = 1

    producer_count, each_produces = 9, 2  # total 24
    consumer_count, each_consumes = 1, 18  # total 24

    _item_id = 1
    mutex = threading.Lock()
    condition = threading.Condition()

    def producer():
        """Produce items when buffer has space."""
        nonlocal _item_id
        curr_thread_name = threading.current_thread().name
        for i in range(each_produces):
            print(f"  [{curr_thread_name}]({i}): waiting for lock...")
            with condition:
                # Wait while buffer is full
                while len(buffer) >= MAX_SIZE:
                    print(f"  [{curr_thread_name}]({i}): Buffer full, waiting...")
                    condition.wait()
                    print(f"  [{curr_thread_name}]({i}): is notified!")

                # Produce item
                with mutex:
                    item = f"item-{_item_id}"
                    _item_id += 1
                buffer.append(item)
                print(
                    f"  [{curr_thread_name}]({i}): produced {item}, buffer size: {len(buffer)}"
                )

                # Notify consumers that item is available
                print(f"  [{curr_thread_name}]({i}): Notifying One Consumer...")
                condition.notify()

            time.sleep(random.uniform(0.1, 0.3))

    def consumer():
        """Consume items when buffer has items."""
        i = 0
        curr_thread_name = threading.current_thread().name
        while i < each_consumes:
            print(f"  [{curr_thread_name}]({i}): waiting for lock...")
            with condition:
                # Wait while buffer is empty
                while len(buffer) == 0:
                    print(f"  [{curr_thread_name}]({i}): Buffer empty, waiting...")
                    condition.wait()
                    print(f"  [{curr_thread_name}]({i}): is notified!")

                # Consume item
                item = buffer.pop(0)
                i += 1
                print(
                    f"  [{curr_thread_name}]({i}): consumed {item}, buffer size: {len(buffer)}"
                )

                # Notify producer that space is available
                print(f"  [{curr_thread_name}]({i}): Notifying One Producer...")
                condition.notify()

            time.sleep(random.uniform(0.1, 0.4))

    # Start threads
    producer_threads = [
        threading.Thread(target=producer, name=f"Producer-{i + 1}")
        for i in range(producer_count)
    ]
    consumer_threads = [
        threading.Thread(target=consumer, name=f"Consumer-{i + 1}")
        for i in range(consumer_count)
    ]

    for t in consumer_threads + producer_threads:
        t.start()

    for t in consumer_threads + producer_threads:
        t.join()

    print("\n  ✓ All items produced and consumed!")

    print_subsection("Producer-Consumer with Event- [Better with separate conditions]")

    buffer = []
    MAX_SIZE = 1

    producer_count, each_produces = 9, 2  # total 24
    consumer_count, each_consumes = 1, 18  # total 24

    _item_id = 1
    mutex = threading.Lock()

    _common_mutex = threading.Lock()
    not_full = threading.Condition(_common_mutex)
    not_empty = threading.Condition(_common_mutex)

    # Had to pass a common lock/mutex here bcz:
    #   1. otherwise each condition will use its own internal lock
    #       and then one condition won't be able to call other's notify method
    #       bcz Can't call notify() on a condition whose lock you don't hold
    #   2. both the Producer and the Consumer need to modify the exact same resource (the buffer list).
    def producer():
        """Produce items when buffer has space."""
        nonlocal _item_id
        curr_thread_name = threading.current_thread().name

        for i in range(each_produces):
            print(f"  [{curr_thread_name}]({i}): waiting for lock...")
            with not_full:
                # Wait while buffer is full
                while len(buffer) >= MAX_SIZE:
                    print(f"  [{curr_thread_name}]({i}): Buffer full, waiting...")
                    not_full.wait()
                    print(f"  [{curr_thread_name}]({i}): is notified!")

                # Produce item
                with mutex:
                    item = f"item-{_item_id}"
                    _item_id += 1
                buffer.append(item)
                print(
                    f"  [{curr_thread_name}]({i}): produced {item}, buffer size: {len(buffer)}"
                )

                # Notify consumers that item is available
                print(f"  [{curr_thread_name}]({i}): Notifying One Consumer...")
                not_empty.notify()  # not empty is guarranteed bcz produced one just now

            time.sleep(random.uniform(0.1, 0.3))

    def consumer():
        """Consume items when buffer has items."""
        i = 0
        curr_thread_name = threading.current_thread().name
        while i < each_consumes:
            print(f"  [{curr_thread_name}]({i}): waiting for lock...")
            with not_empty:
                # Wait while buffer is empty
                while len(buffer) == 0:
                    print(f"  [{curr_thread_name}]({i}): Buffer empty, waiting...")
                    not_empty.wait()
                    print(f"  [{curr_thread_name}]({i}): is notified!")

                # Consume item
                item = buffer.pop(0)
                i += 1
                print(
                    f"  [{curr_thread_name}]({i}): consumed {item}, buffer size: {len(buffer)}"
                )

                # Notify producer that space is available
                print(f"  [{curr_thread_name}]({i}): Notifying One Producer...")
                not_full.notify()  # not full is guarranteed bcz consumed one just now

            time.sleep(random.uniform(0.1, 0.4))

    # Start threads

    producer_threads = [
        threading.Thread(target=producer, name=f"Producer-{i + 1}")
        for i in range(producer_count)
    ]
    consumer_threads = [
        threading.Thread(target=consumer, name=f"Consumer-{i + 1}")
        for i in range(consumer_count)
    ]

    for t in consumer_threads + producer_threads:
        t.start()

    for t in consumer_threads + producer_threads:
        t.join()

    print("\n  ✓ All items produced and consumed!")


# =============================================================================
# SECTION 12: THREAD SYNCHRONIZATION - BARRIER
# =============================================================================


@announce("SECTION 12: THREAD SYNCHRONIZATION - BARRIER - [threading.Barrier(n)]")
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
        print(f"  {name}: Getting ready for the race...")
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
        # Called when all threads reach barrier, before releasing.
        print("\n  >>> All threads reached barrier! Starting countdown... <<<")
        for i in range(3, 0, -1):
            print(f"  >>> {i} <<<", end="\r")
            time.sleep(1)
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


@announce("SECTION 13: THREAD-LOCAL DATA - [threading.local()]")
def section_13_thread_local():
    """
    Thread-local data is data that is unique to each thread.
    Each thread sees its own version of the variable.

    Use cases:
    - Database connections per thread
    - Request context in web apps
    - User session data

    extremely common in Web Frameworks (like Flask or Django).
        - Imagine a web server handling 100 requests at the same time using threads.
          You want to access the "current user" or the "current database connection."
        - Instead of passing the user object into every single function as an argument (func(user, db, data)),
          you can store it in threading.local().
            - Request A (Thread A) sets local.user = "Alice"
            - Request B (Thread B) sets local.user = "Bob"
        - Now, any function running inside Thread A can just ask local.user and get "Alice,"
          without worrying about "Bob" overwriting it.
    """

    print("  Thread-local: Each thread has its own copy of the data")
    print("  No need for locks - each thread has isolated data\n")

    # Create thread-local storage ==> a single object that secretly holds separate data for each thread.
    # acts like a smart dict that automatically uses the Current Thread ID as a key.
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
    print("\n  Main thread trying to access thread-local data:")
    try:
        print(f"    worker_id = {thread_local_data.worker_id}")
    except AttributeError:
        print("    ✓ AttributeError - data doesn't exist in main thread!")


# =============================================================================
# SECTION 14: TIMER THREADS
# =============================================================================


@announce(
    "SECTION 14: TIMER THREADS - [threading.Timer(interval, function, args, kwargs)]"
)
def section_14_timer():
    """
    Timer threads execute a function after a specified delay.
    Can be cancelled before execution.
    """

    print("  Timer: Execute function after a delay")
    print("  Can be cancelled before execution\n")

    print_subsection("Basic Timer")

    def delayed_message(message):
        print(f"  [{time.time()}]: ⏰ Timer fired: {message}")

    # Create a timer (2 second delay)
    timer = threading.Timer(1.0, delayed_message, args=("Hello from the future!",))

    print(f"  [{time.time()}]: Starting timer (1 second delay)...")
    timer.start()

    print(f"  [{time.time()}]: Waiting for timer...")
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

        def _run(self):  # runs the function once and then schedule next run
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
        print(f"  [{threading.current_thread().name}]: Tick {counter}!")

    repeating = RepeatingTimer(0.3, tick)
    repeating.start()

    print("  Repeating timer started...")
    time.sleep(2.5)  # Let it tick for sometime

    repeating.stop()
    print("  Repeating timer stopped!")


# =============================================================================
# SECTION 15: THREAD-SAFE QUEUE (PRODUCER-CONSUMER)
# =============================================================================


@announce(
    "SECTION 15: THREAD-SAFE QUEUE (PRODUCER-CONSUMER) - [queue.Queue(maxsize=0)]"
)
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

    work_queue = queue.Queue(maxsize=5)
    # Max 5 items ==> .put(), blocks if full

    def producer(producer_id, num_items):
        """Produce items and put them in the queue."""
        for i in range(1, num_items + 1):
            item = f"P{producer_id}-Item{i}"
            work_queue.put(item)  # Blocks if queue is full
            print(f"  Producer {producer_id}: produced {item}")
            time.sleep(random.uniform(0.1, 0.3))

        print(f"  Producer {producer_id}: Done producing")

    def consumer(consumer_id):
        """Consume items from the queue."""
        tab = "\t\t\t\t"
        while True:
            try:
                # Block for at most 1 second
                item = work_queue.get(timeout=1.0)
                print(f"  {tab}Consumer {consumer_id}: consuming {item}")
                time.sleep(random.uniform(0.2, 0.4))
                work_queue.task_done()
                # A Signal to queue that the item has been processed
                # It will simply DOWN the counter (-1)
            except queue.Empty:
                print(f"  {tab}Consumer {consumer_id}: No more items in queue, exiting")
                break

    # 2 producers, each producing 3 items
    producers = [threading.Thread(target=producer, args=(i, 20)) for i in range(2)]

    # 2 consumers
    consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(2)]

    for t in producers + consumers:
        t.start()

    for t in producers + consumers:
        t.join()

    # Queue methods
    print_subsection("Queue - [queue.Queue(maxsize=0)]")
    """
    Inside queue.Queue, there is a hidden counter called unfinished_tasks.
        [1] q.put(item): counter goes UP (+1).
        [2] q.get(): 
                - You take the item, but the counter still the same. 
                - The Queue knows you have the item, 
                  but it doesn't know if you've finished working on it.
        [3] q.task_done(): counter goes DOWN (-1).
        [4] q.join(): 
                - This method blocks (freezes) the main thread until that counter hits 0.
    
    """

    q = queue.Queue(maxsize=3)
    print("  a queue.Queue with maxsize=3 initialized")

    try:
        x = q.get(block=True, timeout=0.5)  # Would block, so raises Full
    except queue.Empty:
        print("  q.get(block=True, timeout=0.5) raised queue.Empty exception")

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
        print("  q.put(block=False) raised queue.Full exception")

    item = q.get()
    print(f"  get() returned: {item}")

    # Other queue types
    print_subsection("Stack - [queue.LifoQueue(maxsize=0)]")

    # LIFO Queue (Stack)
    lifo = queue.LifoQueue()
    lifo.put(1)
    lifo.put(2)
    lifo.put(3)

    print("  put 1, 2, 3")
    print(f"  LifoQueue: {lifo.get()}, {lifo.get()}, {lifo.get()}")  # 3, 2, 1

    print_subsection("Priority Queue - [queue.PriorityQueue(maxsize=0)]")
    # Priority Queue
    pq = queue.PriorityQueue()
    # Just like a min heap, gives a minimum item first

    pq.put((3, "low priority"))
    pq.put((1, "high priority"))
    pq.put((2, "medium priority"))
    print("  PriorityQueue:")

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
        return f"[{threading.current_thread().name}] Data from {url}"

    urls = [
        "google.com",
        "facebook.com",
        "yahoo.com",
        "bing.com",
        "duckduckgo.com",
        "github.com",
    ]

    # Method 1: map()
    print_subsection("Using map() - Ordered Results")

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_url, urls))

    for url, result in zip(urls, results):
        print(f"  {url}: {result}...")

    # Method 2: submit() + as_completed()
    print_subsection("Using submit() + as_completed() - Results as They Finish")

    # below is the gold-standard pattern for fast, responsive concurrent downloads in Python.
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        # Maps each running Future back to its original URL.

        # Process results as they complete
        for future in as_completed(future_to_url):
            # Yields futures the instant they finish (fast URLs appear first).

            url = future_to_url[future]
            # Instantly know which URL just completed.
            try:
                result = future.result()
                # Get the result (or raise exception if failed).
                print(f"  ✓ {url}: {result}...")
            except Exception as e:
                print(f"  ✗ {url}: Error - {e}")

    # Exception handling
    print_subsection("Exception Handling")

    def fetch_url(url):
        """Simulate fetching a URL."""
        time.sleep(random.uniform(0.5, 1.5))
        if "facebook" in url:
            raise ValueError(
                f"[{threading.current_thread().name}]: Error processing {url}"
            )
        return f"[{threading.current_thread().name}] Data from {url}"

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                print(f"  ✓ {url}: {result}...")
            except ValueError as e:
                print(f"  ✗ {url}: Error - {e}")


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
    
    ✓ SOLUTION - 
        Always acquire locks in the same order  =>  first lock_a, then lock_b
        And release in the opposite order       =>  first lock_b, then lock_a
    """)

    # Pitfall 3: Race condition with check-then-act
    print_subsection("Pitfall 3: Check-Then-Act Race Condition")
    print("""
    # ❌ BAD - Race condition between check and action
    if not queue.empty():
        item = queue.get()  # ← BAD! Two-step race
                            # Another thread might sneak in and get it first!
    
    # ✓ GOOD - Use exception handling or blocking
    try:
        item = queue.get(block=False)   # ← GOOD! One atomic operation
        # If something is there → you get it. 
        # If not → immediate Empty exception.
        # Hence No race possible
    except queue.Empty:
        pass
    
    """)

    # Best practices summary
    print_subsection("Best Practices Summary")
    print("""
    1. Use `with` statement for locks (context managers)
    
    2. Prefer `concurrent.futures.ThreadPoolExecutor` over raw `threading` for most cases
    
    3. Use `queue.Queue` for thread communication
    
    4. Use `threading.Event()` for simple signaling between threads
    
    5. Keep critical sections (locked code) as short as possible
    
    6. Avoid shared mutable state when possible
    
    7. Use `threading.local()` for thread-specific data
    
    8. Always handle exceptions in threads
    
    9. Use timeouts to prevent indefinite blocking:
        - lock.acquire(timeout=5)
        - queue.get(timeout=5)
        - event.wait(timeout=5)
    """)

    # GIL reminder
    print_subsection("Remember: The GIL")
    print("""
    Python has a Global Interpreter Lock (GIL) → only one thread can run Python code at a time.
        
    This means:
    
    [✓] Threading  (or asyncio) works great for I/O-bound tasks (Waiting tasks):
        - Network requests
        - File operations
        - Disk I/O
        - API calls
        - Sleep
        - Database queries
        - User input
        - Downloading files
        - Reading/writing files
    
    [✗] Threading does NOT speed up CPU-bound tasks (Heavy Calculation tasks):
        - Mathematical computations
        - Image processing
        - Data crunching
        - Machine learning
        - Data analysis
    
        For CPU-bound tasks, use:
        - multiprocessing
        - ProcessPoolExecutor
        - Or libraries like NumPy that release the GIL
          
    # ╔══════════════════╦══════════════════╦═════════╦══════════════════════════════╗
    # ║ Task Type        ║ Example          ║ Choice  ║ Why                          ║
    # ╠══════════════════╬══════════════════╬═════════╬══════════════════════════════╣
    # ║ Download URLs    ║ requests.get(),  ║ Thread  ║ Wait for Net -> GIL releases ║
    # ║                  ║ aiohttp          ║         ║ -> threads fly!              ║
    # ╠══════════════════╬══════════════════╬═════════╬══════════════════════════════╣
    # ║ Resize Images    ║ Pillow, OpenCV   ║ Multi-  ║ CPU work -> GIL blocks       ║
    # ║                  ║ loops            ║ Proc    ║ threads -> 1 core used       ║
    # ║                  ║                  ║         ║ → slow!                      ║
    # ╠══════════════════╬══════════════════╬═════════╬══════════════════════════════╣
    # ║ Fetch API +      ║ Network + light  ║ Thread  ║ 95% waiting -> threading     ║
    # ║ Parse JSON       ║ JSON parse       ║         ║ wins easily.                 ║
    # ╠══════════════════╬══════════════════╬═════════╬══════════════════════════════╣
    # ║ ML Model Train,  ║ Pure CPU/Math    ║ Multi-  ║ Bypasses GIL -> uses all     ║
    # ║ Encrypt files,   ║                  ║ Proc    ║ CPU cores (4-8x faster).     ║
    # ║ Video Encoding   ║                  ║         ║                              ║
    # ╠══════════════════╬══════════════════╬═════════╬══════════════════════════════╣
    # ║ Web Scraping     ║ Selenium,        ║ Thread  ║ Lots of waiting -> Fast      ║
    # ║                  ║ Requests         ║         ║ (50-200 threads).            ║
    # ╠══════════════════╬══════════════════╬═════════╬══════════════════════════════╣
    # ║ Number Crunch,   ║ Pandas, Ray      ║ Multi-  ║ Must bypass GIL or it        ║
    # ║ Ray Tracing,     ║ Tracing          ║ Proc    ║ stays slow (1 core).         ║
    # ║ pandas heavy ops ║                  ║         ║                              ║
    # ╚══════════════════╩══════════════════╩═════════╩══════════════════════════════╝
    # ║                  ║                  ║         ║                              ║
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
    ║  This tutorial covers all important aspects of Python threading.     ║
    ║  Each section builds on the previous one.                            ║
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
    main()
