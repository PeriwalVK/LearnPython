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
