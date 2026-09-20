# Row Count Ledger

How many rows each table loaded, kept as `table → count`.

## 1 · `lookup()`

`lookup(counts, table)` — rows for one table. A table that never ran is `0`,
**not** an error.

```python
lookup({"orders": 1500}, "orders")   # 1500
lookup({"orders": 1500}, "events")   # 0
```

## 2 · `merge_runs()`

`merge_runs(first, second)` merges a later run over an earlier one. Where both
ran the same table, the later count wins.

```python
merge_runs({"orders": 1500, "events": 300}, {"events": 350, "users": 90})
# {'orders': 1500, 'events': 350, 'users': 90}
```

## 3 · `add_row()`

`add_row(index, table, row_id)` files a row id under its table, starting the
list when it's the first one.

```python
add_row({}, "events", "e1")               # {'events': ['e1']}
add_row({"orders": ["r1"]}, "orders", "r2")   # {'orders': ['r1', 'r2']}
```

## 4 · `ledger_report()`

`ledger_report(counts)` — one line per table **in name order**, then the total.

```python
ledger_report({"orders": 1500, "events": 300})
```

```text
events: 300
orders: 1500
TOTAL: 1800
```

## 5 · `drop_table()`

`drop_table(counts, table)` removes a table. Dropping one that isn't there is
not an error.

## 6 · `column_order()`

`column_order(pairs)` builds a schema from `(name, type)` pairs and reports the
column names **in the order they were added**.

```python
column_order([("id", "int"), ("amount", "float"), ("created", "date")])
# ['id', 'amount', 'created']
```

## Notes

- **`counts["events"]` raises `KeyError` when the table never ran.** That is the
  single most common dict bug, and `.get(key, default)` is the fix: it asks the
  same question without the explosion. A test proves the bracket form raises.
- **`.setdefault(key, [])` is the grouping idiom.** It returns the existing list
  if there is one and installs a new one if there isn't — so
  `d.setdefault(t, []).append(x)` files an item under a key that may not exist
  yet, in one line, with no `if`.
- **`.update()` mutates the dict it's called on.** `merge_runs` must copy first,
  or it quietly rewrites the caller's earlier run. `add_row` has the same
  problem one level deeper: copying the dict still leaves both dicts sharing the
  same *lists*, so the lists need copying too.
- **`.pop(key, None)` is the safe delete.** `del d[key]` raises on a key that
  isn't there; `.pop` with a default doesn't.
- `.items()` gives key and value together, `.values()` gives just the values,
  and `sorted(counts)` sorts the **keys** — iterating a dict gives you its keys
  unless you ask for otherwise.
- **Dicts keep insertion order**, guaranteed since Python 3.7. That is why
  `column_order` works at all, and why a schema built from a dict stays in the
  order you declared it.
