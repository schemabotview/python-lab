assert len(run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()) == 6, "six summary lines"
assert run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()[0] == "Runs: 9", "nine runs counted"
assert run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()[1] == "Total: 180m", "the accumulated total"
assert run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()[2] == "Average: 20.0m", "total divided by count, one decimal"
assert run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()[3] == "Fastest: 8m", "the smallest runtime"
assert run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()[4] == "Slowest: 30m", "the largest runtime"
assert run_stats([15, 22, 19, 30, 8, 25, 19, 30, 12], 25).splitlines()[5] == "Over SLA: 2", "two runs beat 25m — the two 30s"

assert run_stats([7], 25).splitlines()[3] == "Fastest: 7m", "one run is both the fastest and the slowest"
assert run_stats([7], 25).splitlines()[4] == "Slowest: 7m", "and the slowest"
assert run_stats([40, 50], 25).splitlines()[3] == "Fastest: 40m", "a 0-seeded fastest would report 0 here"
assert run_stats([40, 50], 25).splitlines()[5] == "Over SLA: 2", "both are over"
assert run_stats([25, 25], 25).splitlines()[5] == "Over SLA: 0", "exactly the SLA is not over it"
assert run_stats([3, 4], 25).splitlines()[2] == "Average: 3.5m", "the average keeps its decimal"

assert run_stats([], 25).splitlines()[0] == "Runs: 0", "an empty night"
assert run_stats([], 25).splitlines()[1] == "Total: 0m", "nothing to total"
assert run_stats([], 25).splitlines()[2] == "Average: 0.0m", "no division by zero"
assert run_stats([], 25).splitlines()[3] == "Fastest: 0m", "nothing ran"
assert run_stats([], 25).splitlines()[4] == "Slowest: 0m", "nothing ran"

assert table_report(["orders", "customers", "events"], [15, 22, 19]).splitlines()[0] == "1. orders 15m", "numbering starts at 1"
assert table_report(["orders", "customers", "events"], [15, 22, 19]).splitlines()[1] == "2. customers 22m", "the second pair"
assert table_report(["orders", "customers", "events"], [15, 22, 19]).splitlines()[2] == "3. events 19m", "the third pair"
assert len(table_report(["a"], [1]).splitlines()) == 1, "one table, one line"
assert table_report([], []) == "", "nothing scheduled, nothing reported"

assert locate(["orders", "events"], "events") == "events at position 1", "found at index 1"
assert locate(["orders", "events"], "orders") == "orders at position 0", "found at index 0"
assert locate(["orders"], "payments") == "payments not scheduled", "the loop finished without finding it"
assert locate([], "orders") == "orders not scheduled", "an empty schedule finds nothing"

assert first_breach([15, 22, 19, 30, 8], 25) == 3, "the 30 at index 3 is the first over"
assert first_breach([30, 8], 25) == 0, "a breach on the very first run"
assert first_breach([15, 22, 19], 25) == -1, "every run inside the SLA"
assert first_breach([], 25) == -1, "nothing ran, so nothing breached"
assert first_breach([25, 26], 25) == 1, "exactly the SLA is not a breach, 26 is"

assert drain(["ok:orders", "retry:events", "ok:users", "fatal:disk", "ok:never", "END"]) == ["orders", "users"], "retries skipped, everything behind the fatal abandoned"
assert drain(["END"]) == [], "an empty queue"
assert drain(["ok:a", "ok:b", "END"]) == ["a", "b"], "a clean run processes everything"
assert drain(["fatal:disk", "ok:a", "END"]) == [], "a fatal on the first item stops it there"
assert drain(["retry:a", "retry:b", "END"]) == [], "everything skipped"

QUEUE = ["ok:orders", "END"]

assert drain(QUEUE) == ["orders"], "the queue drains"
assert QUEUE == ["ok:orders", "END"], "work on a copy — the caller's queue must survive"
