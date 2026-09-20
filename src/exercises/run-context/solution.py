from contextlib import contextmanager


class Transaction:
  """Commits on a clean exit, rolls back on an exception — always one or the other."""

  def __init__(self, log):
    self.log = log

  def __enter__(self):
    self.log.append("BEGIN")
    return self

  def write(self, row):
    self.log.append(f"WRITE {row}")

  def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is None:
      self.log.append("COMMIT")
    else:
      self.log.append(f"ROLLBACK {exc_type.__name__}")
    # Falsy: the exception carries on out of the with block.
    return False


class Suppressing(Transaction):
  """The same, but swallows the exception by returning True from __exit__."""

  def __exit__(self, exc_type, exc_value, traceback):
    super().__exit__(exc_type, exc_value, traceback)
    return exc_type is not None


@contextmanager
def staged(log, name):
  """The easy way: everything before the yield is enter, everything after is exit."""
  log.append(f"START {name}")
  try:
    yield name.upper()
  finally:
    log.append(f"END {name}")
