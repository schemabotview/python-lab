def parse_line(line):
  """Break a run-log line into its four leading parts."""
  pass


def normalise(name):
  """Turn a hand-typed CSV header into a safe column name."""
  pass


def redact(line, secret):
  """Hide a secret before the line reaches the log."""
  pass


def source_kind(path):
  """Route an input path by where it lives and what it is."""
  pass


def field(line, key):
  """Pull one key=value field out of a line. Missing keys give ""."""
  pass


def to_csv(values):
  """Join values into one CSV line, trimming each."""
  pass
