
import time

def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def announce(msg: str):
    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


@announce("Example 1: Progress Dots")
def example_1_progress_dots():
    print("Downloading", end="", flush=True)

    for i in range(10):
        time.sleep(0.3)
        print(".", end="", flush=True)  # Each dot appears immediately

    print(" Complete!")


@announce("Example 2: Progress Bar")
def example_2_progress_bar():
    for i in range(101):
        bar = "█" * (i // 5) + "░" * (20 - i // 5)
        print(f"\r[{bar}] {i}%", end="", flush=True)  # Must flush!
        time.sleep(0.05)

    print()  # Final newline


@announce("Example 3: Countdown Timer")
def example_3_countdown_timer():
    for i in range(5, 0, -1):
        print(f"\rStarting in {i}...", end="", flush=True)
        time.sleep(1)

    print("\rGo!            ")  # Extra spaces to clear previous text


@announce("Example 4: Spinner Animation")
def example_4_spinner_animation():
    spinner = "|/-\\"

    for i in range(20):
        print(f"\rLoading {spinner[i % 4]}", end="", flush=True)
        time.sleep(0.1)

    print("\rDone!     ")





def carriage_return_otgher_example():

    # ───────────────────────────────────────────────────────
    # Example 4b: \r WITHOUT flush (may not work properly)
    # ───────────────────────────────────────────────────────
    print("\n--- Example 4b: \\r WITHOUT flush=True ---")
    print("  Attempting countdown (may not update properly)...")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ WITHOUT flush=True:                                                 │
    # │                                                                     │
    # │   Buffer: [\r5] → [\r5\r4] → [\r5\r4\r3] → ... → FLUSH              │
    # │                                                                     │
    # │   All the \r and numbers accumulate in buffer!                      │
    # │   When finally flushed, you might see garbled output or just        │
    # │   the final number.                                                 │
    # └─────────────────────────────────────────────────────────────────────┘

    for i in range(5, 0, -1):
        print(f"\r  Countdown: {i}", end="")  # NO flush - may buffer!
        time.sleep(0.5)
    print()  # Newline triggers flush

    print("  Did you see the countdown update? (Probably not smoothly!)")

    time.sleep(2)

    # ───────────────────────────────────────────────────────
    # Example 4c: \r WITH flush (works correctly)
    # ───────────────────────────────────────────────────────
    print("\n--- Example 4c: \\r WITH flush=True ---")
    print("  Countdown with proper flush...")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ WITH flush=True:                                                    │
    # │                                                                     │
    # │   Iteration 1: print("\rCountdown: 5") → FLUSH → Screen: Countdown: 5
    # │   Iteration 2: print("\rCountdown: 4") → FLUSH → Screen: Countdown: 4
    # │   Iteration 3: print("\rCountdown: 3") → FLUSH → Screen: Countdown: 3
    # │   ...                                                               │
    # │                                                                     │
    # │   Each update IMMEDIATELY appears and overwrites previous!          │
    # └─────────────────────────────────────────────────────────────────────┘

    for i in range(5, 0, -1):
        print(f"\r  Countdown: {i}", end="", flush=True)  # Immediate update!
        time.sleep(0.5)
    print("\r  Blast off! 🚀")  # Overwrites "Countdown: 1"

    print("  Now the countdown updated smoothly!")

    time.sleep(2)

    # ═══════════════════════════════════════════════════════
    # PART 5: Practical \r Examples
    # ═══════════════════════════════════════════════════════
    print("\n=== PART 5: Practical \\r Examples ===")

    # ───────────────────────────────────────────────────────
    # Example 5a: Progress Bar
    # ───────────────────────────────────────────────────────
    print("\n--- Example 5a: Progress Bar ---")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ PROGRESS BAR TECHNIQUE:                                             │
    # │                                                                     │
    # │   1. Print progress bar with \r at start (go to line beginning)     │
    # │   2. Use end="" (don't go to next line)                             │
    # │   3. Use flush=True (display immediately)                           │
    # │   4. Each iteration overwrites the previous bar                     │
    # │                                                                     │
    # │   Screen updates:                                                   │
    # │     [██░░░░░░░░] 20%  →  [████░░░░░░] 40%  →  [██████████] 100%     │
    # └─────────────────────────────────────────────────────────────────────┘

    total = 20
    for i in range(total + 1):
        # Calculate progress
        percent = (i / total) * 100
        filled = int(i / total * 20)
        bar = "█" * filled + "░" * (20 - filled)

        # \r moves to start, overwrites previous bar
        print(f"\r  [{bar}] {percent:5.1f}%", end="", flush=True)
        time.sleep(0.1)

    print("  ✓ Complete!")

    time.sleep(2)

    # ───────────────────────────────────────────────────────
    # Example 5b: Spinner Animation
    # ───────────────────────────────────────────────────────
    print("\n--- Example 5b: Spinner Animation ---")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ SPINNER TECHNIQUE:                                                  │
    # │                                                                     │
    # │   Use a sequence of characters that look like rotation:             │
    # │   | → / → - → \ → | → / → ...                                       │
    # │                                                                     │
    # │   \r + flush=True makes each frame replace the previous one         │
    # └─────────────────────────────────────────────────────────────────────┘

    spinner_frames = ["|", "/", "-", "\\"]

    print("  ", end="")  # Initial spacing
    for i in range(16):  # 4 complete rotations
        frame = spinner_frames[i % 4]
        print(f"\r  Loading {frame}", end="", flush=True)
        time.sleep(0.15)

    # Clear spinner and show done (extra spaces to overwrite "Loading X")
    print("\r  Done!      ")

    time.sleep(2)

    # ───────────────────────────────────────────────────────
    # Example 5c: Animated Dots
    # ───────────────────────────────────────────────────────
    print("\n--- Example 5c: Animated Loading Dots ---")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ ANIMATED DOTS:                                                      │
    # │                                                                     │
    # │   Processing.   →   Processing..   →   Processing...   →   repeat  │
    # └─────────────────────────────────────────────────────────────────────┘

    for cycle in range(3):  # 3 cycles
        for dots in range(4):  # 0, 1, 2, 3 dots
            # Spaces after dots clear previous longer text
            print(f"\r  Processing{'.' * dots}   ", end="", flush=True)
            time.sleep(0.3)

    print("\r  Processing... Done! ✓")

    time.sleep(2)

    # ───────────────────────────────────────────────────────
    # Example 5d: Live Status Update
    # ───────────────────────────────────────────────────────
    print("\n--- Example 5d: Live Status Update ---")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ STATUS UPDATE:                                                      │
    # │                                                                     │
    # │   Show different status messages on the same line                   │
    # │   Use extra spaces to clear longer previous messages                │
    # └─────────────────────────────────────────────────────────────────────┘

    statuses = [
        "Connecting to server...",
        "Authenticating...",
        "Downloading data...",
        "Processing results...",
        "Almost done...",
        "Complete! ✓",
    ]

    for status in statuses:
        # Pad with spaces to clear any longer previous message
        print(f"\r  Status: {status:<25}", end="", flush=True)
        time.sleep(0.8)

    print()  # Final newline

    time.sleep(2)

    # ───────────────────────────────────────────────────────
    # Example 5e: Typing Effect with Backspace
    # ───────────────────────────────────────────────────────
    print("\n--- Example 5e: Typing and Correcting ---")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ COMBINING \r with typing effect:                                    │
    # │                                                                     │
    # │   Type "Helo" → pause → use \r to retype as "Hello"                 │
    # └─────────────────────────────────────────────────────────────────────┘

    print("  ", end="", flush=True)

    # Type "Helo" (with typo)
    for char in "Helo":
        print(char, end="", flush=True)
        time.sleep(0.15)

    time.sleep(0.5)  # Pause

    # Use \r to go back and retype correctly
    print("\r  ", end="", flush=True)  # Go to start

    # Type "Hello" correctly
    for char in "Hello, World!":
        print(char, end="", flush=True)
        time.sleep(0.1)

    print()  # Final newline

    time.sleep(2)

    # ═══════════════════════════════════════════════════════
    # PART 6: Common Pitfall - Clearing Previous Text
    # ═══════════════════════════════════════════════════════
    print("\n=== PART 6: Common Pitfall - Text Length ===")

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ THE PROBLEM:                                                        │
    # │                                                                     │
    # │   \r only moves cursor - it doesn't ERASE anything!                 │
    # │   If new text is SHORTER than old text, old characters remain.      │
    # │                                                                     │
    # │   Example:                                                          │
    # │     print("LONG MESSAGE")  → Screen: LONG MESSAGE                   │
    # │     print("\rHI")          → Screen: HI G MESSAGE  (oops!)          │
    # │                                      ↑↑                             │
    # │                                    new text, but old text remains!  │
    # └─────────────────────────────────────────────────────────────────────┘

    print("\n--- Problem: Shorter text doesn't clear longer text ---")
    time.sleep(1)

    print("  Watch this problem:")
    print("  LONG MESSAGE HERE", end="", flush=True)
    time.sleep(1)
    print("\r  SHORT", end="", flush=True)  # Doesn't clear all!
    time.sleep(1)
    print()  # Newline
    print("  See? 'SHORT' overwrote 'LONG M', but 'ESSAGE HERE' remains!")

    time.sleep(2)

    print("\n--- Solution: Pad with spaces OR clear entire line ---")
    time.sleep(1)

    # Solution 1: Pad with spaces
    print("  Solution 1 - Pad with spaces:")
    print("  LONG MESSAGE HERE", end="", flush=True)
    time.sleep(1)
    print("\r  SHORT             ", end="", flush=True)  # Extra spaces!
    time.sleep(1)
    print()
    print("  Now 'SHORT' is clean because spaces cleared the rest!")

    time.sleep(1)

    # Solution 2: Use fixed width formatting
    print("\n  Solution 2 - Fixed width formatting:")
    messages = ["Downloading...", "Processing...", "Done!"]
    for msg in messages:
        # {:<20} left-aligns and pads to 20 characters
        print(f"\r  {msg:<20}", end="", flush=True)

if __name__ == "__main__":
    carriage_return_otgher_example()