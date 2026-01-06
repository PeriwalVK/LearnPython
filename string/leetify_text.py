masked = {
    "0": "O",
    "1": "l",
    "2": "Z",
    "3": "3",
    "4": "4",
    "5": "S",
    "6": "G",
    "7": "7",
    "8": "B",
    "9": "g",
    
    "a": "4",
    "b": "8",
    "c": "(",
    "d": "d",
    "e": "3",
    "f": "f",
    "g": "6",
    "h": "#",
    "i": "!",
    "j": "j",
    "k": "k",
    "l": "1",
    "m": "^^",
    "n": "n",
    "o": "0",
    "p": "p",
    "q": "q",
    "r": "r",
    "s": "5",
    "t": "7",
    "u": "u",
    "v": "\\/",
    "w": "\\/\\/",
    "x": "><",
    "y": "Y",
    "z": "2",
}


def mask(msg):
    return "".join(map(lambda x: masked.get(x.lower(), x), msg))


print(mask("The quick brown fox jumps over the lazy dog 0123456789"))
