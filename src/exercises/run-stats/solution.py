def run_stats(durations, sla):
  """Summarise last night's run times without any aggregate built-ins."""
  count = 0
  total = 0
  fastest = None
  slowest = None
  over_sla = 0
  for duration in durations:
    count += 1
    total += duration
    # Seed from the first value rather than from 0 — a 0 seed would make
    # `fastest` wrong for every list of positive numbers.
    if fastest is None or duration < fastest:
      fastest = duration
    if slowest is None or duration > slowest:
      slowest = duration
    if duration > sla:
      over_sla += 1
  average = total / count if count else 0.0
  return "\n".join([
    f"Runs: {count}",
    f"Total: {total}m",
    f"Average: {average:.1f}m",
    f"Fastest: {fastest or 0}m",
    f"Slowest: {slowest or 0}m",
    f"Over SLA: {over_sla}",
  ])


def table_report(names, durations):
  """Number each table beside its runtime, walking both lists in lockstep."""
  lines = []
  for position, (name, duration) in enumerate(zip(names, durations), start=1):
    lines.append(f"{position}. {name} {duration}m")
  return "\n".join(lines)


def locate(names, wanted):
  """Say where a table sits in tonight's schedule, or that it isn't in it."""
  for index in range(len(names)):
    if names[index] == wanted:
      return f"{wanted} at position {index}"
  else:
    # Reached only when the loop finished without returning.
    return f"{wanted} not scheduled"


def first_breach(durations, sla):
  """Index of the first run over the SLA, or -1. Hand-tracked index, no for."""
  index = 0
  while index < len(durations):
    if durations[index] > sla:
      return index
    index += 1
  return -1


def drain(queue):
  """Process a sentinel-terminated queue: skip retries, stop dead on a fatal."""
  items = list(queue)
  done = []
  while (item := items.pop(0)) != "END":
    kind, _, name = item.partition(":")
    if kind == "retry":
      continue
    if kind == "fatal":
      break
    done.append(name)
  return done
