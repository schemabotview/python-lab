def lookup(counts, table):
  """Rows loaded for a table — 0 for one that never ran."""
  pass


def merge_runs(first, second):
  """Merge a later run over an earlier one. Neither input is touched."""
  pass


def add_row(index, table, row_id):
  """File a row id under its table, starting the list if it's the first."""
  pass


def ledger_report(counts):
  """One line per table in name order, then the total."""
  pass


def drop_table(counts, table):
  """Remove a table from the ledger. Dropping one that isn't there is fine."""
  pass


def column_order(pairs):
  """Build a schema from (name, type) pairs and report the column order."""
  pass
