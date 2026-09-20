assert repr(Rows(1500)) == "Rows(1500)", "__repr__ is the debug view"
assert str(Rows(1500)) == "1500 rows", "__str__ is the human view — print() reaches for this one"
assert f"{Rows(5)}" == "5 rows", "an f-string uses __str__ too"

assert (Rows(5) == Rows(5)) is True, "two counts of the same size are equal"
assert (Rows(5) == Rows(6)) is False, "different sizes are not"
assert (Rows(5) != Rows(6)) is True, "!= comes free once __eq__ is defined"
assert (Rows(5) == "5") is False, "a Rows is not a string, however it prints"

assert (Rows(5) < Rows(9)) is True, "__lt__ answers <"
assert (Rows(9) < Rows(5)) is False, "and the other way round"
assert (Rows(9) > Rows(5)) is True, "> comes free — Python flips the operands"
assert sorted([Rows(9), Rows(1), Rows(5)]) == [Rows(1), Rows(5), Rows(9)], "sorted() works because it is built on __lt__"
assert max([Rows(1), Rows(9)]) == Rows(9), "so does max()"

assert Rows(5) + Rows(9) == Rows(14), "__add__ answers +"
assert isinstance(Rows(1) + Rows(2), Rows), "and returns a Rows, not a bare number"
assert (Rows(1) + Rows(2)).count == 3, "carrying the total"

assert len(Rows(1500)) == 1500, "__len__ answers len()"
assert len(Rows(0)) == 0, "an empty count"

assert len({Rows(5), Rows(5), Rows(9)}) == 2, "equal objects collapse in a set — which needs BOTH __eq__ and __hash__"
assert {Rows(5): "orders"}[Rows(5)] == "orders", "and a Rows can be a dict key"
assert hash(Rows(5)) == hash(Rows(5)), "equal objects must hash equal, or dicts break"


class CountWithoutHash:
  def __init__(self, count):
    self.count = count

  def __eq__(self, other):
    return self.count == other.count


try:
  {CountWithoutHash(1)}
except TypeError:
  DROPPED = "unhashable"
else:
  DROPPED = "still hashable"

assert DROPPED == "unhashable", "defining __eq__ alone DROPS __hash__ — that is why Rows defines it back"
