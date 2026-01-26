# #!/usr/bin/env python3
# """
# PYTHON ASYNCIO - QUICK REVISION GUIDE (Python 3.11+)
# ====================================================
# """

# import asyncio
# from os import sep
# import time
# import random
# from contextlib import asynccontextmanager


# def separator(msg: str, l: int = 100):
#     n = len(msg)
#     hash_len = (l - n - 2) // 2
#     print(" ")
#     print("=" * l)
#     print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
#     print("=" * l)
#     print(" ")


# def print_subsection(title, l: int = 100):
#     n = len(title)
#     hash_len = (l - n - 2) // 2
#     print(f"\n{'-' * hash_len} {title} {'-' * hash_len}\n")


# def announce(msg: str):
#     def _deco(func):
#         def wrapper2(*args, **kwargs):
#             separator(msg)
#             func(*args, **kwargs)

#         return wrapper2

#     return _deco


# # ============================================================================
# # 1. BASICS - Coroutines & Running
# # ============================================================================

# async def _1_basic_coroutine():
#     """Coroutines are defined with 'async def'."""
#     separator("1. BASICS - Coroutines & Running")

#     print(f"[{time.time()}]: Hello from coroutine!")
#     await asyncio.sleep(0.1)  # Non-blocking sleep
#     print(f"[{time.time()}]: Hello from coroutine!")
#     return 42

# # Run with asyncio.run() - main entry point
# # result = asyncio.run(basic_coroutine())


# # ============================================================================
# # 2. CONCURRENT EXECUTION - Tasks & Gather
# # ============================================================================

# async def worker(name: str, delay: float) -> str:
#     print(f"{name}: Starting")
#     await asyncio.sleep(delay)
#     print(f"{name}: Done")
#     return f"{name} result"


# async def _2_concurrent_demo():
#     """Sequential vs Concurrent execution."""
#     separator("2. CONCURRENT EXECUTION - Tasks & Gather")


#     # SEQUENTIAL - slow (3 seconds)
#     # await worker("A", 1)
#     # await worker("B", 1)
#     # await worker("C", 1)

#     # CONCURRENT with create_task - fast (1 second)
#     t1 = asyncio.create_task(worker("A", 1), name="Task-A")
#     t2 = asyncio.create_task(worker("B", 1), name="Task-B")
#     t3 = asyncio.create_task(worker("C", 1), name="Task-C")
#     await t1; await t2; await t3

#     # CONCURRENT with gather - cleaner
#     results = await asyncio.gather(
#         worker("X", 0.5),
#         worker("Y", 0.5),
#         worker("Z", 0.5),
#     )
#     print(f"Results: {results}")


# # ============================================================================
# # 3. GATHER - Exception Handling
# # ============================================================================

# async def may_fail(name: str, fail: bool):
#     await asyncio.sleep(0.1)
#     if fail:
#         raise ValueError(f"{name} failed!")
#     return f"{name} OK"


# async def _3_gather_exceptions():
#     # return_exceptions=True prevents one failure from stopping all
#     results = await asyncio.gather(
#         may_fail("A", False),
#         may_fail("B", True),   # Will fail
#         may_fail("C", False),
#         return_exceptions=True
#     )

#     for r in results:
#         if isinstance(r, Exception):
#             print(f"Error: {r}")
#         else:
#             print(f"Success: {r}")


# # ============================================================================
# # 4. WAITING - wait(), wait_for(), as_completed()
# # ============================================================================

# async def _4_waiting_demo():
#     tasks = {
#         asyncio.create_task(worker("Fast", 0.2)),
#         asyncio.create_task(worker("Slow", 0.5)),
#     }

#     # Wait for ALL (default)
#     done, pending = await asyncio.wait(tasks)

#     # Wait for FIRST completed
#     # done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

#     # With TIMEOUT
#     result = await asyncio.wait_for(worker("Timed", 0.1), timeout=1.0)

#     # Process AS COMPLETED (order of completion)
#     coros = [worker("A", 0.3), worker("B", 0.1), worker("C", 0.2)]
#     for coro in asyncio.as_completed(coros):
#         result = await coro
#         print(f"Completed: {result}")


# # ============================================================================
# # 5. TIMEOUT - Context Manager (Python 3.11+)
# # ============================================================================

# async def _5_timeout_demo():
#     try:
#         async with asyncio.timeout(1.0):
#             await asyncio.sleep(5)  # Will timeout
#     except TimeoutError:
#         print("Operation timed out!")

