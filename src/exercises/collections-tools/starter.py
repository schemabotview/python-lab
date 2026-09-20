from collections import Counter, defaultdict, deque, namedtuple

Run = namedtuple("Run", ["table", "rows", "status"])


def top_tables(names, count):
  """The most frequently loaded tables, busiest first."""
  pass


def tally(names):
  """How many times each table appeared, as a plain dict."""
  pass


def group_rows(pairs):
  """Collect (table, row_id) pairs under their table — no key-exists dance."""
  pass


def recent(events, size):
  """A sliding window that keeps only the last `size` events."""
  pass


def as_queue(items):
  """Drain from the left, which a list does badly."""
  pass


def summarise(run):
  """A namedtuple reads like a record but still behaves like a tuple."""
  pass
