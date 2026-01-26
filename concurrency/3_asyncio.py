#!/usr/bin/env python3
"""
================================================================================
                    PYTHON ASYNCIO LIBRARY - COMPLETE TUTORIAL
================================================================================

Author: Tutorial Script
Python Version: 3.7+ (some features require 3.9+, 3.11+)
YouTube references: [
    https://www.youtube.com/watch?v=oAkLSJNr5zY,
]

This tutorial covers everything you need to know about Python's asyncio library
for writing concurrent code using the async/await syntax.

TABLE OF CONTENTS:
==================
1.  Introduction to Asyncio
2.  Basic Concepts - Event Loop, Coroutines, async/await
3.  Running Coroutines - asyncio.run(), create_task()
4.  Tasks - Creating and Managing Tasks
5.  Gathering Multiple Coroutines - asyncio.gather()
6.  Waiting for Tasks - asyncio.wait(), wait_for()
7.  Timeouts and Cancellation
8.  Async Sleep vs Time Sleep
9.  Synchronization Primitives (Locks, Semaphores, Events)
10. Async Queues - Producer/Consumer Pattern
11. Async Context Managers
12. Async Iterators and Generators
13. Running Blocking/Sync Code in Async Context
14. Streams - TCP Client/Server
15. Subprocesses
16. Error Handling in Asyncio
17. TaskGroups (Python 3.11+)
18. Practical Examples
19. Asyncio vs Threading vs Multiprocessing
20. Best Practices and Common Pitfalls

================================================================================
"""

import asyncio
import random
import threading
import time
import concurrent.futures

# Check Python version for feature availability
# PYTHON_VERSION = sys.version_info
# print(f"Python Version: {PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.{PYTHON_VERSION.micro}")


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


# ================================================================================
# SECTION 1: INTRODUCTION TO ASYNCIO
# ================================================================================


def _1_introduction_to_asyncio():
    separator("1. INTRODUCTION TO ASYNCIO")

    print("""
WHAT IS ASYNCIO?
================

asyncio is Python's built-in library for writing concurrent code using the 
async/await syntax. It provides:

1. An EVENT LOOP that manages and distributes the execution of tasks
2. COROUTINES - special functions defined with async def
3. TASKS - wrappers around coroutines for concurrent execution
4. Synchronization primitives (locks, events, semaphores, queues)
5. Network I/O support (TCP, UDP, SSL)

WHEN TO USE ASYNCIO:
====================
✓ I/O-bound operations (network requests, file I/O, database queries)
✓ High number of concurrent connections (web servers, chat applications)
✓ Real-time data processing
✓ WebSocket connections
✓ API clients making many requests
✓ CPU-bound tasks offloaded via executors (threads / processes)

WHEN NOT TO USE ASYNCIO:
========================
✗ CPU-bound tasks directly in the event loop (use multiprocessing instead)
✗ Simple scripts with no concurrency needs
✗ When using libraries that don't support async

ASYNCIO vs THREADING:
=====================
┌─────────────────────┬────────────────────────┬─────────────────────────┐
│ Aspect              │ Asyncio                │ Threading               │
├─────────────────────┼────────────────────────┼─────────────────────────┤
│ Concurrency Model   │ Cooperative (single    │ Preemptive (OS          │
│                     │ thread, yields control)│ schedules threads)      │
├─────────────────────┼────────────────────────┼─────────────────────────┤
│ Memory Overhead     │ Low (coroutines are    │ Higher (each thread     │
│                     │ lightweight)           │ needs stack space)      │
├─────────────────────┼────────────────────────┼─────────────────────────┤
│ Context Switching   │ Explicit (await)       │ Implicit (OS decides)   │
├─────────────────────┼────────────────────────┼─────────────────────────┤
│ Race Conditions     │ Fewer (explicit yield) │ More common             │
├─────────────────────┼────────────────────────┼─────────────────────────┤
│ Scalability         │ 10,000s of tasks       │ 100s of threads         │
└─────────────────────┴────────────────────────┴─────────────────────────┘

KEY TERMINOLOGY:
================
• Coroutine: A function defined with 'async def' that can be paused/resumed
• Awaitable: Object that can be used with 'await' (coroutines, tasks, futures)
• Task: A wrapper around a coroutine, scheduled to run on the event loop 
        (i.e. a wrapped couroutine that can be executed independently)
        (Tasks are how we actually run coroutine concurrently)
• Future: A low-level awaitable representing an eventual result
• Event Loop: The central execution mechanism that runs async code
""")


# ================================================================================
# SECTION 2: BASIC CONCEPTS - EVENT LOOP, COROUTINES, ASYNC/AWAIT
# ================================================================================


async def _2_basic_concepts():
    separator("2. BASIC CONCEPTS - EVENT LOOP, COROUTINES, ASYNC/AWAIT")

    # ------------------------------------------------------------------------------
    # 2.1 Coroutines
    # ------------------------------------------------------------------------------

    print_subsection("2.1 Coroutines - The Building Blocks")

    # A coroutine is defined using 'async def'
    async def my_first_coroutine():
        """A simple coroutine that returns a value."""
        print("inside my_first_coroutine()!")
        return 42

    # Creating a coroutine object (doesn't execute it!)
    coroutine_obj = my_first_coroutine()

    print(f"Coroutine object: {coroutine_obj}")
    print(f"Type: {type(coroutine_obj)}")
    print("\tNotice the coroutine function hasn't started running yet...")
    print("\tbcz it'll just create coroutine_obj but not schedule it on our event loop")
    print(
        "\tusing 'await coroutine_obj' or 'asyncio.run(coroutine_obj)' "
        "\n\t\t=> will schedule them and run them to completion at the same time"
    )

    # Must close unused coroutine to avoid warning
    coroutine_obj.close()

    # To actually run a coroutine, use asyncio.run() or await it
    coroutine_obj = my_first_coroutine()

    result = await coroutine_obj
    print(f"Result: {result}")

    # ------------------------------------------------------------------------------
    # 2.2 The 'await' Keyword
    # ------------------------------------------------------------------------------

    print_subsection("2.2 The 'await' Keyword")

    async def fetch_data():
        """Simulate fetching data with a delay."""
        print("Fetching data...")
        await asyncio.sleep(1)  # Non-blocking sleep
        print("Data fetched!")
        return {"id": 1, "name": "Example"}

    async def process_data():
        """Process data by awaiting another coroutine."""
        print("Starting data processing...")

        # 'await' pauses this coroutine until fetch_data completes
        data = await fetch_data()

        print(f"Processing: {data}")
        return f"Processed: {data['name']}"

    # Run the coroutine
    print("\nRunning process_data():")
    result = await process_data()
    print(f"Final result: {result}")

    # ------------------------------------------------------------------------------
    # 2.3 What Can Be Awaited?
    # ------------------------------------------------------------------------------

    print_subsection("2.3 What Can Be Awaited?")

    async def demonstrate_awaitables():
        """Show different types of awaitables."""

        # 1. Coroutines can be awaited
        async def simple_coro():
            return "coroutine result"

        result1 = await simple_coro()
        print(f"1. Awaited coroutine: {result1}")

        # 2. Tasks can be awaited
        task = asyncio.create_task(simple_coro())
        result2 = await task
        print(f"2. Awaited task: {result2}")

        # 3. asyncio.sleep returns an awaitable
        await asyncio.sleep(0.1)
        print("3. Awaited sleep")

        # 4. asyncio.gather returns an awaitable
        results = await asyncio.gather(simple_coro(), simple_coro())
        print(f"4. Awaited gather: {results}")

        # 5. Futures can be awaited
        loop = asyncio.get_running_loop()

        future1, future2 = loop.create_future(), loop.create_future()
        print(f"5.1 Created future1: {future1}")
        print(f"5.1 Created future2: {future2}")

        future1.set_result("manual_result")
        future2.set_exception(Exception("manual_exception"))

        result1 = await future1
        print(f"5.2 Awaited future1 result: {result1}")

        try:
            result2 = await future2
        except Exception as e:
            print(f"5.2 Awaited future2 exception: {e}")

    # asyncio.run(demonstrate_awaitables())
    await demonstrate_awaitables()

    # ------------------------------------------------------------------------------
    # 2.4 Event Loop Basics
    # ------------------------------------------------------------------------------

    print_subsection("2.4 Event Loop Basics")

    async def show_event_loop():
        """Demonstrate event loop access."""

        # Get the running event loop
        loop = asyncio.get_running_loop()

        print(f"Event loop: {loop}")
        print(f"Is running: {loop.is_running()}")
        print(f"Is closed: {loop.is_closed()}")
        print(f"Time: {loop.time():.2f}")  # Loop's internal clock

    # asyncio.run(show_event_loop())
    await show_event_loop()

    # ------------------------------------------------------------------------------
    # 2.5 Event Loop Lifecycle Example (using asyncio.sleep)
    # ------------------------------------------------------------------------------

    print_subsection("2.5 Event Loop Lifecycle Example (using asyncio.sleep)")

    async def fetch_data_async_sleep(param):
        print(f"Do something with {param}...")
        await asyncio.sleep(param)  # Non-blocking sleep
        print(f"Done with {param}")
        return f"Result of {param}"

    async def _2_5_lifecycle_example():
        task1 = asyncio.create_task(fetch_data_async_sleep(1))
        task2 = asyncio.create_task(fetch_data_async_sleep(2))
        result2 = await task2
        # Jaruri nahi ki task 2 pahle pick hoga
        # (event loop to jo bhi ready rhega kisi ko bhi run kr skta hai
        #     ==> task 1 bhi ho skta bcz dono hi scheduled ho chuke hai
        #     ==> event loop uses FIFO queue -> so task1 hi jayega iss case me),
        # but ye guarantee hai ki jb tk task 2 complete na ho tb tk idhar se hilega nahi
        print("Task 2 fully completed")
        result1 = await task1
        print("Task 1 fully completed")
        return [result1, result2]

    t1 = time.perf_counter()

    results = await _2_5_lifecycle_example()
    print(results)

    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1:.2f} seconds")

    # ------------------------------------------------------------------------------
    # 2.6 Event Loop Lifecycle Example (using time.sleep)
    # ------------------------------------------------------------------------------

    print_subsection("2.6 Event Loop Lifecycle Example (using time.sleep)")

    async def fetch_data_time_sleep(param):
        print(f"Do something with {param}...")
        time.sleep(param)  # Blocking sleep
        print(f"Done with {param}")
        return f"Result of {param}"

    async def _2_6_lifecycle_example():
        task1 = asyncio.create_task(fetch_data_time_sleep(1))
        task2 = asyncio.create_task(fetch_data_time_sleep(2))
        result1 = await task1
        print("Task 1 fully completed")
        result2 = await task2
        print("Task 2 fully completed")
        return [result1, result2]

    t1 = time.perf_counter()

    results = await _2_6_lifecycle_example()
    """
    # Do something with 1...
    # Done with 1
    # Do something with 2... [==> bcz idhar event loop ne main k bajay task2 ko pick kiya 
    #                         ==> becase task2 usse phle se ready state me baitha tha 
    #                         ==> jabki `main` to task1 k complete hone ka wait kr rha tha and 
    #                             just abhi dubara se ready state me aaya hai 
    #                         ==> hence FIFO queue ne task2 prefer kiya]
    # Done with 2
    # Task 1 fully completed
    # Task 2 fully completed
    # ['Result of 1', 'Result of 2']
    # Finished in 3.00 seconds
    """

    print(results)

    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1:.2f} seconds")


