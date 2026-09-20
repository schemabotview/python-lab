assert parse_line("2026-01-04 02:15:31 info orders loaded=1500 ms=4200").splitlines()[0] == "Date: 2026-01-04", "the date sliced off the front"
assert parse_line("2026-01-04 02:15:31 info orders loaded=1500 ms=4200").splitlines()[1] == "Time: 02:15:31", "the second whitespace-separated part"
assert parse_line("2026-01-04 02:15:31 info orders loaded=1500 ms=4200").splitlines()[2] == "Level: INFO", "reported in capitals however it was written"
assert parse_line("2026-01-04 02:15:31 info orders loaded=1500 ms=4200").splitlines()[3] == "Table: orders", "the fourth part"
assert parse_line("2026-01-04 02:15:31 ERROR events x=1").splitlines()[2] == "Level: ERROR", "already-capital levels are unchanged"
assert parse_line("2026-01-04 02:15:31 warn users x=1").splitlines()[3] == "Table: users", "a different table"

assert normalise("  Order  Total ") == "order_total", "trimmed, lowered, and the double space collapsed to ONE underscore"
assert normalise("ID") == "id", "already one word"
assert normalise("first name") == "first_name", "a single space"
assert normalise("  spaced   out   name ") == "spaced_out_name", "several runs of whitespace"
assert normalise("Total") == "total", "no whitespace at all"
assert normalise("") == "", "an empty header"
assert normalise("   ") == "", "a header that was only whitespace"

assert redact("user=admin password=hunter2", "hunter2") == "user=admin password=***", "the secret is hidden"
assert redact("a hunter2 b hunter2", "hunter2") == "a *** b ***", "every occurrence goes"
assert redact("nothing to hide", "hunter2") == "nothing to hide", "a secret that isn't there changes nothing"

ORIGINAL_LINE = "password=hunter2"
redact(ORIGINAL_LINE, "hunter2")

assert ORIGINAL_LINE == "password=hunter2", "strings are immutable — .replace() returns a new one and leaves this alone"

assert source_kind("s3://bucket/x.csv") == "s3-csv", "on S3 and a csv"
assert source_kind("s3://bucket/x.parquet") == "s3-other", "on S3, not a csv"
assert source_kind("data/x.csv") == "local-csv", "a local csv"
assert source_kind("x.txt") == "unknown", "neither"
assert source_kind("") == "unknown", "an empty path must not raise"
assert source_kind("s3:") == "unknown", "shorter than the prefix, and still fine"

assert field("loaded=1500 ms=4200", "ms") == "4200", "the last field"
assert field("loaded=1500 ms=4200", "loaded") == "1500", "the first field, stopping at the space"
assert field("loaded=1500", "missing") == "", "a key that isn't there"
assert field("", "anything") == "", "an empty line"
assert field("a=1 b= c=3", "b") == "", "a key that is there but has no value"
assert field("a=1", "a") == "1", "the only field, with no trailing space"

assert to_csv([" a ", "b ", "  c"]) == "a,b,c", "each value trimmed, then joined"
assert to_csv(["one"]) == "one", "one value needs no comma"
assert to_csv([]) == "", "nothing to join"
assert to_csv(["  ", "a"]) == ",a", "a value that was only whitespace becomes empty, not dropped"
