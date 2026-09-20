# Log Line Parser

Run logs look like this:

```text
2026-01-04 02:15:31 info orders loaded=1500 ms=4200
```

## 1 · `parse_line()`

`parse_line(line)` breaks out the four leading parts. The level is reported in
capitals however it was written.

```text
Date: 2026-01-04
Time: 02:15:31
Level: INFO
Table: orders
```

## 2 · `normalise()`

`normalise(name)` turns a hand-typed CSV header into a safe column name:
trimmed, lowercased, runs of whitespace collapsed to single underscores.

```python
normalise("  Order  Total ")   # "order_total"
normalise("ID")                # "id"
```

## 3 · `redact()`

`redact(line, secret)` hides a secret before the line reaches the log.

```python
redact("user=admin password=hunter2", "hunter2")
# "user=admin password=***"
```

## 4 · `source_kind()`

`source_kind(path)` routes an input path.

| Path | Kind |
| --- | --- |
| on S3 **and** a `.csv` | `"s3-csv"` |
| on S3, anything else | `"s3-other"` |
| a local `.csv` | `"local-csv"` |
| anything else | `"unknown"` |

## 5 · `field()`

`field(line, key)` pulls one `key=value` field out of a line. A key that isn't
there gives `""`.

```python
field("loaded=1500 ms=4200", "ms")     # "4200"
field("loaded=1500", "missing")        # ""
```

## 6 · `to_csv()`

`to_csv(values)` joins values into one CSV line, trimming each first.

```python
to_csv([" a ", "b ", "  c"])   # "a,b,c"
```

## Notes

- **Strings never change.** `.upper()`, `.strip()` and `.replace()` all return a
  **new** string and leave the original exactly as it was. Writing
  `line.strip()` on its own line does nothing at all — you have to keep what it
  hands back. A test pins this.
- **`.split()` with no argument is not the same as `.split(" ")`.** The bare
  form splits on runs of any whitespace and drops the empties, which is why
  `normalise` can collapse a double space with `"_".join(name.split())` and
  never produce `order__total`.
- `line[:10]` slices the date straight off the front. Slicing a string works
  exactly like slicing a list, because both are sequences.
- **`.partition(sep)` always returns three pieces** — before, the separator
  itself, after — and never raises. The middle piece is `""` when the separator
  wasn't found, which is how `field` tells "missing key" from "empty value"
  without a `.find()` returning `-1` to remember to check.
- `.startswith()` and `.endswith()` say what you mean far better than
  `path[:5] == "s3://"`, and they don't go wrong when the string is shorter
  than the slice.