# ================================================================================
# SECTION 3: RUNNING COROUTINES
# ================================================================================


async def _3_running_coroutines():
    separator("3. RUNNING COROUTINES")

    # ------------------------------------------------------------------------------
    # 3.1 asyncio.run() - The Main Entry Point
    # ------------------------------------------------------------------------------

    print_subsection("3.1 asyncio.run() - The Main Entry Point")

    async def main_entry_point():
        """Main coroutine demonstrating asyncio.run()."""
        print("This is the main entry point")
        await asyncio.sleep(0.1)
        return "Completed!"

    # asyncio.run() does several things:
    # 1. Creates a new event loop
    # 2. Runs the coroutine until complete
    # 3. Closes the loop
    # 4. Returns the result

    # asyncio.run(main_entry_point()) ki jagah ye call krna pdega idhar
    result = await main_entry_point()
    print(f"Result: {result}")

    # Note: asyncio.run() should typically be called once per program
    # It cannot be called from within a running event loop

    # ------------------------------------------------------------------------------
    # 3.2 create_task() - Scheduling Concurrent Execution
    # ------------------------------------------------------------------------------

    print_subsection("3.2 create_task() - Scheduling Concurrent Execution")

    async def task_example(name: str, delay: float) -> str:
        """A coroutine that simulates work with a delay."""
        print(f"Task {name}: Starting (delay={delay}s)")
        await asyncio.sleep(delay)
        print(f"Task {name}: Completed")
        return f"Result from {name}"

    async def run_tasks_sequentially():
        """Run tasks one after another (not concurrent)."""
        print("\n[Sequential Execution]")
        start = time.perf_counter()

        # These run one after another,
        # because it Schedules and Runs them to completion in a single step one by one
        #     so when result 1 is getting scheduled and running
        #     => result2 and result 3 wali lines are not yet reached -> so not yet scheduled
        result1 = await task_example("A", 1)  # 1 second
        result2 = await task_example("B", 1)  # 1 second
        result3 = await task_example("C", 1)  # 1 second

        elapsed = time.perf_counter() - start
        print(f"Sequential time: {elapsed:.2f}s")  # 3 seconds
        return [result1, result2, result3]

    async def run_tasks_concurrently():
        """Run tasks concurrently using create_task()."""
        print("\n[Concurrent Execution with create_task()]")
        start = time.perf_counter()

        # Create tasks - they start running immediately
        # (handed over to event loop and scheduled to run whenever it gets a chance).
        #     so jab task 1 me `await asyncio.sleep(delay)` call hoga,
        #     then task 1 will be suspended and event loop will meanwhile look for other scheduled tasks,
        #     which is one of task2 or task 3 (task 2 hi hoga bcz internally FIFO hai)
        # Hence concurrency will be achieved
        # refer to https://www.youtube.com/watch?v=oAkLSJNr5zY
        task1 = asyncio.create_task(task_example("A", 1))  # 1 second
        task2 = asyncio.create_task(task_example("B", 1))  # 1 second
        task3 = asyncio.create_task(task_example("C", 1))  # 1 second

        # Wait for all tasks to complete
        result1 = await task1
        result2 = await task2
        result3 = await task3
        # time.sleep(5)

        elapsed = time.perf_counter() - start
        print(f"Concurrent time: {elapsed:.2f}s")  # 1 second
        return [result1, result2, result3]

    # Compare sequential vs concurrent
    await run_tasks_sequentially()
    await run_tasks_concurrently()

    # ------------------------------------------------------------------------------
    # 3.3 Task Naming and Identification - [asyncio.current_task().get_name()]
    # ------------------------------------------------------------------------------

    print_subsection(
        "3.3 Task Naming and Identification - [asyncio.current_task().get_name()]"
    )

    async def named_task_demo():
        """Demonstrate task naming."""

        async def worker():
            task = asyncio.current_task()
            print(f"Running task: {task.get_name()}")
            await asyncio.sleep(0.1)

        # Create named tasks
        task1 = asyncio.create_task(worker(), name="Worker-1")
        task2 = asyncio.create_task(worker(), name="Worker-2")
        task3 = asyncio.create_task(worker(), name="DataProcessor")

        await asyncio.gather(task1, task2, task3)

        # Get current task
        current = asyncio.current_task()
        print(f"Current task: {current.get_name()}")

        # Get all tasks in the event loop
        all_tasks = asyncio.all_tasks()
        print(f"All running tasks: {[t.get_name() for t in all_tasks]}")

    # asyncio.run(named_task_demo())
    await named_task_demo()


# ================================================================================
# SECTION 4: TASKS - CREATING AND MANAGING TASKS
# ================================================================================


async def _4_tasks_creating_and_managing_tasks():
    separator("4. TASKS - CREATING AND MANAGING TASKS")

    # ------------------------------------------------------------------------------
    # 4.1 Task States and Properties
    # ------------------------------------------------------------------------------

    print_subsection("4.1 Task States and Properties")

    async def demonstrate_task_states():
        """Show different task states and properties."""

        async def slow_operation():
            await asyncio.sleep(0.5)
            return "Done!"

        async def failing_operation():
            await asyncio.sleep(0.2)
            raise ValueError("Something went wrong!")

        print("\n--- Task with No Exception  [task.result()] ---")

        # Create a task
        task = asyncio.create_task(slow_operation(), name="SlowTask")

        # Check state before completion
        print(f"Task name: {task.get_name()}")
        print("\nBefore awaiting/completion:")
        print(f"Done: {task.done()}")
        print(f"Cancelled: {task.cancelled()}")

        # Wait for completion
        result = await task

        # Check state after completion
        print("\nAfter awaiting/completion:")
        print(f"Done: {task.done()}")
        print(f"Result: {task.result()}")
        print(
            f"result(= await task) is same as task.result(): {result is task.result()}"
        )  # True

        # Task with exception
        print("\n--- Task with Exception  [task.exception()] ---")
        failing_task = asyncio.create_task(failing_operation(), name="FailingTask")

        try:
            await failing_task
        except ValueError as e:
            print(f"Task raised exception: {e}")
            print(f"Exception: {failing_task.exception()}")

    await demonstrate_task_states()

    # ------------------------------------------------------------------------------
    # 4.2 Cancelling Tasks
    # ------------------------------------------------------------------------------

    print_subsection("4.2 Cancelling Tasks - [task.cancel()]")

    async def custom_sleep(delay: float, step: int):
        print(f"step-{step}: before awaiting sleep {delay} block")
        await asyncio.sleep(delay)  # ✔️ suspension point
        print(f"step-{step}: after awaiting sleep {delay} block")

    async def cancellable_task(name: str):
        """A task that can be cancelled."""
        try:
            print(f"{name}: Starting long operation...")
            for i in range(10):
                print(f"{name}: Step {i + 1}/10")
                await custom_sleep(
                    0.5, i + 1
                )  # ❌ no suspension here (suspends occurs inside)
            print(f"{name}: Completed successfully")
            return f"{name} result"
        except asyncio.CancelledError:
            print(f"{name}: Task was cancelled! Cleaning up...")
            # Perform cleanup here
            raise  # Re-raise to properly cancel

    async def cancel_demo():
        """Demonstrate task cancellation."""

        # Create a task
        task = asyncio.create_task(cancellable_task("Worker"))

        # Let it run for a bit
        await asyncio.sleep(1.5)

        # Cancel the task
        print("\n>>> Cancelling task...")
        task.cancel()
        # step 1: task.cancel() → marks the Task as "cancelled" (no immediate stop)
        # step 2: cancellation is delivered at the NEXT *suspending* await
        #         (not every syntactic await, only where the task actually pauses)
        #         e.g. sleep → asyncio.sleep()
        #              io    → reader.read()
        #              task  → await some_task
        #              future→ await future
        #              lock  → lock.acquire()
        #              queue → queue.get()
        #              sync  → await coroutine()  # suspends only at inner await
        #         (cancellation hits the active suspension point, not function boundaries)
        #         (may be nested, but always within the same task)
        #         (CPU work runs until the next await)
        # step 3: await task → raises asyncio.CancelledError

        try:
            # Wait for cancellation to complete
            await task
        except asyncio.CancelledError:
            print("Task cancellation confirmed")

        print(f"Task done: {task.done()}")
        print(f"Task cancelled: {task.cancelled()}")

    await cancel_demo()

    # ------------------------------------------------------------------------------
    # 4.3 Cancellation with Custom Message (Python 3.9+)
    # ------------------------------------------------------------------------------

    print_subsection("4.3 Cancellation with Custom Message - [task.cancel(msg)]")

    async def cancel_with_message():
        """Demonstrate cancellation with a custom message."""

        async def worker():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError as e:
                print(f"Cancelled with message: {e.args}")
                raise

        task = asyncio.create_task(worker())
        await asyncio.sleep(0.1)

        # Cancel with a custom message
        task.cancel("Timeout exceeded")

        try:
            await task
        except asyncio.CancelledError:
            pass

    await cancel_with_message()

    # ------------------------------------------------------------------------------
    # 4.4 Shielding Tasks from Cancellation - [asyncio.shield()]
    # ------------------------------------------------------------------------------

    print_subsection("4.4 Shielding Tasks from Cancellation - [asyncio.shield()]")

    async def shield_demo():
        """Demonstrate shielding a task from cancellation."""
        """Shield protects inner task from cancellation"""

        async def critical_operation():
            """An operation that should complete even if outer task is cancelled."""
            print("[CRITICAL]: Entered")
            await asyncio.sleep(1)
            print("[CRITICAL]: Completed!")
            return "[CRITICAL] result"

        async def outer_task_critical_coroutine_obj(prevent_schedule=True):
            """Outer task that shields the critical operation."""
            try:
                if prevent_schedule:
                    # """ delaying sufficient enough to make sure
                    # cancel() is called before it is scheduled
                    # Now shielded task won't run"""

                    print(
                        "[OUTER_TASK]: Before sleeping... (observe 'after sleeping' wont get printed)"
                    )
                    await asyncio.sleep(1)  #  cancel arrives here
                    print(
                        "[OUTER_TASK]: After sleeping"
                    )  # wont get printed, and go to catch block

                result = await asyncio.shield(critical_operation())
                # """
                # if this line is reached before cancel() is called -> means scheduled ✔️
                #   then shielded task will run to complete,
                # else
                #   it will never run
                # """
                return result
            except asyncio.CancelledError:
                print(
                    "[OUTER_TASK]: Outer task cancelled, but critical operation continues if already scheduled..."
                )
                raise

        async def outer_task_critical_task():
            """Outer task that shields the critical operation."""
            try:
                critical_task = asyncio.create_task(critical_operation())
                print(
                    "[OUTER_TASK]: critical task is scheduled, so it will run to completion..."
                )

                print("[OUTER_TASK]: Before sleeping")
                await asyncio.sleep(1)  #  cancel arrives here
                print(
                    "[OUTER_TASK]: After sleeping"
                )  # wont get printed, and go to catch block

                result = await asyncio.shield(critical_task)
                # but this will run to completion as it is already scheduled

                return result  # code won't reach here
            except asyncio.CancelledError:
                print(
                    "[OUTER_TASK]: Outer task cancelled, but critical operation continues..."
                )
                raise

        async def run_example(input):
            task = asyncio.create_task(input)

            # Try to cancel quickly
            await asyncio.sleep(0.3)
            task.cancel()

            try:
                result = await task
                print(f"[MAIN]: Result: {result}")
            except asyncio.CancelledError:
                print("[MAIN]: Task was cancelled")
                # Give time for shielded task to complete
                await asyncio.sleep(1)

        print("\n--- Shielding COROUTINE obj (LET IT SCHEDULE) ---")
        await run_example(outer_task_critical_coroutine_obj(prevent_schedule=False))

        print("\n--- Shielding COROUTINE obj (PREVENT SCHEDULE) ---")
        await run_example(outer_task_critical_coroutine_obj(prevent_schedule=True))

        print("\n--- Shielding TASK (`asyncio.create_task` will schedule itself) ---")
        await run_example(outer_task_critical_task())

    await shield_demo()


