def insertion_sort(values):
  """Sort by sliding each value back into place. Returns (sorted, comparisons)."""
  items = list(values)
  comparisons = 0
  for index in range(1, len(items)):
    current = items[index]
    position = index - 1
    while position >= 0:
      comparisons += 1
      if items[position] <= current:
        break
      items[position + 1] = items[position]
      position -= 1
    items[position + 1] = current
  return items, comparisons


def merge(left, right):
  """Merge two sorted lists. Returns (merged, comparisons)."""
  merged = []
  comparisons = 0
  i = j = 0
  while i < len(left) and j < len(right):
    comparisons += 1
    if left[i] <= right[j]:
      merged.append(left[i])
      i += 1
    else:
      merged.append(right[j])
      j += 1
  merged.extend(left[i:])
  merged.extend(right[j:])
  return merged, comparisons


def merge_sort(values):
  """Split, sort each half, merge. Returns (sorted, comparisons)."""
  if len(values) <= 1:
    return list(values), 0
  middle = len(values) // 2
  left, left_cost = merge_sort(values[:middle])
  right, right_cost = merge_sort(values[middle:])
  merged, merge_cost = merge(left, right)
  return merged, left_cost + right_cost + merge_cost
