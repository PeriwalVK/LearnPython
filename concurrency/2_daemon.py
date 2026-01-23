# import threading
# import time

# def background_autosave():
#     cnt = 0
#     while True:
#         cnt += 1
#         print(f"[DAEMON_TARGET][{cnt}] Saving work...", flush=True)
#         time.sleep(0.5)


# def daemon_in_a_function() -> threading.Thread:

#     t = threading.Thread(target=background_autosave, daemon=True)
#     t.start()

#     print("[DAEMON_WALA_FUNCTION] Working on main task (3 seconds)...")
#     time.sleep(3)
#     print("[DAEMON_WALA_FUNCTION] Work finished. Exiting FUNCTION and returning thread object.")
#     # Function ends here, but daemon keeps running!
#     return t




# # ═══════════════════════════════════════════════════════════════════
# # TEST: What happens after function ends?
# # ═══════════════════════════════════════════════════════════════════

# print("=== Program Started ===\n")

# t: threading.Thread = daemon_in_a_function()

# print("\n[MAIN] Function ended, but I'm still running!")
# print("[MAIN] Yopu can see that Daemon thread is STILL ALIVE! and keeps printing!\n")

# time.sleep(3)  # Wait 3 more seconds - daemon keeps printing!

# print("\n[MAIN] NOW I'm exiting. Daemon will be killed.")


import threading
import time

def worker(name, duration):
    """Simulate a task that takes some time."""
    print(f"  {name}: Starting (will take {duration} seconds)")
    for i in range(duration):
        time.sleep(1)
        print(f"  {name}: Working... ({i+1}/{duration})")
    print(f"  {name}: Finished!")  # Will this print?

# ═══════════════════════════════════════════════════════════
# EXAMPLE 1: NON-DAEMON (default) - Program waits
# ═══════════════════════════════════════════════════════════
def example_non_daemon():
    print("\n=== NON-DAEMON THREAD (daemon=False) ===")
    print("Main: Starting worker thread...")
    
    t = threading.Thread(target=worker, args=("NON-Daemon-Worker", 3), daemon=False)
    t.start()
    
    print("Main: I'm done with my work!")
    print("Main: But I'll WAIT for the worker to finish...\n")
    # Program waits for worker to complete before exiting

# ═══════════════════════════════════════════════════════════
# EXAMPLE 2: DAEMON - Program kills thread and exits
# ═══════════════════════════════════════════════════════════
def example_daemon():
    print("\n=== DAEMON THREAD (daemon=True) ===")
    print("Main: Starting daemon worker thread...")
    
    t = threading.Thread(target=worker, args=("Daemon-Worker", 5), daemon=True)
    t.start()
    
    time.sleep(2)  # Let daemon work for 2 seconds
    
    print("\nMain: I'm done! Exiting NOW!")
    print("Main: Daemon thread will be KILLED immediately!")
    print("      (You won't see 'Finished!' from the worker)\n")
    # Program exits, daemon is killed mid-work!


# Run examples
if __name__ == "__main__":
    # Uncomment ONE at a time to see the difference:
    # example_non_daemon()  # Worker finishes, then program exits
    example_daemon()    # Program exits, worker is killed