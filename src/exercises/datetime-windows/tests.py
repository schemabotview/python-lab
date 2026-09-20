from datetime import datetime, timedelta, timezone

assert parse_stamp("2026-01-04T02:15:00") == datetime(2026, 1, 4, 2, 15), "ISO text parses without a format string"
assert parse_stamp("2026-01-04") == datetime(2026, 1, 4, 0, 0), "a date alone is midnight"
assert parse_stamp("2026-01-04T02:15:00").hour == 2, "and the parts are reachable"

assert parse_custom("04/01/2026 02:15") == datetime(2026, 1, 4, 2, 15), "day/month/year needs an explicit pattern"
assert parse_custom("31/12/2025 23:59") == datetime(2025, 12, 31, 23, 59), "the end of the year"

assert format_stamp(datetime(2026, 1, 4, 2, 15)) == "2026-01-04 02:15", "formatted back out"
assert format_stamp(datetime(2026, 1, 4)) == "2026-01-04 00:00", "midnight is written in full"
assert format_stamp(parse_stamp("2026-01-04T02:15:00")) == "2026-01-04 02:15", "a round trip"

assert window_end(datetime(2026, 1, 4, 2, 0), 6) == datetime(2026, 1, 4, 8, 0), "six hours later"
assert window_end(datetime(2026, 1, 4, 22, 0), 6) == datetime(2026, 1, 5, 4, 0), "crossing midnight is handled for you"
assert window_end(datetime(2026, 1, 4, 2, 0), 0) == datetime(2026, 1, 4, 2, 0), "a zero shift"
assert window_end(datetime(2026, 2, 28, 12, 0), 24) == datetime(2026, 3, 1, 12, 0), "and so is the end of a non-leap February"

assert duration_minutes(datetime(2026, 1, 4, 2, 0), datetime(2026, 1, 4, 3, 30)) == 90, "subtracting two points gives the span"
assert duration_minutes(datetime(2026, 1, 4, 2, 0), datetime(2026, 1, 4, 2, 0)) == 0, "no time passed"
assert duration_minutes(datetime(2026, 1, 4, 23, 0), datetime(2026, 1, 5, 1, 0)) == 120, "across midnight"

assert isinstance(datetime(2026, 1, 4, 3, 0) - datetime(2026, 1, 4, 2, 0), timedelta), "the difference of two datetimes is a duration, not a number"

assert is_stale(datetime(2026, 1, 1), datetime(2026, 1, 4), 24) is True, "three days old, budget one day"
assert is_stale(datetime(2026, 1, 4, 0, 0), datetime(2026, 1, 4, 6, 0), 24) is False, "six hours old, budget one day"
assert is_stale(datetime(2026, 1, 4, 0, 0), datetime(2026, 1, 5, 0, 0), 24) is False, "exactly the budget is not over it"
assert is_stale(datetime(2026, 1, 4, 0, 0), datetime(2026, 1, 5, 0, 1), 24) is True, "one minute past is"

assert utc_now_is_aware() is True, "datetime.now(timezone.utc) carries its zone"
assert datetime(2026, 1, 4).tzinfo is None, "a plain datetime is NAIVE — it has no idea where it is"

try:
  datetime(2026, 1, 4, tzinfo=timezone.utc) - datetime(2026, 1, 4)
except TypeError:
  MIXED = "refused"
else:
  MIXED = "compared"

assert MIXED == "refused", "mixing an aware datetime with a naive one raises — the classic timezone bug"
