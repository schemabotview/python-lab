def read_rows(rows):
  """The simplest generator: hand back one row at a time."""
  pass


def chunked(rows, size):
  """Batch a stream into lists of `size`, with a short final batch."""
  pass


def run_ids(prefix):
  """An endless stream of ids. Safe, because nothing is produced until asked."""
  pass


def take(stream, count):
  """The first `count` values of any stream, however long it is."""
  pass


def merge_streams(*streams):
  """Re-emit every stream's items in turn, without a manual inner loop."""
  pass
