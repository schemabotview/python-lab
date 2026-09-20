# Transactions & Stages

A `with` block guarantees cleanup — on the way out, however you leave.

Each class here appends to a `log` list so the sequence is visible.

## `Transaction`

- `__enter__` logs `"BEGIN"` and returns the transaction itself.
- `write(row)` logs `"WRITE <row>"`.
- `__exit__` logs `"COMMIT"` on a clean exit, or `"ROLLBACK <ExceptionName>"`
  when the block raised — and **lets the exception carry on**.

```python
log = []
with Transaction(log) as txn:
    txn.write("r1")
# ['BEGIN', 'WRITE r1', 'COMMIT']
```

## `Suppressing(Transaction)`

The same cleanup, but it **swallows** the exception instead of re-raising.

## `staged(log, name)`

The `@contextmanager` version. Logs `"START <name>"` on the way in, yields the
name **uppercased**, and logs `"END <name>"` on the way out — **even when the
block raises**.

```python
log = []
with staged(log, "extract") as name:
    log.append(f"working on {name}")
# ['START extract', 'working on EXTRACT', 'END extract']
```

## Notes

- **`__exit__` receives the exception, or three `None`s.** Checking
  `exc_type is None` is how you tell a clean exit from a failed one — that's the
  whole commit-or-rollback decision.
- **The return value of `__exit__` decides whether the exception continues.**
  Falsy (including `None`, which is what you get by forgetting to return) lets
  it propagate; `True` swallows it. Swallowing by accident hides real failures,
  so returning `False` explicitly is the honest default.
- **`__exit__` runs on a `return` from inside the block too.** A test returns
  early from a function and checks `COMMIT` was still logged — you cannot skip
  cleanup by leaving early, which is the guarantee the whole construct exists
  for.
- **In `@contextmanager`, the `yield` splits the function**: before it is enter,
  after it is exit, and the yielded value is what `as` binds. The `try`/
  `finally` around the yield is **not optional** — without it, an exception in
  the block skips everything after the yield and the cleanup never runs.
- Blocks unwind inside out, which is why nesting two of these produces
  `START outer, START inner, END inner, END outer`.
