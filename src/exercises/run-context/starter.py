from contextlib import contextmanager


class Transaction:
  """Commits on a clean exit, rolls back on an exception — always one or the other."""

  def __init__(self, log):
    self.log = log

  def __enter__(self):
    pass

  def write(self, row):
    pass

  def __exit__(self, exc_type, exc_value, traceback):
    pass


class Suppressing(Transaction):
  """The same, but swallows the exception by returning True from __exit__."""

  def __exit__(self, exc_type, exc_value, traceback):
    pass


@contextmanager
def staged(log, name):
  """The easy way: everything before the yield is enter, everything after is exit."""
  pass
