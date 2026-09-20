def table_names(records):
  """Every table name, in the order the records arrived."""
  pass


def loaded_only(records):
  """Just the tables that loaded cleanly."""
  pass


def rows_by_table(records):
  """A table -> rows lookup, built in one line."""
  pass


def distinct_statuses(records):
  """The statuses seen, without repeats, sorted."""
  pass


def flatten(batches):
  """One flat list of row ids from a list of batches."""
  pass


def total_rows(records):
  """Total rows, summed straight from a generator — no list in between."""
  pass


def lazy_names(records):
  """A generator of table names, producing nothing until it is walked."""
  pass
