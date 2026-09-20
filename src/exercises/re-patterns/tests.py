LINE_TEXT = "2026-01-04T02:15 INFO orders loaded"

assert find_level(LINE_TEXT) == "INFO", "the level token"
assert find_level("2026-01-04T02:15 ERROR events failed") == "ERROR", "a different level"
assert find_level("nonsense") == "", "a line that doesn't match gives empty, not a crash"
assert find_level("") == "", "an empty line"

assert parse_line(LINE_TEXT) == ("2026-01-04T02:15", "INFO", "orders"), "three named groups pulled out at once"
assert parse_line("nonsense") == ("", "", ""), "no match, three empties"
assert parse_line("2026-01-05T00:00 WARN users slow")[2] == "users", "the table group"

assert all_tables("table=orders rows=5 table=events rows=3") == ["orders", "events"], "findall returns every capture, in order"
assert all_tables("nothing here") == [], "no matches at all"
assert all_tables("table=orders") == ["orders"], "a single match"

assert redact("host=db password=hunter2 port=5432") == "host=db password=*** port=5432", "the secret is replaced, the rest is left alone"
assert redact("password=a password=bbbb") == "password=*** password=***", "every occurrence, whatever its length"
assert redact("nothing to hide") == "nothing to hide", "no match, no change"

assert split_fields("a b  c") == ["a", "b", "c"], "a run of spaces is one separator"
assert split_fields("a;b;;c") == ["a", "b", "c"], "so is a run of semicolons"
assert split_fields("a; b ;c") == ["a", "b", "c"], "and a mixture"
assert split_fields("  padded  ") == ["padded"], "the strip keeps the edges from producing empties"

assert row_counts("rows=1500 rows=300") == [1500, 300], "captures converted to integers"
assert row_counts("rows=0") == [0], "zero counts"
assert row_counts("rows=abc") == [], "\\d+ does not match letters, so nothing is captured"
assert row_counts("") == [], "nothing at all"

assert LINE.search(LINE_TEXT).group("table") == "orders", "a compiled pattern is reusable"
assert LINE.search(LINE_TEXT).group(0) == "2026-01-04T02:15 INFO orders", "group 0 is the whole match"
assert LINE.search(LINE_TEXT).group(1) == "2026-01-04T02:15", "groups are numbered as well as named"

import re

assert re.match(r"orders", "the orders table") is None, "match() is anchored at the START and finds nothing here"
assert re.search(r"orders", "the orders table") is not None, "search() looks anywhere"
assert len(r"\d") == 2, "a raw string keeps the backslash — it is two characters, not an escape"
