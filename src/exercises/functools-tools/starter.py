import functools

LOOKUPS = {"calls": 0}


def total_rows(batches):
  """Fold a sequence down to one value."""
  pass


def widest(batches):
  """Fold with a comparison instead of a sum."""
  pass


def qualify(env):
  """Pre-fill the first argument and hand back a simpler function."""
  pass


def table_name(env, schema, table):
  return f"{env}.{schema}.{table}"


# Decorate this so repeat lookups are free. Keep the LOOKUPS counter in the body.
def row_count(table):
  """Pretend this is an expensive query. The cache makes repeats free."""
  LOOKUPS["calls"] += 1
  return len(table) * 100
