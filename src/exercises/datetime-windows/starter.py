from datetime import datetime, timedelta, timezone


def parse_stamp(text):
  """ISO text in, datetime out."""
  pass


def parse_custom(text):
  """A non-ISO format needs an explicit pattern."""
  pass


def format_stamp(moment):
  """The warehouse's preferred stamp format."""
  pass


def window_end(start, hours):
  """Shift a point in time by a duration."""
  pass


def duration_minutes(start, end):
  """The span between two points, in whole minutes."""
  pass


def is_stale(stamp, now, max_hours):
  """Whether a load is older than the freshness budget."""
  pass


def utc_now_is_aware():
  """Whether the recommended now() actually carries a timezone."""
  pass
