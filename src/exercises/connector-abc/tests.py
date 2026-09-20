assert PostgresConnector().name() == "postgres", "the concrete subclass supplies name"
assert PostgresConnector().fetch() == [1, 2, 3], "and fetch"
assert PostgresConnector().report() == "postgres: 3 rows", "report is inherited, and calls both abstract methods"
assert EmptyConnector().report() == "empty: 0 rows", "the same inherited report, a different answer"
assert issubclass(PostgresConnector, Connector) is True, "an ABC is nominal — the subclass says so explicitly"

try:
  Connector()
except TypeError:
  ABSTRACT = "refused"
else:
  ABSTRACT = "constructed"

assert ABSTRACT == "refused", "an ABC with abstract methods cannot be instantiated"


class HalfDone(Connector):
  def name(self):
    return "half"


try:
  HalfDone()
except TypeError:
  INCOMPLETE = "refused"
else:
  INCOMPLETE = "constructed"

assert INCOMPLETE == "refused", "a subclass that skipped fetch() is refused too — at construction, not later"


class NotAConnector:
  def fetch(self):
    return ["a"]


assert can_fetch(NotAConnector()) is True, "a Protocol is structural — the right method is enough"
assert issubclass(NotAConnector, Connector) is False, "even though it inherits from nothing"
assert can_fetch(PostgresConnector()) is True, "a real connector matches as well"
assert can_fetch("just a string") is False, "a string has no fetch()"
assert can_fetch(42) is False, "nor does a number"
