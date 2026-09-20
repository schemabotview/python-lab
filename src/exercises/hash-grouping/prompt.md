# Hashing & Grouping

One dict, one pass — the shape behind most "make it fast" rewrites.

## `two_sum(numbers, target)`

The indices of two values summing to the target, as `(i, j)` with `i < j`, or
`None`. **One pass**: for each value, ask whether the one you still need has
already been seen.

```python
two_sum([2, 7, 11, 15], 9)   # (0, 1)
two_sum([1, 2, 3], 100)      # None
```

## `two_sum_naive(numbers, target)`

Every pair compared. Returns `(answer, steps)` — same answers, so the counts
can be compared.

## `group_by_schema(tables)`

Group `(name, columns)` pairs by their **set** of columns. Returns
`{frozenset: [sorted names]}`.

```python
group_by_schema([("orders", ["id", "amount"]), ("orders_v2", ["amount", "id"])])
# {frozenset({'id', 'amount'}): ['orders', 'orders_v2']}
```

## `join_keys(left, right)` → the keys on **both** sides, sorted

## `index_by(rows, field)`

A lookup from a field's value to the rows carrying it, in arrival order.

## Notes

- **The dict turns "search" into "remember".** The naive two-sum asks "does any
  later value complete this one?" and has to look. The one-pass version asks
  "has the value I need already gone past?" — and a dict answers that without
  looking. 200 values: 19,900 comparisons against one pass.
- **`frozenset` is what makes `group_by_schema` work.** Column order shouldn't
  change a schema's identity, and a set ignores order — but a plain `set` can't
  be a dict key, so it has to be frozen. That's the exact pairing from the
  Schema Drift and Partition Keys exercises, now doing real work.
- **`setdefault(key, []).append(x)` is the grouping idiom**, the same one
  `row-ledger` used. `defaultdict(list)` is the other spelling; either is fine.
- **Trading memory for time is the deal.** The dict holds every value you've
  seen. On 200 numbers that's free; on a billion-row join it's the thing that
  decides whether the job fits in memory — which is why real engines pick
  between hash joins and sort-merge joins by exactly this question.
