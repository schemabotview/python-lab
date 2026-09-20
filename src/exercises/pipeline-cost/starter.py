# Rates the finance team publishes. Name them here, in UPPER_CASE.


def cost_report(compute_hours, storage_gb, egress_gb, discount_percent):
  """Return the nightly cost summary as one multi-line string."""
  pass


def parse_env(raw_hours, raw_retries, raw_debug):
  """Return (hours, retries, debug) converted from their env-var strings."""
  pass


def describe(value):
  """Return the kind of a config value: int, float, str, bool, none or other."""
  pass


def to_iso(stamp):
  """Turn a DD-MM-YYYY stamp into YYYY-MM-DD."""
  pass


def split_fields(line):
  """Split a CSV line into (table_name, [the remaining fields])."""
  pass
