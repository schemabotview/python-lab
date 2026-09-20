class Dataset:
  """A named dataset. Every instance owns its own column list."""

  # Shared and immutable — safe in the class body.
  region = "eu-west-1"

  def __init__(self, name):
    pass

  def add_column(self, column):
    pass


def same_object(first, second):
  """Whether two names point at one object, not merely equal ones."""
  pass


def same_type(value, kind):
  """Whether a value is of the given type."""
  pass


def attributes(obj):
  """Every instance attribute the object is carrying, sorted."""
  pass


def tag(obj, key, value):
  """Attach an attribute that was never declared on the class."""
  pass
