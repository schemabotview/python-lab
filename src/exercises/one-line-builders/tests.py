RECORDS = [
  {"table": "orders", "rows": 1500, "status": "ok"},
  {"table": "events", "rows": 300, "status": "failed"},
  {"table": "users", "rows": 90, "status": "ok"},
]

assert table_names(RECORDS) == ["orders", "events", "users"], "every name, in arrival order"
assert table_names([]) == [], "no records"
assert table_names([{"table": "a", "rows": 1, "status": "ok"}]) == ["a"], "one record"

assert loaded_only(RECORDS) == ["orders", "users"], "the failed table is filtered out"
assert loaded_only([]) == [], "nothing to filter"
assert loaded_only([{"table": "a", "rows": 1, "status": "failed"}]) == [], "everything filtered out"
assert loaded_only([{"table": "a", "rows": 1, "status": "ok"}]) == ["a"], "nothing filtered out"

assert rows_by_table(RECORDS) == {"orders": 1500, "events": 300, "users": 90}, "table to rows"
assert rows_by_table([]) == {}, "an empty lookup"
assert isinstance(rows_by_table(RECORDS), dict), "a dict comprehension, not a list of pairs"

assert distinct_statuses(RECORDS) == ["failed", "ok"], "two distinct statuses, sorted"
assert distinct_statuses([]) == [], "no statuses"
assert distinct_statuses([{"table": "a", "rows": 1, "status": "ok"}, {"table": "b", "rows": 1, "status": "ok"}]) == ["ok"], "the repeat collapses"
assert isinstance(distinct_statuses(RECORDS), list), "sorted() gives a list back, which is what makes this assertable"

assert flatten([["a", "b"], ["c"]]) == ["a", "b", "c"], "two batches become one list"
assert flatten([]) == [], "no batches"
assert flatten([[], []]) == [], "empty batches"
assert flatten([["a"]]) == ["a"], "one batch, one id"
assert flatten([["a", "b"], [], ["c", "d"]]) == ["a", "b", "c", "d"], "an empty batch in the middle contributes nothing"

assert total_rows(RECORDS) == 1890, "the rows summed"
assert total_rows([]) == 0, "sum of nothing is 0, not an error"
assert total_rows([{"table": "a", "rows": 7, "status": "ok"}]) == 7, "one record"

assert list(lazy_names(RECORDS)) == ["orders", "events", "users"], "walking the generator gives the names"
assert not isinstance(lazy_names(RECORDS), list), "return a generator, not a list — the brackets decide"
assert list(lazy_names([])) == [], "an empty generator"

WALKED_ONCE = lazy_names(RECORDS)
FIRST_WALK = list(WALKED_ONCE)
SECOND_WALK = list(WALKED_ONCE)

assert FIRST_WALK == ["orders", "events", "users"], "the first walk gets everything"
assert SECOND_WALK == [], "a generator is single-use — the second walk gets nothing"
