NAMES = ["orders", "events", "orders", "users", "orders", "events"]

assert top_tables(NAMES, 2) == [("orders", 3), ("events", 2)], "the two busiest, with their counts"
assert top_tables(NAMES, 1) == [("orders", 3)], "just the busiest"
assert len(top_tables(NAMES, 10)) == 3, "asking for more than there are gives what there is"
assert top_tables([], 3) == [], "nothing loaded"

assert tally(NAMES) == {"orders": 3, "events": 2, "users": 1}, "every table counted"
assert tally([]) == {}, "an empty tally"
assert tally(["a"]) == {"a": 1}, "a single name"

assert group_rows([("orders", "r1"), ("events", "e1"), ("orders", "r2")]) == {"orders": ["r1", "r2"], "events": ["e1"]}, "rows collected under their table"
assert group_rows([]) == {}, "nothing to group"
assert group_rows([("a", "1")]) == {"a": ["1"]}, "one pair"

assert recent(["a", "b", "c", "d"], 2) == ["c", "d"], "maxlen drops from the left as new items arrive"
assert recent(["a"], 3) == ["a"], "fewer events than the window holds"
assert recent([], 3) == [], "no events"
assert recent(["a", "b", "c"], 1) == ["c"], "a window of one keeps only the newest"

assert as_queue(["a", "b", "c"]) == ["a", "b", "c"], "first in, first out"
assert as_queue([]) == [], "an empty queue"
assert as_queue(["only"]) == ["only"], "one item"

assert Run("orders", 1500, "ok").table == "orders", "fields are reachable by name"
assert Run("orders", 1500, "ok").rows == 1500, "which is the whole point over a plain tuple"
assert summarise(Run("orders", 1500, "ok")) == "orders: 1500 rows (ok)", "and it reads like a record"

assert Run("orders", 1500, "ok")[0] == "orders", "it is still a tuple, so indexing works"
assert tuple(Run("a", 1, "ok")) == ("a", 1, "ok"), "and it unpacks like one"
assert Run("a", 1, "ok") == ("a", 1, "ok"), "it even compares equal to the plain tuple"

TABLE, ROWS, STATUS = Run("orders", 1500, "ok")

assert (TABLE, ROWS, STATUS) == ("orders", 1500, "ok"), "so it unpacks into names at the call site"

try:
  Run("orders", 1500, "ok").rows = 5
except AttributeError:
  IMMUTABLE = "refused"
else:
  IMMUTABLE = "assigned"

assert IMMUTABLE == "refused", "a namedtuple is immutable, like the tuple it is"
