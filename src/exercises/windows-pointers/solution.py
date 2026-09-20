def max_window_naive(values, size):
  """Re-add every window from scratch. Returns (best, steps)."""
  if size <= 0 or size > len(values):
    return 0, 0
  best = None
  steps = 0
  for start in range(len(values) - size + 1):
    total = 0
    for offset in range(size):
      steps += 1
      total += values[start + offset]
    if best is None or total > best:
      best = total
  return best, steps


def max_window(values, size):
  """Slide the window: add the new value, drop the old. Returns (best, steps)."""
  if size <= 0 or size > len(values):
    return 0, 0
  total = 0
  steps = 0
  for index in range(size):
    steps += 1
    total += values[index]
  best = total
  for index in range(size, len(values)):
    steps += 1
    total += values[index] - values[index - size]
    if total > best:
      best = total
  return best, steps


def pair_sum_sorted(values, target):
  """Two pointers walking inwards. Returns (i, j) or None."""
  low = 0
  high = len(values) - 1
  while low < high:
    total = values[low] + values[high]
    if total == target:
      return low, high
    if total < target:
      low += 1
    else:
      high -= 1
  return None


def dedupe_sorted(values):
  """Collapse runs of equal neighbours in one pass."""
  unique = []
  for value in values:
    if not unique or unique[-1] != value:
      unique.append(value)
  return unique


def longest_under(values, limit):
  """The longest run whose total stays at or below the limit."""
  best = 0
  total = 0
  start = 0
  for end in range(len(values)):
    total += values[end]
    while total > limit and start <= end:
      total -= values[start]
      start += 1
    if end - start + 1 > best:
      best = end - start + 1
  return best
