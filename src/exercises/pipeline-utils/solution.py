DEFAULTS = {"env": "prod", "retries": 3, "parallel": 4}


def version():
  """The build stamp this module ships under."""
  return "1.0.0"


def table_name(schema, table, env="prod"):
  """Fully qualify a table. The environment defaults to production."""
  return f"{env}.{schema}.{table}"


def summarize(*durations):
  """Return (total, average) for any number of runs, including none."""
  if not durations:
    return 0, 0
  total = sum(durations)
  return total, total / len(durations)


def build_config(**overrides):
  """Merge per-run overrides onto the defaults, leaving DEFAULTS untouched."""
  config = dict(DEFAULTS)
  config.update(overrides)
  return config


def apply_all(value, *steps):
  """Run a value through a chain of transforms, in order."""
  for step in steps:
    value = step(value)
  return value


def first_failure(results):
  """The name of the first failed step, or None when every step passed."""
  for step, status in results:
    if status != "ok":
      return step
  return None


def report(results):
  """Describe a run. Guards on the None that first_failure can return."""
  failed = first_failure(results)
  if failed is None:
    return "all steps ok"
  return f"first failure: {failed}"


def check_row(row):
  """One guard per rule, in priority order, each returning immediately."""
  if not row.get("table"):
    return "no table name"
  if not row.get("checksum"):
    return f"{row['table']}: no checksum"
  if row.get("rows", 0) < 1:
    return f"{row['table']}: empty"
  return f"{row['table']}: accepted"


def collect(message, errors=None):
  """Append a message to an error list, starting a fresh one when none is given."""
  # `errors=[]` would build ONE list at definition time and reuse it forever.
  if errors is None:
    errors = []
  errors.append(message)
  return errors
