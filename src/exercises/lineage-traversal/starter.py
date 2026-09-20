from collections import deque


def downstream(graph, table):
  """Everything that depends on this table, however far away."""
  pass


def upstream(graph, table):
  """Everything this table depends on, by walking the edges backwards."""
  pass


def path_between(graph, start, end):
  """The shortest path, or [] when there is none."""
  pass


def impacted_by(graph, table):
  """The table itself plus everything downstream — the blast radius."""
  pass
