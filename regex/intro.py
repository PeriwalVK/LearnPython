"""

## 🧩 1. What is `re` in Python?

`re` is Python's **regular expression** module — it helps you **search, match, or extract patterns** from text.

👉 You import it using:

```python
import re
```

---

## ⚙️ 2. The main functions you'll use

| Function       | What it does                                     | Example                                     |
| -------------- | ------------------------------------------------ | ------------------------------------------- |
| `re.match()`   | Match from **start** of string                   | `re.match('a', 'abc')` ✅                    |
| `re.search()`  | Match **anywhere** in string                     | `re.search('a', 'cba')` ✅                   |
| `re.findall()` | Return **all matching substrings** in a **list** | `re.findall('a', 'banana') → ['a','a','a']` |
| `re.sub()`     | Replace matches                                  | `re.sub('\d', 'X', 'a1b2') → 'aXbX'`        |

---

## 🧠 3. Basic Building Blocks (Meta-characters)

Here’s what the `r'\b\w+\b'` pattern is made of — but first, the **vocabulary** 👇

| Symbol  | Meaning                               | Example                                       |
| ------- | ------------------------------------- | --------------------------------------------- |
| `.`     | Any character except newline          | `a.b` → matches `acb`, `a3b`                  |
| `\d`    | Any digit `[0-9]`                     | `\d+` → `123`                                 |
| `\w`    | Word character `[a-zA-Z0-9_]`         | `\w+` → `hello123`                            |
|         | Matches letter, digit, underscore (_) |                                               |
| `\s`    | Whitespace                            | `'a\sb'` → `'a b'`                            |
| `^`     | Start of string                       | `^Hi` matches only if text **starts** with Hi |
| `$`     | End of string                         | `bye$` matches only if text **ends** with bye |
| `\b`    | **Word boundary** (start/end of word) | `\bcat\b` won't match "concatenate"           |
| `+`     | 1 or more                             | `\d+` → `123`                                 |
| `*`     | 0 or more                             | `a*` → `''`, `'a'`, `'aaaa'`                  |
| `?`     | 0 or 1                                | `colou?r` → `'color'` or `'colour'`           |
| `[abc]` | Any one of `a` or `b` or `c`          | `'a'`, `'b'`, `'c'`                           |
| `(abc)` | Group (capture)                       | for extraction                                |

---

## 🧩 4. The **r'' (raw string)** prefix

When you write regex in Python, you often use **raw strings** like `r'\bword\b'`.

Because otherwise, Python treats `\b` as a **backspace character**, not a regex boundary.

✅ `r'\bword\b'` → real regex
🚫 `'\bword\b'` → Python thinks `\b` means backspace

So always use the **`r''`** prefix for regex patterns.

---

## 🧪 5. Now decode your pattern:

```python
re.findall(r'\b\w+\b', text.lower())
```

Let's break it step by step 👇

1. **`text.lower()`** → Converts the whole text to lowercase.
   Example: `"Hello World"` → `"hello world"`

2. **`r'\b\w+\b'`**

   * `\b` → start of a word
   * `\w+` → one or more word characters (letters/digits/underscore)
   * `\b` → end of a word

   So this pattern means → **match complete words** only.

3. **`re.findall(...)`** → returns all matches as a list.

Example:

```python
import re

text = "Hello, world! 123 times."
words = re.findall(r'\b\w+\b', text.lower())
print(words)
```

Output:

```
['hello', 'world', '123', 'times']
```

So basically — this extracts all *words* from the string, ignoring punctuation and capitalization.

---

## 💡 6. More Quick Examples

| Example                        | Code                                  | Output                          |
| ------------------------------ | ------------------------------------- | ------------------------------- |
| Find all digits                | `re.findall(r'\d+', 'a12b3')`         | `['12', '3']`                   |
| Split on punctuation           | `re.split(r'\W+', 'Hi! I, am fine.')` | `['Hi', 'I', 'am', 'fine', '']` |
| Replace digits                 | `re.sub(r'\d', 'X', 'Room 123')`      | `'Room XXX'`                    |
| Check if text starts with word | `re.match(r'^hello', 'hello world')`  | ✅ Match object                  |

---

## 🚀 7. Mini practice

Try these to get a feel:

```python
re.findall(r'\d+', "My phone number is 9876543210")
re.findall(r'\b[a-z]{3}\b', "The cat sat on the mat")
re.findall(r'[A-Z][a-z]+', "Alice and Bob met Charlie")
re.sub(r'\s+', ' ', "This   has   many   spaces")
```

---

Would you like me to give you a **10-minute hands-on exercise set** to master regex patterns (starting easy to interview-level)?
"""

