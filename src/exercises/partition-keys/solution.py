def parse_partition(path):
  """Pull the values out of a Hive-style partition path."""
  parts = path.split("/")
  values = []
  for part in parts:
    name, _, value = part.partition("=")
    values.append(value)
  return tuple(values)


def partition_key(record):
  """Build the composite key a row is grouped under."""
  return record["table"], record["year"], record["month"]


def bounds(values):
  """Return (lowest, highest, count) — three values from one call."""
  if not values:
    return 0, 0, 0
  lowest = highest = values[0]
  for value in values:
    if value < lowest:
      lowest = value
    if value > highest:
      highest = value
  return lowest, highest, len(values)


def one_item(value):
  """Wrap a single value in a tuple of length one."""
  return (value,)


def rekey(pair):
  """Flip a (table, year) pair into (year, table)."""
  table, year = pair
  return year, table


def group_counts(rows):
  """Count rows per (table, date) — a tuple is hashable, so it can be a key."""
  counts = {}
  for table, date in rows:
    key = (table, date)
    counts[key] = counts.get(key, 0) + 1
  return counts
