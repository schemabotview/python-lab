# Pipeline Run Cost

Five small pieces of the daily job report. Each is one function.

## 1 · The rates

The finance team publishes three rates. Name them at the top of the file, in
`UPPER_CASE` — Python has no `const` keyword, so capitals are how you say
"don't reassign this".

```python
COMPUTE_RATE = 0.55     # per hour
STORAGE_RATE = 0.023    # per GB
EGRESS_RATE  = 0.09     # per GB
```

## 2 · `cost_report()`

`cost_report(compute_hours, storage_gb, egress_gb, discount_percent)` returns the
summary as one multi-line string.

```python
cost_report(6.5, 120.0, 45.0, 10)
```

```text
--- Nightly Run Cost ---
Compute (6.5h): $3.58
Storage (120.0GB): $2.76
Egress (45.0GB): $4.05
------------------------
Subtotal: $10.38
Discount (10%): $1.04
Total: $9.35
```

Quantities show one decimal, money shows two, the separator is 24 dashes, and
there is no trailing newline.

## 3 · `parse_env()`

`parse_env(raw_hours, raw_retries, raw_debug)` — environment variables are
**always strings**. Return a tuple of the three
converted to `float`, `int` and `bool`.

```python
parse_env("6.5", "3", "false")   # (6.5, 3, False)
parse_env("8", "0", "true")      # (8.0, 0, True)
```

## 4 · `describe()`

Report what a config value actually turned out to be — `"int"`, `"float"`,
`"str"`, `"bool"`, `"none"`, or `"other"` for anything else.

```python
describe(42)      # "int"
describe(None)    # "none"
describe([1, 2])  # "other"
```

## 5 · `to_iso()`

The upstream feed sends `DD-MM-YYYY`. The warehouse wants `YYYY-MM-DD`.

```python
to_iso("04-01-2026")   # "2026-01-04"
```

## 6 · `split_fields()`

Column 0 is the table name; everything after it is data. Return both.

```python
split_fields("orders,1500,ok")   # ("orders", ["1500", "ok"])
```

## Notes

- Use `isinstance()` rather than `type(x) ==`.
- **`bool` is a subclass of `int`.** `isinstance(True, int)` is `True`, so if
  `describe` tests for `int` first it will call every `True` an `"int"`. Order
  those checks deliberately.
- **`bool("false")` is `True`.** Any non-empty string is truthy, so passing an
  env var straight to `bool()` makes `"false"`, `"0"` and `"no"` all mean yes.
  This is a real bug that reaches real production. Compare the text instead.
- `split_fields` wants a starred name: `first, *rest = ...` collects whatever
  is left into a list, however many fields there are.
- **The money is not rounded the way you expect, twice over.** The subtotal is
  `10.385` but prints `$10.38`. That is not a rule about `.5` going down —
  `10.385` cannot be stored exactly in binary, and the value actually stored is
  a hair *below* it, so it rounds down honestly. Separately, a value that *is*
  stored exactly and lands exactly halfway goes to the **even** digit. Both are
  correct. Never use `float` for money you have to reconcile — that is what
  `decimal.Decimal` is for.
