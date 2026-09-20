import re

# Compiled once, reused on every line — the pattern is hot.
LINE = re.compile(r"^(?P<stamp>\S+) (?P<level>[A-Z]+) (?P<table>\w+)")
SECRET = re.compile(r"password=\S+")


def find_level(line):
  """The level token, or "" when the line doesn't match."""
  pass


def parse_line(line):
  """Stamp, level and table as a tuple — or empty strings if it doesn't match."""
  pass


def all_tables(text):
  """Every table named in a block of log text."""
  pass


def redact(text):
  """Replace every password, however long."""
  pass


def split_fields(line):
  """Split on any run of whitespace or semicolons."""
  pass


def row_counts(text):
  """Every rows=N as a real integer."""
  pass
