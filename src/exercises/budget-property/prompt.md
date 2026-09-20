# Spend Budget

A budget that enforces its own rules — while callers keep writing plain
`budget.limit`, with no parentheses and no `get_`/`set_` methods.

`__init__` is written for you: the real values live in `_limit` and `_spent`.

## The properties

| Property | Behaviour |
| --- | --- |
| `spent` | read-only |
| `limit` | readable, and **writable through a validating setter** |
| `remaining` | `limit - spent`, computed on every read |
| `exhausted` | `True` once `spent` reaches `limit` |

## The setter

`budget.limit = value` raises `ValueError` when the new limit is:

- negative → `"limit cannot be negative"`
- below what is already spent → `"limit cannot be below what is already spent"`

## `spend(amount)`

Returns `"approved"` and records the spend, or `"denied"` and changes nothing
when the amount is more than `remaining`.

```python
b = Budget(100)
b.spend(30)    # "approved"
b.remaining    # 70
b.spend(80)    # "denied"
b.spent        # still 30
```

## Notes

- **A `@property` is a method that reads like an attribute.** `budget.limit`
  runs your getter, but the caller can't tell — no parentheses. That's the whole
  point: you keep control without forcing `get_limit()` on everyone.
- **The setter is where validation belongs**, because it runs *before* the value
  is stored. Check in a plain method and a bad value is already inside the
  object by the time anyone notices.
- **A property with no setter is read-only**, and assigning to it raises
  `AttributeError`. That is how `spent` stays under the control of `spend()`.
- **`remaining` is computed, not stored.** A stored copy would go stale the
  moment `spent` moved, and keeping two facts in sync is a bug waiting to
  happen. Computing it on read means it can never disagree with itself.
- **Python has no real `private`.** The leading `_` is a convention that says
  "internal, don't touch" — and a test reads `_limit` directly to prove nothing
  is actually locked. The naming signals intent; Python trusts you with the
  rest. (A double `__` goes further and gets name-mangled, which is about
  avoiding collisions in subclasses, not security.)
