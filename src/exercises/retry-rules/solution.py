def decide(attempt, max_attempts, exit_code, duration_s, is_critical, last_success_days, run_hour):
  """Return the orchestrator's verdict on a finished task, as one multi-line string."""
  failed = exit_code != 0
  should_retry = failed and attempt < max_attempts
  page_on_call = (is_critical and failed and not should_retry) or (last_success_days > 3)
  backfill_needed = last_success_days > 1
  sla_breached = duration_s > 3600
  in_window = 0 <= run_hour < 6
  # A bool is 1 or 0 in arithmetic, so this zeroes the backoff without branching.
  backoff = 30 * (2 ** attempt) * should_retry
  return "\n".join([
    f"Should retry: {should_retry}",
    f"Page on-call: {page_on_call}",
    f"Backfill needed: {backfill_needed}",
    f"SLA breached: {sla_breached}",
    f"In window: {in_window}",
    f"Backoff: {backoff}s",
  ])


def partition_plan(total_rows, rows_per_file):
  """Return how the writer will split the rows, as one multi-line string."""
  full_files = total_rows // rows_per_file
  remainder = total_rows % rows_per_file
  files_written = full_files + (remainder > 0)
  return "\n".join([
    f"Rows: {total_rows}",
    f"Full files: {full_files}",
    f"Remainder: {remainder}",
    f"Files written: {files_written}",
  ])


def decode_status(mask):
  """Unpack a status bitmask into (retried, partial, schema_drift)."""
  return bool(mask & 1), bool(mask & 2), bool(mask & 4)


def identity_check(a, b):
  """Return (is the same object, holds an equal value)."""
  return a is b, a == b


def has_rows(result):
  """Return whether a result set has anything in it."""
  return bool(result)


def with_default(raw, fallback):
  """Return the configured value, or the fallback when it is blank."""
  return raw or fallback


def is_allowed(table, allowlist):
  """Return whether this table may be loaded."""
  return table in allowlist