# ================================================================================
# SECTION 5: GATHERING MULTIPLE COROUTINES - asyncio.gather()
# ================================================================================


async def _5_gather_coroutines():
    separator("5. GATHERING MULTIPLE COROUTINES - asyncio.gather()")

    # ------------------------------------------------------------------------------
    # 5.1 Basic Gather Usage
    # ------------------------------------------------------------------------------

    # """
    # Can pass a couroutine if concerned about result only
    # Can pass as task if want to do some interaction or monitor or something else
    #     (as tasks have some extra functionalities)
    # """
    print_subsection("5.1.1 Basic Gather Usage - (gather coroutines)")

    async def fetch_url(url: str, delay: float) -> dict:
        """Simulate fetching a URL."""
        print(f"Fetching {url}...")
        await asyncio.sleep(delay)
        return {"url": url, "status": 200, "data": f"Content from {url}"}

    async def gather_couroutines():
        """Basic example of asyncio.gather()."""

        start = time.perf_counter()

        # All coroutines are Scheduled and Run to completion concurrently
        # and results are returned in order
        results = await asyncio.gather(
            fetch_url("https://api.example.com/users", 1.0),
            fetch_url("https://api.example.com/posts", 0.5),
            fetch_url("https://api.example.com/comments", 1.5),
            # return_exceptions=False (default `False` but always recommended to set `True` for better error handling)
        )

        elapsed = time.perf_counter() - start

        print(f"\nAll fetches completed in {elapsed:.2f}s")
        print("Coroutines Results:")
        for result in results:
            print(f"  - {result}")

    await gather_couroutines()

    print_subsection("5.1.2 Basic Gather Usage - (gather tasks)")

    async def gather_tasks():
        """Basic example of asyncio.gather()."""

        start = time.perf_counter()

        # All tasks are already Scheduled
        # `await gather` ==> Runs to completion concurrently
        # and returns results in order
        results = await asyncio.gather(
            asyncio.create_task(fetch_url("https://api.example.com/users", 1.0)),
            asyncio.create_task(fetch_url("https://api.example.com/posts", 0.5)),
            asyncio.create_task(fetch_url("https://api.example.com/comments", 1.5)),
        )

        elapsed = time.perf_counter() - start

        print(f"\nAll fetches completed in {elapsed:.2f}s")
        print("Tasks Results:")
        for result in results:
            print(f"  - {result}")

        return results

    await gather_tasks()

    # ------------------------------------------------------------------------------
    # 5.2 Gather with Exception Handling
    # ------------------------------------------------------------------------------

    print_subsection("5.2 Gather with Exception Handling")

    async def may_fail(name: str, should_fail: bool) -> str:
        """A coroutine that may raise an exception."""
        await asyncio.sleep(0.5)
        if should_fail:
            raise ValueError(f"{name} failed!")
        return f"{name} succeeded"

    async def gather_exception_handling():
        """Handle exceptions in gather()."""

        # when return_exceptions=False(default),if one coroutine/task fails:
        #   => it immediately raises that first exception that it sees
        #   => and other tasks won't be cancelled
        #   => returns no bundle of errors or successful results
        # Hence risk of orphaned tasks

        #   [Also Do check out task groups(secion 17)]
        #   [  => also fails quickly]
        #   [ => but offers better errors and handling cleanups]
        print("1. Default behavior (exception propagates):")
        try:
            results = await asyncio.gather(
                may_fail("Task-A", False),
                may_fail("Task-B", True),  # This will fail
                may_fail("Task-C", False),
            )
        except ValueError as e:
            print(f"   Exception caught: {e}")

        # With return_exceptions=True, exceptions are returned as results
        # when return_exceptions=True:
        #   => Every awaitable in that gather finishes
        #   => each result is either the result_value or the exception
        print("\n2. With return_exceptions=True:")
        results = await asyncio.gather(
            may_fail("Task-A", False),
            may_fail("Task-B", True),
            may_fail("Task-C", False),
            return_exceptions=True,
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   Task {i}: Exception - {result}")
            else:
                print(f"   Task {i}: Success - {result}")

    await gather_exception_handling()

    # ------------------------------------------------------------------------------
    # 5.3 Nested Gather
    # ------------------------------------------------------------------------------

    print_subsection("5.3 Nested Gather")

    async def nested_gather():
        """Demonstrate nested gather calls."""

        async def api_call(endpoint: str) -> str:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            return f"Data from {endpoint}"

        # Fetch user data and posts concurrently
        async def get_user_data(user_id: int):
            results = await asyncio.gather(
                api_call(f"/users/{user_id}"),
                api_call(f"/users/{user_id}/profile"),
                api_call(f"/users/{user_id}/settings"),
            )
            return {"user_id": user_id, "data": results}

        # Fetch data for multiple users concurrently
        all_user_data = await asyncio.gather(
            get_user_data(1),
            get_user_data(2),
            get_user_data(3),
        )

        for user_data in all_user_data:
            print(f"User {user_data['user_id']}: {user_data['data']}")

    await nested_gather()


# ================================================================================
# SECTION 6: WAITING FOR TASKS - asyncio.wait(), wait_for()
# ================================================================================


async def _6_waiting_for_tasks():
    separator("6. WAITING FOR TASKS - asyncio.wait(), wait_for()")

    # ------------------------------------------------------------------------------
    # 6.1 asyncio.wait() - Flexible Waiting
    # ------------------------------------------------------------------------------

    print_subsection("6.1 asyncio.wait() - Flexible Waiting")

    async def worker_task(name: str, duration: float) -> str:
        """A worker task that takes some time."""
        await asyncio.sleep(duration)
        return f"{name} completed in {duration}s"

    async def wait_demo():
        """Demonstrate asyncio.wait() with different options."""

        # Create tasks
        tasks = [
            asyncio.create_task(worker_task("Task-A", 1.0), name="Task-A"),
            asyncio.create_task(worker_task("Task-B", 0.5), name="Task-B"),
            asyncio.create_task(worker_task("Task-C", 1.5), name="Task-C"),
            asyncio.create_task(worker_task("Task-D", 0.3), name="Task-D"),
        ]

        # Wait for ALL tasks to complete (default)
        print("1. WAIT_ALL_COMPLETED:")
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        print(f"   Done: {len(done)}, Pending: {len(pending)}")
        for task in done:
            print(f"   - {task.get_name()}: {task.result()}")

    async def wait_first_completed():
        """Wait for the first task to complete."""
        tasks = [
            asyncio.create_task(worker_task("Fast", 0.3), name="Fast"),
            asyncio.create_task(worker_task("Medium", 0.6), name="Medium"),
            asyncio.create_task(worker_task("Slow", 1.0), name="Slow"),
        ]

        print("\n2. FIRST_COMPLETED:")
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        print(f"   Done: {len(done)}, Pending: {len(pending)}")
        print(f"   First completed: {[t.get_name() for t in done]}")
        print(f"   Still pending: {[t.get_name() for t in pending]}")

        for task in pending:
            task_name = task.get_name()

            # Request cancellation
            cancel_accepted = task.cancel()

            # Immediate state (before await)
            print(f"   [{task_name}] Immediate Results:")
            print(f"       cancel() returned : {cancel_accepted}")
            print(f"       cancelled()       : {task.cancelled()}")
            print(f"       done()            : {task.done()}")

            # Wait for completion
            print(f"   [{task_name}] Waiting to finish...")
            try:
                await task
                print("       Completed normally")
                print(f"       done(): {task.done()}")
            except asyncio.CancelledError:
                print("       Cancellation complete")
                print(f"       cancelled(): {task.cancelled()}")

            print()  # Empty line between tasks

    async def wait_first_exception():
        """Wait for the first exception or all to complete."""

        async def may_raise(name: str, delay: float, should_raise: bool):
            await asyncio.sleep(delay)
            if should_raise:
                raise ValueError(f"{name} error!")
            return f"{name} OK"

        tasks = [
            asyncio.create_task(may_raise("T1", 1.0, False), name="T1"),
            asyncio.create_task(may_raise("T2", 0.5, True), name="T2"),  # Will raise
            asyncio.create_task(may_raise("T3", 0.3, False), name="T3"),
        ]

        print("\n3. FIRST_EXCEPTION:")
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

        # Handle completed tasks
        print(f"   Done: {len(done)}, Pending: {len(pending)}")
        print()

        print("   === Completed Tasks ===")
        for task in done:
            task_name = task.get_name()
            if task.exception():
                print(f"   [{task_name}] Exception: {task.exception()}")
            else:
                print(f"   [{task_name}] Result: {task.result()}")

        # Cleanup pending tasks
        print()
        print("   === Cleaning Up Pending Tasks ===")
        for task in pending:
            task_name = task.get_name()
            task.cancel()
            try:
                await task
                print(f"   [{task_name}] Completed normally")
            except asyncio.CancelledError:
                print(f"   [{task_name}] Cancelled")

    await wait_demo()
    await wait_first_completed()
    await wait_first_exception()

    # ------------------------------------------------------------------------------
    # 6.2 asyncio.wait_for() - Timeout on Single Awaitable
    # ------------------------------------------------------------------------------

    print_subsection("6.2 asyncio.wait_for() - Timeout on Single Awaitable")

    async def wait_for_demo():
        """Demonstrate wait_for with timeout."""

        async def slow_operation():
            await asyncio.sleep(5)
            return "Completed!"

        # Wait with timeout
        print("Waiting for slow operation with 1 second timeout...")
        try:
            result = await asyncio.wait_for(slow_operation(), timeout=1.0)
            print(
                f"Result: {result} [SHOULDN'T HAVE REACHED HERE]"
            )  # Shouldn't reach here
        except asyncio.TimeoutError:
            print("Operation timed out!")  # Should reach here

        # Successful wait
        async def fast_operation():
            await asyncio.sleep(0.3)
            return "Fast result!"

        print("\nWaiting for fast operation with 1 second timeout...")
        try:
            result = await asyncio.wait_for(fast_operation(), timeout=1.0)
            print(f"Result: {result}")  # Should reach here
        except asyncio.TimeoutError:
            print(
                "Operation timed out! [SHOULDN'T HAVE REACHED HERE]"
            )  # Shouldn't reach here

    await wait_for_demo()

    # ------------------------------------------------------------------------------
    # 6.3 as_completed() - Process Results as They Complete
    # ------------------------------------------------------------------------------

    print_subsection("6.3 as_completed() - Process Results as They Complete")

    async def as_completed_demo():
        """Process tasks as they complete, not in order."""

        async def fetch_with_delay(url: str, delay: float):
            await asyncio.sleep(delay)
            return f"Fetched {url} in {delay}s"

        tasks = [
            fetch_with_delay("url1", 1.5),  # yielded last
            fetch_with_delay("url2", 0.3),  # yielded first
            fetch_with_delay("url3", 0.8),  # yielded third
            fetch_with_delay("url4", 0.5),  # yielded second
        ]

        print("Processing results as they complete:")

        # as_completed yields futures as they complete
        for i, coro in enumerate(asyncio.as_completed(tasks)):
            result = await coro
            print(f"  {i + 1}. {result}")

    await as_completed_demo()


# # ================================================================================
# # SECTION 7: TIMEOUTS AND CANCELLATION
# # ================================================================================

# separator("7. TIMEOUTS AND CANCELLATION")

# # ------------------------------------------------------------------------------
# # 7.1 asyncio.timeout() - Context Manager (Python 3.11+)
# # ------------------------------------------------------------------------------

# print_subsection("7.1 asyncio.timeout() - Context Manager (Python 3.11+)")


# async def timeout_context_manager():
#     """Use async timeout context manager."""

#     async def long_operation():
#         await asyncio.sleep(5)
#         return "Done"

#     # Using timeout context manager
#     try:
#         async with asyncio.timeout(1.0):
#             result = await long_operation()
#             print(f"Result: {result}")
#     except TimeoutError:
#         print("Operation timed out!")

#     # Timeout that doesn't trigger
#     try:
#         async with asyncio.timeout(2.0):
#             await asyncio.sleep(0.5)
#             print("Completed within timeout!")
#     except TimeoutError:
#         print("This won't be reached")

#     # Using timeout_at for absolute deadline
#     loop = asyncio.get_running_loop()
#     deadline = loop.time() + 1.0

#     try:
#         async with asyncio.timeout_at(deadline):
#             await asyncio.sleep(2.0)
#     except TimeoutError:
#         print("Deadline exceeded!")


# asyncio.run(timeout_context_manager())


# # ------------------------------------------------------------------------------
# # 7.2 Manual Timeout Pattern
# # ------------------------------------------------------------------------------

# print_subsection("7.2 Manual Timeout Pattern")


# async def manual_timeout():
#     """Implement timeout manually for more control."""

#     async def worker():
#         await asyncio.sleep(3)
#         return "Worker result"

#     # Create the task
#     task = asyncio.create_task(worker())

#     # Create a timeout task
#     timeout_duration = 1.0

#     try:
#         # Wait for either completion or timeout
#         done, pending = await asyncio.wait({task}, timeout=timeout_duration)

#         if task in done:
#             print(f"Task completed: {task.result()}")
#         else:
#             print("Task timed out, cancelling...")
#             task.cancel()
#             try:
#                 await task
#             except asyncio.CancelledError:
#                 print("Task cancelled successfully")

#     except Exception as e:
#         print(f"Error: {e}")


# asyncio.run(manual_timeout())


# ================================================================================
# SECTION 8: ASYNC SLEEP VS TIME SLEEP
# ================================================================================


async def _8_sleep_comparison():
    """Compare asyncio.sleep() vs time.sleep()."""

    separator("8. ASYNC SLEEP VS TIME SLEEP")

    # time.sleep() - BLOCKS the entire event loop!
    print("1. time.sleep() - BLOCKING (Don't do this!)")

    async def blocking_task(name: str):
        print(f"{name}: Starting")
        time.sleep(1)  # This blocks everything!
        print(f"{name}: Done")

    start = time.perf_counter()
    await asyncio.gather(
        blocking_task("A"),
        blocking_task("B"),
        blocking_task("C"),
    )
    print(f"Total time (blocking): {time.perf_counter() - start:.2f}s")

    # asyncio.sleep() - Allows other tasks to run
    print("\n2. asyncio.sleep() - NON-BLOCKING (Correct!)")

    async def async_task(name: str):
        print(f"{name}: Starting")
        await asyncio.sleep(1)  # Yields to other tasks
        print(f"{name}: Done")

    start = time.perf_counter()
    await asyncio.gather(
        async_task("A"),
        async_task("B"),
        async_task("C"),
    )
    print(f"Total time (non-blocking): {time.perf_counter() - start:.2f}s")


# # ================================================================================
# # SECTION 9: SYNCHRONIZATION PRIMITIVES
# # ================================================================================

# separator("9. SYNCHRONIZATION PRIMITIVES")

# # ------------------------------------------------------------------------------
# # 9.1 asyncio.Lock
# # ------------------------------------------------------------------------------

# print_subsection("9.1 asyncio.Lock - Mutual Exclusion")


# async def lock_demo():
#     """Demonstrate asyncio.Lock for mutual exclusion."""

#     # Shared resource
#     shared_counter = {"value": 0}
#     lock = asyncio.Lock()

#     async def increment_without_lock(name: str):
#         """Increment without lock (may cause race conditions)."""
#         for _ in range(1000):
#             current = shared_counter["value"]
#             await asyncio.sleep(0)  # Yield to simulate real async work
#             shared_counter["value"] = current + 1

#     async def increment_with_lock(name: str):
#         """Increment with lock (safe)."""
#         for _ in range(1000):
#             async with lock:  # Acquire lock
#                 current = shared_counter["value"]
#                 await asyncio.sleep(0)
#                 shared_counter["value"] = current + 1

#     # Test without lock
#     shared_counter["value"] = 0
#     await asyncio.gather(
#         increment_without_lock("A"),
#         increment_without_lock("B"),
#     )
#     print(f"Without lock: {shared_counter['value']} (expected 2000)")

#     # Test with lock
#     shared_counter["value"] = 0
#     await asyncio.gather(
#         increment_with_lock("A"),
#         increment_with_lock("B"),
#     )
#     print(f"With lock: {shared_counter['value']} (expected 2000)")

#     # Manual lock acquisition
#     print("\nManual lock acquisition:")
#     lock2 = asyncio.Lock()

#     await lock2.acquire()
#     print(f"Lock acquired: {lock2.locked()}")
#     lock2.release()
#     print(f"Lock released: {lock2.locked()}")


# asyncio.run(lock_demo())


# # ------------------------------------------------------------------------------
# # 9.2 asyncio.Semaphore
# # ------------------------------------------------------------------------------

# print_subsection("9.2 asyncio.Semaphore - Limiting Concurrency")


# async def semaphore_demo():
#     """Demonstrate asyncio.Semaphore for limiting concurrent access."""

#     # Limit to 3 concurrent operations
#     semaphore = asyncio.Semaphore(3)

#     async def limited_task(name: str):
#         """A task that respects the semaphore limit."""
#         print(f"{name}: Waiting for semaphore...")

#         async with semaphore:
#             print(f"{name}: Acquired semaphore, working...")
#             await asyncio.sleep(1)
#             print(f"{name}: Done, releasing semaphore")

#     # Start 6 tasks, but only 3 can run at a time
#     start = time.perf_counter()
#     await asyncio.gather(*[limited_task(f"Task-{i}") for i in range(6)])

#     elapsed = time.perf_counter() - start
#     print(f"\nTotal time: {elapsed:.2f}s (6 tasks, 3 concurrent, ~2 batches)")


# asyncio.run(semaphore_demo())


# # BoundedSemaphore example
# async def bounded_semaphore_demo():
#     """Demonstrate BoundedSemaphore (prevents over-release)."""

#     sem = asyncio.BoundedSemaphore(2)

#     print("BoundedSemaphore prevents releasing more than acquired:")
#     await sem.acquire()
#     await sem.acquire()
#     sem.release()
#     sem.release()

#     try:
#         sem.release()  # This will raise!
#     except ValueError as e:
#         print(f"Error on extra release: {e}")


# asyncio.run(bounded_semaphore_demo())


# # ------------------------------------------------------------------------------
# # 9.3 asyncio.Event
# # ------------------------------------------------------------------------------

# print_subsection("9.3 asyncio.Event - Signaling Between Tasks")


# async def event_demo():
#     """Demonstrate asyncio.Event for task signaling."""

#     event = asyncio.Event()

#     async def waiter(name: str):
#         """Wait for the event to be set."""
#         print(f"{name}: Waiting for event...")
#         await event.wait()
#         print(f"{name}: Event received! Proceeding...")

#     async def setter():
#         """Set the event after some delay."""
#         print("Setter: Preparing data...")
#         await asyncio.sleep(1)
#         print("Setter: Data ready! Setting event...")
#         event.set()

#     # Start waiters and setter
#     await asyncio.gather(
#         waiter("Waiter-1"),
#         waiter("Waiter-2"),
#         waiter("Waiter-3"),
#         setter(),
#     )

#     print(f"\nEvent is set: {event.is_set()}")

#     # Clear the event
#     event.clear()
#     print(f"After clear, event is set: {event.is_set()}")


# asyncio.run(event_demo())


# # ------------------------------------------------------------------------------
# # 9.4 asyncio.Condition
# # ------------------------------------------------------------------------------

# print_subsection("9.4 asyncio.Condition - Complex Synchronization")


# async def condition_demo():
#     """Demonstrate asyncio.Condition for complex synchronization."""

#     condition = asyncio.Condition()
#     shared_data = {"ready": False, "data": None}

#     async def producer():
#         """Produce data and notify consumers."""
#         await asyncio.sleep(0.5)  # Simulate preparation

#         async with condition:
#             shared_data["data"] = "Important Data"
#             shared_data["ready"] = True
#             print("Producer: Data is ready, notifying all...")
#             condition.notify_all()

#     async def consumer(name: str):
#         """Wait for data to be ready."""
#         async with condition:
#             # Wait until condition is met
#             await condition.wait_for(lambda: shared_data["ready"])
#             print(f"{name}: Received data: {shared_data['data']}")

#     await asyncio.gather(
#         consumer("Consumer-1"),
#         consumer("Consumer-2"),
#         producer(),
#     )


# asyncio.run(condition_demo())


# # ------------------------------------------------------------------------------
# # 9.5 asyncio.Barrier (Python 3.11+)
# # ------------------------------------------------------------------------------

# print_subsection("9.5 asyncio.Barrier (Python 3.11+)")


# async def barrier_demo():
#     """Demonstrate asyncio.Barrier for synchronizing multiple tasks."""

#     # Barrier for 3 parties
#     barrier = asyncio.Barrier(3)

#     async def worker(name: str, delay: float):
#         print(f"{name}: Working (delay={delay}s)...")
#         await asyncio.sleep(delay)

#         print(f"{name}: Waiting at barrier...")
#         await barrier.wait()

#         print(f"{name}: Passed barrier, continuing...")

#     await asyncio.gather(
#         worker("Fast", 0.3),
#         worker("Medium", 0.6),
#         worker("Slow", 1.0),
#     )


# asyncio.run(barrier_demo())


# # ================================================================================
# # SECTION 10: ASYNC QUEUES - PRODUCER/CONSUMER PATTERN
# # ================================================================================

# separator("10. ASYNC QUEUES - PRODUCER/CONSUMER PATTERN")

# # ------------------------------------------------------------------------------
# # 10.1 Basic Queue Usage
# # ------------------------------------------------------------------------------

# print_subsection("10.1 Basic Queue Usage")


# async def basic_queue_demo():
#     """Basic asyncio.Queue usage."""

#     queue = asyncio.Queue()

#     # Put items
#     await queue.put("item1")
#     await queue.put("item2")
#     queue.put_nowait("item3")  # Non-blocking put

#     print(f"Queue size: {queue.qsize()}")
#     print(f"Queue empty: {queue.empty()}")

#     # Get items
#     item1 = await queue.get()
#     item2 = queue.get_nowait()  # Non-blocking get

#     print(f"Got: {item1}, {item2}")

#     # Mark task as done (for join())
#     queue.task_done()
#     queue.task_done()


# asyncio.run(basic_queue_demo())


# # ------------------------------------------------------------------------------
# # 10.2 Producer/Consumer Pattern
# # ------------------------------------------------------------------------------

# print_subsection("10.2 Producer/Consumer Pattern")


# async def producer_consumer_demo():
#     """Classic producer/consumer pattern with async queue."""

#     queue = asyncio.Queue(maxsize=5)  # Bounded queue

#     async def producer(name: str, count: int):
#         """Produce items and put them in the queue."""
#         for i in range(count):
#             item = f"{name}-item-{i}"
#             await queue.put(item)  # Blocks if queue is full
#             print(f"Produced: {item}")
#             await asyncio.sleep(random.uniform(0.1, 0.3))

#         print(f"{name}: Done producing")

#     async def consumer(name: str):
#         """Consume items from the queue."""
#         while True:
#             try:
#                 item = await asyncio.wait_for(queue.get(), timeout=1.0)
#                 print(f"{name} consumed: {item}")
#                 queue.task_done()
#                 await asyncio.sleep(random.uniform(0.2, 0.5))
#             except asyncio.TimeoutError:
#                 print(f"{name}: Timeout, stopping...")
#                 break

#     # Start producers and consumers
#     await asyncio.gather(
#         producer("P1", 5),
#         producer("P2", 5),
#         consumer("C1"),
#         consumer("C2"),
#     )

#     print(f"Final queue size: {queue.qsize()}")


# asyncio.run(producer_consumer_demo())


# # ------------------------------------------------------------------------------
# # 10.3 Queue with Join
# # ------------------------------------------------------------------------------

# print_subsection("10.3 Queue with Join (Wait for All Items)")


# async def queue_join_demo():
#     """Wait for all items to be processed using join()."""

#     queue = asyncio.Queue()

#     async def worker(name: str):
#         """Process items until None is received."""
#         while True:
#             item = await queue.get()
#             if item is None:
#                 queue.task_done()
#                 print(f"{name}: Received stop signal")
#                 break

#             print(f"{name}: Processing {item}...")
#             await asyncio.sleep(0.3)
#             queue.task_done()

#     # Start workers
#     workers = [asyncio.create_task(worker(f"Worker-{i}")) for i in range(3)]

#     # Add items to process
#     for i in range(9):
#         await queue.put(f"Task-{i}")

#     # Add stop signals for each worker
#     for _ in workers:
#         await queue.put(None)

#     # Wait for all items to be processed
#     await queue.join()
#     print("All items processed!")

#     # Wait for workers to finish
#     await asyncio.gather(*workers)


# asyncio.run(queue_join_demo())


# # ------------------------------------------------------------------------------
# # 10.4 Priority Queue and LIFO Queue
# # ------------------------------------------------------------------------------

# print_subsection("10.4 Priority Queue and LIFO Queue")


# async def special_queues_demo():
#     """Demonstrate PriorityQueue and LifoQueue."""

#     # Priority Queue (lowest priority first)
#     print("Priority Queue:")
#     pq = asyncio.PriorityQueue()

#     # Items: (priority, data)
#     await pq.put((3, "Low priority"))
#     await pq.put((1, "High priority"))
#     await pq.put((2, "Medium priority"))

#     while not pq.empty():
#         priority, item = await pq.get()
#         print(f"  Priority {priority}: {item}")

#     # LIFO Queue (Stack)
#     print("\nLIFO Queue (Stack):")
#     lifo = asyncio.LifoQueue()

#     await lifo.put("First")
#     await lifo.put("Second")
#     await lifo.put("Third")

#     while not lifo.empty():
#         item = await lifo.get()
#         print(f"  Popped: {item}")


# asyncio.run(special_queues_demo())


# # ================================================================================
# # SECTION 11: ASYNC CONTEXT MANAGERS
# # ================================================================================

# separator("11. ASYNC CONTEXT MANAGERS")

# # ------------------------------------------------------------------------------
# # 11.1 Using Async Context Managers
# # ------------------------------------------------------------------------------

# print_subsection("11.1 Using Async Context Managers")


# async def async_context_usage():
#     """Show how to use async context managers."""

#     # asyncio.Lock as context manager
#     lock = asyncio.Lock()

#     async with lock:
#         print("Lock acquired via context manager")

#     print("Lock released automatically")

#     # asyncio.Semaphore as context manager
#     sem = asyncio.Semaphore(2)

#     async with sem:
#         print("Semaphore acquired")

#     # Timeout context manager (Python 3.11+)
#     async with asyncio.timeout(1.0):
#         await asyncio.sleep(0.5)
#         print("Completed within timeout context")


# asyncio.run(async_context_usage())


# # ------------------------------------------------------------------------------
# # 11.2 Creating Custom Async Context Managers
# # ------------------------------------------------------------------------------

# print_subsection("11.2 Creating Custom Async Context Managers")


# # Method 1: Using a class
# class AsyncResource:
#     """An async resource with async context manager support."""

#     def __init__(self, name: str):
#         self.name = name
#         self.connected = False

#     async def __aenter__(self):
#         """Async enter - called when entering 'async with'."""
#         print(f"{self.name}: Connecting...")
#         await asyncio.sleep(0.2)  # Simulate connection
#         self.connected = True
#         print(f"{self.name}: Connected!")
#         return self

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         """Async exit - called when exiting 'async with'."""
#         print(f"{self.name}: Disconnecting...")
#         await asyncio.sleep(0.1)  # Simulate disconnection
#         self.connected = False
#         print(f"{self.name}: Disconnected!")

#         # Return True to suppress exception, False to propagate
#         return False

#     async def do_something(self):
#         """Perform an operation."""
#         if not self.connected:
#             raise RuntimeError("Not connected!")
#         print(f"{self.name}: Doing something...")
#         await asyncio.sleep(0.1)


# async def class_based_context_demo():
#     """Demonstrate class-based async context manager."""

#     async with AsyncResource("Database") as db:
#         await db.do_something()
#         print(f"Connected: {db.connected}")

#     print("After context: should be disconnected")


# asyncio.run(class_based_context_demo())

# # Method 2: Using contextlib.asynccontextmanager
# from contextlib import asynccontextmanager


# @asynccontextmanager
# async def async_connection(name: str):
#     """Create an async context manager using decorator."""
#     print(f"{name}: Opening connection...")
#     connection = {"name": name, "open": True}
#     await asyncio.sleep(0.2)

#     try:
#         yield connection  # Control passes to the with block
#     finally:
#         print(f"{name}: Closing connection...")
#         connection["open"] = False
#         await asyncio.sleep(0.1)
#         print(f"{name}: Connection closed")


# async def decorator_context_demo():
#     """Demonstrate decorator-based async context manager."""

#     async with async_connection("API") as conn:
#         print(f"Using connection: {conn}")

#     print("Context exited")


# asyncio.run(decorator_context_demo())


# # ================================================================================
# # SECTION 12: ASYNC ITERATORS AND GENERATORS
# # ================================================================================

# separator("12. ASYNC ITERATORS AND GENERATORS")

# # ------------------------------------------------------------------------------
# # 12.1 Async Iterators (Using Class)
# # ------------------------------------------------------------------------------

# print_subsection("12.1 Async Iterators (Using Class)")


# class AsyncRange:
#     """An async iterator that yields numbers with delays."""

#     def __init__(self, start: int, end: int, delay: float = 0.1):
#         self.start = start
#         self.end = end
#         self.delay = delay
#         self.current = start

#     def __aiter__(self):
#         """Return the async iterator."""
#         return self

#     async def __anext__(self):
#         """Get the next value asynchronously."""
#         if self.current >= self.end:
#             raise StopAsyncIteration

#         value = self.current
#         self.current += 1
#         await asyncio.sleep(self.delay)
#         return value


# async def async_iterator_demo():
#     """Demonstrate async iterator usage."""

#     print("Iterating with async for:")
#     async for num in AsyncRange(0, 5):
#         print(f"  Got: {num}")


# asyncio.run(async_iterator_demo())


# # ------------------------------------------------------------------------------
# # 12.2 Async Generators (Using async def with yield)
# # ------------------------------------------------------------------------------

# print_subsection("12.2 Async Generators")


# async def async_countdown(start: int):
#     """An async generator that counts down."""
#     for i in range(start, 0, -1):
#         await asyncio.sleep(0.3)
#         yield i
#     yield "Liftoff!"


# async def async_data_stream(count: int):
#     """Simulate a data stream with async generator."""
#     for i in range(count):
#         await asyncio.sleep(0.1)
#         yield {"id": i, "data": f"Chunk-{i}", "timestamp": time.time()}


# async def async_generator_demo():
#     """Demonstrate async generators."""

#     print("Countdown:")
#     async for value in async_countdown(5):
#         print(f"  {value}")

#     print("\nData stream:")
#     async for chunk in async_data_stream(5):
#         print(f"  Received: {chunk}")


# asyncio.run(async_generator_demo())


# # ------------------------------------------------------------------------------
# # 12.3 Async Comprehensions
# # ------------------------------------------------------------------------------

# print_subsection("12.3 Async Comprehensions")


# async def async_comprehensions_demo():
#     """Demonstrate async list/set/dict comprehensions."""

#     async def get_value(x):
#         await asyncio.sleep(0.05)
#         return x * 2

#     async def async_range(n):
#         for i in range(n):
#             await asyncio.sleep(0.05)
#             yield i

#     # Async list comprehension
#     values = [await get_value(i) async for i in async_range(5)]
#     print(f"Async list comprehension: {values}")

#     # Async set comprehension
#     value_set = {await get_value(i) async for i in async_range(5)}
#     print(f"Async set comprehension: {value_set}")

#     # Async dict comprehension
#     value_dict = {i: await get_value(i) async for i in async_range(5)}
#     print(f"Async dict comprehension: {value_dict}")

#     # Mixing async and sync
#     squared = [x**2 for x in [await get_value(i) for i in range(5)]]
#     print(f"Nested comprehension: {squared}")


# asyncio.run(async_comprehensions_demo())


# ================================================================================
# SECTION 13: RUNNING BLOCKING/SYNC CODE IN ASYNC CONTEXT
# ================================================================================


# moved this fn to the module level
# so that ProcessPoolExecutor can pickle it and share it between processes


def cpu_bound_operation(n: int) -> int:
    """A CPU-bound operation."""
    print(f"Computing sum of squares up to {n}...")
    result = sum(i * i for i in range(n))
    print("Computation complete!")
    return result


async def _13_running_blocking_sync_code_in_async_context():
    separator("13. RUNNING BLOCKING/SYNC CODE IN ASYNC CONTEXT")

    # ------------------------------------------------------------------------------
    # 13.1 run_in_executor() - Running Blocking Code
    # ------------------------------------------------------------------------------

    print_subsection("13.1 run_in_executor() - Running Blocking Code")

    # ThreadPoolExecutor works fine with nested functions
    # because threads share the same memory space and don't need to pickle the function.
    def blocking_io_operation(name: str, duration: float) -> str:
        """A blocking I/O operation (e.g., file I/O, network call)."""
        print(f"{name}: Starting blocking operation...")
        time.sleep(duration)  # Simulates blocking I/O
        print(f"{name}: Completed!")
        return f"{name} result"

    # """
    # ProcessPoolExecutor needs to pickle the function to send it to child processes,
    # But Local/nested functions cannot be pickled
    # bcz they don't have a module-level reference
    # Hence has to move this fn to the module level (outside any function).
    # """
    # def cpu_bound_operation(n: int) -> int:
    #     """A CPU-bound operation."""
    #     print(f"Computing sum of squares up to {n}...")
    #     result = sum(i * i for i in range(n))
    #     print("Computation complete!")
    #     return result

    async def run_in_executor_demo():
        """Run blocking code in a thread pool executor."""

        loop = asyncio.get_running_loop()

        # Using ThreadPoolExecutor (for I/O-bound tasks)
        # These run in separate threads, not blocking the event loop,
        print("Running blocking I/O operations concurrently:")
        start = time.perf_counter()

        results = await asyncio.gather(
            # executor=None uses default ThreadPoolExecutor
            loop.run_in_executor(None, blocking_io_operation, "Task-1", 1),
            loop.run_in_executor(None, blocking_io_operation, "Task-2", 1),
            loop.run_in_executor(None, blocking_io_operation, "Task-3", 1),
        )

        # """use below for custom"""
        # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        #     results = await asyncio.gather(
        #         loop.run_in_executor(pool, blocking_io_operation, "Task-1", 1),
        #         loop.run_in_executor(pool, blocking_io_operation, "Task-2", 1),
        #         loop.run_in_executor(pool, blocking_io_operation, "Task-3", 1),
        #     )

        elapsed = time.perf_counter() - start
        print(f"All completed in {elapsed:.2f}s")
        print(f"Results: {results}")

        # Using ProcessPoolExecutor (for CPU-bound tasks)
        print("\nRunning CPU-bound operation in process pool:")

        with concurrent.futures.ProcessPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, cpu_bound_operation, 1000000)
            print(f"CPU result: {result}")

    print(f"__name__ is {__name__}")
    # Note: Must be in __main__ for ProcessPoolExecutor
    #     Will ensure this will be run only by main process, not by our child processes
    #     otherwise child processes whle importing function from this module
    #     will run this module again and end up running it again
    #     and it will be stuck in infinite loop
    # Guard Not required for to_thread() or ThreadPoolExecutor ==> But still a good practice
    #     bcz All threads in a process share the SAME objects
    #     Hence No import needed!
    if __name__ == "__main__":
        await run_in_executor_demo()

    # ------------------------------------------------------------------------------
    # 13.2 to_thread() - Simpler API (Python 3.9+)
    # ------------------------------------------------------------------------------

    print_subsection("13.2 to_thread() - Simpler API (Python 3.9+)")

    async def to_thread_demo():
        """
        Use asyncio.to_thread() for running sync code.
        Will wrap synchronous function with a future and make it awaitable
        """

        def sync_function(name: str, value: int) -> str:
            """A synchronous function jiska async available nhi hai
            So will do a jugaad => will run it in thread."""

            prefx = f"{threading.current_thread().name}:{name}"
            print(
                f"{prefx}: Sync Function is starting blocking operation...", flush=True
            )
            time.sleep(0.5)
            print(f"{prefx}: Completed! returning result", flush=True)
            return f"{prefx}: {value * 2}"

        # to_thread is simpler than run_in_executor
        results = await asyncio.gather(
            asyncio.to_thread(sync_function, "A", 1),
            asyncio.to_thread(sync_function, "B", 2),
            asyncio.to_thread(sync_function, "C", 3),
        )

        print(f"Results: {results}")

    await to_thread_demo()

    # # ------------------------------------------------------------------------------
    # # 13.3 Creating Async Wrappers for Sync Code
    # # ------------------------------------------------------------------------------

    # print_subsection("13.3 Creating Async Wrappers for Sync Code")

    # def make_async(func):
    #     """Decorator to make a sync function async."""

    #     @functools.wraps(func)
    #     async def wrapper(*args, **kwargs):
    #         loop = asyncio.get_running_loop()
    #         return await loop.run_in_executor(
    #             None, functools.partial(func, *args, **kwargs)
    #         )

    #     return wrapper

    # # Apply decorator to sync function
    # @make_async
    # def sync_download(url: str) -> str:
    #     """Simulated synchronous download."""
    #     time.sleep(0.5)
    #     return f"Downloaded content from {url}"

    # async def wrapper_demo():
    #     """Use the async wrapper."""

    #     results = await asyncio.gather(
    #         sync_download("http://example.com/1"),
    #         sync_download("http://example.com/2"),
    #         sync_download("http://example.com/3"),
    #     )

    #     for result in results:
    #         print(f"  {result}")

    # asyncio.run(wrapper_demo())


