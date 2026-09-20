# Sorting Runs by Key

Every run is a dict:

```python
{"name": "orders", "duration": 30, "status": "ok"}
```

| Function | Returns |
| --- | --- |
| `by_duration(runs)` | the runs, ordered by duration |
| `slowest(runs)` | the **name** of the longest run |
| `by_name_then_duration(runs)` | ordered by name, then duration |
| `names_upper(runs)` | every name, uppercased — use `map` |
| `failures(runs)` | only the runs that didn't succeed — use `filter` |
| `all_ok(runs)` | whether every run succeeded |
| `any_slow(runs, limit)` | whether any run went over `limit` |

## Notes

- **`key=` is the idiom you'll use most.** `sorted`, `min` and `max` all take
  it, and it answers "sort by *what*". Without it, `sorted` would try to compare
  the dicts themselves and raise.
- **`max(runs, key=...)` returns the whole run**, not the duration — so
  `slowest` has to reach into it for the name afterwards. That's usually what
  you want: it finds the winner *by* a measure, and hands you the winner.
- **A tuple key sorts by one field, then the next**, with no extra work. It's
  the same rule that makes tuples compare the way they do.
- **`map` and `filter` are lazy** — they return iterators, not lists, so
  `list(...)` is needed to see anything. A comprehension often reads clearer for
  exactly these two jobs; they're here because you will meet them in other
  people's code.
- **`all([])` is `True` and `any([])` is `False`.** That surprises people, but
  it's the only consistent answer: `all` asks whether there's a counterexample
  and `any` asks whether there's an example, and an empty list has neither.
  Both tests pin it.
- `all` and `any` **short-circuit** — they stop at the first decisive value, so
  feeding them a generator means the rest is never computed.
