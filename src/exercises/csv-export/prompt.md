# Row Export

CSV looks trivial until a field contains a comma. Let the module do it.

| Function | Does |
| --- | --- |
| `write_rows(path, fieldnames, rows)` | writes a header then the dict rows; returns how many rows |
| `read_rows(path)` | a list of dicts, keyed by the header |
| `column(path, name)` | one column's values, **by name** |
| `read_positional(path)` | every row as a plain list, **header included** |
| `naive_split(path)` | the wrong way: each line `.split(",")` |

`naive_split` is deliberate — the tests use it to show what the module is
saving you from.

```python
write_rows(path, ["table", "rows"], [{"table": "orders", "rows": "1500"}])
read_rows(path)   # [{'table': 'orders', 'rows': '1500'}]
```

## Notes

- **The whole point is fields that contain the delimiter.** A note reading
  `loaded 1,500 rows` is one field, and the module quotes it on the way out and
  unquotes it on the way back. A test proves `naive_split` sees **four** fields
  where there are three — silently, with no error, producing a corrupted row
  that looks fine until someone reads it.
- **Quotes and even newlines survive inside a field.** A test round-trips a
  value containing `\n` and checks the file still holds exactly **one** row.
- **`newline=""` is not optional.** It tells Python to leave line endings alone
  so the csv module can manage them itself. Without it you get blank rows
  between every record on some platforms, and embedded newlines break.
- **`DictReader` reads by name, so reordered columns don't matter.** A test
  writes the same data with the fieldnames in a different order and checks
  `row["table"]` still works — while `read_positional` shows the positions
  genuinely changed. Reading by index is what breaks when an upstream team adds
  a column.
- **Everything comes back as a string.** CSV has no types; `"1500"` is text, and
  converting it is your job — which is what the ingest-validation exercise was
  about.
