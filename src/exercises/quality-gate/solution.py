def quality_grade(null_percent):
  """Grade a table on how many of its values came back null."""
  if null_percent < 1:
    return "A"
  elif null_percent < 5:
    return "B"
  elif null_percent < 10:
    return "C"
  elif null_percent < 25:
    return "D"
  else:
    return "F"


def gate(table, row_count, null_percent, freshness_hours, note):
  """Return the promotion decision for one loaded table, as a multi-line string."""
  grade = quality_grade(null_percent)
  freshness = "OK" if freshness_hours <= 24 else "STALE"
  volume = "OK" if row_count >= 1000 else "LOW"
  # A truthy check, not `note == ""` — None and "" both mean "nothing was said".
  if note:
    note_line = f"Note: {note}"
  else:
    note_line = "Note: none"
  healthy = grade in ("A", "B", "C") and freshness == "OK" and volume == "OK"
  verdict = "PROMOTE" if healthy else "QUARANTINE"
  return "\n".join([
    f"Table: {table}",
    f"Grade: {grade}",
    f"Freshness: {freshness}",
    f"Volume: {volume}",
    note_line,
    f"Verdict: {verdict}",
  ])


def route(event_type):
  """Return the raw table an incoming event belongs in."""
  match event_type:
    case "order.created" | "order.shipped":
      return "orders_raw"
    case "user.signup":
      return "users_raw"
    case "click" | "view":
      return "events_raw"
    case _:
      return "dead_letter"
