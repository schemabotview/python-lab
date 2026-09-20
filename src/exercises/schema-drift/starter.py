def drift(expected, actual):
  """Compare the columns a source sent against the ones the target wants."""
  pass


def all_columns(*schemas):
  """Every column named by any of the schemas, sorted."""
  pass


def is_compatible(expected, actual):
  """Whether everything the target needs is present in what arrived."""
  pass


def changed_columns(before, after):
  """Columns on one side only — added or dropped, sorted."""
  pass


def unique_tables(rows):
  """The distinct table names mentioned, sorted."""
  pass


def freeze(columns):
  """An immutable column set, so it can be used as a dict key."""
  pass
