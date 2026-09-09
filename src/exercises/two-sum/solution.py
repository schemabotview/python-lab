def two_sum(numbers, target):
  """Return the (i, j) indices of the two values summing to `target`."""
  seen = {}
  for index, value in enumerate(numbers):
    needed = target - value
    if needed in seen:
      return (seen[needed], index)
    seen[value] = index
  return None
