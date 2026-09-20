def clean_schedule(raw):
  """Drop blanks and duplicates from a hand-typed schedule, sorted."""
  pass


def slice_report(tables):
  """Four views of the same schedule, by slicing alone."""
  pass


def replace_window(tables, start, end, replacement):
  """Swap a run of tables for a different run, without touching the original."""
  pass


def promote(tables, name):
  """Move one table to the front of the run order."""
  pass


def batch_summary(batches):
  """Total the rows across [name, rows] pairs and name the biggest."""
  pass


def snapshot(tables):
  """A copy that later changes to the original can't reach."""
  pass
