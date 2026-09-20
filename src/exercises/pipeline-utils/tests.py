assert version() == "1.0.0", "the build stamp"

assert table_name("sales", "orders") == "prod.sales.orders", "the environment defaults to prod"
assert table_name("sales", "orders", "dev") == "dev.sales.orders", "a positional override"
assert table_name("sales", "orders", env="staging") == "staging.sales.orders", "the same argument by keyword"

assert summarize(4, 8, 15, 16, 23, 42) == (108, 18.0), "total and average of six runs"
assert summarize(10) == (10, 10.0), "one run is its own average"
assert summarize() == (0, 0), "no runs at all must not divide by zero"
assert summarize(1, 2) == (3, 1.5), "the average keeps its fraction"

assert build_config() == {"env": "prod", "retries": 3, "parallel": 4}, "no overrides gives the defaults"
assert build_config(retries=5) == {"env": "prod", "retries": 5, "parallel": 4}, "an override replaces one default"
assert build_config(owner="data")["owner"] == "data", "an unknown key is added, not rejected"
assert build_config(retries=5, owner="data")["retries"] == 5, "several overrides at once"

build_config(retries=99)

assert DEFAULTS == {"env": "prod", "retries": 3, "parallel": 4}, "copy before updating — DEFAULTS must survive a call"

assert apply_all("  Orders ", str.strip, str.lower) == "orders", "each transform feeds the next"
assert apply_all("x") == "x", "no steps leaves the value alone"
assert apply_all("  a  ", str.strip) == "a", "a single step"
assert apply_all(3, abs, str) == "3", "the steps can be any callables, in order"
assert apply_all(-3, str, str.strip) == "-3", "order matters — these two would break if swapped"

assert (first_failure([("extract", "ok"), ("load", "failed")]), first_failure([("extract", "ok")])) == ("load", None), "the first failed step, or None when every step passed"
assert (first_failure([("extract", "failed"), ("load", "failed")]), first_failure([])) == ("extract", None), "the FIRST failure, not the last; and no steps means no failure"

assert report([("extract", "ok"), ("load", "failed")]) == "first failure: load", "names the failure"
assert report([("extract", "ok")]) == "all steps ok", "the None is guarded, not formatted into the message"
assert report([]) == "all steps ok", "an empty run counts as clean"

assert check_row({"table": "orders", "checksum": "abc", "rows": 5}) == "orders: accepted", "nothing wrong with it"
assert check_row({"table": "", "checksum": "abc", "rows": 5}) == "no table name", "the name guard fires first"
assert check_row({"table": "orders", "checksum": "", "rows": 5}) == "orders: no checksum", "the checksum guard"
assert check_row({"table": "orders", "checksum": "abc", "rows": 0}) == "orders: empty", "no rows arrived"
assert check_row({"table": "orders", "checksum": "abc", "rows": 1}) == "orders: accepted", "1 row is not fewer than 1"
assert check_row({"table": "", "checksum": "", "rows": 0}) == "no table name", "three things wrong, only the first is reported"
assert check_row({"table": "orders", "checksum": "", "rows": 0}) == "orders: no checksum", "two things wrong, the earlier guard wins"
assert check_row({}) == "no table name", "a row with nothing in it at all"

assert collect("a") == ["a"], "a fresh list"
assert collect("b") == ["b"], "a SECOND fresh list — errors=[] would return ['a', 'b'] here"
assert collect("c", ["x"]) == ["x", "c"], "appends to the list it was given"

SHARED = []

assert collect("d", SHARED) == ["d"], "the caller's list is used"
assert SHARED == ["d"], "and it is the same list, mutated in place"
