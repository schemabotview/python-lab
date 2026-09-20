assert two_sum([2, 7, 11, 15], 9) == (0, 1), "2 + 7 == 9"
assert two_sum([3, 2, 4], 6) == (1, 2), "2 + 4 == 6, and not the 3 with itself"
assert two_sum([3, 3], 6) == (0, 1), "two equal values are still two elements"
assert (two_sum([2, 7], 9), two_sum([1, 2, 3], 100)) == ((0, 1), None), "a real pair; and None when nothing matches"
assert (two_sum([2, 7], 9), two_sum([], 0)) == ((0, 1), None), "an empty list has no pair"
assert (two_sum([2, 7], 9), two_sum([3], 6)) == ((0, 1), None), "one element cannot be used twice"
assert two_sum([-3, 4, 1], -2) == (0, 2), "negatives work the same way"
assert two_sum([0, 0], 0) == (0, 1), "zeroes too"

assert two_sum_naive([2, 7, 11, 15], 9)[0] == (0, 1), "the naive version finds the same pair"
assert two_sum_naive([1, 2, 3], 100)[0] is None, "and agrees when there is none"

CLEAN = list(range(200))

assert (two_sum(CLEAN, 397), two_sum(CLEAN, 100000)) == ((198, 199), None), "the largest pair; and None when the target is out of reach"
assert two_sum_naive(CLEAN, 100000)[1] == 19900, "the naive version compared every pair"
assert two_sum_naive(CLEAN, 100000)[0] == two_sum(CLEAN, 100000), "for the same answer the dict got in one pass"

TABLES = [
  ("orders", ["id", "amount"]),
  ("orders_v2", ["amount", "id"]),
  ("events", ["id", "kind"]),
]

assert group_by_schema(TABLES)[frozenset(["id", "amount"])] == ["orders", "orders_v2"], "column ORDER does not change the schema"
assert group_by_schema(TABLES)[frozenset(["id", "kind"])] == ["events"], "a different schema, its own group"
assert len(group_by_schema(TABLES)) == 2, "three tables, two distinct schemas"
assert group_by_schema([]) == {}, "no tables"
assert group_by_schema([("a", [])])[frozenset()] == ["a"], "a table with no columns still gets a key"

assert join_keys(["a", "b", "c"], ["b", "c", "d"]) == ["b", "c"], "the keys on both sides"
assert join_keys(["a"], ["b"]) == [], "nothing in common"
assert join_keys([], ["a"]) == [], "one side empty"
assert join_keys(["a", "a"], ["a"]) == ["a"], "duplicates collapse"

ROWS = [
  {"table": "orders", "id": 1},
  {"table": "events", "id": 2},
  {"table": "orders", "id": 3},
]

assert index_by(ROWS, "table")["orders"] == [{"table": "orders", "id": 1}, {"table": "orders", "id": 3}], "both orders rows, in arrival order"
assert index_by(ROWS, "table")["events"] == [{"table": "events", "id": 2}], "one events row"
assert len(index_by(ROWS, "table")) == 2, "two distinct tables"
assert index_by(ROWS, "id")[1] == [{"table": "orders", "id": 1}], "indexing by a different field"
assert index_by([], "table") == {}, "no rows"