#     # With deadline
#     loop = asyncio.get_running_loop()
#     deadline = loop.time() + 2.0
#     async with asyncio.timeout_at(deadline):
#         await asyncio.sleep(0.5)


# # ============================================================================
# # 6. CANCELLATION
# # ============================================================================

# async def _6_cancellation_demo():
#     async def long_task():
#         try:
#             await asyncio.sleep(10)
#         except asyncio.CancelledError:
#             print("Task cancelled! Cleaning up...")
#             raise  # Always re-raise!

#     task = asyncio.create_task(long_task())
#     await asyncio.sleep(0.5)
#     task.cancel("Timeout")  # Cancel with message

#     try:
#         await task
#     except asyncio.CancelledError:
#         print("Cancellation confirmed")

#     # Shield from cancellation
#     # await asyncio.shield(critical_operation())


# # ============================================================================
# # 7. TASKGROUP - Structured Concurrency (Python 3.11+)
# # ============================================================================

# async def _7_taskgroup_demo():
#     async with asyncio.TaskGroup() as tg:
#         t1 = tg.create_task(worker("A", 0.3))
#         t2 = tg.create_task(worker("B", 0.2))
#         t3 = tg.create_task(worker("C", 0.1))

#     # All tasks guaranteed complete here
#     print(f"Results: {t1.result()}, {t2.result()}, {t3.result()}")


# async def _7_1_taskgroup_exception():
#     """Exception handling with TaskGroup."""
#     try:
#         async with asyncio.TaskGroup() as tg:
#             tg.create_task(may_fail("A", False))
#             tg.create_task(may_fail("B", True))  # Fails
#     except* ValueError as eg:
#         for exc in eg.exceptions:
#             print(f"Caught: {exc}")


# # ============================================================================
# # 8. SYNCHRONIZATION PRIMITIVES
# # ============================================================================

# async def _8_sync_primitives_demo():
#     # LOCK - Mutual exclusion
#     lock = asyncio.Lock()
#     async with lock:
#         print("Critical section")

#     # SEMAPHORE - Limit concurrency
#     sem = asyncio.Semaphore(3)  # Max 3 concurrent
#     async with sem:
#         print("Limited access")

#     # EVENT - Signaling
#     event = asyncio.Event()
#     # event.set()    # Signal
#     # await event.wait()  # Wait for signal
#     # event.clear()  # Reset

#     # CONDITION - Complex sync
#     condition = asyncio.Condition()
#     async with condition:
#         await condition.wait_for(lambda: True)  # Wait for condition
#         condition.notify_all()

#     # BARRIER - Sync multiple tasks (Python 3.11+)
#     barrier = asyncio.Barrier(3)
#     # await barrier.wait()  # Wait for 3 tasks


# # ============================================================================
# # 9. QUEUES - Producer/Consumer
# # ============================================================================

# async def _9_queue_demo():
#     queue = asyncio.Queue(maxsize=10)

#     async def producer():
#         for i in range(5):
#             await queue.put(f"item-{i}")
#             print(f"Produced: item-{i}")

#     async def consumer():
#         while True:
#             try:
#                 item = await asyncio.wait_for(queue.get(), timeout=0.5)
#                 print(f"Consumed: {item}")
#                 queue.task_done()
#             except TimeoutError:
#                 break

#     await asyncio.gather(producer(), consumer())
#     await queue.join()  # Wait for all items processed

#     # Also available:
#     # asyncio.PriorityQueue() -


# # ==========================================
# # MAIN ENTRY POINT
# # ==========================================
# async def main():
#     print("=== ASYNCIO TUTORIAL SCRIPT ===")

#     await _1_basic_coroutine()
#     await _2_concurrent_demo()
#     await _3_gather_exceptions()
#     await _4_waiting_demo()
#     await _5_timeout_demo()
#     await _6_cancellation_demo()
#     await _7_taskgroup_demo()
#     await _7_1_taskgroup_exception()
#     await _8_sync_primitives_demo()
#     await _9_queue_demo()

#     print("\n=== TUTORIAL COMPLETE ===")

# if __name__ == "__main__":
#     # This is how you start the Asyncio Event Loop
#     asyncio.run(main())


"""
Python Asyncio Tutorial - Complete Reference Guide
Run this file to see all concepts in action!
"""

import asyncio
from os import sep
import time


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