"""

Perfect 👍 — that's a great mini-table of some of the most important regex building blocks.
Let's quickly **explain these five** clearly with visuals and tiny runnable examples so they stick in memory.

---

### 🔹 `\w`  →  “word character”

Matches **letters**, **digits**, and the **underscore** (`_`).
It's basically shorthand for `[A-Za-z0-9_]`.

```python
import re
re.findall(r'\w+', "Hi_123!")   # ['Hi_123']
```

✅ `Hi_123` is one *word unit* made of valid characters.
❌ `!` is skipped because it's not part of `\w`.

---

### 🔹 `^`  →  “start of string”

Anchors the pattern to the **beginning**.

```python
re.findall(r'^Hi', "Hi there")     # ['Hi']
re.findall(r'^Hi', "Well Hi!")     # []
```

✅ Matches only if `Hi` appears **at the start**.

---

### 🔹 `$`  →  “end of string”

Anchors the pattern to the **end**.

```python
re.findall(r'end$', "the end")     # ['end']
re.findall(r'end$', "endless")     # []
```

✅ Matches only if `end` is **the last thing** in the text.

---

### 🔹 `\b`  →  “word boundary”

Marks the **edges of a word** — i.e., between `\w` and a non-`\w` character.

```python
re.findall(r'\bcat\b', "the cat sat")         # ['cat']
re.findall(r'\bcat\b', "concatenate catnip")  # []
```

✅ Finds `cat` as a *whole word*, not as part of another.

> Think of `\b` as an invisible fence between words and punctuation/spaces.

---

### 🔹 `(abc)`  →  **capturing group**

Groups part of a pattern and lets you **extract** it separately.

```python
re.findall(r'(\d+)-(apple|banana)', "12-apple 99-banana 77-pear")
# [('12', 'apple'), ('99', 'banana')]
```

✅ Parentheses capture specific subparts that you can later reference.

> Note: use `(?:abc)` for a **non-capturing group** (groups without extraction).

---

Would you like me to add the next layer — the **quantifiers and ranges** (`+`, `*`, `{m,n}`, `?`) with small visual rules and examples?


"""


"""
Excellent question 🔥 — you’ve spotted the subtle magic of **`\b` (word boundary)** correctly.

Let’s break this down carefully — because understanding **why `world!` still matches `world`** is a key step to mastering regex.

---

### 🧩 Step 1: Your text

```python
text = "Hello, world! 123 times."
```

When lowercased → `"hello, world! 123 times."`

---

### 🧩 Step 2: Your regex pattern

```python
r'\b\w+\b'
```

Breakdown:

* `\b` → a *word boundary* (transition between a **word character** `\w` and a **non-word character** `\W`)
* `\w+` → one or more word characters `[a-zA-Z0-9_]`
* `\b` → another word boundary

So you’re matching *whole words* separated by spaces, punctuation, etc.

---

### 🧩 Step 3: What happens at `"world!"`

Let's see the characters:

```
... w  o  r  l  d  !  ...
     ↑          ↑  ↑
```

Regex engine checks boundaries like this:

* `\w` characters = `w, o, r, l, d`
* `!` = **non-word** character

So between `'d'` (word char) and `'!'` (non-word char), a **word boundary `\b` exists**.

✅ Hence `\b\w+\b` sees:

```
[boundary]world[boundary before !]
```

That’s why **`world`** gets captured — punctuation like `!`, `.`, `,` or `?` are **non-word characters**, which mark the end boundary.

---

### 🧠 In short:

`\b` doesn’t *represent* `!` —
it represents the **boundary** *between* `d` (word char) and `!` (non-word char).

Think of it like:

```
word boundary exists between:
[ ... word_char | non_word_char ... ]
```

---

### ✅ Demo proof:

```python
import re

text = "world!"
for m in re.finditer(r'\b', text):
    print(f"Boundary at index {m.start()}")
```

Output:

```
Boundary at index 0   ← before 'w'
Boundary at index 5   ← between 'd' and '!'
Boundary at index 6   ← after '!'
```

You can literally **see** the invisible boundaries!

---

### ⚡Summary

| Between                     | Is there a `\b` boundary? |
| --------------------------- | ------------------------- |
| letter and space            | ✅ yes                     |
| letter and punctuation      | ✅ yes                     |
| letter and letter           | ❌ no                      |
| punctuation and punctuation | ❌ no                      |

---

Would you like me to give you a quick **visual diagram** showing exactly where `\b` boundaries lie in a few tricky examples like `"it's cool!"`, `"co-op"`, `"123abc"` etc.? It’ll make this 100% intuitive.

"""
