assert lookup({"orders": 1500}, "orders") == 1500, "a table that ran"
assert lookup({"orders": 1500}, "events") == 0, "a table that never ran is 0, not a KeyError"
assert lookup({}, "anything") == 0, "an empty ledger"
assert lookup({"orders": 0}, "orders") == 0, "a table that ran and loaded nothing"

try:
  {"orders": 1500}["events"]
except KeyError:
  BRACKETS = "raises"
else:
  BRACKETS = "returned something"

assert BRACKETS == "raises", "the bracket form raises — which is why lookup uses .get"

assert merge_runs({"orders": 1500, "events": 300}, {"events": 350, "users": 90}) == {"orders": 1500, "events": 350, "users": 90}, "the later run wins where they overlap"
assert merge_runs({}, {"a": 1}) == {"a": 1}, "merging onto nothing"
assert merge_runs({"a": 1}, {}) == {"a": 1}, "merging nothing on top"
assert merge_runs({}, {}) == {}, "two empty runs"

FIRST = {"orders": 1500}
SECOND = {"orders": 9}

assert merge_runs(FIRST, SECOND) == {"orders": 9}, "the merge happens"
assert FIRST == {"orders": 1500}, "copy before updating — the earlier run must survive"
assert SECOND == {"orders": 9}, "and so must the later one"

assert add_row({}, "events", "e1") == {"events": ["e1"]}, "the first row starts the list"
assert add_row({"orders": ["r1"]}, "orders", "r2") == {"orders": ["r1", "r2"]}, "a later row appends"
assert add_row({"orders": ["r1"]}, "events", "e1") == {"orders": ["r1"], "events": ["e1"]}, "a new table joins the index"

INDEX = {"orders": ["r1"]}

assert add_row(INDEX, "orders", "r2") == {"orders": ["r1", "r2"]}, "the row is filed"
assert INDEX == {"orders": ["r1"]}, "the caller's index is untouched — the inner lists need copying too"

assert ledger_report({"orders": 1500, "events": 300}).splitlines()[0] == "events: 300", "sorted by table name, so events comes first"
assert ledger_report({"orders": 1500, "events": 300}).splitlines()[1] == "orders: 1500", "then orders"
assert ledger_report({"orders": 1500, "events": 300}).splitlines()[2] == "TOTAL: 1800", "the total across the values"
assert ledger_report({}).splitlines() == ["TOTAL: 0"], "an empty ledger still reports its total"
assert len(ledger_report({"a": 1, "b": 2, "c": 3}).splitlines()) == 4, "three tables plus the total"
assert ledger_report({"z": 1, "a": 2}).splitlines()[0] == "a: 2", "insertion order is not name order"

assert drop_table({"a": 1, "b": 2}, "a") == {"b": 2}, "the table is removed"
assert drop_table({"a": 1}, "zzz") == {"a": 1}, "dropping a table that was never there is fine"
assert drop_table({}, "a") == {}, "dropping from an empty ledger"

LEDGER = {"a": 1, "b": 2}

assert drop_table(LEDGER, "a") == {"b": 2}, "the drop happens"
assert LEDGER == {"a": 1, "b": 2}, "the caller's ledger is untouched"

assert column_order([("id", "int"), ("amount", "float"), ("created", "date")]) == ["id", "amount", "created"], "columns keep the order they were declared in"
assert column_order([("z", "int"), ("a", "int")]) == ["z", "a"], "insertion order, not alphabetical"
assert column_order([]) == [], "a schema with no columns"
assert column_order([("id", "int"), ("id", "str")]) == ["id"], "a repeated column is one column, keeping its first position"
