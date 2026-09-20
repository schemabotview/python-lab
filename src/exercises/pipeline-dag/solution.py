from collections import deque


def ready_tasks(deps, done):
  """Tasks whose dependencies are all finished, and which haven't run."""
  finished = set(done)
  ready = []
  for task, needs in deps.items():
    if task in finished:
      continue
    if all(need in finished for need in needs):
      ready.append(task)
  return sorted(ready)


def topo_order(deps):
  """A runnable order, or [] when the graph has a cycle."""
  remaining = {task: set(needs) for task, needs in deps.items()}
  queue = deque(sorted(task for task, needs in remaining.items() if not needs))
  order = []
  while queue:
    task = queue.popleft()
    order.append(task)
    unlocked = []
    for other, needs in remaining.items():
      if task in needs:
        needs.discard(task)
        if not needs and other not in order:
          unlocked.append(other)
    for other in sorted(unlocked):
      queue.append(other)
  if len(order) != len(deps):
    return []
  return order


def has_cycle(deps):
  """Whether anything depends, however indirectly, on itself."""
  return topo_order(deps) == [] and len(deps) > 0


def levels(deps):
  """Waves of tasks that could run in parallel."""
  remaining = {task: set(needs) for task, needs in deps.items()}
  done = set()
  waves = []
  while len(done) < len(deps):
    wave = sorted(
      task for task, needs in remaining.items()
      if task not in done and needs <= done
    )
    if not wave:
      return []
    waves.append(wave)
    done.update(wave)
  return waves
