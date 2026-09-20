class ConsoleSink:
  """Prints somewhere. No base class, no registration — just the method."""

  def write(self, rows):
    pass


class TableSink:
  def __init__(self, table):
    pass

  def write(self, rows):
    pass


class NullSink:
  def write(self, rows):
    pass


class Batch:
  """A batch that answers len(), the same way a list or a string does."""

  def __init__(self, row_ids):
    pass

  def __len__(self):
    pass


def fan_out(sinks, rows):
  """Send the same rows to every sink. The caller never asks what kind each is."""
  pass


def total_size(items):
  """Total length across anything that answers len() — one protocol, many types."""
  pass
