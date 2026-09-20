# Job Retry & Alert Rules

A task just finished. The orchestrator has to decide what happens next — and
the whole exercise is **operators only**.

## 1 · `decide()`

`decide(attempt, max_attempts, exit_code, duration_s, is_critical, last_success_days, run_hour)`

| Line | True when |
| --- | --- |
| `Should retry` | the task failed (`exit_code` is not 0) **and** `attempt` is below `max_attempts` |
| `Page on-call` | it's critical, it failed, and there are no retries left — **or** it hasn't succeeded for more than 3 days |
| `Backfill needed` | the last success was more than 1 day ago |
| `SLA breached` | it ran longer than 3600 seconds |
| `In window` | `run_hour` is in the nightly window: 0 up to but not including 6 |
| `Backoff` | `30 * 2 ** attempt` seconds — but **0** when not retrying |

```python
decide(1, 3, 1, 1200, True, 1, 2)
```

```text
Should retry: True
Page on-call: False
Backfill needed: False
SLA breached: False
In window: True
Backoff: 60s
```

## 2 · `partition_plan()`

`partition_plan(total_rows, rows_per_file)` — how the writer splits a batch.
A leftover row still needs a file of its own.

```python
partition_plan(10500, 1000)
```

```text
Rows: 10500
Full files: 10
Remainder: 500
Files written: 11
```

## 3 · `decode_status()`

A status bitmask from the run API. Bit 1 is retried, bit 2 is partial, bit 4 is
schema drift. Return the three as a tuple of real booleans.

```python
decode_status(5)   # (True, False, True)
decode_status(0)   # (False, False, False)
```

## 4 · `identity_check()`

Two config references. Return whether they're the **same object**, and whether
they merely **hold the same value**.

```python
identity_check([1], [1])   # (False, True)
```

## 5 · `has_rows()`

Did the query come back with anything? Return a real boolean.

## 6 · `with_default()`

An unset environment variable arrives as `""`. Return the configured value, or
the fallback when it's blank.

```python
with_default("", "prod")     # "prod"
with_default("staging", "prod")   # "staging"
```

## 7 · `is_allowed()`

Whether a table is in the allowlist.

## Notes

- **No `if`, `elif`, `else`, and no ternary.** Conditionals are the next topic.
- `Backoff` is the interesting one. You can't branch, but `True` and `False` are
  worth `1` and `0` in arithmetic — multiplying by a flag is how you zero a
  number without an `if`. `Files written` uses the same trick in reverse.
- Put parentheses around the two halves of `Page on-call`. `and` binds tighter
  than `or`, so it's right without them — write them anyway, so the reader
  doesn't have to know that.
- `In window` wants a **chained comparison**: Python lets you write
  `0 <= x < 6` exactly as you would in maths.
- `has_rows` should use **truthiness**, not `len(result) > 0` — an empty list,
  an empty string and an empty dict are all already falsy. `bool()` turns that
  into the real `True`/`False` the tests want.
- `with_default` is the `or` idiom: `or` returns the first truthy operand, not
  a boolean, so `"" or "prod"` is `"prod"`.
- `identity_check` is the bug behind every "why did my shared config change"
  mystery. `==` asks whether two things look alike; `is` asks whether they are
  one and the same object.
