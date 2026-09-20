import functools


def counted(fn):
  """Wrap a step so it keeps a tally of how often it ran."""
  pass


def tagged(label):
  """A decorator that takes an argument — one more layer than `counted`."""
  pass


def retry(times):
  """Re-run a flaky step, returning the last error message if it never works."""
  pass


@counted
def load(table):
  """Load one table."""
  return f"loaded {table}"


@tagged("etl")
def summarise(table):
  """Summarise one table."""
  return f"summary of {table}"
