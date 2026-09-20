import csv


def write_rows(path, fieldnames, rows):
  """Write dict rows with a header, letting the module handle the quoting."""
  with open(path, "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
  return len(rows)


def read_rows(path):
  """Read back as dicts, keyed by the header."""
  with open(path, newline="", encoding="utf-8") as handle:
    return list(csv.DictReader(handle))


def column(path, name):
  """One column's values, by name rather than position."""
  return [row[name] for row in read_rows(path)]


def read_positional(path):
  """Every row as a plain list, header included."""
  with open(path, newline="", encoding="utf-8") as handle:
    return list(csv.reader(handle))


def naive_split(path):
  """The wrong way, kept so the tests can show what it costs."""
  with open(path, newline="", encoding="utf-8") as handle:
    return [line.rstrip("\n").split(",") for line in handle]
