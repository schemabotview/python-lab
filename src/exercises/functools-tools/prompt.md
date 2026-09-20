# Folds, Partials & Caching

Three `functools` tools that replace code you'd otherwise write by hand.

## `total_rows(batches)` and `widest(batches)`

Both fold a list to a single value with `reduce`. Empty input gives `0`.

```python
total_rows([1500, 300, 90])   # 1890
widest([100, 900, 50])        # 900
```

## `qualify(env)`

Pre-fills the first argument of `table_name` and returns the simpler function.

```python
prod = qualify("prod")
prod("sales", "orders")   # "prod.sales.orders"
```

## `row_count(table)`

Decorate it so repeat lookups are free. **Leave the `LOOKUPS` counter in the
body** — the tests use it to prove the body stopped running.

```python
row_count("orders")   # 600, and LOOKUPS["calls"] goes to 1
row_count("orders")   # 600, and LOOKUPS["calls"] stays at 1
```

## Notes

- **`reduce` needs its start value.** `reduce(fn, [])` with no initial value
  raises `TypeError` rather than returning anything — there's nothing to fold
  and no way to invent an answer. Passing `0` is what makes the empty case work,
  and a test covers it for both folds.
- **`partial` returns a real function**, not a closure you wrote — but the
  effect is the one from the previous exercise: arguments fixed now, the rest
  supplied later. The original is untouched and still takes all three.
- **`@lru_cache` is memoisation in one line.** The tests don't check it's
  *faster* — they check the body **stopped running**, via the counter. That's
  the honest way to prove a cache: `cache_info()` then confirms two hits and two
  misses.
- **Only cache pure functions.** Same arguments must mean same result, forever.
  Caching something that reads a database or the clock means serving stale
  answers with total confidence.
- **`maxsize` matters.** `@lru_cache` with no bound holds every result for the
  life of the process — a memory leak that looks like a feature. `cache_clear()`
  empties it, which a test uses to show the body running again.
