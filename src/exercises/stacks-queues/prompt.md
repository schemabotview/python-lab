# Stacks & Queues

Last-in-first-out and first-in-first-out, and what each one is *for*.

## `is_balanced(text)`

Whether every bracket is closed by its own partner, in the right order.
Non-bracket characters are ignored.

```python
is_balanced("(a[b]{c})")   # True
is_balanced("([)]")        # False
```

## `unmatched_at(text)`

The **index** of the first bracket that breaks the rule, or `-1`. An opener
that is never closed reports **its own** index.

## `next_bigger(values)`

For each value, the next larger value to its right — `-1` if there isn't one.

```python
next_bigger([30, 8, 25, 19, 40])   # [40, 25, 40, 40, -1]
```

## `simulate_queue(arrivals, capacity, per_tick)`

`arrivals` is a list of ticks, each a list of jobs. Each tick: everything
arriving joins the queue unless it's **full** (dropped), then up to `per_tick`
jobs are worked, oldest first. Returns `(processed, dropped)`.

## Notes

- **A stack is the right shape whenever the most recent thing must be resolved
  first.** Nested brackets are the classic, but it's the same structure behind
  undo history, call frames and parsing nested config.
- **`next_bigger` is a *monotonic* stack**, and it's worth slowing down over.
  Indices wait on the stack until something bigger arrives, and then **several
  resolve at once** — a test uses `[30, 8, 25, 19, 40]` where `40` settles three
  pending entries in one go. It looks quadratic because of the inner `while`,
  but every index is pushed once and popped once, so it's linear.
- **`unmatched_at` needs the *index* on the stack, not just the character** —
  otherwise there is no way to report where an unclosed opener was.
- **A queue is the other end.** `deque.popleft()` is O(1) where `list.pop(0)`
  shifts everything, which is the difference the collections exercise measured.
- **A bounded queue models backpressure.** When the buffer is full something has
  to give, and dropping is a *decision* — the alternative is unbounded memory
  growth until the process dies. A test sets `capacity=0` to show the degenerate
  case honestly.
