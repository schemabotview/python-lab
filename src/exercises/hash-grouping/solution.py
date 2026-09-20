def two_sum(numbers, target):
  """The (i, j) indices of two values summing to target, or None."""
  seen = {}
  for index, value in enumerate(numbers):
    needed = target - value
    if needed in seen:
      return seen[needed], index
    seen[value] = index
  return None


def two_sum_naive(numbers, target):
  """Every pair, compared. Returns (answer, steps)."""
  steps = 0
  for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
      steps += 1
      if numbers[i] + numbers[j] == target:
        return (i, j), steps
  return None, steps


def group_by_schema(tables):
  """Group (name, columns) by the set of columns they share."""
  grouped = {}
  for name, columns in tables:
    key = frozenset(columns)
    grouped.setdefault(key, []).append(name)
  return {key: sorted(names) for key, names in grouped.items()}


def join_keys(left, right):
  """The keys present in both sides of a join, sorted."""
  return sorted(set(left) & set(right))


def index_by(rows, field):
  """Build a lookup from a field to the rows carrying it."""
  index = {}
  for row in rows:
    index.setdefault(row[field], []).append(row)
  return index
