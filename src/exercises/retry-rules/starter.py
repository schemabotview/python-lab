def decide(attempt, max_attempts, exit_code, duration_s, is_critical, last_success_days, run_hour):
  """Return the orchestrator's verdict on a finished task, as one multi-line string."""
  pass


def partition_plan(total_rows, rows_per_file):
  """Return how the writer will split the rows, as one multi-line string."""
  pass


def decode_status(mask):
  """Unpack a status bitmask into (retried, partial, schema_drift)."""
  pass


def identity_check(a, b):
  """Return (is the same object, holds an equal value)."""
  pass


def has_rows(result):
  """Return whether a result set has anything in it."""
  pass


def with_default(raw, fallback):
  """Return the configured value, or the fallback when it is blank."""
  pass


def is_allowed(table, allowlist):
  """Return whether this table may be loaded."""
  pass
