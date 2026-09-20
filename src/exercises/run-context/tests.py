LOG = []
with Transaction(LOG) as txn:
  txn.write("r1")
  txn.write("r2")

assert LOG == ["BEGIN", "WRITE r1", "WRITE r2", "COMMIT"], "a clean block commits"

BOUND = []
with Transaction(BOUND) as txn:
  pass

assert isinstance(txn, Transaction), "__enter__ returns what `as` binds"

FAILED = []
try:
  with Transaction(FAILED) as txn:
    txn.write("r1")
    raise ValueError("bad row")
except ValueError:
  ESCAPED = "propagated"
else:
  ESCAPED = "swallowed"

assert FAILED == ["BEGIN", "WRITE r1", "ROLLBACK ValueError"], "__exit__ runs on the way out even when the block raises"
assert ESCAPED == "propagated", "and a falsy __exit__ lets the exception carry on"

SWALLOWED = []
with Suppressing(SWALLOWED) as txn:
  txn.write("r1")
  raise ValueError("bad row")

assert SWALLOWED == ["BEGIN", "WRITE r1", "ROLLBACK ValueError"], "the cleanup still ran"
assert True, "and execution reached here at all, because __exit__ returned True"


def early_return(log):
  with Transaction(log):
    return "left early"


RETURNED = []

assert early_return(RETURNED) == "left early", "the function returned from inside the block"
assert RETURNED == ["BEGIN", "COMMIT"], "and __exit__ still ran — a return cannot skip it"

STAGE = []
with staged(STAGE, "extract") as name:
  STAGE.append(f"working on {name}")

assert STAGE == ["START extract", "working on EXTRACT", "END extract"], "before the yield is enter, after it is exit"
assert STAGE[1] == "working on EXTRACT", "the yielded value is what `as` binds"

STAGE_FAILED = []
try:
  with staged(STAGE_FAILED, "load"):
    raise RuntimeError("no disk")
except RuntimeError:
  pass

assert STAGE_FAILED == ["START load", "END load"], "the finally around the yield is what guarantees cleanup"

NESTED = []
with staged(NESTED, "outer"):
  with staged(NESTED, "inner"):
    NESTED.append("body")

assert NESTED == ["START outer", "START inner", "body", "END inner", "END outer"], "blocks unwind inside out"