# =============================================================================
# CONCEPT 0: 3 Ways to Run Coroutines
# =============================================================================
async def concept_0_basics():
    """
    A coroutine is a special function that can pause and resume its execution,
    allowing other code to run during the pause.
    """

    async def my_coroutine():
        await asyncio.sleep(1)
        return "Done"

    # Method 1: asyncio.run() - main entry point
    result = asyncio.run(my_coroutine())
    print(f"asyncio.run(my_coroutine()) ==> Result: {result}")

    # Method 2: await - inside another coroutine
    # But idhar main ko async.run(main()) krke run krna pdega
    async def main1():
        result = await my_coroutine()
        print(f"await my_coroutine() ==> Result: {result}")

    asyncio.run(main1())

    # Method 3: create_task() - run in background
    async def main2():
        task = asyncio.create_task(my_coroutine())
        time.sleep(5)
        # ... do other stuff ...
        result = await task
        print(f"await asyncio.create_task(my_coroutine()) ==> Result: {result}")

    asyncio.run(main2())


# =============================================================================
# CONCEPT 1: Basic async/await Syntax
# =============================================================================
async def concept_1_basics():
    """
    - Use 'async def' to define a coroutine (async function)
    - Use 'await' to pause and wait for async operations
    - Coroutines don't run until awaited or scheduled
    """
    print("\n" + "=" * 50)
    print("CONCEPT 1: Basic async/await Syntax")
    print("=" * 50)

    # Coroutine - can pause and let other code run
    async def greet(name):
        print(f"Hello, {name}!")
        await asyncio.sleep(1)
        # Non-blocking pause. i.e. PAUSE here, other code can run
        print(f"Goodbye, {name}!")

    await greet("Alice")


# =============================================================================
# CONCEPT 2: Blocking vs Non-Blocking (Why use asyncio?)
# =============================================================================
async def concept_2_blocking_vs_nonblocking():
    """
    - time.sleep() = BLOCKING (freezes everything)
    - asyncio.sleep() = NON-BLOCKING (allows other tasks to run)
    - Async saves time when waiting for I/O (network, files, etc.)
    """
    print("\n" + "=" * 50)
    print("CONCEPT 2: Blocking vs Non-Blocking")
    print("=" * 50)

    async def task(name, delay):
        await asyncio.sleep(delay)
        print(f"  Task {name} completed")

    # Running concurrently - both start at same time
    start = time.time()
    await asyncio.gather(task("A", 1), task("B", 1))
    print(f"  Total time: {time.time() - start:.1f}s (not 2s because concurrent!)")


# =============================================================================
# CONCEPT 3: Creating Tasks (Background Execution)
# =============================================================================
async def concept_3_create_task():
    """
    - asyncio.create_task() schedules coroutine to run in background
    - Task starts immediately, doesn't wait for await
    - Use 'await task' to get the result when needed
    """
    print("\n" + "=" * 50)
    print("CONCEPT 3: Creating Tasks")
    print("=" * 50)

    async def background_job(name):
        print(f"  {name}: Started")
        await asyncio.sleep(2)
        print(f"  {name}: Finished")
        return f"{name} result"

    # Task starts running immediately in background
    task = asyncio.create_task(background_job("Download"))

    # Do other work while task runs
    print("  Main: Doing other work...")
    await asyncio.sleep(1)
    print("  Main: Still working...")

    # Wait for task and get result
    result = await task
    print(f"  Main: Got result -> {result}")


# =============================================================================
# CONCEPT 4: gather() - Run Multiple Coroutines Concurrently
# =============================================================================
async def concept_4_gather():
    """
    - asyncio.gather() runs multiple coroutines concurrently
    - Returns results in SAME ORDER as input (not completion order)
    - All coroutines start at the same time
    """
    print("\n" + "=" * 50)
    print("CONCEPT 4: gather() - Multiple Coroutines")
    print("=" * 50)

    async def fetch(source, delay):
        await asyncio.sleep(delay)
        return f"Data from {source}"

    # All three run concurrently
    results = await asyncio.gather(
        fetch("API", 2),  # Slowest
        fetch("Database", 1),  # Medium
        fetch("Cache", 0.5),  # Fastest
    )

    # Results maintain input order, not completion order
    print(f"  Results: {results}")


