"""
defaultdict Tutorial Script
Learn how defaultdict works and why it's useful.
dd = defaultdict(some_callable)
    ex:
        int,
        float,
        str,
        dict,
        lambda: "default msg",
        lambda: defaultdict(float)
"""

from collections import defaultdict


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def announce(msg: str):
    """
    A decorator to announce a message before calling a function.
    """

    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


@announce("1. Basic idea")
def _1_basic_idea():
    print(
        "defaultdict automatically creates a default value when a missing key is accessed.\n"
    )

    # A simple defaultdict that creates integers starting at 0
    counts = defaultdict(int)
    counts["apples"] += 1
    counts["apples"] += 1
    counts["oranges"] += 1

    print("Counts:", counts)
    print(f"dict(counts): {dict(counts)}")
    print("\nNotice: We never created the keys manually.\n")


@announce("2. Comparing dict vs defaultdict")
def _2_comparing_dict_vs_defaultdict():
    regular = {}
    try:
        regular["missing"] += 1  # This will fail
    except KeyError:
        print("Regular dict: KeyError when accessing a missing key")

    auto = defaultdict(int)
    auto["missing"] += 1
    print(
        "defaultdict: automatically initialized to 0, now value is:",
        auto["missing"],
        "\n",
    )


@announce("3. Using different default factories")
def _3_using_different_default_factories():
    # list factory: automatically creates empty lists
    groups = defaultdict(list)
    groups["fruits"].append("apple")
    groups["fruits"].append("banana")
    groups["colors"].append("red")

    print("List groups:", groups, "\n")

    # set factory: automatically creates empty sets
    unique_values = defaultdict(set)
    unique_values["letters"].add("a")
    unique_values["letters"].add("b")
    unique_values["letters"].add("a")  # duplicates ignored because it's a set

    print("Set groups:", unique_values, "\n")


@announce("4. Using a custom default factory")
def _4_using_a_custom_default_factory():
    def default_message():
        return "Key not found, but here's your default!"

    custom = defaultdict(default_message)
    print(custom["hello"])  # Access missing key

    # custom["hello"] = "custom value for key hello"
    # print(custom["hello"])  # now key found

    print("\nCurrent dict:", custom, "\n")


@announce("5. Common real-world use case: Counting words")
def _5_common_real_world_use_case_counting_words():
    text = "the quick brown fox jumps over the lazy dog the fox was quick"

    word_count = defaultdict(int)
    for word in text.split():
        word_count[word] += 1

    print(
        "Word counts:", dict(word_count)
    )  # convert to regular dict for clean printing
    print()


@announce("6. Another use case: Grouping items")
def _6_another_use_case_grouping_items():
    people = [
        ("Alice", "Engineering"),
        ("Bob", "Sales"),
        ("Carlos", "Engineering"),
        ("Dana", "HR"),
        ("Eve", "Engineering"),
    ]

    departments = defaultdict(list)
    for name, dept in people:
        departments[dept].append(name)

    print("Grouped people:", dict(departments))
    print()


@announce("7. Nested defaultdict")
def _7_nested_defaultdict():
    nested = defaultdict(lambda: defaultdict(int))
    nested["a"]["b"] += 1
    print("Nested defaultdict of defaultdict:", nested)

    d = dict()
    dd = defaultdict(lambda: d)  # ❌ wrong — shared dict
    dd["a"]["x"] = 1
    dd["b"]["y"] = 2
    print(dd)

    nested_dd_of_dict = defaultdict(dict)
    nested_dd_of_dict["a"]["b"] = nested_dd_of_dict["a"].get("b", 0) + 1
    print("Nested defaultdict of dict:", nested_dd_of_dict)


@announce("8. Traversing a defaultdict")
def _8_traversing_a_defaultdict():
    """
    Good news: you traverse defaultdict exactly like a normal dictionary.
    """

    dd = defaultdict(dict)
    dd["user1"]["age"] = 30
    dd["user1"]["city"] = "Paris"
    dd["user2"]["age"] = 25

    print("\ntraversing using keys()")
    for user in dd.keys():
        print("User:", user)
        for key in dd[user].keys():
            print("   ", key, "=", dd[user][key])

    print("\ntraversing using values()")
    for user in dd.keys():
        print("User:", user)
        for value in dd[user].values():
            print("   ", value, end=" ")
        print("")

    print("\ntraversing using items()")
    for user, info in dd.items():
        print("User:", user)
        for key, value in info.items():
            print("   ", key, "=", value)


@announce("9. Traversing unknown key")
def _9_traversing_unknown_key():
    dd = defaultdict(dict)
    dd["user1"]["age"] = 30
    dd["user1"]["city"] = "Paris"
    dd["user2"]["age"] = 25

    print("\ntraversing key='user_unknown'")
    print(dd["user_unknown"].items())
    print(dd.items())
    print(
        "\ncalling .items() on an unknown key has caused creation of that key, hence avoid doing that"
    )

    print("\nuse a check instead")
    if "missing" in dd.keys():
        for key, value in dd["missing"].items():
            print("   ", key, "=", value)
    print("this time it didn't cause creation of that key, hence it is fine to do that")
    print(dict(dd))


@announce("End of tutorial!")
def end_of_tutorial():
    print("Play around by adding keys, changing factories, and printing results.")


if __name__ == "__main__":
    _1_basic_idea()
    _2_comparing_dict_vs_defaultdict()
    _3_using_different_default_factories()
    _4_using_a_custom_default_factory()
    _5_common_real_world_use_case_counting_words()
    _6_another_use_case_grouping_items()
    _7_nested_defaultdict()
    _8_traversing_a_defaultdict()
    _9_traversing_unknown_key()
    end_of_tutorial()

