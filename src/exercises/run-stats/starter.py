def run_stats(durations, sla):
  """Summarise last night's run times without any aggregate built-ins."""
  pass


def table_report(names, durations):
  """Number each table beside its runtime, walking both lists in lockstep."""
  pass


def locate(names, wanted):
  """Say where a table sits in tonight's schedule, or that it isn't in it."""
  pass


def first_breach(durations, sla):
  """Index of the first run over the SLA, or -1. Hand-tracked index, no for."""
  pass


def drain(queue):
  """Process a sentinel-terminated queue: skip retries, stop dead on a fatal."""
  pass
