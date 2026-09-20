assert parse_partition("year=2026/month=01/day=04") == ("2026", "01", "04"), "the three partition values"
assert isinstance(parse_partition("year=2026"), tuple), "return a tuple, not a list"
assert parse_partition("year=2026") == ("2026",), "one level — and it still needs the trailing comma to be a tuple"
assert parse_partition("table=orders/date=2026-01-04") == ("orders", "2026-01-04"), "a date value keeps its own dashes"
assert parse_partition("year=2026/month=01/day=04")[1] == "01", "values stay strings — 01 is a name, not the number 1"

assert partition_key({"table": "orders", "year": 2026, "month": 1}) == ("orders", 2026, 1), "table, year, month in that order"
assert isinstance(partition_key({"table": "a", "year": 1, "month": 2}), tuple), "a key must be a tuple"
assert partition_key({"table": "events", "year": 2025, "month": 12, "extra": "ignored"}) == ("events", 2025, 12), "other fields are not part of the key"

assert bounds([15, 22, 8, 30]) == (8, 30, 4), "lowest, highest, count"
assert bounds([7]) == (7, 7, 1), "one value is both bounds"
assert bounds([]) == (0, 0, 0), "nothing to bound"
assert bounds([40, 50]) == (40, 50, 2), "a 0-seeded lowest would report 0 here"
assert bounds([-5, 5]) == (-5, 5, 2), "negatives work the same way"

LOWEST, HIGHEST, COUNT = bounds([15, 22, 8, 30])

assert (LOWEST, HIGHEST, COUNT) == (8, 30, 4), "the three values unpack at the call site"

assert one_item("orders") == ("orders",), "a tuple of length one"
assert len(one_item("orders")) == 1, "one item, not five characters"
assert isinstance(one_item("orders"), tuple), "('orders') without the comma is just the string"
assert one_item(5) == (5,), "any value wraps the same way"

assert rekey(("orders", 2026)) == (2026, "orders"), "the halves swap"
assert rekey((1, 2)) == (2, 1), "numbers too"

assert group_counts([("orders", "2026-01-04"), ("events", "2026-01-04"), ("orders", "2026-01-04")]) == {("orders", "2026-01-04"): 2, ("events", "2026-01-04"): 1}, "two orders rows, one events row"
assert group_counts([]) == {}, "nothing arrived"
assert group_counts([("a", "d")]) == {("a", "d"): 1}, "a single row"
assert list(group_counts([("orders", "2026-01-04")]).keys())[0] == ("orders", "2026-01-04"), "the key really is the tuple"

try:
  {["orders", "2026-01-04"]: 1}
except TypeError:
  WHY_TUPLES = "unhashable"
else:
  WHY_TUPLES = "a list worked as a key"

assert WHY_TUPLES == "unhashable", "a list cannot be a dict key — that is why composite keys are tuples"
