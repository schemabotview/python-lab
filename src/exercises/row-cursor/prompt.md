# The Row Cursor

A `for` loop is not magic. It calls `iter()` once, then `next()` until
`StopIteration`. Here you write both ends of that.

## `Cursor`

`__init__` is done. Add `__iter__` and `__next__` so a `Cursor` can be looped
over, using the `position` it already tracks.

```python
list(Cursor(["r1", "r2", "r3"]))   # ['r1', 'r2', 'r3']
```

## `manual_walk(iterable)`

Drive the protocol yourself — no `for` loop — and collect everything.

```python
manual_walk("hi")            # ['h', 'i']
manual_walk({"a": 1})        # ['a']
```

## `first_n(iterable, count)`

Pull at most `count` values, **leaving the rest unread**.

## `is_iterable(value)`

Whether `iter()` will accept the value at all.

## Notes

- **`__iter__` returns the thing that has `__next__`.** Returning `self` is the
  usual answer for a cursor, because the cursor *is* its own position.
- **`__next__` raises `StopIteration` when it's done.** That exception isn't an
  error — it's the protocol's way of saying "finished", and every `for` loop in
  Python is quietly catching it for you.
- **A cursor is one-shot.** Because `__iter__` returns `self` and `position`
  never resets, walking it a second time yields nothing at all. A test proves
  it. That's not a bug — it's the same behaviour a file object or a database
  cursor has, and it's why `list(...)` exists when you need a second pass.
- **`first_n` must not consume more than it takes.** A test reads one value,
  then walks the rest and expects them intact. This is the whole point of
  pulling on demand: values you never ask for are never produced.
- `is_iterable` is a `try`/`except TypeError` around `iter(value)` — the EAFP
  shape again. There is no reliable way to ask in advance.
