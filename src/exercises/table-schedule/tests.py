assert clean_schedule(["orders", "events", "orders", "users", "", "sessions", "events", "customers"]) == ["customers", "events", "orders", "sessions", "users"], "sorted, with the blank and the duplicates gone"
assert clean_schedule(["b", "a"]) == ["a", "b"], "already clean, just sorted"
assert clean_schedule([]) == [], "an empty schedule"
assert clean_schedule(["", "", "orders"]) == ["orders"], "several blanks all go — .remove() only takes the first"
assert clean_schedule(["orders", "orders", "orders"]) == ["orders"], "one table, however many times it was typed"

RAW = ["orders", "", "orders"]

assert clean_schedule(RAW) == ["orders"], "the schedule is cleaned"
assert RAW == ["orders", "", "orders"], "work on a copy — the caller's list must survive"

assert slice_report(["customers", "events", "orders", "sessions", "users"]).splitlines()[0] == "First three: ['customers', 'events', 'orders']", "tables[:3]"
assert slice_report(["customers", "events", "orders", "sessions", "users"]).splitlines()[1] == "Last two: ['sessions', 'users']", "a negative start counts from the end"
assert slice_report(["customers", "events", "orders", "sessions", "users"]).splitlines()[2] == "Every other: ['customers', 'orders', 'users']", "a step of 2 takes indices 0, 2, 4"
assert slice_report(["customers", "events", "orders", "sessions", "users"]).splitlines()[3] == "Reversed: ['users', 'sessions', 'orders', 'events', 'customers']", "a step of -1 walks backwards"
assert slice_report(["a"]).splitlines()[0] == "First three: ['a']", "asking for more than there is does not raise"
assert slice_report(["a"]).splitlines()[1] == "Last two: ['a']", "nor does asking for the last two of one"
assert slice_report([]).splitlines()[0] == "First three: []", "slicing an empty list is still fine"

assert replace_window(["a", "b", "c", "d", "e"], 1, 3, ["X"]) == ["a", "X", "d", "e"], "two tables replaced by one"
assert replace_window(["a", "b", "c"], 0, 1, ["X", "Y"]) == ["X", "Y", "b", "c"], "one replaced by two — the list grows"
assert replace_window(["a", "b", "c"], 1, 2, []) == ["a", "c"], "an empty replacement deletes the window"
assert replace_window(["a", "b"], 0, 2, ["Z"]) == ["Z"], "the whole list replaced"

WINDOW = ["a", "b", "c"]

assert replace_window(WINDOW, 0, 1, ["X"]) == ["X", "b", "c"], "the window is replaced"
assert WINDOW == ["a", "b", "c"], "slice assignment mutates — so it must happen on a copy"

assert promote(["a", "b", "c"], "c") == ["c", "a", "b"], "the last table moves to the front"
assert promote(["a", "b", "c"], "a") == ["a", "b", "c"], "promoting the first changes nothing"
assert promote(["a", "b"], "b") == ["b", "a"], "a two-table schedule"

ORDER = ["a", "b", "c"]

assert promote(ORDER, "b") == ["b", "a", "c"], "b runs first"
assert ORDER == ["a", "b", "c"], "the caller's run order is untouched"

assert batch_summary([["orders", 1500], ["events", 300], ["users", 90]]).splitlines()[0] == "Tables: 3", "three batches"
assert batch_summary([["orders", 1500], ["events", 300], ["users", 90]]).splitlines()[1] == "Rows: 1890", "the rows totalled across the nested lists"
assert batch_summary([["orders", 1500], ["events", 300], ["users", 90]]).splitlines()[2] == "Largest: orders", "the name beside the biggest count"
assert batch_summary([["a", 5], ["b", 900]]).splitlines()[2] == "Largest: b", "the biggest is not always first"
assert batch_summary([["a", 0]]).splitlines()[2] == "Largest: a", "one batch is its own largest, even at zero rows"
assert batch_summary([]).splitlines()[0] == "Tables: 0", "no batches"
assert batch_summary([]).splitlines()[1] == "Rows: 0", "nothing to total"
assert batch_summary([]).splitlines()[2] == "Largest: none", "and nothing to name"

ORIGINAL = ["orders", "events"]
COPY = snapshot(ORIGINAL)
ORIGINAL.append("users")

assert COPY == ["orders", "events"], "a real copy — `copy = tables` would show 'users' here too"
assert ORIGINAL == ["orders", "events", "users"], "and the original did change"
assert snapshot([]) == [], "copying an empty list"