# # ================================================================================
# # SECTION 14: STREAMS - TCP CLIENT/SERVER
# # ================================================================================

# separator("14. STREAMS - TCP CLIENT/SERVER")

# # ------------------------------------------------------------------------------
# # 14.1 TCP Echo Server
# # ------------------------------------------------------------------------------

# print_subsection("14.1 TCP Echo Server Example")


# async def handle_echo_client(
#     reader: asyncio.StreamReader, writer: asyncio.StreamWriter
# ):
#     """Handle an echo client connection."""
#     addr = writer.get_extra_info("peername")
#     print(f"Connected: {addr}")

#     while True:
#         data = await reader.read(1024)
#         if not data:
#             break

#         message = data.decode()
#         print(f"Received from {addr}: {message}")

#         # Echo back
#         writer.write(data)
#         await writer.drain()

#     print(f"Disconnected: {addr}")
#     writer.close()
#     await writer.wait_closed()


# async def run_echo_server():
#     """Run the echo server."""
#     server = await asyncio.start_server(handle_echo_client, "127.0.0.1", 8888)

#     addr = server.sockets[0].getsockname()
#     print(f"Serving on {addr}")

#     async with server:
#         await server.serve_forever()


# # To run: asyncio.run(run_echo_server())
# print("Echo server code defined (not running in demo)")


