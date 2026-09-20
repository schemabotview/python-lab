def by_duration(runs):
  """Runs ordered by how long they took, slowest last."""
  return sorted(runs, key=lambda run: run["duration"])


def slowest(runs):
  """The name of the run that took longest."""
  return max(runs, key=lambda run: run["duration"])["name"]


def by_name_then_duration(runs):
  """Ordered by table, and within a table by duration."""
  return sorted(runs, key=lambda run: (run["name"], run["duration"]))


def names_upper(runs):
  """Every run name, shouted."""
  return list(map(lambda run: run["name"].upper(), runs))


def failures(runs):
  """Only the runs that did not succeed."""
  return list(filter(lambda run: run["status"] != "ok", runs))


def all_ok(runs):
  """Whether every run succeeded."""
  return all(run["status"] == "ok" for run in runs)


def any_slow(runs, limit):
  """Whether any run went over the limit."""
  return any(run["duration"] > limit for run in runs)
