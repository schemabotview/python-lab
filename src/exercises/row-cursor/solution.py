class Cursor:
  """A cursor over rows — the protocol every for loop runs, written by hand."""

  def __init__(self, rows):
    self.rows = rows
    self.position = 0

  def __iter__(self):
    return self

  def __next__(self):
    if self.position >= len(self.rows):
      raise StopIteration
    row = self.rows[self.position]
    self.position += 1
    return row


def manual_walk(iterable):
  """Drive the protocol by hand: iter once, then next until StopIteration."""
  cursor = iter(iterable)
  collected = []
  while True:
    try:
      collected.append(next(cursor))
    except StopIteration:
      return collected


def first_n(iterable, count):
  """Pull at most `count` values, leaving whatever follows unread."""
  cursor = iter(iterable)
  collected = []
  for _ in range(count):
    try:
      collected.append(next(cursor))
    except StopIteration:
      break
  return collected


def is_iterable(value):
  """Whether iter() will accept this at all."""
  try:
    iter(value)
  except TypeError:
    return False
  return True
