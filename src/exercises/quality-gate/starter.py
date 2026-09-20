def quality_grade(null_percent):
  """Grade a table on how many of its values came back null."""
  pass


def gate(table, row_count, null_percent, freshness_hours, note):
  """Return the promotion decision for one loaded table, as a multi-line string."""
  pass


def route(event_type):
  """Return the raw table an incoming event belongs in."""
  pass
