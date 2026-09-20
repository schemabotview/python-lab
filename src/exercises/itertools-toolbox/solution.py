import itertools


def stitch(*batches):
  """One stream over several batches, without copying them into a new list."""
  return list(itertools.chain(*batches))


def page(stream, start, stop):
  """Slice an iterator — even an endless one — without building a list."""
  return list(itertools.islice(stream, start, stop))


def endless_ids(prefix):
  """An endless id stream, built from a counter."""
  return (f"{prefix}-{n}" for n in itertools.count(1))


def rotate(options, length):
  """Cycle a short list out to a given length."""
  return list(itertools.islice(itertools.cycle(options), length))


def group_by_table(rows):
  """Group (table, rows) pairs by table. The input must be sorted by the key."""
  grouped = {}
  for table, entries in itertools.groupby(sorted(rows), key=lambda row: row[0]):
    grouped[table] = [entry[1] for entry in entries]
  return grouped


def running_total(counts):
  """A cumulative total after each batch."""
  return list(itertools.accumulate(counts))


def pairs(tables):
  """Every unordered pair of tables — for a join-compatibility check."""
  return list(itertools.combinations(tables, 2))
