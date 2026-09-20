RUNS = [
  {"name": "orders", "duration": 30, "status": "ok"},
  {"name": "events", "duration": 8, "status": "failed"},
  {"name": "users", "duration": 19, "status": "ok"},
]

assert [r["name"] for r in by_duration(RUNS)] == ["events", "users", "orders"], "sorted by the key, not by the dicts themselves"
assert by_duration([]) == [], "nothing to sort"
assert len(by_duration(RUNS)) == 3, "every run is still there"
assert RUNS[0]["name"] == "orders", "sorted() returns a new list and leaves the original order alone"

assert slowest(RUNS) == "orders", "max with a key finds the biggest BY that key"
assert slowest([{"name": "only", "duration": 1, "status": "ok"}]) == "only", "one run is its own slowest"

assert [r["name"] for r in by_name_then_duration(RUNS)] == ["events", "orders", "users"], "a tuple key sorts by one field, then the next"

TIED = [
  {"name": "orders", "duration": 30, "status": "ok"},
  {"name": "orders", "duration": 5, "status": "ok"},
]

assert [r["duration"] for r in by_name_then_duration(TIED)] == [5, 30], "same name, so the second element of the key decides"

assert names_upper(RUNS) == ["ORDERS", "EVENTS", "USERS"], "map applies the lambda to each"
assert names_upper([]) == [], "mapping nothing"
assert isinstance(names_upper(RUNS), list), "map is lazy — it needs list() to become a list"

assert [r["name"] for r in failures(RUNS)] == ["events"], "filter keeps the ones the lambda says True for"
assert failures([]) == [], "nothing to filter"
assert failures([{"name": "a", "duration": 1, "status": "ok"}]) == [], "nothing failed"
assert isinstance(failures(RUNS), list), "filter is lazy too"

assert all_ok(RUNS) is False, "one run failed"
assert all_ok([{"name": "a", "duration": 1, "status": "ok"}]) is True, "every run succeeded"
assert all_ok([]) is True, "all() of nothing is True — there is no counterexample"

assert any_slow(RUNS, 25) is True, "the 30 is over 25"
assert any_slow(RUNS, 100) is False, "nothing is over 100"
assert any_slow([], 1) is False, "any() of nothing is False — there is no example"
assert any_slow(RUNS, 30) is False, "exactly the limit is not over it"