# # ------------------------------------------------------------------------------
# # 14.2 TCP Client
# # ------------------------------------------------------------------------------

# print_subsection("14.2 TCP Client Example")


# async def tcp_echo_client(message: str):
#     """Connect to echo server and send a message."""
#     reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

#     print(f"Sending: {message}")
#     writer.write(message.encode())
#     await writer.drain()

#     data = await reader.read(1024)
#     print(f"Received: {data.decode()}")

#     writer.close()
#     await writer.wait_closed()


# # To run: asyncio.run(tcp_echo_client("Hello, World!"))
# print("TCP client code defined (not running in demo)")


# # ------------------------------------------------------------------------------
# # 14.3 HTTP-like Request Example
# # ------------------------------------------------------------------------------

# print_subsection("14.3 Simple HTTP Request Example")


# async def simple_http_get(host: str, path: str = "/") -> str:
#     """Make a simple HTTP GET request."""
#     reader, writer = await asyncio.open_connection(host, 80)

#     # Send HTTP request
#     request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
#     writer.write(request.encode())
#     await writer.drain()

#     # Read response
#     response = await reader.read()

#     writer.close()
#     await writer.wait_closed()

#     return response.decode()


# # Example usage (uncomment to run):
# # response = asyncio.run(simple_http_get("example.com"))
# # print(response[:500])  # Print first 500 chars
# print("HTTP client code defined (not running in demo)")


