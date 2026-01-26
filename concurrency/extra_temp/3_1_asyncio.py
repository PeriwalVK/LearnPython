import asyncio
from os import sep
import time
import random



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




# ==========================================
# HELPER: A standard synchronous timer
# We use this to measure how fast our code runs.
# ==========================================
def mark_time(start_time):
    return f"{time.time() - start_time:.2f} seconds"



# ==========================================
# LEVEL 1: The Basics (Async/Await)
# Concept: Defining a coroutine and running it.
# ==========================================
async def level_1_hello():
    separator("LEVEL 1: The Basics (Async/Await)")
    print("Start")
    
    # We use 'await' to pause this function without blocking the whole program.
    # asyncio.sleep(1) simulates an I/O operation (like downloading a file)
    await asyncio.sleep(1) 
    
    print("Finished (after 1 second)")

# ==========================================
# LEVEL 2: Sequential vs. Concurrent
# Concept: Running things one by one vs. at the same time.
# ==========================================
async def brew_coffee():
    print("☕ Starting coffee...")
    await asyncio.sleep(2) # Simulates brewing taking 2 seconds
    print("☕ Coffee is ready!")
    return "Coffee"

async def toast_bread():
    print("🍞 Starting toast...")
    await asyncio.sleep(1) # Simulates toasting taking 1 second
    print("🍞 Toast is ready!")
    return "Toast"

async def level_2_breakfast():
    separator("LEVEL 2: Sequential vs. Concurrent")
    start = time.time()

    # --- THE SLOW WAY (Sequential) ---
    # print("Doing it sequentially (one after another)...")
    # await brew_coffee()
    # await toast_bread()
    
    # --- THE FAST WAY (Concurrent) ---
    print("Doing it concurrently (Gathering tasks)...")
    # asyncio.gather schedules both to run on the event loop immediately
    # It waits for BOTH to finish.
    # The total time will be roughly equal to the longest task (Coffee: 2s)
    results = await asyncio.gather(brew_coffee(), toast_bread())
    
    print(f"Finished: {results}")
    print(f"Total time: {mark_time(start)}")

# ==========================================
# LEVEL 3: Timeouts and Protections
# Concept: What if a task takes too long?
# ==========================================
async def slow_download():
    print("⬇️ Starting slow download...")
    await asyncio.sleep(5) # Takes 5 seconds
    return "Download Complete"

async def level_3_timeouts():
    separator("LEVEL 3: Timeouts and Protections")    
    try:
        # We wrap the coroutine in wait_for.
        # If it takes longer than 2 seconds, it raises a TimeoutError
        result = await asyncio.wait_for(slow_download(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("❌ Timeout! The download took too long and was cancelled.")

# ==========================================
# LEVEL 4: Background Tasks (Fire and Forget)
# Concept: Starting a task and doing other work while it runs.
# ==========================================
async def background_counter(name):
    for i in range(1, 4):
        print(f"[{name}] Counting {i}")
        await asyncio.sleep(0.5)

async def level_4_tasks():
    separator("LEVEL 4: Background Tasks (Fire and Forget)")
    
    # create_task schedules the coroutine to run immediately on the loop.
    # Unlike 'await', this line does NOT stop the code flow here.
    task = asyncio.create_task(background_counter("Background Worker"))
    
    print("Main: The worker is running in the background...")
    print("Main: I am doing other work here...")
    await asyncio.sleep(1) # Let the background worker tick a few times
    print("Main: waiting for worker to finish completely...")
    
    await task # Now we ensure the background task is done
    print("Main: Done.")

# ==========================================
# LEVEL 5: The "Golden Rule" & Sync Interop
# Concept: NEVER use time.sleep() inside async.
# ==========================================
def blocking_function():
    # This represents a library that doesn't support async (e.g., standard requests, heavy math)
    print("🚫 BLOCKING: Starting heavy calculation...")
    time.sleep(2) # This freezes everything!
    print("🚫 BLOCKING: Done.")

async def non_blocking_wrapper():
    print("✅ WRAPPER: Running blocking code in a separate thread...")
    # We use to_thread (Python 3.9+) to run sync code without freezing the event loop
    await asyncio.to_thread(blocking_function)
    print("✅ WRAPPER: Finished.")

async def level_5_blocking():
    separator("LEVEL 5: The 'Golden Rule' & Sync Interop")
    
    # Start a background ticker to prove the loop is running or frozen
    task = asyncio.create_task(background_counter("Loop Health Check"))
    
    # Run the blocking code safely
    await non_blocking_wrapper()
    
    await task

# ==========================================
# LEVEL 6: Async Queues (Producer/Consumer)
# Concept: Moving data between workers
# ==========================================
async def producer(queue):
    for i in range(3):
        # Simulate network delay to fetch an item
        await asyncio.sleep(random.uniform(0.1, 0.5))
        item = f"Data_Packet_{i}"
        await queue.put(item)
        print(f"📤 Produced: {item}")
    
    # Signal that we are done
    await queue.put(None)

async def consumer(queue):
    while True:
        # Wait for an item from the producer
        item = await queue.get()
        
        if item is None:
            # None is our signal to stop
            break
            
        print(f"📥 Consumed: {item} (Processing...)")
        await asyncio.sleep(0.5) # Simulate processing time
        queue.task_done()

async def level_6_queue():
    separator("LEVEL 6: Async Queues (Producer/Consumer)")
    queue = asyncio.Queue()
    
    # Schedule both to run
    # We use gather to run them concurrently
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )
    print("Queue workflow finished.")

# ==========================================
# MAIN ENTRY POINT
# ==========================================
async def main():
    print("=== ASYNCIO TUTORIAL SCRIPT ===")
    
    await level_1_hello()
    await level_2_breakfast()
    await level_3_timeouts()
    await level_4_tasks()
    await level_5_blocking()
    await level_6_queue()
    
    print("\n=== TUTORIAL COMPLETE ===")

if __name__ == "__main__":
    # This is how you start the Asyncio Event Loop
    asyncio.run(main())


