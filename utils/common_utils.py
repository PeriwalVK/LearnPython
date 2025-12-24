def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#'*hash_len} {msg} {'#'*hash_len}")
    print("=" * l)