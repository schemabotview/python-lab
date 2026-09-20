from collections import Counter, defaultdict, deque, namedtuple

Run = namedtuple("Run", ["table", "rows", "status"])


def top_tables(names, count):
  """The most frequently loaded tables, busiest first."""
  return Counter(names).most_common(count)


def tally(names):
  """How many times each table appeared, as a plain dict."""
  return dict(Counter(names))


def group_rows(pairs):
  """Collect (table, row_id) pairs under their table — no key-exists dance."""
  grouped = defaultdict(list)
  for table, row_id in pairs:
    grouped[table].append(row_id)
  return dict(grouped)


def recent(events, size):
  """A sliding window that keeps only the last `size` events."""
  window = deque(maxlen=size)
  for event in events:
    window.append(event)
  return list(window)


def as_queue(items):
  """Drain from the left, which a list does badly."""
  queue = deque(items)
  drained = []
  while queue:
    drained.append(queue.popleft())
  return drained


def summarise(run):
  """A namedtuple reads like a record but still behaves like a tuple."""
  return f"{run.table}: {run.rows} rows ({run.status})"
