class SchemaError(Exception):
  """Raised when an incoming row is missing a column the loader needs."""


def parse_row(raw):
  """Classify one raw CSV line: ok, bad shape, or bad number."""
  pass


def error_rate(failed, total):
  """Percentage of rows that failed, to one decimal. An empty batch is 0.0%."""
  pass


def require_columns(row, needed):
  """Return True, or raise SchemaError naming the first missing column."""
  pass


def load_all(rows):
  """Load every row it can, survive the ones it can't, and report."""
  pass
