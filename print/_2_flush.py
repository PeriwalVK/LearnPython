"""
Your print() → Buffer (memory) → Screen
                    ↑
            Waits until buffer is full
            OR newline (\n) is encountered
            OR program ends
            OR flush=True
"""

import sys
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


@announce("0. Manual Flush")
def manual_flush():
    print("Processing", end="")
    sys.stdout.flush()  # Flush manually

    time.sleep(1)

    print(".", end="")
    sys.stdout.flush()  # Flush again


@announce("1. Without Flush")
def without_flush():
    ############## ❌ WITHOUT flush=True (may not work as expected) #############

    print("Loading", end="")
    for i in range(5):
        print(".", end="")  # These dots may NOT appear one by one!
        time.sleep(0.5)
    # (wait 2.5 seconds... nothing appears)
    # Loading..... Done!    ← All at once!
    print(" Done!")


@announce("2. With Flush")
def with_flush():
    ############# ✓ WITH flush=True (works correctly) #############

    print("Loading", end="")
    for i in range(5):
        print(".", end="", flush=True)  # Each dot appears immediately!
        time.sleep(0.5)
    print(" Done!")



@announce("Example 5.1: Newline Auto Flush")
def example_5_1_newline_auto_flush():
    """Demonstrate that \\n causes auto-flush, but other endings don't."""

    # ═══════════════════════════════════════════════════════
    # PART 1: With \n (auto-flushes)
    # ═══════════════════════════════════════════════════════
    print("=== PART 1: With newline (auto-flush) ===")

    print("Line 1 - appears immediately")  # \n added by default → flushes
    time.sleep(1)
    print("Line 2 - appears after 1 second", end="\n")  # \n explicit → flushes
    time.sleep(1)
    print("Line 3 - appears after another second")

    time.sleep(2)

    # # ═══════════════════════════════════════════════════════
    # # PART 2: Without \n and WITHOUT flush=True (may buffer)
    # # ═══════════════════════════════════════════════════════
    # print("\n=== PART 2: Without newline, NO flush ===")
    # print("Watch carefully...")
    # # Without time.sleep(), you won't notice the difference!
    # time.sleep(1)

    # # print("Hello", end="")            # No newline → buffered
    # # time.sleep(1)                     # ← Add delay to see effect
    # # print("Hello", end="\r")          # Carriage return ≠ newline → buffered
    # # time.sleep(1)                     # ← Add delay to see effect

    # # print("\n")  # Newline → flushes all buffered content + adds blank line

    # for chr in ["A", "B", "C", "D"]:
    #     print(chr, end="")  # # No newline → buffered (May NOT appear immediately)
    #     time.sleep(0.5)  # ← Add delay to see
    # print()  # Newline - NOW everything flushes and appears!

    # print("Did A, B, C, D appear one by one, or all at once?")
    # print("(Behavior depends on your terminal/environment)")

    # time.sleep(2)

    # # ═══════════════════════════════════════════════════════
    # # PART 3: Without \n but WITH flush=True (immediate)
    # # ═══════════════════════════════════════════════════════
    # print("\n=== PART 3: Without newline, WITH flush=True ===")
    # print("Watch carefully...")
    # time.sleep(1)

    # for chr in ["A", "B", "C", "D"]:
    #     print(chr, end="", flush=True)  # Appears immediately!
    #     time.sleep(0.5)
    # print()  # Final newline

    # print("A, B, C, D should have appeared one by one!")


@announce("EXAMPLE 5.2: Without newline, NO flush")
def example_5_2_without_newline_and_without_FLUSH():
    # ═══════════════════════════════════════════════════════
    # PART 2: Without \n and WITHOUT flush=True (may buffer)
    # ═══════════════════════════════════════════════════════
    print("Watch carefully...")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ BUFFER STATE:                                                       │
    # │                                                                     │
    # │   Buffer: [empty] → [A] → [AB] → [ABC] → [ABCD] → FLUSH with \n     │
    # │   Screen: (nothing) (nothing) (nothing) (nothing) → "ABCD"          │
    # │                                                                     │
    # │   All characters wait in buffer until \n triggers flush!            │
    # └─────────────────────────────────────────────────────────────────────┘

    for char in ["A", "B", "C", "D"]:
        print(char, end="")  # No newline → buffered (May NOT appear immediately)
        time.sleep(0.5)
    print()  # Newline - NOW everything flushes and appears!

    print("Did A, B, C, D appear one by one, or all at once?")
    print("(Behavior depends on your terminal/environment)")

    time.sleep(2)


@announce("EXAMPLE 5.3: Without newline, WITH flush=True")
def example_5_3_without_newline_but_with_FLUSH():
    # ═══════════════════════════════════════════════════════
    # PART 3: Without \n but WITH flush=True (immediate)
    # ═══════════════════════════════════════════════════════
    print("Watch carefully...")
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ WITH flush=True - Each character immediately displayed:             │
    # │                                                                     │
    # │   print("A") → Buffer[A] → FLUSH → Screen: A                        │
    # │   print("B") → Buffer[B] → FLUSH → Screen: AB                       │
    # │   print("C") → Buffer[C] → FLUSH → Screen: ABC                      │
    # │   print("D") → Buffer[D] → FLUSH → Screen: ABCD                     │
    # └─────────────────────────────────────────────────────────────────────┘

    for char in ["A", "B", "C", "D"]:
        print(char, end="", flush=True)  # Appears immediately!
        time.sleep(0.5)
    print()  # Final newline

    print("A, B, C, D should have appeared one by one!")

    time.sleep(2)


@announce("PART 4: Carriage Return (\\r) Basics")
def example_8_carriage_return_DOESNT_AUTO_FLUSH():
    # ═══════════════════════════════════════════════════════
    # PART 4: Carriage Return (\r) - DOES NOT AUTO-FLUSH!
    # ═══════════════════════════════════════════════════════

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ IMPORTANT DIFFERENCE:                                               │
    # │                                                                     │
    # │   \n (newline)         = Move to NEXT line      + AUTO-FLUSH ✓      │
    # │   \r (carriage return) = Move to START of line + NO FLUSH ✗         │
    # │                                                                     │
    # │ \r moves cursor back to beginning of line, so next output           │
    # │ OVERWRITES whatever was there before.                               │
    # └─────────────────────────────────────────────────────────────────────┘

    print("Understanding \\r vs \\n:")
    print("  \\n = Newline         → Goes to NEXT line + flushes")
    print("  \\r = Carriage Return → Goes to START of SAME line + NO flush")
    time.sleep(2)



if __name__ == "__main__":
    manual_flush()
    without_flush()
    with_flush()
    example_5_1_newline_auto_flush()
    example_5_2_without_newline_and_without_FLUSH()
    example_5_3_without_newline_but_with_FLUSH()
    example_8_carriage_return_DOESNT_AUTO_FLUSH()