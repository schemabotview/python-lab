def scan_allowed(rows, allowlist):
  """Linear scan. Returns (kept, steps) — steps is every comparison made."""
  pass


def hashed_allowed(rows, allowlist):
  """One hash probe per row, whatever the allowlist's size."""
  pass


def first_duplicate_naive(values):
  """Compare every value against every earlier one. Returns (value, steps)."""
  pass


def first_duplicate_fast(values):
  """Remember what you have seen. Returns (value, steps)."""
  pass
