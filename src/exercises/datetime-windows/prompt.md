# Run Windows

Schedules, freshness budgets and SLA spans are all arithmetic on points in
time.

| Function | Example |
| --- | --- |
| `parse_stamp(text)` | `"2026-01-04T02:15:00"` → a `datetime` |
| `parse_custom(text)` | `"04/01/2026 02:15"` → a `datetime` |
| `format_stamp(moment)` | → `"2026-01-04 02:15"` |
| `window_end(start, hours)` | shifts a point forward |
| `duration_minutes(start, end)` | the span, in **whole minutes** |
| `is_stale(stamp, now, max_hours)` | older than the budget? |
| `utc_now_is_aware()` | does `datetime.now(timezone.utc)` carry a zone? |

`parse_custom` reads **day/month/year**.

## Notes

- **A point and a span are different types.** A `datetime` is a moment; a
  `timedelta` is a duration. Add a span to a point and you get a point;
  subtract two points and you get a span — and a test pins that the result of
  `end - start` really is a `timedelta`, not a number.
- **`fromisoformat` needs no pattern; anything else does.** ISO 8601 is the
  format to insist on precisely so you never write `%d/%m/%Y` again — and when
  an upstream sends `04/01/2026`, `strptime` is how you cope.
- **The calendar is handled for you.** Tests shift across midnight and across
  the end of February, because arithmetic that looks obvious is where
  hand-rolled date maths goes wrong.
- **`total_seconds()` is the one to use**, not `.seconds`. `.seconds` is the
  *remainder within a day* and silently ignores the days part — so a 30-hour
  span reports as 6 hours.
- **A datetime with no zone is naive**, and Python refuses to compare a naive
  one with an aware one — `TypeError`, which a test pins. That refusal is a
  kindness: the alternative is a silently wrong answer. Prefer
  `datetime.now(timezone.utc)` and stay aware end to end.
