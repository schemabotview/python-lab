assert Budget(100).limit == 100, "read the limit with no parentheses — the getter runs"
assert Budget(100).spent == 0.0, "nothing spent yet"
assert Budget(100).remaining == 100, "computed from limit and spent"
assert Budget(100).exhausted is False, "a fresh budget is not exhausted"

SPENDING = Budget(100)

assert SPENDING.spend(30) == "approved", "within budget"
assert SPENDING.spent == 30, "the spend was recorded"
assert SPENDING.remaining == 70, "remaining recomputes on every read — it is never stored"
assert SPENDING.spend(70) == "approved", "spending exactly the remainder is allowed"
assert SPENDING.remaining == 0, "nothing left"
assert SPENDING.exhausted is True, "and now it is exhausted"
assert SPENDING.spend(1) == "denied", "one more is refused"
assert SPENDING.spent == 100, "and a denied spend changes nothing"

RAISED = Budget(100)
RAISED.limit = 500

assert RAISED.limit == 500, "the setter accepted a valid write"
assert RAISED.remaining == 500, "and remaining followed it, because it is computed"

try:
  Budget(100).limit = -1
except ValueError as exc:
  NEGATIVE = str(exc)
else:
  NEGATIVE = "accepted"

assert NEGATIVE == "limit cannot be negative", "the setter rejects a bad value BEFORE it is stored"

GUARDED = Budget(100)
GUARDED.spend(80)

try:
  GUARDED.limit = 50
except ValueError as exc:
  TOO_LOW = str(exc)
else:
  TOO_LOW = "accepted"

assert TOO_LOW == "limit cannot be below what is already spent", "the setter can check against other state too"
assert GUARDED.limit == 100, "and the old value survived the rejected write"

try:
  Budget(100).remaining = 50
except AttributeError:
  READ_ONLY = "refused"
else:
  READ_ONLY = "assignment allowed"

assert READ_ONLY == "refused", "a property with no setter is read-only"

try:
  Budget(100).spent = 999
except AttributeError:
  SPENT_LOCKED = "refused"
else:
  SPENT_LOCKED = "assignment allowed"

assert SPENT_LOCKED == "refused", "spent moves only through spend()"
assert Budget(100)._limit == 100, "the underscore name is the real storage — reachable, but marked internal"
