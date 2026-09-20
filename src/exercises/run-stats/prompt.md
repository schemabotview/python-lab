# Batch Run Statistics

Last night's pipeline finished. These are the numbers you report on.

**No `sum()`, `min()`, `max()`, `len()` on the values, `sorted()` or `.count()`
for the statistics.** Building them by hand is the entire point — the
accumulator pattern is what every aggregation you will ever write is made of.

## 1 · `run_stats()`

`run_stats(durations, sla)` — runtimes in minutes.

```python
run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25)
```

```text
Runs: 9
Total: 180m
Average: 20.0m
Fastest: 8m
Slowest: 30m
Over SLA: 2
```

An empty list must not crash: every number reports `0`, and the average `0.0`.

## 2 · `table_report()`

`table_report(names, durations)` — the two lists line up by position.

```python
table_report(["orders", "customers", "events"], [15, 22, 19])
```

```text
1. orders 15m
2. customers 22m
3. events 19m
```

## 3 · `locate()`

`locate(names, wanted)` — where a table sits in tonight's schedule.

```python
locate(["orders", "events"], "events")   # "events at position 1"
locate(["orders"], "payments")           # "payments not scheduled"
```

## 4 · `first_breach()`

`first_breach(durations, sla)` — the index of the first run over the SLA, or
`-1` if every run was inside it. **Use `while`, not `for`** — track the index
yourself and step it by hand.

## 5 · `drain()`

`drain(queue)` — work through a queue that ends with the sentinel `"END"`.
Each item is `kind:name`. Skip anything marked `retry`, stop the whole loop
dead on a `fatal`, and collect the names of everything else.

```python
drain(["ok:orders", "retry:events", "ok:users", "fatal:disk", "ok:never", "END"])
# ["orders", "users"]
```

Note what is *not* in that result: `events` was skipped, and `never` was never
reached.

## Notes

- **Seed your accumulators carefully.** `total` starts at `0`, which is right.
  `fastest` starting at `0` is wrong — no positive runtime will ever be below
  it, so it stays `0` forever. Start it from the first value you see instead.
- The average is the one place a `/` can blow up. An empty list has nothing to
  divide by.
- `table_report` wants `zip` to walk two lists together and `enumerate` to
  number them. `enumerate` takes a `start=` if you don't want to count from 0.
- `locate` is the `for`/`else` shape: the `else` on a loop runs only when the
  loop finished **without** breaking out. It is the cleanest way to say "I
  looked at everything and didn't find it".
- `drain` wants the walrus: `while (item := items.pop(0)) != "END":` takes the
  next item and tests it in one breath. Work on a copy — `list(queue)` — so
  you don't empty the caller's queue.
- `continue` skips to the next item; `break` abandons the loop entirely. The
  order you check them in decides what happens to the items behind a `fatal`.
