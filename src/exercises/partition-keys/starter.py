def parse_partition(path):
  """Pull the values out of a Hive-style partition path."""
  pass


def partition_key(record):
  """Build the composite key a row is grouped under."""
  pass


def bounds(values):
  """Return (lowest, highest, count) — three values from one call."""
  pass


def one_item(value):
  """Wrap a single value in a tuple of length one."""
  pass


def rekey(pair):
  """Flip a (table, year) pair into (year, table)."""
  pass


def group_counts(rows):
  """Count rows per (table, date) — a tuple is hashable, so it can be a key."""
  pass
