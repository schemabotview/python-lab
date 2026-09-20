# A Rows Value Type

`Rows` wraps a count. Define the hooks and Python's own syntax starts working
on it.

| Hook | Makes this work | Result |
| --- | --- | --- |
| `__repr__` | `repr(Rows(1500))` | `"Rows(1500)"` |
| `__str__` | `str(Rows(1500))` | `"1500 rows"` |
| `__eq__` | `Rows(5) == Rows(5)` | `True` |
| `__lt__` | `sorted([...])` | ordered |
| `__add__` | `Rows(5) + Rows(9)` | `Rows(14)` |
| `__len__` | `len(Rows(1500))` | `1500` |
| `__hash__` | `{Rows(5)}` | works |

`__init__` is written for you.

## Notes

- **You get more than you write.** Define `__eq__` and `!=` works. Define
  `__lt__` and `>`, `sorted()` and `max()` all work — because every one of them
  is built on the same hook. That is what "one uniform protocol" buys you.
- **`__repr__` is for you, `__str__` is for the user.** `repr` should look like
  the code that would rebuild the object; `str` should read like English.
  `print()` and f-strings reach for `__str__`, the REPL and containers reach for
  `__repr__`.
- **`__add__` returns a new `Rows`, not a number.** A value type that degrades
  into an `int` the first time you add two together isn't a value type.
- **Defining `__eq__` silently sets `__hash__` to `None`.** Python does this
  because two objects that compare equal *must* hash equal, and it can't guess
  your rule. The consequence is that your class stops working in sets and as a
  dict key, with a `TypeError` that arrives far from the cause. A test builds a
  class without `__hash__` and proves it. Define it from the same value `__eq__`
  compares, and they stay consistent.
- Returning `NotImplemented` from `__eq__` for an unrelated type is the polite
  form — it lets Python fall back to the other object's answer rather than
  claiming a definite `False`.
