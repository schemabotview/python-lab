# Log Patterns

Two patterns are compiled for you at the top. Use them.

```python
LINE   = r"^(?P<stamp>\S+) (?P<level>[A-Z]+) (?P<table>\w+)"
SECRET = r"password=\S+"
```

| Function | Example |
| --- | --- |
| `find_level(line)` | `"2026-01-04T02:15 INFO orders loaded"` → `"INFO"` |
| `parse_line(line)` | → `('2026-01-04T02:15', 'INFO', 'orders')` |
| `all_tables(text)` | `"table=orders rows=5 table=events"` → `['orders', 'events']` |
| `redact(text)` | `"password=hunter2"` → `"password=***"` |
| `split_fields(line)` | `"a; b ;c"` → `['a', 'b', 'c']` |
| `row_counts(text)` | `"rows=1500 rows=300"` → `[1500, 300]` |

A line that doesn't match gives `""` from `find_level` and three empty strings
from `parse_line` — never a crash.

## Notes

- **`search` returns `None` when nothing matches, and `None` has no `.group()`.**
  That `AttributeError` is the single most common regex bug. Check for `None`
  first — it's the guard-clause shape again.
- **Named groups beat numbered ones.** `m.group("level")` still reads right
  after someone adds a group in the middle; `m.group(2)` quietly starts
  returning something else. Both work here, and a test shows `group(0)` is the
  whole match.
- **`match` is anchored at the start, `search` looks anywhere.** A test proves
  `re.match(r"orders", "the orders table")` finds nothing at all — which looks
  like a broken pattern and isn't.
- **Always write patterns as raw strings.** In `r"\d"` the backslash reaches the
  regex engine; in `"\d"` Python gets first refusal on the escape. A test checks
  `len(r"\d") == 2` to make the difference concrete.
- **`re.compile` once when a pattern is hot** — per-line parsing is exactly
  that. The compiled object carries the same `search`/`sub`/`findall` methods.
- **Don't over-reach.** These are flat log lines, which regex is genuinely good
  at. For HTML, JSON or CSV, use the parser — the CSV exercise showed what
  hand-rolled splitting costs on data that only *looks* simple.
