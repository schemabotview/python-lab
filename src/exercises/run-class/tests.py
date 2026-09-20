assert PipelineRun("orders").table == "orders", "__init__ stores the table on the instance"
assert PipelineRun("orders").rows == 0, "rows defaults to 0"
assert PipelineRun("orders", 50).rows == 50, "or comes from the argument"
assert PipelineRun("orders").status == "pending", "a fresh run has not gone anywhere yet"

FIRST = PipelineRun("orders")
SECOND = PipelineRun("events")
FIRST.load(100)

assert FIRST.rows == 100, "the first run took the rows"
assert SECOND.rows == 0, "every object owns its own state — the second is untouched"
assert FIRST.table == "orders" and SECOND.table == "events", "and its own table"

assert PipelineRun("orders").load(100) == "loaded", "a normal load"
assert PipelineRun("orders").load(-5) == "rejected", "the method guards the rule, it doesn't just store"

GUARDED = PipelineRun("orders", 10)
GUARDED.load(-5)

assert GUARDED.rows == 10, "a rejected load changes nothing"
assert GUARDED.status == "pending", "and leaves the status alone"

LOADED = PipelineRun("orders")
LOADED.load(7)

assert LOADED.status == "loaded", "a successful load updates the status"
assert LOADED.load(3) == "loaded" and LOADED.rows == 10, "rows accumulate across loads"

FAILED = PipelineRun("events")

assert FAILED.fail("timeout") == "failed: timeout", "fail reports the reason"
assert FAILED.status == "failed: timeout", "and remembers it on self"

BEFORE = PipelineRun.runs_started
PipelineRun("a")
PipelineRun("b")

assert PipelineRun.runs_started == BEFORE + 2, "the counter is a CLASS attribute, shared by every instance"
assert PipelineRun("c").runs_started == PipelineRun.runs_started, "an instance reads the same shared value"

assert repr(PipelineRun("orders", 5)) == "PipelineRun(orders, 5)", "__repr__ names the object, not its address"
assert "0x" not in repr(PipelineRun("orders")), "the default repr would print a memory address"

assert PipelineRun.from_dict({"table": "orders", "rows": 42}).table == "orders", "the alternate constructor"
assert PipelineRun.from_dict({"table": "orders", "rows": 42}).rows == 42, "and it carries the rows over"
assert PipelineRun.from_dict({"table": "orders"}).rows == 0, "a missing rows key falls back to the default"
assert isinstance(PipelineRun.from_dict({"table": "o"}), PipelineRun), "a classmethod returns a real instance"
