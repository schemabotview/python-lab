import logging

SINK = []
LOG = make_logger("lab.debug", logging.DEBUG, SINK)
log_run(LOG, "orders", 1500)

assert SINK == ["INFO loaded 1500 rows into orders"], "the format string is filled in by the logger"

SINK.clear()
log_slow(LOG, "events", 90)
log_failure(LOG, "users", "timeout")

assert SINK == ["WARNING events took 90s", "ERROR users failed: timeout"], "each level is stamped on its line"

QUIET = []
PROD = make_logger("lab.prod", logging.WARNING, QUIET)
log_run(PROD, "orders", 1500)

assert QUIET == [], "INFO is below the WARNING threshold, so it is not emitted at all"

log_slow(PROD, "events", 90)

assert QUIET == ["WARNING events took 90s"], "WARNING is at the threshold, so it passes"

log_failure(PROD, "users", "timeout")

assert QUIET == ["WARNING events took 90s", "ERROR users failed: timeout"], "and ERROR is above it"
assert len(QUIET) == 2, "the INFO call is still missing — the same code, a different threshold"

LOUD = []
DEV = make_logger("lab.dev", logging.DEBUG, LOUD)
log_run(DEV, "orders", 1500)

assert LOUD == ["INFO loaded 1500 rows into orders"], "the SAME call now emits, because the threshold moved — no code changed"

CRASH = []
CRASHY = make_logger("lab.crash", logging.DEBUG, CRASH)
try:
  1 / 0
except ZeroDivisionError:
  log_crash(CRASHY, "orders")

assert CRASH[0].startswith("ERROR orders crashed"), "exception() logs at ERROR level"
assert "ZeroDivisionError" in CRASH[0], "and appends the traceback, which is the whole reason to use it"
assert "Traceback" in CRASH[0], "the full traceback, not just the message"


class Explodes:
  def __str__(self):
    raise AssertionError("formatted a message that was never emitted")


BELOW = []
THRESHOLD = make_logger("lab.lazy", logging.WARNING, BELOW)
THRESHOLD.info("this argument is %s", Explodes())

assert BELOW == [], "nothing emitted — and the argument was never formatted, or its __str__ would have raised on the line above"
