def roster_report(roster):
  """Return the cleaned-up roster summary as one multi-line string."""
  working = list(roster)
  working.remove("")
  names = sorted(set(working))
  final = names + ["Noor"]
  return "\n".join([
    f"Roster: {names}",
    f"Unique students: {len(names)}",
    f"First: {names[0]}",
    f"Last: {names[-1]}",
    f"Middle: {names[len(names) // 2]}",
    f"Final: {final}",
  ])
