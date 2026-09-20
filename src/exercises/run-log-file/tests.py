LOG = "/tmp/lab/run.log"

import os
os.makedirs("/tmp/lab", exist_ok=True)

assert write_log(LOG, ["INFO started", "INFO loading"]) == 2, "two lines written"
assert read_all(LOG) == "INFO started\nINFO loading\n", "each line got its own newline"
assert count_lines(LOG) == 2, "two lines counted"

assert write_log(LOG, ["INFO again"]) == 1, "writing again"
assert read_all(LOG) == "INFO again\n", "\"w\" TRUNCATES — the previous two lines are gone"
assert count_lines(LOG) == 1, "only the new line remains"

assert append_log(LOG, "WARN slow") == "WARN slow", "append returns the line"
assert read_all(LOG) == "INFO again\nWARN slow\n", "\"a\" adds instead of wiping"
assert count_lines(LOG) == 2, "two lines now"

assert write_log(LOG, []) == 0, "writing no lines"
assert read_all(LOG) == "", "leaves an empty file, not a missing one"
assert count_lines(LOG) == 0, "and nothing to count"

write_log(LOG, ["INFO started", "WARN slow", "ERROR disk full", "ERROR second"])

assert count_lines(LOG) == 4, "four lines"
assert first_error(LOG) == "ERROR disk full", "the FIRST error, with its newline stripped"
assert "\n" not in first_error(LOG), "the trailing newline is not part of the line"

write_log(LOG, ["INFO all fine"])

assert first_error(LOG) == "", "no error in the file"

write_log(LOG, ["ERROR at the very top"])

assert first_error(LOG) == "ERROR at the very top", "an error on the first line"

write_log(LOG, [])

assert first_error(LOG) == "", "an empty file has no error"

write_log(LOG, ["line with, a comma", "line with \"quotes\""])

assert count_lines(LOG) == 2, "punctuation is just text to a plain file"
assert read_all(LOG).splitlines()[1] == 'line with "quotes"', "and nothing is escaped on the way in or out"
