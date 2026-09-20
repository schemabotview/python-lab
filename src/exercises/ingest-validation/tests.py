assert issubclass(SchemaError, Exception), "SchemaError is an exception"

assert parse_row("2026-01-04,orders,1500") == "ok: orders 1500", "a clean row"
assert parse_row("2026-01-04,orders,0") == "ok: orders 0", "zero rows is still a number"
assert parse_row("2026-01-04,orders,-5") == "ok: orders -5", "a negative converts fine — .isdigit() would reject it"
assert parse_row("2026-01-04,orders,many") == "bad number: many", "not a number"
assert parse_row("2026-01-04,orders,") == "bad number: ", "an empty count is not a number either"
assert parse_row("2026-01-04,orders") == "bad shape: 2 fields", "too few fields"
assert parse_row("a,b,c,d") == "bad shape: 4 fields", "too many fields"
assert parse_row("") == "bad shape: 1 fields", "an empty line splits to one empty field"

assert error_rate(1, 3) == "33.3%", "one in three, to one decimal"
assert error_rate(0, 10) == "0.0%", "a clean batch"
assert error_rate(10, 10) == "100.0%", "everything failed"
assert error_rate(0, 0) == "0.0%", "an empty batch must not divide by zero"
assert error_rate(5, 0) == "0.0%", "nothing to divide by, however many failed"

assert require_columns({"table": "orders", "rows": "5"}, ["table", "rows"]) is True, "every column present"
assert require_columns({"table": "o", "rows": "5", "extra": 1}, ["table"]) is True, "extra columns are fine"
assert require_columns({}, []) is True, "nothing needed, nothing missing"

try:
  require_columns({"table": "orders"}, ["table", "rows"])
except SchemaError as exc:
  MISSING = str(exc)
else:
  MISSING = "nothing was raised"

assert MISSING == "missing column: rows", "raises SchemaError naming the missing column"

try:
  require_columns({"rows": "5"}, ["table", "rows"])
except SchemaError as exc:
  FIRST = str(exc)
else:
  FIRST = "nothing was raised"

assert FIRST == "missing column: table", "names the first missing column, in the order asked for"

BATCH = [
  {"table": "orders", "rows": "1500"},
  {"table": "events"},
  {"table": "users", "rows": "many"},
  {"table": "x", "rows": "7"},
]

assert load_all(BATCH).splitlines()[0] == "Attempted: 4", "finally counts every row, however it went"
assert load_all(BATCH).splitlines()[1] == "Loaded: 2", "two rows were clean"
assert load_all(BATCH).splitlines()[2] == "Skipped: 2", "two rows had problems"
assert load_all(BATCH).splitlines()[3] == "- missing column: rows", "the schema problem, reported first"
assert load_all(BATCH).splitlines()[4] == "- bad number: many", "then the conversion problem"
assert len(load_all(BATCH).splitlines()) == 5, "three counts plus one line per problem"

assert load_all([]).splitlines()[0] == "Attempted: 0", "an empty batch"
assert load_all([]).splitlines()[1] == "Loaded: 0", "nothing loaded"
assert len(load_all([]).splitlines()) == 3, "no problem lines when there were no problems"
assert load_all([{"table": "a", "rows": "1"}]).splitlines()[2] == "Skipped: 0", "a clean batch skips nothing"
