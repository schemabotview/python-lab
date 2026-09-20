def clean_schedule(raw):
  """Drop blanks and duplicates from a hand-typed schedule, sorted."""
  working = list(raw)
  while "" in working:
    working.remove("")
  return sorted(set(working))


def slice_report(tables):
  """Four views of the same schedule, by slicing alone."""
  return "\n".join([
    f"First three: {tables[:3]}",
    f"Last two: {tables[-2:]}",
    f"Every other: {tables[::2]}",
    f"Reversed: {tables[::-1]}",
  ])


def replace_window(tables, start, end, replacement):
  """Swap a run of tables for a different run, without touching the original."""
  updated = list(tables)
  updated[start:end] = replacement
  return updated


def promote(tables, name):
  """Move one table to the front of the run order."""
  updated = list(tables)
  updated.remove(name)
  updated.insert(0, name)
  return updated


def batch_summary(batches):
  """Total the rows across [name, rows] pairs and name the biggest."""
  total = 0
  largest = ""
  largest_rows = -1
  for batch in batches:
    total += batch[1]
    if batch[1] > largest_rows:
      largest_rows = batch[1]
      largest = batch[0]
  return "\n".join([
    f"Tables: {len(batches)}",
    f"Rows: {total}",
    f"Largest: {largest or 'none'}",
  ])


def snapshot(tables):
  """A copy that later changes to the original can't reach."""
  return list(tables)
