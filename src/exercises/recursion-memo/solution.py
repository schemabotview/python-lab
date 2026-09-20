def depth_of(value):
  """How deeply a manifest nests. A plain value is depth 0."""
  if isinstance(value, dict):
    if not value:
      return 1
    return 1 + max(depth_of(item) for item in value.values())
  if isinstance(value, list):
    if not value:
      return 1
    return 1 + max(depth_of(item) for item in value)
  return 0


def flatten(value):
  """Every leaf of an arbitrarily nested list, left to right."""
  leaves = []
  for item in value:
    if isinstance(item, list):
      leaves.extend(flatten(item))
    else:
      leaves.append(item)
  return leaves


def count_leaves(value):
  """How many non-container values a manifest holds."""
  if isinstance(value, dict):
    return sum(count_leaves(item) for item in value.values())
  if isinstance(value, list):
    return sum(count_leaves(item) for item in value)
  return 1


def fib_naive(n):
  """The textbook recursion. Returns (value, calls)."""
  calls = {"n": 0}

  def step(k):
    calls["n"] += 1
    if k < 2:
      return k
    return step(k - 1) + step(k - 2)

  return step(n), calls["n"]


def fib_memo(n):
  """The same recursion, remembering. Returns (value, calls)."""
  calls = {"n": 0}
  cache = {}

  def step(k):
    if k in cache:
      return cache[k]
    calls["n"] += 1
    result = k if k < 2 else step(k - 1) + step(k - 2)
    cache[k] = result
    return result

  return step(n), calls["n"]
