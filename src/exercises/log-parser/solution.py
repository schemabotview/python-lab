def parse_line(line):
  """Break a run-log line into its four leading parts."""
  parts = line.split()
  return "\n".join([
    f"Date: {line[:10]}",
    f"Time: {parts[1]}",
    f"Level: {parts[2].upper()}",
    f"Table: {parts[3]}",
  ])


def normalise(name):
  """Turn a hand-typed CSV header into a safe column name."""
  return "_".join(name.split()).lower()


def redact(line, secret):
  """Hide a secret before the line reaches the log."""
  return line.replace(secret, "***")


def source_kind(path):
  """Route an input path by where it lives and what it is."""
  if path.startswith("s3://") and path.endswith(".csv"):
    return "s3-csv"
  if path.startswith("s3://"):
    return "s3-other"
  if path.endswith(".csv"):
    return "local-csv"
  return "unknown"


def field(line, key):
  """Pull one key=value field out of a line. Missing keys give ""."""
  _, found, rest = line.partition(key + "=")
  if not found:
    return ""
  value, _, _ = rest.partition(" ")
  return value


def to_csv(values):
  """Join values into one CSV line, trimming each."""
  trimmed = []
  for value in values:
    trimmed.append(value.strip())
  return ",".join(trimmed)
