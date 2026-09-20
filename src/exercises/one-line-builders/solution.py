def table_names(records):
  """Every table name, in the order the records arrived."""
  return [record["table"] for record in records]


def loaded_only(records):
  """Just the tables that loaded cleanly."""
  return [record["table"] for record in records if record["status"] == "ok"]


def rows_by_table(records):
  """A table -> rows lookup, built in one line."""
  return {record["table"]: record["rows"] for record in records}


def distinct_statuses(records):
  """The statuses seen, without repeats, sorted."""
  return sorted({record["status"] for record in records})


def flatten(batches):
  """One flat list of row ids from a list of batches."""
  return [row_id for batch in batches for row_id in batch]


def total_rows(records):
  """Total rows, summed straight from a generator — no list in between."""
  return sum(record["rows"] for record in records)


def lazy_names(records):
  """A generator of table names, producing nothing until it is walked."""
  return (record["table"] for record in records)
