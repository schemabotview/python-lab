import os
os.makedirs("/tmp/lab", exist_ok=True)
EXPORT = "/tmp/lab/export.csv"
FIELDS = ["table", "rows", "note"]

assert write_rows(EXPORT, FIELDS, [{"table": "orders", "rows": "1500", "note": "ok"}]) == 1, "one row written"
assert read_rows(EXPORT) == [{"table": "orders", "rows": "1500", "note": "ok"}], "and read back as a dict"
assert column(EXPORT, "table") == ["orders"], "one column by name"

write_rows(EXPORT, FIELDS, [
  {"table": "orders", "rows": "1500", "note": "ok"},
  {"table": "events", "rows": "300", "note": "late"},
])

assert len(read_rows(EXPORT)) == 2, "two rows"
assert column(EXPORT, "rows") == ["1500", "300"], "values come back as strings — csv does no type conversion"
assert column(EXPORT, "note") == ["ok", "late"], "a different column"
assert read_positional(EXPORT)[0] == ["table", "rows", "note"], "csv.reader includes the header row"
assert len(read_positional(EXPORT)) == 3, "header plus two rows"

assert write_rows(EXPORT, FIELDS, []) == 0, "no rows"
assert read_rows(EXPORT) == [], "reads back empty"
assert read_positional(EXPORT) == [["table", "rows", "note"]], "but the header is still written"

write_rows(EXPORT, FIELDS, [{"table": "orders", "rows": "5", "note": "loaded 1,500 rows"}])

assert read_rows(EXPORT)[0]["note"] == "loaded 1,500 rows", "a comma INSIDE a field survives, because the module quoted it"
assert len(read_rows(EXPORT)) == 1, "still one row"
assert len(naive_split(EXPORT)[1]) == 4, "split(',') sees four fields where there are three — the row is corrupted"
assert len(read_positional(EXPORT)[1]) == 3, "the module gets it right"

write_rows(EXPORT, FIELDS, [{"table": "orders", "rows": "5", "note": 'he said "ok"'}])

assert read_rows(EXPORT)[0]["note"] == 'he said "ok"', "quotes inside a field survive too"

write_rows(EXPORT, FIELDS, [{"table": "orders", "rows": "5", "note": "line one\nline two"}])

assert read_rows(EXPORT)[0]["note"] == "line one\nline two", "even a NEWLINE inside a field, which is why newline='' matters"
assert len(read_rows(EXPORT)) == 1, "it is one row, not two"

write_rows(EXPORT, ["rows", "table", "note"], [{"table": "orders", "rows": "5", "note": "ok"}])

assert read_rows(EXPORT)[0]["table"] == "orders", "reading by name survives the columns being reordered"
assert read_positional(EXPORT)[0] == ["rows", "table", "note"], "though the positions really did change"
