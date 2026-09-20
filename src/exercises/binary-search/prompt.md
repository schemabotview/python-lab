# Binary Search

The list is **already sorted**. That one fact is what buys everything here.

| Function | Returns |
| --- | --- |
| `binary_search(values, target)` | the index, or `-1` |
| `probes(values, target)` | how many values the search looked at |
| `first_index(values, target)` | the **leftmost** position, or `-1` |
| `last_index(values, target)` | the **rightmost** position, or `-1` |
| `insert_point(values, target)` | where it would go to keep the list sorted |
| `partition_range(dates, start, end)` | the dates in `[start, end)` |

Write `binary_search` and `probes` by hand. For the rest, use `bisect` — it is
the same algorithm, already correct.

```python
first_index([1, 3, 3, 3, 5], 3)   # 1
last_index([1, 3, 3, 3, 5], 3)    # 3
partition_range(dates, "2026-01-04", "2026-01-10")
```

## Notes

- **Halving is why this scales.** A thousand values take at most 10 probes; a
  **million** take at most 20. Tests pin both. Compare that with the previous
  exercise, where doubling the input quadrupled the work — here, doubling the
  input adds **one** step.
- **`(low + high) // 2` and the `low <= high` loop are where the bugs live.**
  Use `low = middle + 1` and `high = middle - 1`, not `middle` — leaving the
  midpoint in the range means a target that isn't there loops forever. Tests
  search for absent values above, below and inside the range for exactly that
  reason.
- **`bisect_left` and `bisect_right` are the first/last pair.** `bisect_left`
  gives the leftmost spot the value could go, `bisect_right` the rightmost —
  which is why `last_index` subtracts one. Both return a position even when the
  value is absent, so you still have to check what's actually there.
- **`partition_range` is a range query, and it's half-open** — start included,
  end excluded, exactly like a Python slice and exactly like every sane
  date-range filter. Two `bisect` calls give you both edges without touching
  anything in between.
- **Sortedness is a precondition, not a detail.** Binary search on unsorted data
  doesn't error — it returns a confidently wrong answer.
