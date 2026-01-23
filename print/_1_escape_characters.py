import time
import sys


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


# ==========================================
# 1. The Newline (\n)
# ==========================================
@announce("1. Newline (\\n)")
def _1_learn_newline():
    # Standard usage
    print("Line 1\nLine 2\nLine 3")

    # It allows you to format text blocks in a single string
    print("\nResult:")
    print("Shopping List:\n- Eggs\n- Milk\n- Bread")
    # time.sleep(1)


# ==========================================
# 2. The Horizontal Tab (\t)
# ==========================================
@announce("2. Tab (\\t)")
def _2_learn_tab():
    print("Without tabs:")
    print("ID Name Role")
    print("1 Alice CEO")
    print("2 Bob Developer")

    print("\nWith tabs (aligns to grid):")
    # \t jumps the cursor to the next 'tab stop' (usually every 4 or 8 spaces)
    print("ID\tName\tRole")
    print("1\tAlice\tCEO")
    print("2\tBob\tDev")
    print("100\tCharlie\tManager")


# ==========================================
# 3. The Carriage Return (\r)
# ==========================================
@announce("3. Carriage Return (\\r)")
def _3_learn_carriage_return():
    print("This moves the cursor back to the START of the line.")
    print("It allows us to overwrite text (great for loading bars).")

    print("Downloading...", end="")  # Stay on same line
    time.sleep(1)

    # \r moves cursor to start, then we overwrite with new text
    print("\rDownloading... 25%", end="")
    time.sleep(1)

    print("\rDownloading... 50%", end="")
    time.sleep(1)

    print("\rDownloading... 100%", end="")
    time.sleep(1)

    print("\nDone!")  # Move to next line finally


@announce("Example 3a: Simple \\r demonstration")
def _3_a_Simple_carriage_return_demonstration():
    # ───────────────────────────────────────────────────────
    # Example 3a: Simple \r demonstration
    # ───────────────────────────────────────────────────────
    time.sleep(1)

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ What happens with \r:                                               │
    # │                                                                     │
    # │   print("AAAAA\rBB")                                                │
    # │                                                                     │
    # │   Step 1: Print "AAAAA"  → Screen: AAAAA                            │
    # │   Step 2: \r             → Cursor moves to start: |AAAAA            │
    # │   Step 3: Print "BB"     → Overwrites first 2 chars: BBAAA          │
    # │                                                                     │
    # │   Final result: "BBAAA"                                             │
    # └─────────────────────────────────────────────────────────────────────┘

    print("Printing 'AAAAA\\rBB':")
    print("AAAAA\rBB")
    print("  Notice: BB overwrote the first two A's → BBAAA")

    time.sleep(2)


# ==========================================
# 4. The Backspace (\b)
# ==========================================
@announce("4. Backspace (\\b)")
def _4_learn_backspace():
    print("This literally deletes the character to the left.")

    """
    print("Hello WorlX", end="", flush=True)


    flush=True: 
        "Put this text on the screen immediately, right now."
        If you are printing normal lines (with \n), you don't need to worry about flush.
        If you are using end="" to make loading bars, countdowns, or typing animations, you MUST use flush=True.
    flush=False (Default): 
        "Put this text in a temporary storage (buffer). 
        Wait until you have a full line or a lot of text, 
        then dump it on the screen all at once."
    """

    # Example: Simulating a typo fix
    print("Hello WorlX", end="", flush=True)
    time.sleep(1)

    # Move back one step, overwrite X with d
    print("\b", end="", flush=True)
    time.sleep(0.5)
    print("d", end="", flush=True)
    print("\nResult: Hello World")


# ==========================================
# 5. Escaping Quotes & Backslashes (\\, \", \')
# ==========================================
@announce("5. Escaping Symbols")
def _5_learn_escaping_symbols():
    # PROBLEM: Python thinks the string ends at the second quote
    # print("She said "Hello" to me")  <-- This causes an error

    # SOLUTION: Use the backslash to ignore the quote's functionality
    print('She said "Hello" to me.')

    # PROBLEM: How do you print a backslash? (e.g. Windows file paths)
    # print("C:\Users\Name") <-- Python thinks \U is an escape code

    # SOLUTION: Double backslash
    print("C:\\Users\\Name\\Documents")


# ==========================================
# 6. Raw Strings (The "I hate backslashes" solution)
# ==========================================
@announce("6. Raw Strings (r'...')")
def _6_learn_raw_strings():
    # If you put an 'r' before the string, Python ignores ALL escape characters.
    # This is heavily used in Regex and File Paths.

    path = r"C:\Users\New\Table\read.txt"
    print(f"Raw string output: {path}")
    print("(Notice I didn't have to double the backslashes!)")


