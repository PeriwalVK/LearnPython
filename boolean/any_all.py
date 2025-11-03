def separator(msg: str, l: int = 120):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print("=" * l)
    print(f"{'#'*hash_len} {msg} {'#'*hash_len}")
    print("=" * l)


def f1(out: bool) -> bool:
    print(f"f1 called with {out}")
    return out


def f2(out: bool) -> bool:
    print(f"f2 called with {out}")
    return out


def f3(out: bool) -> bool:
    print(f"f3 called with {out}")
    return out


def f4(out: bool) -> bool:
    print(f"f4 called with {out}")
    return out


separator("All Should Run")
print(any([f1(True), f2(True), f3(True), f4(True)]))
print(any(f for f in [f1(True), f2(True), f3(True), f4(True)]))


separator("But these will Short circuit at f1")
print(any(f(True) for f in [f1, f2, f3, f4]))  # <class 'generator'>
print(f1(True) or f2(True) or f3(True) or f4(True))


separator("All Should Run")
print(all([f1(False), f2(False), f3(True), f4(False)]))


separator("But these will Short circuit at f1")
print(all(f(False) for f in [f1, f2, f3, f4]))
print(f1(False) and f2(False) and f3(False) and f4(False))
