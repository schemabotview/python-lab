# Nightly Table Schedule

The list of tables tonight's run will load. It was typed by hand, so it needs
cleaning before anything else can use it.

## 1 · `clean_schedule()`

`clean_schedule(raw)` returns the schedule sorted, with blanks and duplicates
gone. Still a list.

```python
clean_schedule(["orders", "events", "orders", "users", "", "sessions", "events", "customers"])
# ['customers', 'events', 'orders', 'sessions', 'users']
```

## 2 · `slice_report()`

`slice_report(tables)` — four views of the same schedule, each by slicing.

```python
slice_report(["customers", "events", "orders", "sessions", "users"])
```

```text
First three: ['customers', 'events', 'orders']
Last two: ['sessions', 'users']
Every other: ['customers', 'orders', 'users']
Reversed: ['users', 'sessions', 'orders', 'events', 'customers']
```

## 3 · `replace_window()`

`replace_window(tables, start, end, replacement)` swaps a run of tables for a
different run — one merged job replacing two.

```python
replace_window(["a", "b", "c", "d", "e"], 1, 3, ["X"])
# ['a', 'X', 'd', 'e']
```

Note that the replacement doesn't have to be the same length as the window.

## 4 · `promote()`

`promote(tables, name)` moves one table to the front, so it runs first.

```python
promote(["a", "b", "c"], "c")   # ['c', 'a', 'b']
```

## 5 · `batch_summary()`

`batch_summary(batches)` takes `[name, rows]` pairs — a **list of lists**.

```python
batch_summary([["orders", 1500], ["events", 300], ["users", 90]])
```

```text
Tables: 3
Rows: 1890
Largest: orders
```

An empty batch list reports `0`, `0` and `none`.

## 6 · `snapshot()`

`snapshot(tables)` returns a copy that later changes to the original can't
reach.

## Notes

- **`snapshot` is the whole point of this exercise.** `copy = tables` does
  *not* copy anything — it binds a second name to the same list, so appending
  through one name changes what the other sees. `list(tables)` or `tables[:]`
  builds a genuinely new list. This is the single most common way a beginner
  loses data, and a test pins it.
- **Every function here leaves its argument alone.** `.remove()`, `.insert()`
  and slice assignment all mutate in place, so copy first and work on the copy.
  The caller's list belongs to the caller.
- `.remove()` takes one item out **by value**, and raises if it isn't there. It
  also removes only the *first* match, which is why `clean_schedule` needs a
  loop if there could be several blanks.
- De-duplicate with `set`, and sort with `sorted()`. Don't hand-write a
  duplicate check — scanning the list for every item is the O(n²) shape the
  `list` lesson warns about, and `set` exists precisely to avoid it.
- A slice takes `[start:stop:step]`. A negative start counts from the end, and
  a step of `-1` walks backwards. `tables[:3]` and `tables[-2:]` never raise,
  even when the list is shorter than you asked for.
- `sorted()` compares characters by their code point, so **every capital letter
  sorts before every lowercase one**. `'Orders'` would come before `'customers'`.
  That is not a bug to fix — it is how sorting actually works.
