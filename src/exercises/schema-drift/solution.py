def drift(expected, actual):
  """Compare the columns a source sent against the ones the target wants."""
  expected_set = set(expected)
  actual_set = set(actual)
  return "\n".join([
    f"Missing: {sorted(expected_set - actual_set)}",
    f"Unexpected: {sorted(actual_set - expected_set)}",
    f"Shared: {sorted(expected_set & actual_set)}",
  ])


def all_columns(*schemas):
  """Every column named by any of the schemas, sorted."""
  seen = set()
  for schema in schemas:
    seen |= set(schema)
  return sorted(seen)


def is_compatible(expected, actual):
  """Whether everything the target needs is present in what arrived."""
  return set(expected) <= set(actual)


def changed_columns(before, after):
  """Columns on one side only — added or dropped, sorted."""
  return sorted(set(before) ^ set(after))


def unique_tables(rows):
  """The distinct table names mentioned, sorted."""
  return sorted(set(rows))


def freeze(columns):
  """An immutable column set, so it can be used as a dict key."""
  return frozenset(columns)
