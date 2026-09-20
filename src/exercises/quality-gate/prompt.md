# Data Quality Gate

A table just finished loading. Decide whether it is fit to promote.

## 1 · `quality_grade()`

`quality_grade(null_percent)` grades a table on its null rate.

| Null rate | Grade |
| --- | --- |
| under 1% | `"A"` |
| under 5% | `"B"` |
| under 10% | `"C"` |
| under 25% | `"D"` |
| 25% or more | `"F"` |

## 2 · `gate()`

`gate(table, row_count, null_percent, freshness_hours, note)` returns the
verdict as one multi-line string.

- **Grade** — reuse `quality_grade`, don't rewrite the thresholds.
- **Freshness** — `"OK"` at 24 hours or less, `"STALE"` beyond that.
- **Volume** — `"OK"` at 1000 rows or more, `"LOW"` below that.
- **Note** — the operator's note if there is one, otherwise `"Note: none"`.
- **Verdict** — `"PROMOTE"` when the grade is C or better **and** freshness is
  OK **and** volume is OK. Otherwise `"QUARANTINE"`.

```python
gate("orders", 12000, 3.2, 4, "")
```

```text
Table: orders
Grade: B
Freshness: OK
Volume: OK
Note: none
Verdict: PROMOTE
```

```python
gate("clicks", 200, 30.0, 40, "upstream late")
```

```text
Table: clicks
Grade: F
Freshness: STALE
Volume: LOW
Note: upstream late
Verdict: QUARANTINE
```

## 3 · `route()`

`route(event_type)` sends an incoming event to its raw table. Use `match`.

| Event | Table |
| --- | --- |
| `order.created`, `order.shipped` | `orders_raw` |
| `user.signup` | `users_raw` |
| `click`, `view` | `events_raw` |
| anything else | `dead_letter` |

## Notes

- **Order your `elif`s deliberately.** Test `quality_grade(3.2)` and confirm you
  get `"B"`. A chain written low-to-high returns the wrong grade for every input
  that isn't an A — and it never errors, so nothing tells you it's wrong.
- **Don't rebuild the grade inside `gate`.** Call `quality_grade` once and reuse
  the variable. Two copies of a threshold table is two places to get it wrong.
- **Use a truthy check for the note**, not `note == ""`. An operator who left
  the field alone entirely sends `None`, which `== ""` would miss — and a truthy
  check catches both.
- **Verdict must be a ternary** — `a if cond else b`, one line.
- `match` takes several patterns on one arm with `|`, and `case _` is the
  catch-all default. It is not a C-style switch: there is no fall-through.