def other_not_yet_refactored():
    # =============================================================================
    # PYTHON ESCAPE SEQUENCES COMPLETE TUTORIAL
    # =============================================================================
    # A comprehensive guide to Python's escape sequences and special characters.

    # Author: Escape Sequences Tutorial
    # Python Version: 3.7+

    # Table of Contents:
    #     1. Newline (\n)
    #     2. Carriage Return (\r)
    #     3. Tab Characters (\t, \v)
    #     4. Backspace (\b)
    #     5. Bell/Alert (\a)
    #     6. Form Feed (\f)
    #     7. Backslash (\\)
    #     8. Quotes (\' and \")
    #     9. Null Character (\0)
    #     10. Hexadecimal (\xhh)
    #     11. Octal (\ooo)
    #     12. Unicode 16-bit (\uxxxx)
    #     13. Unicode 32-bit (\Uxxxxxxxx)
    #     14. Unicode by Name (\N{name})
    #     15. Raw Strings (r"...")
    #     16. Combining Escape Sequences
    #     17. Practical Examples

    # Run this script to see all examples in action!
    # =============================================================================

    import time
    import sys

    def print_section(title, section_num):
        """Helper function to print section headers."""
        print("\n" + "=" * 70)
        print(f" SECTION {section_num}: {title}")
        print("=" * 70 + "\n")

    def print_subsection(title):
        """Helper function to print subsection headers."""
        print(f"\n--- {title} ---\n")

    def show_repr(string, description=""):
        """Show both the printed version and repr of a string."""
        if description:
            print(f"  {description}")
        print(f"    Printed:  {string}")
        print(f"    repr():   {repr(string)}")
        print()

    # =============================================================================
    # SECTION 1: NEWLINE (\n)
    # =============================================================================

    def section_1_newline():
        """
        \n - Newline (Line Feed)
        Moves cursor to the beginning of the NEXT line.
        Most common escape sequence.
        """
        print_section("NEWLINE (\\n)", 1)

        print("  The newline character moves cursor to the next line.\n")

        # Basic usage
        print_subsection("Basic Usage")

        print("  Line 1\n  Line 2\n  Line 3")

        print()
        show_repr("Hello\nWorld", "Two lines:")

        # Multiple newlines
        print_subsection("Multiple Newlines")

        print("  Before\n\n\n  After (3 blank lines above)")

        # In strings
        print_subsection("In Multi-line Strings")

        message = "Dear User,\n\nWelcome to Python!\n\nBest regards,\nThe Team"
        print(f"  {message}")

        # Split by newline
        print_subsection("Splitting by Newline")

        text = "apple\nbanana\ncherry"
        lines = text.split("\n")
        print(f"  Original: {repr(text)}")
        print(f"  Split:    {lines}")

        # Platform differences
        print_subsection("Platform Line Endings")
        print("""
        Different systems use different line endings:
        
        \\n      - Unix/Linux/macOS (LF - Line Feed)
        \\r\\n    - Windows (CRLF - Carriage Return + Line Feed)  
        \\r      - Old Mac OS (CR - Carriage Return)
        
        Python's open() with text mode handles this automatically!
        """)

    # =============================================================================
    # SECTION 2: CARRIAGE RETURN (\r)
    # =============================================================================

    def section_2_carriage_return():
        """
        \r - Carriage Return
        Moves cursor to the beginning of the SAME line (without advancing).
        Used for progress indicators, overwriting text.
        """
        print_section("CARRIAGE RETURN (\\r)", 2)

        print("  Carriage return moves cursor to start of SAME line.")
        print("  Next output OVERWRITES previous content.\n")

        # Basic demonstration
        print_subsection("Basic Demonstration")

        print("  Watch what happens:")
        print("  'AAAAA\\rBB' produces:", "AAAAA\rBB")
        print()

        show_repr("AAAAA\rBB", "Overwriting first 2 characters:")

        # Visual explanation
        print_subsection("Visual Explanation")
        print("""
        "Hello\\rXX" → What happens:
        
        Step 1: Print "Hello"    → Screen shows: Hello
        Step 2: \\r moves cursor  → Cursor at: |Hello (beginning)
        Step 3: Print "XX"       → Screen shows: XXllo
        
        Result: "XXllo"
        """)

        print(f"  Actual output: 'Hello\rXX' → '{'Hello'[:0] + 'XX' + 'Hello'[2:]}'")
        print(f"  Printed: Hello\rXX")

        # Progress bar
        print_subsection("Progress Bar Example")
        print("  Simulating download progress:")

        for i in range(0, 101, 10):
            bar = "█" * (i // 5) + "░" * (20 - i // 5)
            print(f"\r  [{bar}] {i:3d}%", end="", flush=True)
            time.sleep(0.2)
        print()  # Final newline

        # Spinner
        print_subsection("Spinner Animation")
        print("  Simulating loading spinner:")

        spinner_chars = "|/-\\"
        for i in range(20):
            print(f"\r  Loading {spinner_chars[i % 4]}", end="", flush=True)
            time.sleep(0.1)
        print("\r  Done!     ")  # Extra spaces to clear spinner

        # Countdown
        print_subsection("Countdown Timer")

        for i in range(5, 0, -1):
            print(f"\r  Countdown: {i}", end="", flush=True)
            time.sleep(0.5)
        print("\r  Blast off! 🚀")

    # =============================================================================
    # SECTION 3: TAB CHARACTERS (\t, \v)
    # =============================================================================

    def section_3_tabs():
        """
        \t - Horizontal Tab (moves cursor to next tab stop, usually 8 spaces)
        \v - Vertical Tab (moves cursor down, rarely used)
        """
        print_section("TAB CHARACTERS (\\t, \\v)", 3)

        # Horizontal tab
        print_subsection("Horizontal Tab (\\t)")

        print("  Tab moves cursor to next tab stop (usually every 8 characters)\n")

        print("  No tabs:")
        print("  Name Age City")
        print()
        print("  With tabs:")
        print("  Name\tAge\tCity")
        print("  Alice\t25\tNew York")
        print("  Bob\t30\tLos Angeles")
        print("  Charlie\t35\tChicago")

        show_repr("Col1\tCol2\tCol3", "\n  Tab representation:")

        # Tab alignment issues
        print_subsection("Tab Alignment (Can Be Tricky!)")

        print("  Tabs align to fixed positions, not fixed widths:\n")
        print("  12345678|2345678|2345678|2345678")  # Shows tab stops
        print("  A\tB\tC\tD")  # Short strings
        print("  Long\tB\tC\tD")  # Medium string
        print("  VeryLong\tB\tC")  # Long string shifts alignment

        print("\n  Notice how 'VeryLong' pushes B to the next tab stop!")

        # Better alternative for tables
        print_subsection("Better Alternative: String Formatting")

        print("  Using f-strings with fixed width:\n")
        print(f"  {'Name':<12}{'Age':<8}{'City':<15}")
        print(f"  {'-' * 12}{'-' * 8}{'-' * 15}")
        print(f"  {'Alice':<12}{25:<8}{'New York':<15}")
        print(f"  {'Bob':<12}{30:<8}{'Los Angeles':<15}")
        print(f"  {'Charlie':<12}{35:<8}{'Chicago':<15}")

        # Vertical tab
        print_subsection("Vertical Tab (\\v) - Rarely Used")

        print("  Vertical tab moves cursor down (terminal-dependent):")
        print("  Before\vAfter vertical tab")
        print()
        print("  Note: Behavior varies by terminal. Often shows as special character.")

        show_repr("A\vB", "Vertical tab representation:")

    # =============================================================================
    # SECTION 4: BACKSPACE (\b)
    # =============================================================================

    def section_4_backspace():
        """
        \b - Backspace
        Moves cursor ONE position backward (doesn't delete by itself).
        """
        print_section("BACKSPACE (\\b)", 4)

        print("  Backspace moves cursor back ONE position.")
        print("  It does NOT delete - next character overwrites.\n")

        # Basic demonstration
        print_subsection("Basic Demonstration")

        print("  'Hello\\b\\b\\b\\bXX' produces:", "Hello\b\b\b\bXX")

        show_repr("Hello\b\b\b\bXX", "Moving back 4 positions, writing XX:")

        # Visual explanation
        print_subsection("Visual Explanation")
        print("""
        "ABCDE\\b\\bXY" → What happens:
        
        Step 1: Print "ABCDE"    → Screen: ABCDE, Cursor after E
        Step 2: \\b (backspace)   → Cursor moves back to D
        Step 3: \\b (backspace)   → Cursor moves back to C
        Step 4: Print "X"        → Overwrites C with X
        Step 5: Print "Y"        → Overwrites D with Y
        
        Result: "ABXYE"
        """)

        print(f"  Actual: ABCDE\b\bXY")

        # Erasing effect
        print_subsection("Simulating Backspace Delete")

        print("  To actually 'delete', use: \\b \\b (backspace, space, backspace)")
        print()
        print("  Watch: Typing then deleting...")

        text = "Hello World"
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.1)

        time.sleep(0.5)

        # "Delete" the word "World"
        for _ in range(5):
            print("\b \b", end="", flush=True)  # Backspace, space (erase), backspace
            time.sleep(0.15)

        time.sleep(0.3)
        print("Python!")  # Type new text

        # Practical: Simple animation
        print_subsection("Animation Using Backspace")

        frames = [
            "[=     ]",
            "[ =    ]",
            "[  =   ]",
            "[   =  ]",
            "[    = ]",
            "[     =]",
            "[    = ]",
            "[   =  ]",
            "[  =   ]",
            "[ =    ]",
        ]

        print("  ", end="")
        for _ in range(2):  # Two cycles
            for frame in frames:
                print(frame, end="", flush=True)
                time.sleep(0.1)
                print("\b" * len(frame), end="", flush=True)
        print("[  ●   ] Done!")

    # =============================================================================
    # SECTION 5: BELL/ALERT (\a)
    # =============================================================================

    def section_5_bell():
        """
        \a - Bell/Alert
        Makes a beep sound (terminal-dependent).
        """
        print_section("BELL/ALERT (\\a)", 5)

        print("  The bell character produces an audible beep.")
        print("  (If your terminal supports it)\n")

        print_subsection("Basic Usage")

        print("  Ringing bell 3 times (you may hear beeps)...")
        for i in range(3):
            print(f"\a  Beep {i + 1}!", flush=True)
            time.sleep(0.5)

        show_repr("\a", "Bell representation:")

        print_subsection("Common Uses")
        print("""
        - Alerting user that a long task is complete
        - Warning about errors
        - Notification sounds in terminal applications
        
        Note: Many modern terminals have bells disabled or muted.
        Some show a visual flash instead of sound.
        """)

        # Practical example
        print_subsection("Practical: Task Completion Alert")

        print("  Simulating long task...")
        for i in range(3):
            print(f"  Processing step {i + 1}/3...", flush=True)
            time.sleep(0.5)
        print("\a  Task complete! (bell)")

    # =============================================================================
    # SECTION 6: FORM FEED (\f)
    # =============================================================================

    def section_6_form_feed():
        """
        \f - Form Feed
        Originally used to advance printer to next page.
        In terminals, behavior varies (often just a special character).
        """
        print_section("FORM FEED (\\f)", 6)

        print("  Form feed was used to advance printers to the next page.")
        print("  In modern terminals, behavior varies.\n")

        print_subsection("Basic Usage")

        show_repr("Page 1\fPage 2", "Form feed representation:")

        print("  Printed: Page 1\fPage 2")

        print_subsection("Historical Context")
        print("""
        In the old days of line printers:
        
        \\f (Form Feed) = Eject current page, start new page
        
        This was useful for:
        - Printing multiple documents
        - Starting new sections on fresh pages
        - Print job separation
        
        Today: Mostly obsolete, but still valid escape sequence.
        Some terminals clear the screen, others show a symbol.
        """)

    # =============================================================================
    # SECTION 7: BACKSLASH (\\)
    # =============================================================================

    def section_7_backslash():
        # \\ - Literal Backslash
        # Since \ starts escape sequences, use \\ for literal backslash.

        print_section("BACKSLASH (\\\\)", 7)

        print("  Since \\ starts escape sequences, use \\\\ for literal backslash.\n")

        print_subsection("The Problem")

        print("  Trying to print 'C:\\new_folder':")
        print("  ❌ print('C:\\new_folder')  → C:")
        print("                               ew_folder")
        print("     (\\n was interpreted as newline!)")

        print_subsection("The Solution")

        print("  ✓ print('C:\\\\new_folder') →", "C:\\new_folder")
        print("  ✓ print(r'C:\\new_folder')  →", r"C:\new_folder", "(raw string)")

        show_repr("C:\\Users\\name", "\n  Windows path:")

        # Common cases
        print_subsection("Common Cases Needing \\\\")

        paths = [
            ("Windows path", "C:\\Users\\Documents\\file.txt"),
            ("UNC path", "\\\\server\\share\\folder"),
            ("Regex pattern", "\\d+\\.\\d+"),
            ("LaTeX", "\\alpha + \\beta"),
        ]

        for name, path in paths:
            print(f"  {name + ':':<20} {path}")

        print_subsection("Counting Backslashes")

        s = "A\\B\\\\C"
        print(f"  String: {repr(s)}")
        print(f"  Printed: {s}")
        print(f"  Number of backslashes: {s.count(chr(92))}")  # chr(92) is backslash

    # =============================================================================
    # SECTION 8: QUOTES (\' and \")
    # =============================================================================

    def section_8_quotes():
        """
        \' - Escaped single quote
        \" - Escaped double quote
        Used when you need quotes inside strings.
        """
        print_section("QUOTES (\\' and \\\")", 8)

        print("  Use escaped quotes when string delimiters conflict.\n")

        print_subsection("The Problem")
        print("""
        # ❌ Syntax Error:
        message = "He said "Hello" to me"
        
        # ❌ Syntax Error:
        message = 'It's a beautiful day'
        """)

        print_subsection("Solutions")

        # Solution 1: Escape the quotes
        print("  Solution 1: Escape the quotes")
        print(f'    "He said \\"Hello\\" to me" → He said "Hello" to me')
        print(f"    'It\\'s a beautiful day'    → It's a beautiful day")
        print()

        # Solution 2: Use different outer quotes
        print("  Solution 2: Use different outer quotes")
        print(f'    \'He said "Hello" to me\'   → He said "Hello" to me')
        print(f"    \"It's a beautiful day\"    → It's a beautiful day")
        print()

        # Solution 3: Triple quotes
        print("  Solution 3: Triple quotes")
        multi = '''He said "Hello" and then added, "It's great!"'''
        print(f"    {repr(multi[:30])}...")
        print(f"    → {multi}")

        # Examples
        print_subsection("Practical Examples")

        examples = [
            ("JSON-like string", '{"name": "John", "age": 30}'),
            ("SQL query", "SELECT * FROM users WHERE name='O\\'Brien'"),
            ("Dialogue", '''She asked, "What\\'s your name?"'''),
            ("HTML attribute", '<div class="container">'),
        ]

        for name, example in examples:
            print(f"  {name}:")
            print(f"    {example}")
            print()

    # =============================================================================
    # SECTION 9: NULL CHARACTER (\0)
    # =============================================================================

    def section_9_null():
        """
        \0 - Null Character (ASCII 0)
        Represents "nothing" - used in C for string termination.
        In Python, it's just another character.
        """
        print_section("NULL CHARACTER (\\0)", 9)

        print(
            "  Null character (ASCII 0) - historically used for string termination.\n"
        )

        print_subsection("Basic Info")

        null_char = "\0"
        print(f"  Null character: {repr(null_char)}")
        print(f"  ASCII value: {ord(null_char)}")
        print(f"  Length of '\\0': {len(null_char)} (it IS a character!)")

        print_subsection("Python vs C")
        print("""
        In C:
        - Strings are null-terminated
        - "Hello" is actually 'H','e','l','l','o','\\0' (6 bytes)
        - Null marks the end of the string
        
        In Python:
        - Strings are length-prefixed objects
        - Null is just another character
        - "Hello\\0World" has length 11
        """)

        # Demonstration
        print_subsection("Demonstration")

        s = "Hello\0World"
        print(f"  String: {repr(s)}")
        print(f"  Length: {len(s)}")
        print(f"  Printed: {s}")  # May show nothing for \0 or a space
        print()

        # Split by null
        parts = s.split("\0")
        print(f"  Split by null: {parts}")

        # Common use cases
        print_subsection("Use Cases")
        print("""
        - Interfacing with C libraries (ctypes)
        - Binary file formats
        - Some network protocols
        - Null-terminated strings in databases
        """)

    # =============================================================================
    # SECTION 10: HEXADECIMAL (\xhh)
    # =============================================================================

    def section_10_hex():
        # \xhh - Character by hexadecimal value
        # hh = two hex digits (00 to FF)

        print_section("HEXADECIMAL (\\xhh)", 10)

        print(
            "  \\xhh represents a character by its hexadecimal ASCII/Unicode value.\n"
        )

        print_subsection("Basic Syntax")
        print("""
        \\xhh where hh is exactly 2 hex digits (0-9, A-F)
        
        Examples:
        \\x41 = 'A' (65 in decimal)
        \\x42 = 'B' (66 in decimal)
        \\x20 = ' ' (space, 32 in decimal)
        \\x00 = null character
        \\xFF = 255
        """)

        print_subsection("Common Characters")

        hex_chars = [
            ("\\x00", "\x00", "Null"),
            ("\\x09", "\x09", "Tab"),
            ("\\x0A", "\x0a", "Newline (\\n)"),
            ("\\x0D", "\x0d", "Carriage Return (\\r)"),
            ("\\x20", "\x20", "Space"),
            ("\\x41", "\x41", "A"),
            ("\\x5A", "\x5a", "Z"),
            ("\\x61", "\x61", "a"),
            ("\\x7A", "\x7a", "z"),
        ]

        print(f"  {'Escape':<10} {'Char':<8} {'Description':<20} {'Ord'}")
        print(f"  {'-' * 10} {'-' * 8} {'-' * 20} {'-' * 5}")

        for escape, char, desc in hex_chars:
            display = repr(char) if char in "\x00\x09\x0a\x0d" else char
            print(f"  {escape:<10} {display:<8} {desc:<20} {ord(char)}")

        # Building strings with hex
        print_subsection("Building Strings")

        # Spell "HELLO" using hex
        hello_hex = "\x48\x45\x4c\x4c\x4f"
        print(f"  \\x48\\x45\\x4C\\x4C\\x4F = '{hello_hex}'")

        # Mixing hex with regular characters
        mixed = "Price: \x24100"  # \x24 is $
        print(f"  'Price: \\x24100' = '{mixed}'")

        print_subsection("Converting Characters")

        char = "A"
        print(f"  Character: '{char}'")
        print(f"  ord('{char}'): {ord(char)}")
        print(f"  hex(ord('{char}')): {hex(ord(char))}")
        print(f"  Escape: \\x{ord(char):02X}")

    # =============================================================================
    # SECTION 11: OCTAL (\ooo)
    # =============================================================================

    def section_11_octal():
        # \ooo - Character by octal value
        # ooo = one to three octal digits (0-7)

        print_section("OCTAL (\\ooo)", 11)

        print("  \\ooo represents a character by its octal (base-8) value.\n")

        print_subsection("Basic Syntax")
        print("""
        \\ooo where ooo is 1-3 octal digits (0-7)
        
        Examples:
        \\101 = 'A' (65 in decimal = 101 in octal)
        \\102 = 'B' (66 in decimal = 102 in octal)
        \\040 = ' ' (space, 32 in decimal = 40 in octal)
        \\000 = null character
        \\377 = 255 (maximum for one byte)
        """)

        print_subsection("Octal vs Decimal vs Hex")

        print(f"  {'Char':<6} {'Decimal':<10} {'Octal':<10} {'Hex':<10}")
        print(f"  {'-' * 6} {'-' * 10} {'-' * 10} {'-' * 10}")

        for char in "ABCXYZ":
            dec = ord(char)
            print(
                f"  {char:<6} {dec:<10} \\{oct(dec)[2:]:<9} \\x{hex(dec)[2:].upper():<8}"
            )

        print_subsection("Demonstration")

        # Spell "HELLO" using octal
        hello_octal = "\110\105\114\114\117"
        print(f"  \\110\\105\\114\\114\\117 = '{hello_octal}'")

        # Permissions example (common use of octal)
        print_subsection("Common Use: File Permissions")
        print("""
        Octal is commonly used for Unix file permissions:
        
        Permission Octal:
        7 = rwx (read + write + execute)
        6 = rw- (read + write)
        5 = r-x (read + execute)
        4 = r-- (read only)
        0 = --- (no permission)
        
        Example: 0o755 = rwxr-xr-x (owner: all, others: read+execute)
        
        import os
        os.chmod("file.txt", 0o755)  # Octal literal in Python
        """)

    # =============================================================================
    # SECTION 12: UNICODE 16-BIT (\uxxxx)
    # =============================================================================

    def section_12_unicode_16():
        # \uxxxx - Unicode character (16-bit)
        # xxxx = exactly 4 hex digits
        # Covers Basic Multilingual Plane (most common characters)

        print_section("UNICODE 16-BIT (\\uxxxx)", 12)

        print("  \\uxxxx represents Unicode characters using 4 hex digits.\n")

        print_subsection("Basic Syntax")
        print("""
        \\uxxxx where xxxx is exactly 4 hex digits
        
        Range: \\u0000 to \\uFFFF (65,536 characters)
        This covers the Basic Multilingual Plane (BMP)
        """)

        print_subsection("Examples by Category")

        # Various Unicode examples
        categories = [
            (
                "Currency Symbols",
                [
                    ("\\u0024", "\u0024", "Dollar"),
                    ("\\u20AC", "\u20ac", "Euro"),
                    ("\\u00A3", "\u00a3", "Pound"),
                    ("\\u00A5", "\u00a5", "Yen"),
                    ("\\u20B9", "\u20b9", "Rupee"),
                ],
            ),
            (
                "Math Symbols",
                [
                    ("\\u00B1", "\u00b1", "Plus-minus"),
                    ("\\u00D7", "\u00d7", "Multiply"),
                    ("\\u00F7", "\u00f7", "Divide"),
                    ("\\u221E", "\u221e", "Infinity"),
                    ("\\u2211", "\u2211", "Summation"),
                ],
            ),
            (
                "Arrows",
                [
                    ("\\u2190", "\u2190", "Left"),
                    ("\\u2191", "\u2191", "Up"),
                    ("\\u2192", "\u2192", "Right"),
                    ("\\u2193", "\u2193", "Down"),
                    ("\\u21C4", "\u21c4", "Exchange"),
                ],
            ),
            (
                "Greek Letters",
                [
                    ("\\u03B1", "\u03b1", "Alpha"),
                    ("\\u03B2", "\u03b2", "Beta"),
                    ("\\u03B3", "\u03b3", "Gamma"),
                    ("\\u03C0", "\u03c0", "Pi"),
                    ("\\u03A9", "\u03a9", "Omega"),
                ],
            ),
            (
                "Misc Symbols",
                [
                    ("\\u2764", "\u2764", "Heart"),
                    ("\\u2605", "\u2605", "Star"),
                    ("\\u263A", "\u263a", "Smiley"),
                    ("\\u2602", "\u2602", "Umbrella"),
                    ("\\u266B", "\u266b", "Music"),
                ],
            ),
        ]

        for category, symbols in categories:
            print(f"  {category}:")
            for escape, char, name in symbols:
                print(f"    {escape} → {char}  ({name})")
            print()

        print_subsection("International Text")

        greetings = [
            ("English", "Hello"),
            ("Japanese", "\u3053\u3093\u306b\u3061\u306f"),
            ("Chinese", "\u4f60\u597d"),
            ("Korean", "\uc548\ub155"),
            ("Russian", "\u041f\u0440\u0438\u0432\u0435\u0442"),
            ("Arabic", "\u0645\u0631\u062d\u0628\u0627"),
            ("Hindi", "\u0928\u092e\u0938\u094d\u0924\u0947"),
        ]

        for lang, greeting in greetings:
            print(f"  {lang + ':':<12} {greeting}")

        print_subsection("Finding Unicode Values")

        char = "π"
        print(f"  Character: {char}")
        print(f"  ord('{char}'): {ord(char)}")
        print(f"  hex: {hex(ord(char))}")
        print(f"  Escape: \\u{ord(char):04X}")

    # =============================================================================
    # SECTION 13: UNICODE 32-BIT (\Uxxxxxxxx)
    # =============================================================================

    def section_13_unicode_32():
        # \Uxxxxxxxx - Unicode character (32-bit)
        # xxxxxxxx = exactly 8 hex digits
        # Covers ALL Unicode characters including emojis

        print_section("UNICODE 32-BIT (\\Uxxxxxxxx)", 13)

        print("  \\Uxxxxxxxx (capital U) for characters beyond BMP.\n")

        print_subsection("Basic Syntax")
        print("""
        \\Uxxxxxxxx where xxxxxxxx is exactly 8 hex digits
        
        Used for characters above \\uFFFF (code points > 65535)
        This includes: Emojis, rare scripts, historic scripts, etc.
        """)

        print_subsection("Emojis (require \\U)")

        emojis = [
            ("\\U0001F600", "\U0001f600", "Grinning face"),
            ("\\U0001F4BB", "\U0001f4bb", "Laptop"),
            ("\\U0001F40D", "\U0001f40d", "Snake (Python!)"),
            ("\\U0001F680", "\U0001f680", "Rocket"),
            ("\\U0001F3AF", "\U0001f3af", "Target"),
            ("\\U0001F389", "\U0001f389", "Party popper"),
            ("\\U0001F525", "\U0001f525", "Fire"),
            ("\\U0001F4A1", "\U0001f4a1", "Light bulb"),
        ]

        print(f"  {'Escape':<16} {'Emoji':<6} {'Name'}")
        print(f"  {'-' * 16} {'-' * 6} {'-' * 20}")

        for escape, emoji, name in emojis:
            print(f"  {escape:<16} {emoji:<6} {name}")

        print_subsection("\\u vs \\U")
        print("""
        \\uxxxx  → 4 hex digits, Basic Multilingual Plane only (0-65535)
        \\Uxxxxxxxx → 8 hex digits, ALL Unicode (0-1114111)
        
        Examples:
        \\u0041      → A (works)
        \\U00000041  → A (also works, same character)
        
        \\u1F600     → ❌ Error! Only 4 digits allowed
        \\U0001F600  → 😀 Correct!
        """)

        print_subsection("Getting Emoji Code Points")

        emoji = "🐍"
        print(f"  Emoji: {emoji}")
        print(f"  ord(): {ord(emoji)}")
        print(f"  hex(): {hex(ord(emoji))}")
        print(f"  Escape: \\U{ord(emoji):08X}")

    # =============================================================================
    # SECTION 14: UNICODE BY NAME (\N{name})
    # =============================================================================

    def section_14_unicode_name():
        # \N{name} - Unicode character by name
        # Most readable way to include special characters

        print_section("UNICODE BY NAME (\\N{name})", 14)

        print("  \\N{name} lets you use the official Unicode character name.\n")

        print_subsection("Basic Syntax")
        print("""
        \\N{UNICODE CHARACTER NAME}
        
        Names are defined by the Unicode Standard.
        Case-insensitive in Python 3.
        """)

        print_subsection("Examples")

        examples = [
            ("\\N{GREEK SMALL LETTER PI}", "\N{GREEK SMALL LETTER PI}"),
            ("\\N{INFINITY}", "\N{INFINITY}"),
            ("\\N{EURO SIGN}", "\N{EURO SIGN}"),
            ("\\N{COPYRIGHT SIGN}", "\N{COPYRIGHT SIGN}"),
            ("\\N{REGISTERED SIGN}", "\N{REGISTERED SIGN}"),
            ("\\N{DEGREE SIGN}", "\N{DEGREE SIGN}"),
            ("\\N{BLACK HEART SUIT}", "\N{BLACK HEART SUIT}"),
            ("\\N{WHITE SMILING FACE}", "\N{WHITE SMILING FACE}"),
            ("\\N{SNAKE}", "\N{SNAKE}"),
            ("\\N{ROCKET}", "\N{ROCKET}"),
        ]

        print(f"  {'Name Escape':<40} {'Result'}")
        print(f"  {'-' * 40} {'-' * 6}")

        for escape, char in examples:
            print(f"  {escape:<40} {char}")

        print_subsection("Mathematical Formulas")

        formula = "\N{GREEK SMALL LETTER PI} \N{ALMOST EQUAL TO} 3.14159"
        print(f"  {formula}")

        einstein = "E = mc\N{SUPERSCRIPT TWO}"
        print(f"  {einstein}")

        water = "H\N{SUBSCRIPT TWO}O"
        print(f"  {water}")

        print_subsection("Finding Character Names")

        import unicodedata

        chars = ["π", "∞", "€", "♠", "★"]

        print(f"  {'Char':<6} {'Name'}")
        print(f"  {'-' * 6} {'-' * 40}")

        for char in chars:
            name = unicodedata.name(char, "UNKNOWN")
            print(f"  {char:<6} {name}")

        print("\n  You can use unicodedata.name() to find any character's name!")

    # =============================================================================
    # SECTION 15: RAW STRINGS (r"...")
    # =============================================================================

    def section_15_raw_strings():
        """
        r"..." or r'...' - Raw strings
        Escape sequences are NOT processed.
        """
        print_section('RAW STRINGS (r"...")', 15)

        print("  Raw strings treat backslash as a literal character.\n")

        print_subsection("Comparison: Normal vs Raw")

        comparisons = [
            ("Normal", "C:\\new\\folder", "C:\new\folder"),  # \n and \f interpreted
            ("Raw", r"C:\new\folder", r"C:\new\folder"),
        ]

        print(f"  String type:  Normal string       Raw string")
        print(f"  Code:         'C:\\\\new\\\\folder'   r'C:\\new\\folder'")
        print(f"  Result:       C:\\new\\folder      C:\\new\\folder")

        print_subsection("Why Raw Strings?")
        print("""
        Raw strings are useful when you have many backslashes:
        
        1. Windows file paths
        2. Regular expressions
        3. LaTeX strings
        """)

        print_subsection("Windows Paths")

        # Normal string - need double backslashes
        path_normal = "C:\\Users\\John\\Documents\\file.txt"

        # Raw string - single backslashes work
        path_raw = r"C:\Users\John\Documents\file.txt"

        print(f"  Normal: {path_normal}")
        print(f"  Raw:    {path_raw}")
        print(f"  Same?   {path_normal == path_raw}")

        print_subsection("Regular Expressions")

        import re

        text = "My phone is 123-456-7890"

        # Without raw string - need to escape backslashes
        pattern_normal = "\\d{3}-\\d{3}-\\d{4}"

        # With raw string - cleaner
        pattern_raw = r"\d{3}-\d{3}-\d{4}"

        print(f"  Text: {text}")
        print(f"  Normal pattern: {repr(pattern_normal)}")
        print(f"  Raw pattern:    {repr(pattern_raw)}")
        print(f"  Same pattern?   {pattern_normal == pattern_raw}")

        match = re.search(pattern_raw, text)
        print(f"  Match found:    {match.group()}")

        print_subsection("Limitations")
        print("""
        Raw strings CANNOT end with odd number of backslashes:
        
        ❌ r"C:\\folder\\"   → SyntaxError
        ✓  r"C:\\folder" + "\\\\"  → C:\\folder\\
        ✓  "C:\\\\folder\\\\"      → C:\\folder\\
        
        Reason: The parser still needs to handle quote escaping
                to know where the string ends.
        """)

    # =============================================================================
    # SECTION 16: COMBINING ESCAPE SEQUENCES
    # =============================================================================

    def section_16_combining():
        """
        Combining multiple escape sequences for complex output.
        """
        print_section("COMBINING ESCAPE SEQUENCES", 16)

        print("  Combining escapes for complex formatting.\n")

        print_subsection("Formatted Text Block")

        text_block = """
    \t╔════════════════════════════════╗
    \t║  Welcome to Python!            ║
    \t║                                ║
    \t║  Today\'s lesson: \"Escapes\"    ║
    \t║  Path: C:\\Python\\scripts       ║
    \t╚════════════════════════════════╝
    """
        print(text_block)

        print_subsection("CRLF Line Endings (Windows-style)")

        windows_text = "Line 1\r\nLine 2\r\nLine 3"
        print(f"  repr(): {repr(windows_text)}")
        print(f"  Lines: {windows_text.split(chr(13) + chr(10))}")

        print_subsection("Complex Table with Tabs")

        print("\tID\tName\tPrice\tQty")
        print("\t--\t----\t-----\t---")
        print("\t1\tApple\t\u00241.00\t10")
        print("\t2\tBanana\t\u00240.50\t25")
        print("\t3\tOrange\t\u00240.75\t15")

        print_subsection("Escape Sequence in Escape Sequence")

        # Showing escape sequences literally requires escaping
        print("  To print '\\n' literally:")
        print("    print('\\\\n')  → \\n")
        print("    print(r'\\n')   → \\n")

        print_subsection("Building Dynamic Strings")

        def format_file_info(path, size, modified):
            # Combine various escapes
            return f"\u2022 Path:\t{path}\n  Size:\t{size}\n  Modified:\t{modified}\n"

        info = format_file_info(r"C:\Users\data.txt", "1.5 KB", "2024-01-15")
        print(info)

    # =============================================================================
    # SECTION 17: PRACTICAL EXAMPLES
    # =============================================================================

    def section_17_practical():
        """
        Real-world practical examples using escape sequences.
        """
        print_section("PRACTICAL EXAMPLES", 17)

        print_subsection("1. Progress Bar")

        def progress_bar(current, total, width=40):
            percent = current / total
            filled = int(width * percent)
            bar = "█" * filled + "░" * (width - filled)
            print(f"\r  [{bar}] {percent * 100:.1f}%", end="", flush=True)

        print("  Downloading file...")
        for i in range(101):
            progress_bar(i, 100)
            time.sleep(0.02)
        print(" Done!")

        print_subsection("2. ASCII Art Box")

        def print_box(title, content):
            width = max(len(title), max(len(line) for line in content)) + 4

            print("  ┌" + "─" * width + "┐")
            print(f"  │ {title.center(width - 2)} │")
            print("  ├" + "─" * width + "┤")
            for line in content:
                print(f"  │ {line.ljust(width - 2)} │")
            print("  └" + "─" * width + "┘")

        print_box(
            "Python Tips",
            [
                "Use raw strings for regex",
                "\\n = newline, \\t = tab",
                "\\u for Unicode characters",
            ],
        )

        print_subsection("3. Typewriter Effect")

        def typewriter(text, delay=0.03):
            for char in text:
                print(char, end="", flush=True)
                time.sleep(delay)
            print()

        print("  ", end="")
        typewriter("Hello, World! 🌍")

        print_subsection("4. Status Spinner")

        def spinner_demo(duration=2):
            spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            end_time = time.time() + duration
            i = 0

            while time.time() < end_time:
                print(f"\r  {spinner[i % len(spinner)]} Loading...", end="", flush=True)
                time.sleep(0.1)
                i += 1
            print("\r  ✓ Complete!   ")

        spinner_demo(1.5)

        print_subsection("5. Colored Text (ANSI Escapes)")

        # ANSI escape codes for terminal colors
        print("  Using ANSI escape codes (\\033[...):\n")

        colors = [
            ("\033[31m", "Red"),
            ("\033[32m", "Green"),
            ("\033[33m", "Yellow"),
            ("\033[34m", "Blue"),
            ("\033[35m", "Magenta"),
            ("\033[36m", "Cyan"),
        ]

        for code, name in colors:
            print(f"  {code}This text is {name}\033[0m")

        print("\n  Note: ANSI codes may not work in all terminals.")

        print_subsection("6. Multi-line String Templates")

        def email_template(name, product, price):
            return f"""\
    Dear {name},

    Thank you for purchasing {product}!

    \tOrder Details:
    \t--------------
    \tProduct:\t{product}
    \tPrice:\t\t\u00a3{price:.2f}

    Best regards,
    The Team \U0001f4e7
    """

        print(email_template("John", "Python Course", 49.99))

        print_subsection("Complete Escape Sequence Reference")

        print("""
        ╔═══════════════╦══════════════════════════════════════════╗
        ║ Escape        ║ Description                              ║
        ╠═══════════════╬══════════════════════════════════════════╣
        ║ \\n            ║ Newline (line feed)                      ║
        ║ \\r            ║ Carriage return                          ║
        ║ \\t            ║ Horizontal tab                           ║
        ║ \\v            ║ Vertical tab                             ║
        ║ \\b            ║ Backspace                                ║
        ║ \\f            ║ Form feed                                ║
        ║ \\a            ║ Bell/alert                               ║
        ║ \\\\            ║ Literal backslash                        ║
        ║ \\'            ║ Single quote                             ║
        ║ \\"            ║ Double quote                             ║
        ║ \\0            ║ Null character                           ║
        ║ \\xhh          ║ Hex value (2 digits)                     ║
        ║ \\ooo          ║ Octal value (1-3 digits)                 ║
        ║ \\uxxxx        ║ Unicode 16-bit (4 hex digits)            ║
        ║ \\Uxxxxxxxx    ║ Unicode 32-bit (8 hex digits)            ║
        ║ \\N{name}      ║ Unicode by name                          ║
        ║ r"..."        ║ Raw string (no escape processing)        ║
        ╚═══════════════╩══════════════════════════════════════════╝
        """)

    # =============================================================================
    # MAIN - RUN ALL SECTIONS
    # =============================================================================

    def run_all():
        """Run all tutorial sections."""
        print("""
        ╔══════════════════════════════════════════════════════════════════════╗
        ║           PYTHON ESCAPE SEQUENCES COMPLETE TUTORIAL                  ║
        ║                                                                      ║
        ║  Learn all escape sequences: \\n \\r \\t \\x \\u and more!              ║
        ╚══════════════════════════════════════════════════════════════════════╝
        """)

        sections = [
            ("Newline (\\n)", section_1_newline),
            ("Carriage Return (\\r)", section_2_carriage_return),
            ("Tab Characters (\\t, \\v)", section_3_tabs),
            ("Backspace (\\b)", section_4_backspace),
            ("Bell/Alert (\\a)", section_5_bell),
            ("Form Feed (\\f)", section_6_form_feed),
            ("Backslash (\\\\)", section_7_backslash),
            ("Quotes (\\' and \\\")", section_8_quotes),
            ("Null Character (\\0)", section_9_null),
            ("Hexadecimal (\\xhh)", section_10_hex),
            ("Octal (\\ooo)", section_11_octal),
            ("Unicode 16-bit (\\uxxxx)", section_12_unicode_16),
            ("Unicode 32-bit (\\Uxxxxxxxx)", section_13_unicode_32),
            ("Unicode by Name (\\N{name})", section_14_unicode_name),
            ('Raw Strings (r"...")', section_15_raw_strings),
            ("Combining Escape Sequences", section_16_combining),
            ("Practical Examples", section_17_practical),
        ]

        print("  Available sections:")
        for i, (name, _) in enumerate(sections, 1):
            print(f"    {i:2}. {name}")

        print("\n  Options:")
        print("    - Enter section number (1-17) to run specific section")
        print("    - Enter 'all' to run all sections")
        print("    - Enter 'q' to quit\n")

        while True:
            choice = input("  Your choice: ").strip().lower()

            if choice == "q":
                print("\n  Thanks for learning Python escape sequences! 👋\n")
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

    run_all()


# ==========================================
# MAIN RUNNER
# ==========================================
if __name__ == "__main__":
    _1_learn_newline()
    _2_learn_tab()
    _3_learn_carriage_return()
    _3_a_Simple_carriage_return_demonstration()
    _4_learn_backspace()
    _5_learn_escaping_symbols()
    _6_learn_raw_strings()
    other_not_yet_refactored()
    

    # separator("--- Class Dismissed ---")
