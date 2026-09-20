SORTED = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

assert binary_search(SORTED, 23) == 5, "found in the middle-right"
assert binary_search(SORTED, 2) == 0, "the first value"
assert binary_search(SORTED, 91) == 9, "the last value"
assert binary_search(SORTED, 4) == -1, "a value that isn't there"
assert binary_search(SORTED, 100) == -1, "past the end"
assert binary_search(SORTED, 0) == -1, "before the start"
assert binary_search([], 5) == -1, "an empty list"
assert binary_search([7], 7) == 0, "a single match"
assert binary_search([7], 8) == -1, "a single miss"

BIG = list(range(1000))

assert binary_search(BIG, 999) == 999, "the last of a thousand"
assert probes(BIG, 999) <= 10, "ten probes or fewer for a thousand values — that is log2(1000)"
assert probes(BIG, 0) <= 10, "wherever it sits"
assert probes(BIG, 12345) <= 10, "and even when it is absent"

HUGE = list(range(1000000))

assert probes(HUGE, 999999) <= 20, "a thousand times more data costs only ten more probes"
assert probes(HUGE, 999999) < probes(BIG, 999) * 3, "doubling the data adds ONE probe, not double the work"

REPEATED = [1, 3, 3, 3, 5, 5, 9]

assert first_index(REPEATED, 3) == 1, "the leftmost 3"
assert last_index(REPEATED, 3) == 3, "the rightmost 3"
assert first_index(REPEATED, 5) == 4, "leftmost 5"
assert last_index(REPEATED, 5) == 5, "rightmost 5"
assert first_index(REPEATED, 9) == 6, "a value appearing once"
assert last_index(REPEATED, 9) == 6, "is its own first and last"
assert first_index(REPEATED, 4) == -1, "absent"
assert last_index(REPEATED, 4) == -1, "absent the other way too"
assert first_index([], 1) == -1, "empty"

assert insert_point(SORTED, 4) == 1, "4 belongs between 2 and 5"
assert insert_point(SORTED, 1) == 0, "before everything"
assert insert_point(SORTED, 100) == 10, "after everything"
assert insert_point([], 5) == 0, "into an empty list"
assert insert_point(REPEATED, 3) == 1, "at the left of an existing run"

DATES = ["2026-01-01", "2026-01-04", "2026-01-05", "2026-01-09", "2026-01-11"]

assert partition_range(DATES, "2026-01-04", "2026-01-10") == ["2026-01-04", "2026-01-05", "2026-01-09"], "the end is excluded, the start included"
assert partition_range(DATES, "2026-01-01", "2026-01-01") == [], "an empty range"
assert partition_range(DATES, "2026-01-02", "2026-01-03") == [], "a range that spans no dates"
assert partition_range(DATES, "2025-01-01", "2027-01-01") == DATES, "a range covering everything"
assert partition_range([], "a", "z") == [], "no dates at all"
