class Dataset:
  """A named dataset. Every instance owns its own column list."""

  # Shared and immutable — safe in the class body.
  region = "eu-west-1"

  def __init__(self, name):
    self.name = name
    # On self, not in the class body: a list here would be shared by everyone.
    self.columns = []

  def add_column(self, column):
    self.columns.append(column)
    return self.columns


def same_object(first, second):
  """Whether two names point at one object, not merely equal ones."""
  return first is second


def same_type(value, kind):
  """Whether a value is of the given type."""
  return isinstance(value, kind)


def attributes(obj):
  """Every instance attribute the object is carrying, sorted."""
  return sorted(vars(obj))


def tag(obj, key, value):
  """Attach an attribute that was never declared on the class."""
  setattr(obj, key, value)
  return sorted(vars(obj))
