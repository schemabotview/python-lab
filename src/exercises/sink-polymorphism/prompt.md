# Sink Fan-Out

The same rows go to several destinations. The code doing the sending never asks
what kind each destination is.

## Three sinks

Each has a `write(rows)` method and **nothing else in common** — no shared base
class.

```python
ConsoleSink().write(5)        # "console: 5"
TableSink("orders").write(5)  # "orders: 5"
NullSink().write(5)           # "discarded"
```

## `fan_out(sinks, rows)`

Sends the same rows to every sink and collects what each returned.

```python
fan_out([ConsoleSink(), TableSink("orders"), NullSink()], 5)
# ['console: 5', 'orders: 5', 'discarded']
```

## `Batch`

Holds `row_ids` and answers `len()`.

```python
len(Batch(["r1", "r2", "r3"]))   # 3
```

## `total_size(items)`

Totals the length of anything that answers `len()`.

```python
total_size(["hi", [1, 2], Batch(["a"])])   # 5
```

## Notes

- **`fan_out` is one line and contains no type check.** It calls `.write()` and
  each object's own version runs. The moment you write `if isinstance(sink,
  ...)` you've thrown polymorphism away and gone back to a switch statement.
- **Duck typing means no base class is required.** A test defines a
  `MetricsSink` that inherits from nothing at all, and `fan_out` handles it
  without being told — because it has the right method. Python checks at call
  time, not by declared type.
- **`len()` is polymorphism you already use.** `len("hi")` and `len([1, 2])` are
  the same call reaching two different `__len__` implementations. Defining
  `__len__` on `Batch` puts your class into that same protocol, and
  `total_size` then treats it identically to the built-ins.
- `__len__` must return a non-negative integer — Python enforces that, so you
  can't return a string from it.
