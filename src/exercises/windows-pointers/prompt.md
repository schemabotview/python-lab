# Windows & Two Pointers

Run durations, and questions about consecutive stretches of them.

## `max_window_naive(values, size)` and `max_window(values, size)`

The busiest stretch of `size` consecutive runs. Both return
**`(best, steps)`** — the naive one re-adds each window from scratch, the real
one slides. A `size` of 0, or bigger than the data, returns `(0, 0)`.

```python
max_window([15, 22, 19, 30, 8, 25, 19], 3)   # (71, 7)
```

## `pair_sum_sorted(values, target)`

Two indices whose values sum to the target, or `None`. The list is **sorted** —
walk inwards from both ends.

```python
pair_sum_sorted([2, 5, 8, 12, 16, 23], 20)   # (2, 3)
```

## `dedupe_sorted(values)`

Collapse runs of equal **neighbours** in one pass.

## `longest_under(values, limit)`

The length of the longest consecutive run whose total stays at or below the
limit. A **growing and shrinking** window.

## Notes

- **A sliding window adds one value and drops one.** The total is already known
  from last time, so recomputing it is wasted work. On 200 values with a window
  of 50 the naive version takes 7,550 steps and the sliding one takes **200** —
  the same answer for 2.6% of the effort, and the tests pin both figures.
- **Two pointers only work because the list is sorted.** When the sum is too
  small the only way to grow it is to move the left pointer right; too big, move
  the right pointer left. Each step rules out a whole row of pairs, which is why
  one pass replaces the nested loop.
- **`dedupe_sorted` only collapses neighbours** — a test feeds it `[1, 2, 1]`
  and expects **both** `1`s back. That's the same precondition `groupby` had in
  the itertools exercise, and the same silent data loss if you forget it.
- **`longest_under` is the variable-size window.** Grow at the right, and shrink
  from the left only while the constraint is violated. The inner `while` looks
  like it makes this quadratic — it doesn't, because `start` only ever moves
  forward, so each value is added once and removed at most once.
