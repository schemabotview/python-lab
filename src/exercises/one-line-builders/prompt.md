# One-Line Builders

A run produces records like these:

```python
[
    {"table": "orders", "rows": 1500, "status": "ok"},
    {"table": "events", "rows": 300, "status": "failed"},
    {"table": "users", "rows": 90, "status": "ok"},
]
```

Every function below is **one comprehension**. If you're writing an empty list
and a `.append()`, you're writing the long version of what this exercise is
about.

## 1 · `table_names()` → `['orders', 'events', 'users']`

A plain list comprehension, in arrival order.

## 2 · `loaded_only()` → `['orders', 'users']`

The same thing with a **condition** — only the clean loads.

## 3 · `rows_by_table()` → `{'orders': 1500, 'events': 300, 'users': 90}`

A **dict** comprehension: `{key: value for ...}`.

## 4 · `distinct_statuses()` → `['failed', 'ok']`

A **set** comprehension for the uniqueness, sorted for a stable answer.

## 5 · `flatten()`

Two `for` clauses in one comprehension.

```python
flatten([["a", "b"], ["c"]])   # ['a', 'b', 'c']
```

## 6 · `total_rows()` → `1890`

`sum()` fed by a **generator expression** — no list built in between.

## 7 · `lazy_names()`

Returns a **generator**, not a list. Nothing is produced until someone walks it.

```python
list(lazy_names(records))   # ['orders', 'events', 'users']
```

## Notes

- The shape is always the same: **output expression first, then the loop, then
  the optional condition.** `[x["table"] for x in records if x["status"] == "ok"]`
  reads out of order the first few times and then never again.
- **Brackets pick the type.** `[...]` builds a list, `{k: v for ...}` a dict,
  `{...}` a set — and `(...)` builds neither, it builds a **generator**.
- **In `flatten`, the `for` clauses read left to right**, exactly the order
  you'd write the nested loops in. Getting them backwards is the usual mistake,
  and it raises rather than quietly misbehaving.
- **A generator expression holds no results.** `sum(x["rows"] for x in records)`
  never builds the intermediate list, which is what lets the same line work on a
  batch too big for memory. The cost is that a generator is **single-use**: walk
  it twice and the second walk gets nothing. A test proves that.
- **Comprehensions stop being a win when they stop being readable.** Two `for`
  clauses and a condition is roughly the ceiling; past that, the plain loop is
  the better code. This is a tool for the simple cases, not a challenge to fit
  everything into one line.
