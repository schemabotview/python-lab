def scaler(factor):
  """Manufacture a function that remembers its factor."""
  pass


def make_counter(start=0):
  """A running count. Reassigning the captured name needs `nonlocal`."""
  pass


def threshold(limit):
  """A predicate configured by what you passed in."""
  pass


def build_scalers(factors):
  """One scaler per factor — each capturing independently."""
  pass


def compose(*functions):
  """Build a transform chain once; the returned function remembers the steps."""
  pass
