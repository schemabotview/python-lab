# The Cost of a Lookup

Every function here returns **`(answer, steps)`**. The answers match; the step
counts are the lesson.

## `scan_allowed(rows, allowlist)`

Check each row by comparing it against the allowlist entries in turn, stopping
at the first match. Count **every comparison**.

## `hashed_allowed(rows, allowlist)`

The same answer, using a `set`. Count **one step per row**.

```python
rows  = ["orders", "secrets", "events", "temp", "users"]
allow = ["orders", "events", "users"]

scan_allowed(rows, allow)     # (['orders', 'events', 'users'], 12)
hashed_allowed(rows, allow)   # (['orders', 'events', 'users'], 5)
```

## `first_duplicate_naive(values)`

Compare each value against **every earlier one**. Return the first repeat, or
`None`, plus the step count.

## `first_duplicate_fast(values)`

Same answer, remembering what you've seen in a `set`.

Both return `(None, steps)` when there is no duplicate.

## Notes

- **This is why every earlier exercise said "use a set".** Here it's measured
  rather than asserted. With a 300-entry allowlist the scan takes **606** steps
  for five rows; the hash still takes **5**. The allowlist's size simply doesn't
  appear in the second number.
- **Counting steps, not seconds.** A timer would give a different answer on
  every machine and every run. A step counter is deterministic, so it can be
  tested — and it's the thing Big-O notation actually describes.
- **Watch what doubling does.** With 200 clean values the naive duplicate check
  takes 19,900 steps and the fast one takes 200. Double the input to 400 and
  the fast one doubles to 400 — while the naive one **quadruples** to 79,800.
  That is the entire difference between O(n) and O(n²), and tests pin both.
- **The scan short-circuits, and that isn't a rescue.** It stops at the first
  match, so a matching row is cheap — but a row that *isn't* there costs the
  whole list, and misses are the common case in a filter.
- A `set` costs memory and requires hashable values. That's the trade: you are
  buying time with space, which is most of algorithm design in one sentence.