# =============================================================================
# CONCEPT 5: Timeouts with wait_for()
# =============================================================================
async def concept_5_timeout():
    """
    - asyncio.wait_for() adds timeout to any coroutine
    - Raises asyncio.TimeoutError if time exceeded
    - Useful for network requests, preventing infinite waits
    """
    print("\n" + "=" * 50)
    print("CONCEPT 5: Timeouts with wait_for()")
    print("=" * 50)

    async def slow_operation():
        await asyncio.sleep(5)
        return "Done"

    # Try with timeout shorter than operation
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"  Result: {result}")
    except asyncio.TimeoutError:
        print("  Operation timed out! (expected)")

    # Try with sufficient timeout
    async def fast_operation():
        await asyncio.sleep(0.5)
        return "Success"

    result = await asyncio.wait_for(fast_operation(), timeout=2.0)
    print(f"  Result: {result}")


# =============================================================================
# CONCEPT 6: Exception Handling in gather()
# =============================================================================
async def concept_6_exception_handling():
    """
    - By default, one exception cancels all tasks in gather()
    - Use return_exceptions=True to collect errors without stopping
    - Check results for Exception instances
    """
    print("\n" + "=" * 50)
    print("CONCEPT 6: Exception Handling")
    print("=" * 50)

    async def might_fail(n):
        await asyncio.sleep(0.5)
        if n == 2:
            raise ValueError(f"Task {n} failed!")
        return f"Task {n} success"

    # return_exceptions=True prevents cancellation of other tasks
    results = await asyncio.gather(
        might_fail(1),
        might_fail(2),  # This will fail
        might_fail(3),
        return_exceptions=True,
    )

    # Process results - some may be exceptions
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"  Task {i}: ERROR - {result}")
        else:
            print(f"  Task {i}: {result}")


# =============================================================================
# CONCEPT 7: Semaphore - Limit Concurrency
# =============================================================================
async def concept_7_semaphore():
    """
    - Semaphore limits how many coroutines run simultaneously
    - Use 'async with semaphore:' to acquire/release automatically
    - Perfect for rate limiting API calls, database connections
    """
    print("\n" + "=" * 50)
    print("CONCEPT 7: Semaphore - Limit Concurrency")
    print("=" * 50)

    # Only 2 tasks can run at the same time
    semaphore = asyncio.Semaphore(2)

    async def limited_task(name):
        async with semaphore:  # Waits here if 2 tasks already running
            print(f"  {name}: Started (inside semaphore)")
            await asyncio.sleep(1)
            print(f"  {name}: Finished")

    # Start 5 tasks, but only 2 run at a time
    start = time.time()
    await asyncio.gather(
        limited_task("Task-1"),
        limited_task("Task-2"),
        limited_task("Task-3"),
        limited_task("Task-4"),
        limited_task("Task-5"),
    )
    print(f"  Total time: {time.time() - start:.1f}s (5 tasks, 2 at a time = ~3s)")


# =============================================================================
# CONCEPT 8: Queue - Producer/Consumer Pattern
# =============================================================================
async def concept_8_queue():
    """
    - asyncio.Queue() for thread-safe async data passing
    - Producer puts items, Consumer gets items
    - queue.put() and queue.get() are async operations
    - Use sentinel value (None) to signal completion
    """
    print("\n" + "=" * 50)
    print("CONCEPT 8: Queue - Producer/Consumer")
    print("=" * 50)

    queue = asyncio.Queue(maxsize=3)  # Max 3 items buffered

    async def producer():
        for i in range(5):
            await queue.put(f"item-{i}")
            print(f"  Producer: Added item-{i}")
            await asyncio.sleep(0.3)
        await queue.put(None)  # Signal: no more items

    async def consumer():
        while True:
            item = await queue.get()
            if item is None:  # Stop signal received
                print("  Consumer: Received stop signal")
                break
            print(f"  Consumer: Processing {item}")
            await asyncio.sleep(0.5)  # Simulate processing
            queue.task_done()

    await asyncio.gather(producer(), consumer())


# =============================================================================
# CONCEPT 9: Event - Synchronization Between Tasks
# =============================================================================
async def concept_9_event():
    """
    - asyncio.Event() for signaling between coroutines
    - event.wait() pauses until event.set() is called
    - event.clear() resets the event
    - Useful for coordinating task startup/shutdown
    """
    print("\n" + "=" * 50)
    print("CONCEPT 9: Event - Task Synchronization")
    print("=" * 50)

    event = asyncio.Event()

    async def waiter(name):
        print(f"  {name}: Waiting for signal...")
        await event.wait()  # Blocks until event.set()
        print(f"  {name}: Got signal! Proceeding...")

    async def setter():
        print("  Setter: Preparing...")
        await asyncio.sleep(1)
        print("  Setter: Sending signal!")
        event.set()  # All waiters will proceed

    await asyncio.gather(waiter("Waiter-1"), waiter("Waiter-2"), setter())


