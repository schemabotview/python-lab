class Cursor:
  """A cursor over rows — the protocol every for loop runs, written by hand."""

  def __init__(self, rows):
    self.rows = rows
    self.position = 0

  def __iter__(self):
    pass

  def __next__(self):
    pass


def manual_walk(iterable):
  """Drive the protocol by hand: iter once, then next until StopIteration."""
  pass


def first_n(iterable, count):
  """Pull at most `count` values, leaving whatever follows unread."""
  pass


def is_iterable(value):
  """Whether iter() will accept this at all."""
  pass
