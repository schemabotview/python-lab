# Ingest Row Validation

The upstream feed is messy. One bad row must never take down the whole run.

## 1 · `SchemaError`

A custom exception, already declared in the starter. Nothing to add — but note
how little it takes: a class, inheriting `Exception`, with a docstring for a
body.

## 2 · `parse_row()`

`parse_row(raw)` classifies one raw CSV line of `stamp,table,rows`.

```python
parse_row("2026-01-04,orders,1500")   # "ok: orders 1500"
parse_row("2026-01-04,orders,many")   # "bad number: many"
parse_row("2026-01-04,orders")        # "bad shape: 2 fields"
```

## 3 · `error_rate()`

`error_rate(failed, total)` — the failure percentage to one decimal. A batch
with nothing in it is `"0.0%"`, not a crash.

```python
error_rate(1, 3)    # "33.3%"
error_rate(0, 0)    # "0.0%"
```

## 4 · `require_columns()`

`require_columns(row, needed)` returns `True` when every needed column is
present, and otherwise **raises** `SchemaError` naming the first one missing.

```python
require_columns({"table": "orders", "rows": "5"}, ["table", "rows"])   # True
require_columns({"table": "orders"}, ["table", "rows"])
# SchemaError: missing column: rows
```

## 5 · `load_all()`

`load_all(rows)` takes a list of dicts, loads what it can, and reports. A row
is good when it has both columns **and** its `rows` value converts to an
integer.

```python
load_all([
    {"table": "orders", "rows": "1500"},
    {"table": "events"},
    {"table": "users", "rows": "many"},
    {"table": "x", "rows": "7"},
])
```

```text
Attempted: 4
Loaded: 2
Skipped: 2
- missing column: rows
- bad number: many
```

Problems are listed in the order they happened, one `- ` line each.

## Notes

- **Ask forgiveness, not permission.** Don't inspect `raw_rows` with
  `.isdigit()` before converting — that check is wrong for `"-5"`, for `" 7"`
  and for every unicode digit you weren't thinking about. Call `int()` and
  catch the `ValueError`. The conversion already knows the rules.
- **`else` on a `try`** runs only when nothing was raised. Putting the success
  path there, rather than at the end of the `try`, keeps the `try` down to the
  one line that can actually fail.
- **`finally` runs either way** — success, failure, even a `return` from inside
  the `try`. That is what makes it the right home for `attempted`: a counter
  incremented on the success path alone will quietly drift every time a row
  fails.
- `load_all` needs **two `except` arms**, one per failure kind, because the two
  report differently. The first arm that matches wins, so order them the way
  you'd want them read.
- `error_rate` catching `ZeroDivisionError` is the honest version of the
  "guard the denominator" habit — the operation itself tells you when it can't
  proceed.
