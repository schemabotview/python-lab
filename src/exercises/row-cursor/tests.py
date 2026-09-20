assert list(Cursor(["r1", "r2", "r3"])) == ["r1", "r2", "r3"], "a for loop over your own class, via __iter__ and __next__"
assert list(Cursor([])) == [], "an empty cursor stops immediately"

STEPPED = Cursor(["r1", "r2"])

assert next(STEPPED) == "r1", "next() pulls one value"
assert next(STEPPED) == "r2", "and the cursor remembers where it was"

try:
  next(STEPPED)
except StopIteration:
  EXHAUSTED = "stopped"
else:
  EXHAUSTED = "kept going"

assert EXHAUSTED == "stopped", "past the end, __next__ raises StopIteration — that is how a for loop knows to end"

ONE_SHOT = Cursor(["r1", "r2"])
FIRST_PASS = list(ONE_SHOT)
SECOND_PASS = list(ONE_SHOT)

assert FIRST_PASS == ["r1", "r2"], "the first walk reads everything"
assert SECOND_PASS == [], "a cursor is spent once read — __iter__ returns self, so there is no rewind"

assert manual_walk(["a", "b"]) == ["a", "b"], "a list, walked by hand"
assert manual_walk("hi") == ["h", "i"], "a string is iterable too — the same protocol"
assert manual_walk([]) == [], "nothing to walk"
assert manual_walk({"a": 1, "b": 2}) == ["a", "b"], "iterating a dict gives its keys"
assert manual_walk(Cursor(["r1"])) == ["r1"], "and your own class plugs into the same machinery"
assert manual_walk(range(3)) == [0, 1, 2], "a range produces its values on demand"

assert first_n(["a", "b", "c", "d"], 2) == ["a", "b"], "just the first two"
assert first_n(["a"], 5) == ["a"], "asking for more than there is stops cleanly"
assert first_n([], 3) == [], "nothing there at all"
assert first_n(["a", "b"], 0) == [], "asking for none"

PARTIAL = Cursor(["a", "b", "c"])
first_n(PARTIAL, 1)

assert list(PARTIAL) == ["b", "c"], "only one value was consumed — the rest are still waiting"

assert is_iterable([1, 2]) is True, "a list"
assert is_iterable("text") is True, "a string"
assert is_iterable({"a": 1}) is True, "a dict"
assert is_iterable(Cursor([])) is True, "your own class, because it has __iter__"
assert is_iterable(42) is False, "a number is not iterable"
assert is_iterable(None) is False, "nor is None"
