import json
import os
from datetime import datetime
import sys

"""
Common kwargs for json.dump() and json.dumps():
    obj: The Python object to serialize.
    fp: (dump only) The file-like object to write to.
    skipkeys: If True, skip keys that aren't basic types (str, int, etc) instead of raising TypeError.
    ensure_ascii: If True (default), output is ASCII (escapes unicode). Set False for proper characters.
    check_circular: Check for circular references (default True).
    allow_nan: Allow NaN, Infinity, -Infinity (default True).
    indent: If non-negative integer, pretty prints with that indent level.
    separators: Tuple (item_separator, key_separator). Used for compact encoding.
    default: A function to handle custom types (like datetime).
    sort_keys: If True, output of dictionaries will be sorted by key.
"""


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


##############################################################################################
##############################################################################################


# SECTION 1: Prepare Data
def get_sample_data(to_print=False):
    """Returns a dictionary with various data types to demonstrate mapping."""

    data = {
        "string": "Hello World",
        "integer": 42,
        "float": 3.14159,
        "boolean": True,  # becomes true
        "none": None,  # becomes null
        "list": [1, 2, "three"],
        "nested_dict": {"key": "value", "active": False},
    }

    if to_print:
        separator("1. PREPARE SAMPLE DATA")
        print(data)

    return data


##############################################################################################
##############################################################################################


# SECTION 2: Serialization (dumps) - Python to JSON String
def serialization_to_string_using_json_dumps():
    separator("2. SERIALIZATION (json.dumps)")
    data = get_sample_data()

    # json.dumps() = dump json to string
    json_string = json.dumps(data)

    print(f"Original Type: {type(data)}")
    print(f"Result Type:   {type(json_string)}")
    print(f"Raw String:    {json_string}\n")

    print(f""" Notice: True -> true, None -> null, ' -> " """)


##############################################################################################
##############################################################################################


# SECTION 3: Pretty Printing (indent and sort_keys)
def pretty_printing():
    separator("3. PRETTY PRINTING")
    data = get_sample_data()

    # indent adds spaces, sort_keys guarantees order (useful for diffs/version control)
    pretty_json = json.dumps(data, indent=4, sort_keys=True)

    print(pretty_json)
    print("\n")


##############################################################################################
##############################################################################################


# SECTION 4: Compact Encoding (Minification)
def compact_encoding():
    separator("4. COMPACT ENCODING (MINIFICATION)")
    data = get_sample_data()

    # By default, separators are (', ', ': '). We remove the whitespace.
    standard_json = json.dumps(data)
    compact_json = json.dumps(data, separators=(",", ":"))

    print(
        f"Standard (len={len(standard_json)}, size={sys.getsizeof(standard_json)} Bytes): {standard_json}"
    )
    print(
        f"Compact (len={len(compact_json)}, size={sys.getsizeof(compact_json)} Bytes): {compact_json}"
    )


##############################################################################################
##############################################################################################


# SECTION 5: Deserialization (loads) - JSON String to Python
def deserialization_from_string():
    separator("5. DESERIALIZATION (json.loads)")

    # A standard JSON string
    json_input = '{"id": 101, "name": "Alice", "is_admin": true, "skills": null}'

    # json.loads() = load json from string
    python_obj = json.loads(json_input)

    print(f"Input String ==> {json_input}")
    print(f"Result Type ==>  {type(python_obj)}")
    print(f"Result ==>  {python_obj}")
    print("")

    compact_json_input = json.dumps(get_sample_data(), separators=(",", ":"))
    python_obj_from_compact = json.loads(compact_json_input)

    print(f"Input String ==> {compact_json_input}")
    print(f"Result Type ==>  {type(python_obj_from_compact)}")
    print(f"Result ==>  {python_obj_from_compact}")


##############################################################################################
##############################################################################################


# SECTION 6: File Operations (dump and load)
def file_operations():
    # separator("6. FILE I/O (json.dump / json.load)")
    filename = "tutorial_temp.json"
    data = get_sample_data()

    # --- WRITING (json.dump) ---
    separator(f"6.1 Writing to {filename}... using json.dump")
    with open(filename, "w", encoding="utf-8") as f:
        # Note: 'dump' takes the object AND the file pointer. No 's' at the end.
        json.dump(data, f, indent=2)
        print(f"Data written successfully to {filename} ==> {data}")

    # --- READING (json.load) ---
    separator(f"6.2 Reading from {filename}... using json.load")
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        # print(f"Data read successfully. Nested value: {loaded_data['nested_dict']['key']}")
        print(f"Data read successfully. loaded_data ==> {loaded_data}")

        # Cleanup
        os.remove(filename)
        print("File deleted cleanup.")
    print("\n")


##############################################################################################
##############################################################################################


# SECTION 7: Handling Custom Objects (datetime/Classes)
def handling_custom_objects():
    separator("7. HANDLING CUSTOM OBJECTS BY WRITING CUSTOM ENCODER")

    class User:
        def __init__(self, name, id):
            self.name = name
            self.id = id

    # Create data with types JSON doesn't understand natively
    data = {"timestamp": datetime.now(), "user_obj": User("Bob", 55)}

    # Helper function to tell json how to convert unknown types
    def custom_encoder(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert date to string
        if isinstance(obj, User):
            return obj.__dict__  # Convert object to dict
        # Raise error for anything else
        raise TypeError(f"Type {type(obj)} is not serializable")

    try:
        # This works because we pass the 'default' parameter
        json_output = json.dumps(data, default=custom_encoder, indent=2)
        print(json_output)
    except TypeError as e:
        print(f"Serialization failed: {e}")
    print("\n")


##############################################################################################
##############################################################################################


# SECTION 8: Error Handling (Malformed JSON)
def error_handling():
    separator("8. ERROR HANDLING (JSONDecodeError)")

    # A string with a syntax error (trailing comma, single quotes)
    # JSON requires double quotes "", not single ''
    bad_json = "{'name': 'Alice',}"

    try:
        json.loads(bad_json)
    except json.JSONDecodeError as e:
        print("Error caught: JSONDecodeError")
        print(f"Message: {e.msg}")
        print(f"Line: {e.lineno}, Column: {e.colno}")
    print("\n")


##############################################################################################
##############################################################################################


# SECTION 9: Unicode and ASCII
def unicode_handling():
    separator("9. UNICODE AND ASCII")

    data = {"currency": "€", "emoji": "🐍"}

    # Default: ensure_ascii=True (Safe, but ugly for non-English)
    ascii_safe = json.dumps(data)
    print(f"Default(ensure_ascii=True): {ascii_safe}")

    # ensure_ascii=False (Readable, preserves characters)
    utf8_clean = json.dumps(data, ensure_ascii=False)
    print(f"ensure_ascii=False: {utf8_clean}\n")


if __name__ == "__main__":
    get_sample_data(to_print=True)
    serialization_to_string_using_json_dumps()
    pretty_printing()
    compact_encoding()
    deserialization_from_string()
    file_operations()
    handling_custom_objects()
    error_handling()
    unicode_handling()

    separator("Tutorial complete!")
