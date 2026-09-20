import logging


class ListHandler(logging.Handler):
  """Collects formatted records into a list, so tests can read them."""

  def __init__(self, sink):
    super().__init__()
    self.sink = sink

  def emit(self, record):
    self.sink.append(self.format(record))


def make_logger(name, level, sink):
  """A logger wired to a ListHandler, with a threshold."""
  pass


def log_run(log, table, rows):
  """Routine progress — lazy %-formatting, not an f-string."""
  pass


def log_slow(log, table, seconds):
  pass


def log_failure(log, table, error):
  pass


def log_crash(log, table):
  """Inside an except block, this adds the traceback for you."""
  pass
