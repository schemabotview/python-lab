import functools


def counted(fn):
  """Wrap a step so it keeps a tally of how often it ran."""
  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    wrapper.calls += 1
    return fn(*args, **kwargs)
  wrapper.calls = 0
  return wrapper


def tagged(label):
  """A decorator that takes an argument — one more layer than `counted`."""
  def decorate(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
      return f"[{label}] {fn(*args, **kwargs)}"
    return wrapper
  return decorate


def retry(times):
  """Re-run a flaky step, returning the last error message if it never works."""
  def decorate(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
      last = ""
      for _ in range(times):
        try:
          return fn(*args, **kwargs)
        except Exception as exc:
          last = str(exc)
      return f"gave up after {times}: {last}"
    return wrapper
  return decorate


@counted
def load(table):
  """Load one table."""
  return f"loaded {table}"


@tagged("etl")
def summarise(table):
  """Summarise one table."""
  return f"summary of {table}"
