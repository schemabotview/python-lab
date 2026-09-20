DEFAULTS = {"env": "prod", "retries": 3, "parallel": 4}


def version():
  """The build stamp this module ships under."""
  pass


def table_name(schema, table, env="prod"):
  """Fully qualify a table. The environment defaults to production."""
  pass


def summarize(*durations):
  """Return (total, average) for any number of runs, including none."""
  pass


def build_config(**overrides):
  """Merge per-run overrides onto the defaults, leaving DEFAULTS untouched."""
  pass


def apply_all(value, *steps):
  """Run a value through a chain of transforms, in order."""
  pass


def first_failure(results):
  """The name of the first failed step, or None when every step passed."""
  pass


def report(results):
  """Describe a run. Guards on the None that first_failure can return."""
  pass


def check_row(row):
  """One guard per rule, in priority order, each returning immediately."""
  pass


def collect(message, errors=None):
  """Append a message to an error list, starting a fresh one when none is given."""
  pass
