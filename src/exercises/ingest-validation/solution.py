class SchemaError(Exception):
  """Raised when an incoming row is missing a column the loader needs."""


def parse_row(raw):
  """Classify one raw CSV line: ok, bad shape, or bad number."""
  parts = raw.split(",")
  if len(parts) != 3:
    return f"bad shape: {len(parts)} fields"
  stamp, table, raw_rows = parts
  try:
    rows = int(raw_rows)
  except ValueError:
    return f"bad number: {raw_rows}"
  else:
    # Runs only when the conversion didn't raise.
    return f"ok: {table} {rows}"


def error_rate(failed, total):
  """Percentage of rows that failed, to one decimal. An empty batch is 0.0%."""
  try:
    return f"{failed / total * 100:.1f}%"
  except ZeroDivisionError:
    return "0.0%"


def require_columns(row, needed):
  """Return True, or raise SchemaError naming the first missing column."""
  for column in needed:
    if column not in row:
      raise SchemaError(f"missing column: {column}")
  return True


def load_all(rows):
  """Load every row it can, survive the ones it can't, and report."""
  attempted = 0
  loaded = 0
  problems = []
  for row in rows:
    try:
      require_columns(row, ["table", "rows"])
      int(row["rows"])
    except SchemaError as exc:
      problems.append(str(exc))
    except ValueError:
      problems.append(f"bad number: {row['rows']}")
    else:
      loaded += 1
    finally:
      # Runs whichever way the row went, so the count can never drift.
      attempted += 1
  lines = [
    f"Attempted: {attempted}",
    f"Loaded: {loaded}",
    f"Skipped: {attempted - loaded}",
  ]
  for problem in problems:
    lines.append(f"- {problem}")
  return "\n".join(lines)
