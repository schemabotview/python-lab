import functools

LOOKUPS = {"calls": 0}


def total_rows(batches):
  """Fold a sequence down to one value."""
  return functools.reduce(lambda running, batch: running + batch, batches, 0)


def widest(batches):
  """Fold with a comparison instead of a sum."""
  return functools.reduce(lambda a, b: a if a >= b else b, batches, 0)


def qualify(env):
  """Pre-fill the first argument and hand back a simpler function."""
  return functools.partial(table_name, env)


def table_name(env, schema, table):
  return f"{env}.{schema}.{table}"


@functools.lru_cache(maxsize=128)
def row_count(table):
  """Pretend this is an expensive query. The cache makes repeats free."""
  LOOKUPS["calls"] += 1
  return len(table) * 100