# # ================================================================================
# # SECTION 15: SUBPROCESSES
# # ================================================================================

# separator("15. SUBPROCESSES")

# # ------------------------------------------------------------------------------
# # 15.1 Running Subprocesses
# # ------------------------------------------------------------------------------

# print_subsection("15.1 Running Subprocesses")


# async def subprocess_demo():
#     """Demonstrate running subprocesses with asyncio."""

#     # Run a simple command
#     print("1. Simple command execution:")

#     process = await asyncio.create_subprocess_exec(
#         "echo", "Hello from subprocess!", stdout=asyncio.subprocess.PIPE
#     )

#     stdout, _ = await process.communicate()
#     print(f"   Output: {stdout.decode().strip()}")
#     print(f"   Return code: {process.returncode}")

#     # Run with shell
#     print("\n2. Shell command:")

#     process = await asyncio.create_subprocess_shell(
#         'echo "Current directory: $(pwd)"', stdout=asyncio.subprocess.PIPE
#     )

#     stdout, _ = await process.communicate()
#     print(f"   Output: {stdout.decode().strip()}")

#     # Multiple concurrent subprocesses
#     print("\n3. Concurrent subprocesses:")

#     async def run_command(cmd: str):
#         process = await asyncio.create_subprocess_shell(
#             cmd, stdout=asyncio.subprocess.PIPE
#         )
#         stdout, _ = await process.communicate()
#         return stdout.decode().strip()

#     commands = ['echo "Process 1"', 'echo "Process 2"', 'echo "Process 3"']
#     results = await asyncio.gather(*[run_command(cmd) for cmd in commands])

#     for result in results:
#         print(f"   {result}")


# asyncio.run(subprocess_demo())


# # ================================================================================
# # SECTION 16: ERROR HANDLING IN ASYNCIO
# # ================================================================================

# separator("16. ERROR HANDLING IN ASYNCIO")

# # ------------------------------------------------------------------------------
# # 16.1 Exception Handling in Coroutines
# # ------------------------------------------------------------------------------

# print_subsection("16.1 Exception Handling in Coroutines")


# async def may_raise_error(should_fail: bool):
#     """A coroutine that may raise an error."""
#     await asyncio.sleep(0.1)
#     if should_fail:
#         raise ValueError("Something went wrong!")
#     return "Success!"


# async def exception_handling_demo():
#     """Demonstrate exception handling patterns."""

#     # Basic try/except in async
#     print("1. Basic try/except:")
#     try:
#         result = await may_raise_error(True)
#     except ValueError as e:
#         print(f"   Caught exception: {e}")

#     # Exception in tasks
#     print("\n2. Exception in task (must await to see it):")
#     task = asyncio.create_task(may_raise_error(True))

#     try:
#         await task
#     except ValueError as e:
#         print(f"   Caught from task: {e}")

#     # Unhandled exceptions in tasks (fire and forget)
#     print("\n3. Unhandled task exception:")
#     task = asyncio.create_task(may_raise_error(True))
#     await asyncio.sleep(0.2)  # Let task complete

#     # Check if task has exception
#     if task.done() and task.exception():
#         print(f"   Task failed with: {task.exception()}")


# asyncio.run(exception_handling_demo())


# # ------------------------------------------------------------------------------
# # 16.2 Handling Multiple Task Exceptions
# # ------------------------------------------------------------------------------

# print_subsection("16.2 Handling Multiple Task Exceptions")


# async def multi_exception_demo():
#     """Handle exceptions from multiple tasks."""

#     async def worker(name: str, fail: bool):
#         await asyncio.sleep(random.uniform(0.1, 0.3))
#         if fail:
#             raise RuntimeError(f"{name} failed!")
#         return f"{name} succeeded"

