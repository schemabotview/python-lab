# Partition Keys

A warehouse groups rows under composite keys — `(table, year, month)`. Those
keys have to be **immutable**, and that is what a tuple is for.

## 1 · `parse_partition()`

`parse_partition(path)` pulls the values out of a Hive-style path.

```python
parse_partition("year=2026/month=01/day=04")   # ('2026', '01', '04')
```

They stay strings — `01` is a partition name, not a number.

## 2 · `partition_key()`

`partition_key(record)` builds the key a row is grouped under, from its
`table`, `year` and `month`.

```python
partition_key({"table": "orders", "year": 2026, "month": 1})
# ('orders', 2026, 1)
```

## 3 · `bounds()`

`bounds(values)` returns **three values at once** — lowest, highest, count.
Empty input gives `(0, 0, 0)`.

```python
lowest, highest, count = bounds([15, 22, 8, 30])   # 8, 30, 4
```

## 4 · `one_item()`

`one_item(value)` wraps a single value in a tuple of length **one**.

```python
one_item("orders")   # ('orders',)
```

## 5 · `rekey()`

`rekey(pair)` flips a `(table, year)` pair the other way round.

```python
rekey(("orders", 2026))   # (2026, 'orders')
```

## 6 · `group_counts()`

`group_counts(rows)` counts how many rows arrived per `(table, date)`.

```python
group_counts([("orders", "2026-01-04"), ("events", "2026-01-04"), ("orders", "2026-01-04")])
# {('orders', '2026-01-04'): 2, ('events', '2026-01-04'): 1}
```

## Notes

- **A tuple is what makes `group_counts` possible at all.** Dictionary keys must
  be hashable, and a tuple is because it can never change. Swap in a list and
  Python raises `TypeError: unhashable type: 'list'` — a test proves it. That is
  the whole reason composite keys are tuples everywhere in data work.
- **`("orders")` is not a tuple.** Those parentheses are just grouping, and it's
  the plain string. The comma is what builds a tuple: `("orders",)`. This bites
  everyone once.
- **`return a, b, c` already builds a tuple.** The parentheses are optional, and
  the caller takes it apart with `lowest, highest, count = bounds(...)`. That is
  all "returning multiple values" ever was.
- `rekey` wants unpacking, not indexing: `table, year = pair` says what the two
  halves mean, where `pair[0]` and `pair[1]` don't.
- `.partition("=")` splits a string once, at the first separator, and always
  gives back three pieces — before, the separator, after. It never raises, which
  makes it safer than `.split("=")[1]` on input you don't control.
