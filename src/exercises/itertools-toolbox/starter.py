import itertools


def stitch(*batches):
  """One stream over several batches, without copying them into a new list."""
  pass


def page(stream, start, stop):
  """Slice an iterator — even an endless one — without building a list."""
  pass


def endless_ids(prefix):
  """An endless id stream, built from a counter."""
  pass


def rotate(options, length):
  """Cycle a short list out to a given length."""
  pass


def group_by_table(rows):
  """Group (table, rows) pairs by table. The input must be sorted by the key."""
  pass


def running_total(counts):
  """A cumulative total after each batch."""
  pass


def pairs(tables):
  """Every unordered pair of tables — for a join-compatibility check."""
  pass
