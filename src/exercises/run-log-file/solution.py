def write_log(path, lines):
  """Write the log fresh. Whatever was there before is gone."""
  with open(path, "w", encoding="utf-8") as handle:
    for line in lines:
      handle.write(line + "\n")
  return len(lines)


def append_log(path, line):
  """Add one line without disturbing what is already there."""
  with open(path, "a", encoding="utf-8") as handle:
    handle.write(line + "\n")
  return line


def read_all(path):
  """The whole file as one string."""
  with open(path, encoding="utf-8") as handle:
    return handle.read()


def count_lines(path):
  """Count lines without ever holding the whole file in memory."""
  total = 0
  with open(path, encoding="utf-8") as handle:
    for _ in handle:
      total += 1
  return total


def first_error(path):
  """The first ERROR line, stopping as soon as it is found."""
  with open(path, encoding="utf-8") as handle:
    for line in handle:
      if line.startswith("ERROR"):
        return line.rstrip("\n")
  return ""
