# Tally, Group & Queue

Four containers, each replacing several lines you'd otherwise write by hand.
`Run` is declared for you.

| Function | Example |
| --- | --- |
| `top_tables(names, count)` | → `[('orders', 3), ('events', 2)]` |
| `tally(names)` | → `{'orders': 3, 'events': 2, 'users': 1}` — a plain `dict` |
| `group_rows(pairs)` | `[("orders","r1"),("events","e1"),("orders","r2")]` → `{'orders': ['r1','r2'], 'events': ['e1']}` |
| `recent(events, size)` | `recent(["a","b","c","d"], 2)` → `['c','d']` |
| `as_queue(items)` | drains first-in-first-out |
| `summarise(run)` | → `"orders: 1500 rows (ok)"` |

## Notes

- **`Counter` is the hand-rolled counting dict, done.** No `if key in counts`,
  no `.get(key, 0) + 1`. `most_common(n)` gives the top n already sorted.
- **`defaultdict(list)` skips the "does this key exist?" dance.** Touching a
  missing key creates its default, so `grouped[table].append(x)` just works.
  Return `dict(grouped)` — a `defaultdict` compares equal to a plain dict, but
  returning it hands the caller something that silently invents keys on read,
  which is rarely what they want.
- **`deque(maxlen=size)` is a sliding window for free.** Push past the limit and
  the oldest falls off the other end — no manual trimming, no slicing.
- **`deque` is fast at both ends; a list is not.** `list.pop(0)` shifts every
  remaining element, so draining a queue that way is O(n²). `popleft()` is O(1).
  For a queue of any size that is the difference between working and not.
- **A `namedtuple` is a record that is still a tuple.** Fields by name *and*
  by index, it unpacks, and it compares equal to the plain tuple — tests pin all
  four. It is also **immutable**, which is what separates it from a
  `@dataclass`: reach for `namedtuple` for a fixed record, `@dataclass` when you
  need defaults, methods or mutability.
