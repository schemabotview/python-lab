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
  log = logging.getLogger(name)
  log.handlers.clear()
  log.propagate = False
  log.setLevel(level)
  handler = ListHandler(sink)
  handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
  log.addHandler(handler)
  return log


def log_run(log, table, rows):
  """Routine progress — lazy %-formatting, not an f-string."""
  log.info("loaded %s rows into %s", rows, table)


def log_slow(log, table, seconds):
  log.warning("%s took %ss", table, seconds)


def log_failure(log, table, error):
  log.error("%s failed: %s", table, error)


def log_crash(log, table):
  """Inside an except block, this adds the traceback for you."""
  log.exception("%s crashed", table)
