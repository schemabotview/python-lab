# Stream Toolbox

`itertools` is the lazy counterpart to generators. Every function here returns
a plain `list`, so the answers are assertable — but the work in the middle
stays lazy.

| Function | Example |
| --- | --- |
| `stitch(*batches)` | `stitch(["a","b"], ["c"])` → `['a','b','c']` |
| `page(stream, start, stop)` | `page(["a","b","c","d"], 1, 3)` → `['b','c']` |
| `endless_ids(prefix)` | an **endless** stream: `run-1`, `run-2`, … |
| `rotate(options, length)` | `rotate(["a","b"], 5)` → `['a','b','a','b','a']` |
| `group_by_table(rows)` | `[("orders",5),("events",3),("orders",7)]` → `{'orders':[5,7],'events':[3]}` |
| `running_total(counts)` | `running_total([100,50,25])` → `[100,150,175]` |
| `pairs(tables)` | `pairs(["a","b","c"])` → `[('a','b'),('a','c'),('b','c')]` |

`page` must work on `endless_ids` — a test slices pages 3 and 4 out of an
infinite stream.

## Notes

- **`groupby` only groups *neighbours*.** It walks the stream once and starts a
  new group every time the key changes, so unsorted input silently produces
  several groups with the same key — and if you collect them into a dict, the
  later ones overwrite the earlier and **rows just vanish**. A test runs the
  naive version on unsorted input and pins the wrong answer, so you can see the
  data loss. Sort by the same key first. Always.
- **Nothing here builds a list until you ask.** `cycle` repeats forever and
  `count` counts forever, and both are perfectly safe because `islice` decides
  when to stop. That combination — an endless source and a lazy slice — is the
  whole idea.
- **`islice` takes a half-open range**, like a slice, but it **cannot go
  backwards**: there are no negative indices on an iterator, because it doesn't
  know where the end is.
- **Most of these return one-shot iterators.** Consume one and it's spent — a
  test proves it on `chain`. That's why every function here wraps its result in
  `list()` before returning.
- `accumulate` gives the running total *after each item*, so it returns as many
  values as it was given — not one summary value. `reduce` is the one that
  collapses to a single answer.
