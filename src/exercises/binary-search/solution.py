import bisect


def binary_search(values, target):
  """Index of target in a sorted list, or -1. Halve the range each step."""
  low = 0
  high = len(values) - 1
  while low <= high:
    middle = (low + high) // 2
    if values[middle] == target:
      return middle
    if values[middle] < target:
      low = middle + 1
    else:
      high = middle - 1
  return -1


def probes(values, target):
  """How many values the search actually looked at."""
  low = 0
  high = len(values) - 1
  looked = 0
  while low <= high:
    middle = (low + high) // 2
    looked += 1
    if values[middle] == target:
      return looked
    if values[middle] < target:
      low = middle + 1
    else:
      high = middle - 1
  return looked


def first_index(values, target):
  """Leftmost position of target, or -1 when it isn't there."""
  found = bisect.bisect_left(values, target)
  if found < len(values) and values[found] == target:
    return found
  return -1


def last_index(values, target):
  """Rightmost position of target, or -1."""
  found = bisect.bisect_right(values, target) - 1
  if found >= 0 and values[found] == target:
    return found
  return -1


def insert_point(values, target):
  """Where target would go to keep the list sorted."""
  return bisect.bisect_left(values, target)


def partition_range(dates, start, end):
  """The dates in [start, end), found without scanning the whole list."""
  left = bisect.bisect_left(dates, start)
  right = bisect.bisect_left(dates, end)
  return dates[left:right]