# =============================================================================
# CONCEPT 10: Lock - Prevent Race Conditions
# =============================================================================
async def concept_10_lock():
    """
    - asyncio.Lock() ensures only one coroutine accesses resource
    - Use 'async with lock:' for automatic acquire/release
    - Prevents race conditions on shared data
    """
    print("\n" + "=" * 50)
    print("CONCEPT 10: Lock - Prevent Race Conditions")
    print("=" * 50)

    lock = asyncio.Lock()
    shared_counter = {"value": 0}  # Shared resource

    async def increment(name):
        for _ in range(3):
            async with lock:  # Only one task can be here at a time
                current = shared_counter["value"]
                await asyncio.sleep(0.1)  # Simulate some processing
                shared_counter["value"] = current + 1
                print(f"  {name}: Counter = {shared_counter['value']}")

    await asyncio.gather(increment("Task-A"), increment("Task-B"))
    print(f"  Final counter: {shared_counter['value']} (should be 6)")


# =============================================================================
# CONCEPT 11: Running Blocking Code in Executor
# =============================================================================
async def concept_11_run_in_executor():
    """
    - Some libraries don't support async (blocking I/O)
    - Use run_in_executor() to run blocking code in thread pool
    - Prevents blocking code from freezing event loop
    """
    print("\n" + "=" * 50)
    print("CONCEPT 11: Running Blocking Code")
    print("=" * 50)

    def blocking_operation(n):
        """Simulates blocking I/O (like older libraries)"""
        time.sleep(1)  # Blocking sleep!
        return f"Blocking result {n}"

    loop = asyncio.get_event_loop()

    # Run blocking functions in thread pool
    start = time.time()
    results = await asyncio.gather(
        loop.run_in_executor(None, blocking_operation, 1),
        loop.run_in_executor(None, blocking_operation, 2),
        loop.run_in_executor(None, blocking_operation, 3),
    )

    print(f"  Results: {results}")
    print(f"  Time: {time.time() - start:.1f}s (concurrent despite blocking!)")


# =============================================================================
# CONCEPT 12: Cancelling Tasks
# =============================================================================
async def concept_12_cancel_task():
    """
    - task.cancel() sends CancelledError to the task
    - Use try/except asyncio.CancelledError for cleanup
    - Cancelled tasks raise CancelledError when awaited
    """
    print("\n" + "=" * 50)
    print("CONCEPT 12: Cancelling Tasks")
    print("=" * 50)

    async def long_running_task():
        try:
            print("  Task: Starting long operation...")
            await asyncio.sleep(10)
            print("  Task: Completed!")  # Won't reach here
        except asyncio.CancelledError:
            print("  Task: Cancelled! Cleaning up...")
            raise  # Re-raise to properly cancel

    task = asyncio.create_task(long_running_task())

    await asyncio.sleep(1)
    print("  Main: Cancelling task...")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("  Main: Task was cancelled successfully")


# =============================================================================
# MAIN: Run All Concepts Sequentially
# =============================================================================
async def main():
    """Run all concepts one by one"""

    separator("PYTHON ASYNCIO TUTORIAL - ALL CONCEPTS")

    await concept_0_basics()
    # await concept_1_basics()
    # await concept_2_blocking_vs_nonblocking()
    # await concept_3_create_task()
    # await concept_4_gather()
    # await concept_5_timeout()
    # await concept_6_exception_handling()
    # await concept_7_semaphore()
    # await concept_8_queue()
    # await concept_9_event()
    # await concept_10_lock()
    # await concept_11_run_in_executor()
    # await concept_12_cancel_task()

    print("\n" + "#" * 50)
    print("# TUTORIAL COMPLETE!")
    print("#" * 50)

    # Quick reference summary
    print("""
    QUICK REFERENCE:
    ================
    async def          -> Define coroutine
    await              -> Wait for coroutine
    asyncio.run()      -> Entry point (call once)
    asyncio.create_task() -> Run in background
    asyncio.gather()   -> Run multiple concurrently
    asyncio.sleep()    -> Non-blocking delay
    asyncio.wait_for() -> Add timeout
    asyncio.Semaphore  -> Limit concurrency
    asyncio.Queue      -> Producer/consumer
    asyncio.Event      -> Signal between tasks
    asyncio.Lock       -> Prevent race conditions
    run_in_executor()  -> Run blocking code
    task.cancel()      -> Cancel running task
    """)


# Entry point - only use asyncio.run() once!
if __name__ == "__main__":
    asyncio.run(main())
