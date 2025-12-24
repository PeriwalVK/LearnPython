from enum import Enum, auto, unique
import json
from os import sep

# --- DEFINITIONS ---

# 1. The Enum Way
class ColorEnum(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 2. The Class Way
class ColorClass:
    RED = 1
    GREEN = 2
    BLUE = 3


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#'*hash_len} {msg} {'#'*hash_len}")
    print("=" * l)







# ============================================================================
# 1. REPRESENTATION
# ============================================================================
separator("--- 1. REPRESENTATION ---")
# Enum keeps its identity
print(f"Enum:  {ColorEnum.RED}")        # Output: ColorEnum.RED
print(f"Class: {ColorClass.RED}")       # Output: 1






# ============================================================================
# 2. TYPE SAFETY
# ============================================================================
separator("--- 2. TYPE SAFETY ---")
# Enum is a specific type, Class attributes are just ints
print(f"Is Enum RED an int? {isinstance(ColorEnum.RED, int)}")  # False
print(f"Is Class RED an int? {isinstance(ColorClass.RED, int)}") # True






# ============================================================================
# 3. REVERSE LOOKUP (Value -> Name)
# ============================================================================
separator("--- 3. REVERSE LOOKUP (Value -> Name) ---")
# Enum allows you to find the name if you have the value (useful for APIs/DBs)
try:
    member = ColorEnum(2)
    print(f"Found Enum member corresponding to number 2: {member.name}") # Output: GREEN
except ValueError:
    print("Invalid code")

# Class cannot do this easily
print(f"Class cannot automatically convert '2' back to 'GREEN'")





# ============================================================================
# 4. ITERATION
# ============================================================================
separator("--- 4. ITERATION ---")
# Enums are iterable by default
print("Iterating Enum:")
for color in ColorEnum:
    print(f" - {color.name} is value {color.value}")


# Classes are not easily iterable without inspecting internal __dict__
print("Iterating Class: (Not supported naturally)")

try:
    for item in ColorClass:
        print(item)
except TypeError as e:
    print(f"  ❌ Error: {e}")
    print("  Workaround needed: use __dict__ or vars()")
    print("  using vars(ColorClass).items():")
    for key, value in vars(ColorClass).items():
        if not key.startswith('_'):
            print(f"  {key} = {value}")





# ============================================================================
# 5. IMMUTABILITY
# ============================================================================

separator("--- 5. IMMUTABILITY (Safety) ---")
# Try to overwrite a value at runtime

# Class: Allows overwriting (DANGEROUS)
ColorClass.RED = 999 
print(f"Class RED is now: {ColorClass.RED} (Oh no! ye toh badal gya)")
ColorClass.RED = 1 # Resetting back

# Enum: Protects you
try:
    ColorEnum.RED = 999
except AttributeError as e:
    print(f"✓ Enum protected, can not nutate: {e}") # Output: Cannot reassign members.






# ============================================================================
# 6. IDENTITY & COMPARISON
# ============================================================================
separator("6. IDENTITY & COMPARISON")

# Enum - identity check
print(f"ColorEnum.RED is ColorEnum.RED: {ColorEnum.RED is ColorEnum.RED}")  # True
print(f"ColorEnum.RED == ColorEnum.RED: {ColorEnum.RED == ColorEnum.RED}")  # True
print(f"ColorEnum.RED == 1: {ColorEnum.RED == 1} (bcz type-safe!)")  # False - type-safe!

# Regular class
print("")
print(f"ColorClass.RED == ColorClass.RED: {ColorClass.RED == ColorClass.RED}")  # True
print(f"ColorClass.RED == 1: {ColorClass.RED == 1} (bcz not type-safe!)")  # True - not type-safe!
print(f"ColorClass.RED is 1: {ColorClass.RED is 1} (small int caching)")  # True (small int caching)







# ============================================================================
# 7. HOW TO RESTRICT DUPLICATE VALUES IN ENUMS
# ============================================================================
separator("7. HOW TO RESTRICT DUPLICATE VALUES IN ENUMS")

class Status(Enum):
    PENDING = 1
    WAITING = 1  # Alias for PENDING - allowed by default -  providing an alternative name for the same status.
    ACTIVE = 2

print(f"Status.PENDING is Status.WAITING: {Status.PENDING is Status.WAITING}")
print(f"List of Status: {list(Status)}")  # only unique value will be printed, since WAITING is alias, hence not printed

# Prevent duplicates with @unique
try:
    @unique
    class StrictStatus(Enum):
        PENDING = 1
        WAITING = 1  # ❌ Will raise error
        ACTIVE = 2
except ValueError as e:
    print(f"✓ @unique decorator caught duplicate: {e}")


# Regular class - no protection
class StatusClass:
    PENDING = 1
    WAITING = 1  # Allowed, no warning
    ACTIVE = 2

print(f"StatusClass allows duplicates without warning")










# ============================================================================
# 8. ACCESSING MEMBERS
# ============================================================================
separator("8. ACCESSING MEMBERS")

# Enum - multiple access patterns
print(f"By attribute ==> ColorEnum.RED: {ColorEnum.RED}")
print(f"By value ==> ColorEnum(1): {ColorEnum(1)}")
print(f"By name ==> ColorEnum['RED']: {ColorEnum['RED']}")
print(f"Accessing Name ==> ColorEnum.RED.name: {ColorEnum.RED.name}")
print(f"Accessing Value ==> ColorEnum.RED.value: {ColorEnum.RED.value}")

# Regular class - only attribute access
print("\nRegular ColorClass - only attribute access")
print(f"ColorClass.RED: {ColorClass.RED}")
try:
    print(ColorClass(1))  # ❌ Not callable
except TypeError as e:
    print(f"ColorClass(1) fails: {e}")









# ============================================================================
# 9. TYPE CHECKING
# ============================================================================
separator("9. TYPE CHECKING")

def process_color_enum(color: ColorEnum):
    """Type-safe function"""
    if color == ColorEnum.RED:
        return "Stop"
    elif color == ColorEnum.GREEN:
        return "Go"
    return "Unknown" # kuchh unknown daala to exception raise hoga - idhar nahi aayega [x]

def process_color_class(color: int):
    """Not type-safe - accepts any int"""
    if color == ColorClass.RED:
        return "Stop"
    return "Unknown" # idhar exception raise nhi hoga - idhar aayega [✓]

print(f"Enum: {process_color_enum(ColorEnum.RED)}")
print(f"Enum with wrong type will be caught by type checker (mypy)")

print(f"Class: {process_color_class(ColorClass.RED)}")
print(f"Class: {process_color_class(999)}")  # ✓ No error - accepts any int!












# ============================================================================
# 10. STRING REPRESENTATION
# ============================================================================
separator("10. STRING REPRESENTATION")

print(f"str(ColorEnum.RED): {str(ColorEnum.RED)}")
print(f"repr(ColorEnum.RED): {repr(ColorEnum.RED)}")
print(f"ColorEnum.RED.name: {ColorEnum.RED.name}")
print(f"ColorEnum.RED.value: {ColorEnum.RED.value}")

print("")
print(f"str(ColorClass.RED): {str(ColorClass.RED)}")
print(f"repr(ColorClass.RED): {repr(ColorClass.RED)}")












# ============================================================================
# 11. AUTO VALUES (for automatic numbering)
# ============================================================================
separator("11. AUTO VALUES (for automatic numbering)")

class Priority(Enum):
    LOW = auto()      # 1
    MEDIUM = auto()   # 2
    HIGH = auto()     # 3

print("EnumClass: Using auto() for automatic numbering:")
for p in Priority:
    print(f"  {p.name} = {p.value}")

print("")
print("Regular class - manual assignment needed")
class PriorityClass:
    LOW = 1
    MEDIUM = 2
    HIGH = 3











# ============================================================================
# 12. JSON SERIALIZATION
# ============================================================================
separator("12. JSON SERIALIZATION")

# Enum - needs custom encoder
try:
    json.dumps(ColorEnum.RED)
except TypeError as e:
    print(f"Enum needs custom encoder: {e}")
    print(f"Solution: json.dumps(Color.RED.value) = {json.dumps(ColorEnum.RED.value)}")

# Regular class - just an int
print("")
print(f"Class: json.dumps(ColorClass.RED) = {json.dumps(ColorClass.RED)}")










# ============================================================================
# 13. MEMBERSHIP TESTING
# ============================================================================
separator("13. MEMBERSHIP TESTING")

print(f"ColorEnum.RED in ColorEnum: {ColorEnum.RED in ColorEnum}")
print(f"'RED' in ColorEnum.__members__: {'RED' in ColorEnum.__members__}")
print(f"1 in [c.value for c in ColorEnum]: {1 in [c.value for c in ColorEnum]}")

print("")
print(f"ColorClass has no membership concept (it's just a namespace)")













# ============================================================================
# 14. EXTENDED ENUM WITH METHODS
# ============================================================================
separator("14. EXTENDED ENUM WITH METHODS")

class HTTPStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    SERVER_ERROR = 500
    
    def is_error(self):
        return self.value >= 400
    
    def message(self):
        messages = {
            200: "Success",
            404: "Not Found",
            500: "Server Error"
        }
        return messages.get(self.value, "Unknown")

print(f"HTTPStatus.OK.is_error(): {HTTPStatus.OK.is_error()}")
print(f"HTTPStatus.NOT_FOUND.is_error(): {HTTPStatus.NOT_FOUND.is_error()}")
print(f"HTTPStatus.NOT_FOUND.message(): {HTTPStatus.NOT_FOUND.message()}")










# ============================================================================
# DECISION GUIDE
# ============================================================================
separator("DECISION GUIDE (WHEN TO USE WHAT?)")

print("""
✅ USE ENUM WHEN:
  • You have a fixed set of related constants (states, types, categories)
  • You want type safety and immutability
  • You need to iterate over all possible values
  • You want to prevent accidental value changes
  • You need identity comparison (is operator)
  • Better for: status codes, colors, directions, days of week, etc.

✅ USE REGULAR CLASS WHEN:
  • Simple namespace for related constants
  • Values might need to change at runtime
  • Performance is critical (Enums have slight overhead)
  • You need simple integer values for external APIs/JSON
  • Legacy code compatibility
  
💡 RULE OF THUMB:
   If it's a "type" with limited options → Use Enum
   If it's just grouped constants → Regular class might suffice
""")











# ============================================================================
# REAL WORLD EXAMPLES
# ============================================================================
print("=" * 70)
print("REAL WORLD EXAMPLES")
print("=" * 70)

# Example 1: Traffic Light System
print("\n📍 Example 1: Traffic Light System (Use ENUM)")
print("-" * 70)

class TrafficLight(Enum):
    RED = "stop"
    YELLOW = "caution"
    GREEN = "go"
    
    def next_light(self):
        if self == TrafficLight.RED:
            return TrafficLight.GREEN
        elif self == TrafficLight.GREEN:
            return TrafficLight.YELLOW
        else:
            return TrafficLight.RED

current = TrafficLight.RED
print(f"Current: {current.name} ({current.value})")
print(f"Next: {current.next_light().name}")

# Example 2: Configuration Constants
print("\n📍 Example 2: Configuration Constants (Use CLASS)")
print("-" * 70)

class Config:
    MAX_CONNECTIONS = 100
    TIMEOUT = 30
    RETRY_LIMIT = 3
    API_URL = "https://api.example.com"

print(f"Config.MAX_CONNECTIONS: {Config.MAX_CONNECTIONS}")
print(f"Config.TIMEOUT: {Config.TIMEOUT}")

# Example 3: User Roles with Permissions
print("\n📍 Example 3: User Roles (Use ENUM with methods)")
print("-" * 70)

class UserRole(Enum):
    GUEST = 1
    USER = 2
    ADMIN = 3
    SUPERADMIN = 4
    
    def can_delete(self):
        return self.value >= UserRole.ADMIN.value
    
    def can_edit(self):
        return self.value >= UserRole.USER.value

role = UserRole.USER
print(f"Role: {role.name}")
print(f"Can edit: {role.can_edit()}")
print(f"Can delete: {role.can_delete()}")

print("\n" + "=" * 70)
print("✓ Revision complete! Save this script for future reference.")
print("=" * 70)