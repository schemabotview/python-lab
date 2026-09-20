assert drift(["id", "name", "email", "phone"], ["id", "name", "nickname"]).splitlines()[0] == "Missing: ['email', 'phone']", "expected but absent"
assert drift(["id", "name", "email", "phone"], ["id", "name", "nickname"]).splitlines()[1] == "Unexpected: ['nickname']", "arrived but not wanted — the difference the other way round"
assert drift(["id", "name", "email", "phone"], ["id", "name", "nickname"]).splitlines()[2] == "Shared: ['id', 'name']", "in both"
assert drift(["id"], ["id"]).splitlines()[0] == "Missing: []", "a clean match misses nothing"
assert drift(["id"], ["id"]).splitlines()[1] == "Unexpected: []", "and has nothing spare"
assert drift([], []).splitlines()[2] == "Shared: []", "two empty schemas"
assert drift(["a"], []).splitlines()[0] == "Missing: ['a']", "nothing arrived at all"
assert drift([], ["a"]).splitlines()[1] == "Unexpected: ['a']", "a column nobody asked for"
assert drift(["b", "a"], ["a"]).splitlines()[2] == "Shared: ['a']", "the result is sorted, not in the order given"
assert drift(["id", "id"], ["id"]).splitlines()[0] == "Missing: []", "a column named twice is still one column"

assert all_columns(["id", "name"], ["id", "email"]) == ["email", "id", "name"], "the union, sorted"
assert all_columns(["b"], ["a"], ["c"]) == ["a", "b", "c"], "any number of schemas"
assert all_columns(["a"]) == ["a"], "one schema"
assert all_columns() == [], "no schemas at all"
assert all_columns(["a", "a"], ["a"]) == ["a"], "duplicates collapse"

assert is_compatible(["id"], ["id", "extra"]) is True, "extra columns are fine"
assert is_compatible(["id", "x"], ["id"]) is False, "a missing column is not"
assert is_compatible([], ["anything"]) is True, "needing nothing is always satisfied"
assert is_compatible(["id"], []) is False, "nothing arrived"
assert is_compatible(["a", "b"], ["b", "a"]) is True, "order is irrelevant to a set"

assert changed_columns(["a", "b"], ["b", "c"]) == ["a", "c"], "a was dropped, c was added"
assert changed_columns(["a"], ["a"]) == [], "nothing changed"
assert changed_columns([], ["a"]) == ["a"], "everything is new"
assert changed_columns(["a"], []) == ["a"], "everything was dropped"

assert unique_tables(["orders", "events", "orders"]) == ["events", "orders"], "distinct names, sorted"
assert unique_tables([]) == [], "no rows"
assert unique_tables(["z", "a", "z"]) == ["a", "z"], "sorted, not in first-seen order"

assert freeze(["b", "a"]) == frozenset({"a", "b"}), "the same members, frozen"
assert isinstance(freeze(["a"]), frozenset), "a frozenset, not a set"
assert {freeze(["a", "b"]): "orders"}[freeze(["b", "a"])] == "orders", "order doesn't change the key — a set is a set"

try:
  {set(["a"]): 1}
except TypeError:
  WHY_FROZEN = "unhashable"
else:
  WHY_FROZEN = "a set worked as a key"

assert WHY_FROZEN == "unhashable", "a plain set cannot be a dict key — that is what frozenset is for"
