import csv


def write_rows(path, fieldnames, rows):
  """Write dict rows with a header, letting the module handle the quoting."""
  pass


def read_rows(path):
  """Read back as dicts, keyed by the header."""
  pass


def column(path, name):
  """One column's values, by name rather than position."""
  pass


def read_positional(path):
  """Every row as a plain list, header included."""
  pass


def naive_split(path):
  """The wrong way, kept so the tests can show what it costs."""
  pass