#     tasks = [
#         asyncio.create_task(worker("A", False)),
#         asyncio.create_task(worker("B", True)),  # Will fail
#         asyncio.create_task(worker("C", False)),
#         asyncio.create_task(worker("D", True)),  # Will fail
#     ]

#     # Method 1: gather with return_exceptions
#     print("Method 1 - gather with return_exceptions:")
#     results = await asyncio.gather(
#         *[
#             worker("A", False),
#             worker("B", True),
#             worker("C", False),
#         ],
#         return_exceptions=True,
#     )

#     for i, result in enumerate(results):
#         if isinstance(result, Exception):
#             print(f"  Task {i}: Error - {result}")
#         else:
#             print(f"  Task {i}: Success - {result}")

#     # Method 2: Using wait and checking results
#     print("\nMethod 2 - Using wait:")
#     tasks = [
#         asyncio.create_task(worker("A", False)),
#         asyncio.create_task(worker("B", True)),
#         asyncio.create_task(worker("C", False)),
#     ]

#     done, pending = await asyncio.wait(tasks)

#     for task in done:
#         try:
#             result = task.result()
#             print(f"  Success: {result}")
#         except Exception as e:
#             print(f"  Error: {e}")


# asyncio.run(multi_exception_demo())


# # ------------------------------------------------------------------------------
# # 16.3 Global Exception Handler
# # ------------------------------------------------------------------------------

# print_subsection("16.3 Global Exception Handler")


# async def global_exception_handler_demo():
#     """Set up a global exception handler for the event loop."""

#     def handle_exception(loop, context):
#         """Global exception handler."""
#         msg = context.get("exception", context["message"])
#         print(f"Global handler caught: {msg}")

#     # Get the running loop and set handler
#     loop = asyncio.get_running_loop()
#     loop.set_exception_handler(handle_exception)

#     # Create a task that raises but isn't awaited
#     async def failing_task():
#         await asyncio.sleep(0.1)
#         raise RuntimeError("Unhandled error!")

#     task = asyncio.create_task(failing_task())
#     await asyncio.sleep(0.5)  # Give time for task to fail


# asyncio.run(global_exception_handler_demo())


# ================================================================================
# SECTION 17: TASKGROUPS (Python 3.11+)
# ================================================================================


async def _17_taskgroups():
    separator("17. TASKGROUPS (Python 3.11+)")

    print_subsection("17.1 Basic TaskGroup Usage")

    async def taskgroup_demo():
        """Demonstrate TaskGroup for structured concurrency."""

        async def worker(name: str, delay: float) -> str:
            print(f"{name}: Starting...")
            await asyncio.sleep(delay)
            print(f"{name}: Done!")
            return f"{name} result"

        # context manager can also be async when they need to do IO-operations during setup or teardown
        async with asyncio.TaskGroup() as tg:
            # All the Tasks are automatically awaited when exiting the context
            task1 = tg.create_task(worker("A", 0.5))
            task2 = tg.create_task(worker("B", 0.3))
            task3 = tg.create_task(worker("C", 0.4))
            # or can also write like `results = [tg.create_task(...), ...]`

        # All tasks are guaranteed to be complete here
        print(f"Results: {task1.result()}, {task2.result()}, {task3.result()}")

    await taskgroup_demo()

    print_subsection("17.2 TaskGroup Exception Handling")

    async def taskgroup_exception_demo():
        """Show how TaskGroup handles exceptions."""

        async def may_fail(name: str, should_fail: bool):
            await asyncio.sleep(0.2)
            if should_fail:
                raise ValueError(f"{name} failed!")
            return f"{name} OK"

        try:
            # on the first failure, cancells all the other tasks
            # raises an exception group cointaining all the exceptions from failed tasks
            #     (Including exception from cancelled tasks as well)
            # No option to keep running other tasks after one fails
            # Hence we use this when we want all our tasks to run successfully
            #     yaani either success togather or fail togather
            async with asyncio.TaskGroup() as tg:
                tg.create_task(may_fail("A", False))
                tg.create_task(may_fail("B", True))  # Will fail
                tg.create_task(may_fail("C", False))
        except* ValueError as eg:
            # ExceptionGroup handling (Python 3.11+)
            print(f"Caught exception group with {len(eg.exceptions)} exceptions:")
            for exc in eg.exceptions:
                print(f"  - {exc}")

    await taskgroup_exception_demo()


# # ================================================================================
# # SECTION 18: PRACTICAL EXAMPLES
# # ================================================================================

# separator("18. PRACTICAL EXAMPLES")

# # ------------------------------------------------------------------------------
# # 18.1 Web Scraper Pattern
# # ------------------------------------------------------------------------------

# print_subsection("18.1 Web Scraper Pattern (Simulated)")


# async def web_scraper_example():
#     """Simulate a concurrent web scraper."""

#     # Simulated fetch function (in real app, use aiohttp)
#     async def fetch_page(url: str) -> dict:
#         delay = random.uniform(0.2, 1.0)
#         await asyncio.sleep(delay)
#         return {
#             "url": url,
#             "status": 200,
#             "length": random.randint(1000, 10000),
#             "time": delay,
#         }

#     # Rate limiter using semaphore
#     semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests

#     async def limited_fetch(url: str) -> dict:
#         async with semaphore:
#             return await fetch_page(url)

#     # URLs to scrape
#     urls = [f"https://example.com/page/{i}" for i in range(20)]

#     print(f"Scraping {len(urls)} pages (max 5 concurrent)...")
#     start = time.perf_counter()

#     # Fetch all pages
#     results = await asyncio.gather(*[limited_fetch(url) for url in urls])

#     elapsed = time.perf_counter() - start
#     total_length = sum(r["length"] for r in results)

#     print(f"Completed in {elapsed:.2f}s")
#     print(f"Total content: {total_length} bytes")
#     print(f"Average page size: {total_length // len(results)} bytes")


# asyncio.run(web_scraper_example())


# # ------------------------------------------------------------------------------
# # 18.2 Rate Limiter
# # ------------------------------------------------------------------------------

# print_subsection("18.2 Rate Limiter Implementation")


# class RateLimiter:
#     """A token bucket rate limiter."""

#     def __init__(self, rate: float, capacity: int):
#         """
#         Args:
#             rate: Tokens added per second
#             capacity: Maximum tokens in bucket
#         """
#         self.rate = rate
#         self.capacity = capacity
#         self.tokens = capacity
#         self.last_update = time.monotonic()
#         self.lock = asyncio.Lock()

#     async def acquire(self):
#         """Acquire a token, waiting if necessary."""
#         async with self.lock:
#             while True:
#                 now = time.monotonic()
#                 time_passed = now - self.last_update
#                 self.tokens = min(self.capacity, self.tokens + time_passed * self.rate)
#                 self.last_update = now

#                 if self.tokens >= 1:
#                     self.tokens -= 1
#                     return

#                 # Wait for a token
#                 wait_time = (1 - self.tokens) / self.rate
#                 await asyncio.sleep(wait_time)


# async def rate_limiter_demo():
#     """Demonstrate the rate limiter."""

#     # Allow 3 requests per second, max burst of 3
#     limiter = RateLimiter(rate=3, capacity=3)

#     async def make_request(request_id: int):
#         await limiter.acquire()
#         print(f"Request {request_id} at {time.monotonic():.2f}")

#     start = time.monotonic()

#     # Make 10 requests
#     await asyncio.gather(*[make_request(i) for i in range(10)])

#     elapsed = time.monotonic() - start
#     print(f"\n10 requests completed in {elapsed:.2f}s")


# asyncio.run(rate_limiter_demo())


# # ------------------------------------------------------------------------------
# # 18.3 Async Context Manager for Database Connections
# # ------------------------------------------------------------------------------

# print_subsection("18.3 Async Database Connection Pool Pattern")


# class AsyncConnectionPool:
#     """A simulated async connection pool."""

#     def __init__(self, pool_size: int):
#         self.pool_size = pool_size
#         self.available = asyncio.Queue()
#         self.in_use = 0
#         self._lock = asyncio.Lock()

#     async def initialize(self):
#         """Initialize the connection pool."""
#         for i in range(self.pool_size):
#             conn = {"id": i, "created": time.time()}
#             await self.available.put(conn)
#         print(f"Pool initialized with {self.pool_size} connections")

#     @asynccontextmanager
#     async def acquire(self):
#         """Acquire a connection from the pool."""
#         conn = await self.available.get()
#         self.in_use += 1
#         print(f"Acquired connection {conn['id']} ({self.in_use} in use)")

#         try:
#             yield conn
#         finally:
#             await self.available.put(conn)
#             self.in_use -= 1
#             print(f"Released connection {conn['id']} ({self.in_use} in use)")

#     async def execute(self, query: str):
#         """Execute a query using a pooled connection."""
#         async with self.acquire() as conn:
#             await asyncio.sleep(0.2)  # Simulate query
#             return f"Result from conn {conn['id']}: {query}"


# async def connection_pool_demo():
#     """Demonstrate the connection pool."""

#     pool = AsyncConnectionPool(pool_size=3)
#     await pool.initialize()

#     async def run_query(query_id: int):
#         query = f"SELECT * FROM table_{query_id}"
#         result = await pool.execute(query)
#         return result

#     # Run more queries than pool size
#     results = await asyncio.gather(*[run_query(i) for i in range(6)])

#     print("\nResults:")
#     for result in results:
#         print(f"  {result}")


# asyncio.run(connection_pool_demo())


# # ------------------------------------------------------------------------------
# # 18.4 Periodic Task Runner
# # ------------------------------------------------------------------------------

# print_subsection("18.4 Periodic Task Runner")


# class PeriodicTask:
#     """Run a task periodically."""

#     def __init__(self, interval: float, func, *args, **kwargs):
#         self.interval = interval
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#         self._task: Optional[asyncio.Task] = None
#         self._running = False

#     async def _run(self):
#         """Internal run loop."""
#         while self._running:
#             try:
#                 if asyncio.iscoroutinefunction(self.func):
#                     await self.func(*self.args, **self.kwargs)
#                 else:
#                     self.func(*self.args, **self.kwargs)
#             except Exception as e:
#                 print(f"Periodic task error: {e}")

#             await asyncio.sleep(self.interval)

#     def start(self):
#         """Start the periodic task."""
#         if not self._running:
#             self._running = True
#             self._task = asyncio.create_task(self._run())

#     def stop(self):
#         """Stop the periodic task."""
#         self._running = False
#         if self._task:
#             self._task.cancel()


# async def periodic_demo():
#     """Demonstrate periodic task runner."""

#     counter = {"count": 0}

#     async def heartbeat():
#         counter["count"] += 1
#         print(f"Heartbeat {counter['count']} at {time.monotonic():.2f}")

#     # Create and start periodic task
#     task = PeriodicTask(0.3, heartbeat)
#     task.start()

#     # Let it run for a while
#     await asyncio.sleep(2)

#     # Stop it
#     task.stop()
#     print(f"Stopped after {counter['count']} heartbeats")


# asyncio.run(periodic_demo())


# # ================================================================================
# # SECTION 19: ASYNCIO VS THREADING VS MULTIPROCESSING
# # ================================================================================

# separator("19. ASYNCIO VS THREADING VS MULTIPROCESSING")

