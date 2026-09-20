# Pipeline Utility Module

The helpers file every pipeline repo grows. Nine small functions.

## 1 · `version()` → `"1.0.0"`

No parameters at all.

## 2 · `table_name()`

`table_name(schema, table, env="prod")` fully qualifies a table.

```python
table_name("sales", "orders")          # "prod.sales.orders"
table_name("sales", "orders", "dev")   # "dev.sales.orders"
```

## 3 · `summarize()`

`summarize(*durations)` takes any number of runtimes and returns
`(total, average)`.

```python
summarize(4, 8, 15, 16, 23, 42)   # (108, 18.0)
summarize(10)                     # (10, 10.0)
summarize()                       # (0, 0)
```

## 4 · `build_config()`

`build_config(**overrides)` merges per-run settings onto `DEFAULTS`.

```python
build_config()
# {"env": "prod", "retries": 3, "parallel": 4}

build_config(retries=5, owner="data")
# {"env": "prod", "retries": 5, "parallel": 4, "owner": "data"}
```

## 5 · `apply_all()`

`apply_all(value, *steps)` runs a value through a chain of transforms. The
steps are **functions passed as arguments**.

```python
apply_all("  Orders ", str.strip, str.lower)   # "orders"
apply_all("x")                                 # "x"
```

## 6 · `first_failure()`

`first_failure(results)` takes `(step, status)` pairs and returns the name of
the first failed step — or `None` if they all passed.

## 7 · `report()`

`report(results)` describes the run, guarding on that `None`.

```python
report([("extract", "ok"), ("load", "failed")])   # "first failure: load"
report([("extract", "ok")])                       # "all steps ok"
```

## 8 · `check_row()`

`check_row(row)` returns the first thing wrong, checked **in this order**:

1. no `table` name → `"no table name"`
2. no `checksum` → `"<table>: no checksum"`
3. fewer than 1 row → `"<table>: empty"`
4. otherwise → `"<table>: accepted"`

Four rules, four `return`s, **no `else` anywhere and no nested `if`**. The
accepted line is the last line of the function, at the same indent as the
guards above it.

## 9 · `collect()`

`collect(message, errors=None)` appends to an error list, starting a fresh one
when it isn't handed one.

```python
collect("a")   # ["a"]
collect("b")   # ["b"]   <- not ["a", "b"]
```

## Notes

- **`summarize()` with no arguments must not crash.** `*args` gives you an
  empty tuple, and an empty tuple has nothing to divide by.
- **`build_config` must not damage `DEFAULTS`.** `.update()` mutates whatever
  it's called on, so calling it on `DEFAULTS` itself poisons every later call.
  Copy first.
- **The guard order in `check_row` is the priority order.** A row that is
  nameless *and* has no checksum reports only the first — that's the whole
  point of a guard chain. Don't reorder them to "tidy up".
- **1 row is not fewer than 1 row.** Check your comparison.
- **`def collect(message, errors=[])` is the classic Python trap.** The default
  is built **once**, when the `def` line runs — not per call — so every caller
  who doesn't pass a list shares the same one, and it grows forever. `None`
  plus a check inside is the fix. Test 9 fails loudly if you use `[]`.
- `report` is the guard-clause shape at a call site: get the value, handle the
  `None` and return, then carry on with the normal path unindented.
