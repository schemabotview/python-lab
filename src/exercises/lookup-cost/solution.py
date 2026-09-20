def scan_allowed(rows, allowlist):
  """Linear scan. Returns (kept, steps) — steps is every comparison made."""
  kept = []
  steps = 0
  for row in rows:
    for allowed in allowlist:
      steps += 1
      if row == allowed:
        kept.append(row)
        break
  return kept, steps


def hashed_allowed(rows, allowlist):
  """One hash probe per row, whatever the allowlist's size."""
  lookup = set(allowlist)
  kept = []
  steps = 0
  for row in rows:
    steps += 1
    if row in lookup:
      kept.append(row)
  return kept, steps


def first_duplicate_naive(values):
  """Compare every value against every earlier one. Returns (value, steps)."""
  steps = 0
  for i in range(len(values)):
    for j in range(i):
      steps += 1
      if values[i] == values[j]:
        return values[i], steps
  return None, steps


def first_duplicate_fast(values):
  """Remember what you have seen. Returns (value, steps)."""
  seen = set()
  steps = 0
  for value in values:
    steps += 1
    if value in seen:
      return value, steps
    seen.add(value)
  return None, steps
