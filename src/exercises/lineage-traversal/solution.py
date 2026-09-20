from collections import deque


def downstream(graph, table):
  """Everything that depends on this table, however far away."""
  seen = set()
  queue = deque(graph.get(table, []))
  while queue:
    current = queue.popleft()
    if current in seen:
      continue
    seen.add(current)
    queue.extend(graph.get(current, []))
  return sorted(seen)


def upstream(graph, table):
  """Everything this table depends on, by walking the edges backwards."""
  reversed_graph = {}
  for source, targets in graph.items():
    for target in targets:
      reversed_graph.setdefault(target, []).append(source)
  return downstream(reversed_graph, table)


def path_between(graph, start, end):
  """The shortest path, or [] when there is none."""
  if start == end:
    return [start]
  queue = deque([[start]])
  seen = {start}
  while queue:
    path = queue.popleft()
    for neighbour in graph.get(path[-1], []):
      if neighbour == end:
        return path + [neighbour]
      if neighbour not in seen:
        seen.add(neighbour)
        queue.append(path + [neighbour])
  return []


def impacted_by(graph, table):
  """The table itself plus everything downstream — the blast radius."""
  return sorted(set(downstream(graph, table)) | {table})
