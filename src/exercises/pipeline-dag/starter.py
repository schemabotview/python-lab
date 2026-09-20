from collections import deque


def ready_tasks(deps, done):
  """Tasks whose dependencies are all finished, and which haven't run."""
  pass


def topo_order(deps):
  """A runnable order, or [] when the graph has a cycle."""
  pass


def has_cycle(deps):
  """Whether anything depends, however indirectly, on itself."""
  pass


def levels(deps):
  """Waves of tasks that could run in parallel."""
  pass
