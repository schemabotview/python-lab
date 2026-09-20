import re

# Compiled once, reused on every line — the pattern is hot.
LINE = re.compile(r"^(?P<stamp>\S+) (?P<level>[A-Z]+) (?P<table>\w+)")
SECRET = re.compile(r"password=\S+")


def find_level(line):
  """The level token, or "" when the line doesn't match."""
  found = LINE.search(line)
  if found is None:
    return ""
  return found.group("level")


def parse_line(line):
  """Stamp, level and table as a tuple — or empty strings if it doesn't match."""
  found = LINE.search(line)
  if found is None:
    return "", "", ""
  return found.group("stamp"), found.group("level"), found.group("table")


def all_tables(text):
  """Every table named in a block of log text."""
  return re.findall(r"table=(\w+)", text)


def redact(text):
  """Replace every password, however long."""
  return SECRET.sub("password=***", text)


def split_fields(line):
  """Split on any run of whitespace or semicolons."""
  return re.split(r"[;\s]+", line.strip())


def row_counts(text):
  """Every rows=N as a real integer."""
  return [int(value) for value in re.findall(r"rows=(\d+)", text)]
