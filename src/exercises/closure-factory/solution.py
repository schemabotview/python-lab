def scaler(factor):
  """Manufacture a function that remembers its factor."""
  def scale(value):
    return value * factor
  return scale


def make_counter(start=0):
  """A running count. Reassigning the captured name needs `nonlocal`."""
  current = start

  def bump():
    nonlocal current
    current += 1
    return current

  return bump


def threshold(limit):
  """A predicate configured by what you passed in."""
  def over(value):
    return value > limit
  return over


def build_scalers(factors):
  """One scaler per factor — each capturing independently."""
  return [scaler(factor) for factor in factors]


def compose(*functions):
  """Build a transform chain once; the returned function remembers the steps."""
  def run(value):
    for function in functions:
      value = function(value)
    return value
  return run