# comparison_text = """
# COMPARISON OF CONCURRENCY APPROACHES
# ====================================

# ┌────────────────┬─────────────────────┬─────────────────────┬─────────────────────┐
# │ Aspect         │ asyncio             │ threading           │ multiprocessing     │
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Best for       │ I/O-bound tasks     │ I/O-bound tasks     │ CPU-bound tasks     │
# │                │ Many connections    │ Moderate connections│ Parallel computation│
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Scalability    │ 10,000s of tasks    │ 100s of threads     │ # of CPU cores      │
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ GIL Impact     │ Not affected        │ Limited by GIL      │ Bypasses GIL        │
# │                │ (single thread)     │ (for CPU work)      │ (separate processes)│
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Memory         │ Very low            │ Higher              │ Highest             │
# │ Overhead       │ (coroutines ~200B)  │ (~8KB per thread)   │ (full process copy) │
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Complexity     │ Medium              │ Higher              │ High                │
# │                │ (async/await)       │ (race conditions)   │ (IPC needed)        │
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Context Switch │ Explicit (await)    │ Implicit (OS)       │ Implicit (OS)       │
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Debugging      │ Easier              │ Harder              │ Moderate            │
# │                │ (deterministic)     │ (race conditions)   │ (separate processes)│
# ├────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
# │ Library        │ Requires async      │ Works with sync     │ Works with sync     │
# │ Support        │ libraries           │ libraries           │ libraries           │
# └────────────────┴─────────────────────┴─────────────────────┴─────────────────────┘

# WHEN TO USE EACH:
# =================

# asyncio:
# --------
# ✓ Web scraping (many URLs)
# ✓ API servers handling many connections
# ✓ Chat applications
# ✓ WebSocket servers
# ✓ Database operations with async drivers
# ✓ When you need 1000s of concurrent connections

# threading:
# ----------
# ✓ GUI applications (UI thread + workers)
# ✓ I/O operations with sync libraries
# ✓ When you need true parallelism for I/O
# ✓ Background tasks in sync applications
# ✓ File I/O operations

# multiprocessing:
# ----------------
# ✓ CPU-intensive calculations
# ✓ Data processing
# ✓ Image/video processing
# ✓ Machine learning training
# ✓ Scientific computing

# COMBINING APPROACHES:
# =====================

# You can combine these approaches:

# 1. asyncio + threading:
#    - Use run_in_executor() for blocking code
#    - Use asyncio.to_thread() (Python 3.9+)

# 2. asyncio + multiprocessing:
#    - Use ProcessPoolExecutor with run_in_executor()
#    - Offload CPU-bound work to processes

# 3. threading + multiprocessing:
#    - Worker processes with thread pools
#    - For complex workloads
# """

# print(comparison_text)


# # Example: Combining asyncio with multiprocessing
# async def combined_approach_demo():
#     """Demonstrate combining asyncio with process pool."""

#     def cpu_work(n: int) -> int:
#         """CPU-intensive work."""
#         return sum(i * i for i in range(n))

#     async def io_work(name: str) -> str:
#         """I/O-intensive work."""
#         await asyncio.sleep(0.1)
#         return f"{name} done"

#     loop = asyncio.get_running_loop()

#     # Run CPU work in process pool, I/O work in event loop
#     with concurrent.futures.ProcessPoolExecutor() as pool:
#         cpu_task = loop.run_in_executor(pool, cpu_work, 100000)
#         io_task = io_work("IO-Task")

#         cpu_result, io_result = await asyncio.gather(cpu_task, io_task)

#     print(f"CPU result: {cpu_result}")
#     print(f"I/O result: {io_result}")


# if __name__ == "__main__":
#     asyncio.run(combined_approach_demo())


# # ================================================================================
# # SECTION 20: BEST PRACTICES AND COMMON PITFALLS
# # ================================================================================

# separator("20. BEST PRACTICES AND COMMON PITFALLS")

# best_practices_text = """
# BEST PRACTICES
# ==============

# 1. ALWAYS USE asyncio.run() AS THE MAIN ENTRY POINT
#    ─────────────────────────────────────────────────
#    Good:
#        async def main():
#            await do_stuff()
#        asyncio.run(main())

#    Avoid:
#        loop = asyncio.get_event_loop()
#        loop.run_until_complete(main())


# 2. NEVER USE time.sleep() IN ASYNC CODE
#    ─────────────────────────────────────
#    Good:
#        await asyncio.sleep(1)

#    Bad:
#        time.sleep(1)  # Blocks the entire event loop!


# 3. ALWAYS AWAIT COROUTINES
#    ────────────────────────
#    Good:
#        result = await some_coroutine()

#    Bad:
#        result = some_coroutine()  # Creates coroutine object, doesn't run it!


# 4. USE create_task() FOR CONCURRENT EXECUTION
#    ──────────────────────────────────────────
#    Sequential (slow):
#        await task1()
#        await task2()

#    Concurrent (fast):
#        t1 = asyncio.create_task(task1())
#        t2 = asyncio.create_task(task2())
#        await t1
#        await t2


# 5. HANDLE TASK EXCEPTIONS
#    ──────────────────────
#    Tasks swallow exceptions silently if not awaited:

#        # Exception may go unnoticed!
#        asyncio.create_task(may_fail())

#        # Better: Always await or handle
#        task = asyncio.create_task(may_fail())
#        try:
#            await task
#        except Exception as e:
#            handle_error(e)


# 6. USE SEMAPHORE FOR RATE LIMITING
#    ────────────────────────────────
#    sem = asyncio.Semaphore(10)  # Max 10 concurrent

#    async def limited_operation():
#        async with sem:
#            await do_stuff()


# 7. PREFER gather() WITH return_exceptions FOR MULTIPLE TASKS
#    ─────────────────────────────────────────────────────────
#    results = await asyncio.gather(*tasks, return_exceptions=True)
#    for result in results:
#        if isinstance(result, Exception):
#            handle_error(result)
#        else:
#            process_result(result)


# 8. USE TASKGROUPS IN PYTHON 3.11+
#    ───────────────────────────────
#    async with asyncio.TaskGroup() as tg:
#        tg.create_task(task1())
#        tg.create_task(task2())
#    # All tasks guaranteed complete here


# 9. PROPERLY CLEAN UP RESOURCES
#    ───────────────────────────
#    Use async context managers:

#        async with aiohttp.ClientSession() as session:
#            # Use session
#        # Automatically cleaned up


# 10. USE run_in_executor() FOR BLOCKING CODE
#     ──────────────────────────────────────
#     loop = asyncio.get_running_loop()
#     result = await loop.run_in_executor(None, blocking_function)


# COMMON PITFALLS
# ===============

# 1. ❌ Calling sync code without run_in_executor
#    ────────────────────────────────────────────
#    # This blocks everything:
#    async def bad():
#        result = requests.get(url)  # Blocking!

#    # Do this instead:
#    async def good():
#        async with aiohttp.ClientSession() as session:
#            async with session.get(url) as response:
#                return await response.text()


# 2. ❌ Creating but not awaiting coroutines
#    ───────────────────────────────────────
#    # This does nothing:
#    some_coroutine()

#    # Do this:
#    await some_coroutine()


# 3. ❌ Not handling CancelledError properly
#    ──────────────────────────────────────
#    async def task():
#        try:
#            await some_operation()
#        except asyncio.CancelledError:
#            cleanup()
#            raise  # Always re-raise!


# 4. ❌ Forgetting to cancel pending tasks on shutdown
#    ─────────────────────────────────────────────────
#    async def shutdown():
#        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
#        for task in tasks:
#            task.cancel()
#        await asyncio.gather(*tasks, return_exceptions=True)


# 5. ❌ Using mutable default arguments in async functions
#    ─────────────────────────────────────────────────────
#    # Bad:
#    async def bad(data=[]):
#        data.append(1)

#    # Good:
#    async def good(data=None):
#        if data is None:
#            data = []


# 6. ❌ Not using async-compatible libraries
#    ──────────────────────────────────────
#    Use:
#    - aiohttp instead of requests
#    - aiomysql instead of mysql-connector
#    - asyncpg instead of psycopg2
#    - aiofiles instead of open()


# 7. ❌ Recursive asyncio.run() calls
#    ─────────────────────────────────
#    # This will fail:
#    async def outer():
#        asyncio.run(inner())  # Error!

#    # Use await instead:
#    async def outer():
#        await inner()


# DEBUGGING TIPS
# ==============

# 1. Enable asyncio debug mode:
#    asyncio.run(main(), debug=True)

# 2. Use logging:
#    import logging
#    logging.getLogger('asyncio').setLevel(logging.DEBUG)

# 3. Check for unawaited coroutines:
#    Python will warn: "coroutine was never awaited"

# 4. Use asyncio.current_task() and asyncio.all_tasks() for inspection

# 5. Set custom exception handler:
#    loop.set_exception_handler(my_handler)
# """

# print(best_practices_text)


# # ================================================================================
# # FINAL SUMMARY
# # ================================================================================

# separator("FINAL SUMMARY")

# summary = """
# ASYNCIO QUICK REFERENCE
# =======================

# DEFINING ASYNC FUNCTIONS:
#     async def my_function():
#         return "result"

# RUNNING ASYNC CODE:
#     asyncio.run(main())                    # Main entry point
#     await coroutine()                       # Inside async function
#     task = asyncio.create_task(coro())     # Create task

# CONCURRENT EXECUTION:
#     await asyncio.gather(coro1(), coro2()) # Run concurrently
#     await asyncio.wait(tasks)              # Wait for tasks
#     asyncio.as_completed(tasks)            # Process as complete

# TIMEOUTS:
#     await asyncio.wait_for(coro, timeout)  # With timeout
#     async with asyncio.timeout(seconds):   # Context manager (3.11+)

# SYNCHRONIZATION:
#     async with asyncio.Lock():             # Mutual exclusion
#     async with asyncio.Semaphore(n):       # Limit concurrency
#     await event.wait()                     # Wait for signal
#     await queue.get()                      # Get from queue

# BLOCKING CODE:
#     await loop.run_in_executor(None, fn)   # In thread pool
#     await asyncio.to_thread(fn)            # Simpler (3.9+)

# TASKGROUPS (3.11+):
#     async with asyncio.TaskGroup() as tg:
#         tg.create_task(coro())

# KEY CLASSES:
#     asyncio.Queue, PriorityQueue, LifoQueue
#     asyncio.Lock, Semaphore, BoundedSemaphore
#     asyncio.Event, Condition, Barrier (3.11+)
#     asyncio.StreamReader, StreamWriter
#     asyncio.Task, Future

# ================================================================================
#                         END OF ASYNCIO TUTORIAL
# ================================================================================
# """

# print(summary)


async def main():
    _1_introduction_to_asyncio()
    routines_obj_list = [
        _2_basic_concepts(),
        _3_running_coroutines(),
        _4_tasks_creating_and_managing_tasks(),
        _5_gather_coroutines(),
        _6_waiting_for_tasks(),
        _8_sleep_comparison(),
        _13_running_blocking_sync_code_in_async_context(),
        _17_taskgroups(),
    ]
    for routine_obj in routines_obj_list:
        await routine_obj
    # await asyncio.gather(*routines_obj_list)


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    print(f"Whole script Finished in {end_time - start_time:0.4f} seconds")
