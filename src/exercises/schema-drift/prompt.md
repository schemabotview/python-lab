# Schema Drift

The upstream source changed its columns again. Comparing two sets of names is
exactly what a `set` is for.

**Every function here returns a sorted list, not a set.** A set has no order, so
a set is not something you can assert on — sorting is how you make the answer
reproducible.

## 1 · `drift()`

`drift(expected, actual)` compares what the target wants against what arrived.

```python
drift(["id", "name", "email", "phone"], ["id", "name", "nickname"])
```

```text
Missing: ['email', 'phone']
Unexpected: ['nickname']
Shared: ['id', 'name']
```

## 2 · `all_columns()`

`all_columns(*schemas)` — every column named by any schema.

```python
all_columns(["id", "name"], ["id", "email"])   # ['email', 'id', 'name']
```

## 3 · `is_compatible()`

`is_compatible(expected, actual)` — is everything the target needs present?
Extra columns are fine; missing ones are not.

```python
is_compatible(["id"], ["id", "extra"])   # True
is_compatible(["id", "x"], ["id"])       # False
```

## 4 · `changed_columns()`

`changed_columns(before, after)` — the columns on one side only, whether added
or dropped.

```python
changed_columns(["a", "b"], ["b", "c"])   # ['a', 'c']
```

## 5 · `unique_tables()`

`unique_tables(rows)` — the distinct table names mentioned.

## 6 · `freeze()`

`freeze(columns)` returns an **immutable** column set, so it can be a dict key.

## Notes

- The four set operators are the whole exercise: `-` difference (in the first,
  not the second), `&` intersection (in both), `|` union (in either), and `^`
  symmetric difference (in exactly one). `drift` needs `-` twice — **in both
  directions**, because "missing" and "unexpected" are not the same question.
- `<=` on sets asks **subset**, not size. `{"id"} <= {"id", "extra"}` is `True`
  because every member of the left is in the right.
- **A set drops duplicates and loses order.** Both are the point: `unique_tables`
  wants the first, and the sort puts the order back deliberately rather than
  leaving you to depend on an arrangement Python never promised.
- **`x in some_set` is O(1); `x in some_list` is O(n).** For a membership check
  in a loop, that is the difference between a run that finishes and one that
  doesn't. It is the reason to reach for a set even when you don't need the
  operators.
- **A `set` is mutable, so it can't be a dict key** — the same reason a list
  can't. `frozenset` is the immutable version, and it can. A test proves the
  difference.
