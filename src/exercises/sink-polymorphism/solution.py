class ConsoleSink:
  """Prints somewhere. No base class, no registration — just the method."""

  def write(self, rows):
    return f"console: {rows}"


class TableSink:
  def __init__(self, table):
    self.table = table

  def write(self, rows):
    return f"{self.table}: {rows}"


class NullSink:
  def write(self, rows):
    return "discarded"


class Batch:
  """A batch that answers len(), the same way a list or a string does."""

  def __init__(self, row_ids):
    self.row_ids = row_ids

  def __len__(self):
    return len(self.row_ids)


def fan_out(sinks, rows):
  """Send the same rows to every sink. The caller never asks what kind each is."""
  return [sink.write(rows) for sink in sinks]


def total_size(items):
  """Total length across anything that answers len() — one protocol, many types."""
  total = 0
  for item in items:
    total += len(item)
  return total
