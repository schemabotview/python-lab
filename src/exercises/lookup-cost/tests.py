ROWS = ["orders", "secrets", "events", "temp", "users"]
ALLOW = ["orders", "events", "users"]

assert scan_allowed(ROWS, ALLOW)[0] == ["orders", "events", "users"], "the scan keeps the allowed rows"
assert hashed_allowed(ROWS, ALLOW)[0] == ["orders", "events", "users"], "and so does the hash — same answer, both ways"
assert scan_allowed(ROWS, ALLOW)[0] == hashed_allowed(ROWS, ALLOW)[0], "the two approaches never disagree"

assert hashed_allowed(ROWS, ALLOW)[1] == 5, "one probe per row — five rows, five steps"
assert hashed_allowed(ROWS, ALLOW * 100)[1] == 5, "a 300-entry allowlist costs exactly the same"
assert scan_allowed(ROWS, ALLOW)[1] > hashed_allowed(ROWS, ALLOW)[1], "the scan already costs more on five rows"
assert scan_allowed(ROWS, ALLOW * 100)[1] == 606, "the scan grows with the allowlist — 606 steps for the same five rows"

assert scan_allowed([], ALLOW) == ([], 0), "no rows, no steps"
assert hashed_allowed([], ALLOW) == ([], 0), "likewise"
assert scan_allowed(ROWS, []) == ([], 0), "an empty allowlist keeps nothing and compares nothing"
assert hashed_allowed(ROWS, [])[0] == [], "nothing is allowed"
assert hashed_allowed(ROWS, [])[1] == 5, "but each row is still probed once"

assert scan_allowed(["orders"], ["orders", "x", "y"])[1] == 1, "the scan stops at the first match"
assert scan_allowed(["y"], ["orders", "x", "y"])[1] == 3, "and walks the whole list when the match is last"
assert scan_allowed(["zzz"], ["orders", "x", "y"])[1] == 3, "or when there is no match at all"

assert first_duplicate_naive(["a", "b", "a"])[0] == "a", "the first repeat"
assert first_duplicate_fast(["a", "b", "a"])[0] == "a", "found the same way"
assert first_duplicate_naive(["a", "b", "c"])[0] is None, "no repeats"
assert first_duplicate_fast(["a", "b", "c"])[0] is None, "likewise"
assert first_duplicate_fast([])[0] is None, "nothing at all"

CLEAN = [str(n) for n in range(200)]

assert first_duplicate_fast(CLEAN)[1] == 200, "one step per value — linear"
assert first_duplicate_naive(CLEAN)[1] == 19900, "every pair compared — that is 200 * 199 / 2"
assert first_duplicate_naive(CLEAN)[1] > first_duplicate_fast(CLEAN)[1] * 90, "nearly a hundred times the work, for the same answer"

DOUBLED = [str(n) for n in range(400)]

assert first_duplicate_fast(DOUBLED)[1] == 400, "twice the values, twice the steps — that is what linear means"
assert first_duplicate_naive(DOUBLED)[1] == 79800, "twice the values, FOUR times the steps — that is what quadratic means"
assert first_duplicate_naive(DOUBLED)[1] == first_duplicate_naive(CLEAN)[1] * 4 + 200, "the quadratic term dominates as n grows"
