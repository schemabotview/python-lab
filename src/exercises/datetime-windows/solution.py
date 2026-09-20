from datetime import datetime, timedelta, timezone


def parse_stamp(text):
  """ISO text in, datetime out."""
  return datetime.fromisoformat(text)


def parse_custom(text):
  """A non-ISO format needs an explicit pattern."""
  return datetime.strptime(text, "%d/%m/%Y %H:%M")


def format_stamp(moment):
  """The warehouse's preferred stamp format."""
  return moment.strftime("%Y-%m-%d %H:%M")


def window_end(start, hours):
  """Shift a point in time by a duration."""
  return start + timedelta(hours=hours)


def duration_minutes(start, end):
  """The span between two points, in whole minutes."""
  return int((end - start).total_seconds() // 60)


def is_stale(stamp, now, max_hours):
  """Whether a load is older than the freshness budget."""
  return now - stamp > timedelta(hours=max_hours)


def utc_now_is_aware():
  """Whether the recommended now() actually carries a timezone."""
  return datetime.now(timezone.utc).tzinfo is not None
