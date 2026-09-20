assert Partition("orders", "2026-01-04").table == "orders", "__init__ was generated from the fields"
assert Partition("orders", "2026-01-04").date == "2026-01-04", "both declared fields"
assert Partition("orders", "2026-01-04").rows == 0, "a field default"
assert Partition("orders", "2026-01-04").tags == [], "and a default_factory"
assert Partition("orders", "2026-01-04", 50).rows == 50, "defaults can be overridden positionally"
assert Partition("orders", "2026-01-04", rows=50).rows == 50, "or by keyword"

assert repr(Partition("orders", "2026-01-04")) == "Partition(table='orders', date='2026-01-04', rows=0, tags=[])", "__repr__ was generated too"
assert Partition("orders", "d", 1) == Partition("orders", "d", 1), "__eq__ compares field by field"
assert (Partition("orders", "d", 1) == Partition("orders", "d", 2)) is False, "a differing field means not equal"

assert Partition("ORDERS", "d").table == "orders", "__post_init__ normalised the name after __init__ ran"
assert Partition("Orders", "d").table == "orders", "mixed case too"

FIRST = Partition("orders", "d")
SECOND = Partition("events", "d")
FIRST.tags.append("daily")

assert FIRST.tags == ["daily"], "the tag landed here"
assert SECOND.tags == [], "and NOT on the other — that is what default_factory prevents"

assert sorted([Partition("b", "d"), Partition("a", "d")])[0].table == "a", "order=True generates < , so sorting works"
assert (Partition("a", "d") < Partition("b", "d")) is True, "fields are compared in declaration order"
assert (Partition("a", "2026-01-05") < Partition("a", "2026-01-04")) is False, "then by the next field along"

assert PartitionKey("orders", "2026-01-04") == PartitionKey("orders", "2026-01-04"), "frozen records still compare by value"
assert {PartitionKey("orders", "d"): 5}[PartitionKey("orders", "d")] == 5, "frozen=True makes it hashable, so it works as a key"

try:
  PartitionKey("orders", "d").table = "events"
except Exception as exc:
  FROZEN = type(exc).__name__
else:
  FROZEN = "assignment allowed"

assert FROZEN == "FrozenInstanceError", "a frozen dataclass refuses assignment after construction"

assert as_record(Partition("orders", "2026-01-04", 5)) == {"table": "orders", "date": "2026-01-04", "rows": 5, "tags": []}, "asdict gives a plain dict"
assert isinstance(as_record(Partition("o", "d")), dict), "a real dict, ready to serialise"

ORIGINAL = Partition("orders", "2026-01-04", 5)
UPDATED = with_rows(ORIGINAL, 99)

assert UPDATED.rows == 99, "replace builds a copy with the change applied"
assert UPDATED.table == "orders", "carrying every other field over"
assert ORIGINAL.rows == 5, "and leaving the original alone"
