class PipelineRun:
  """One table's run: what it is, how it went, and how many have started."""

  # A class attribute — one copy, shared by every instance.
  runs_started = 0

  def __init__(self, table, rows=0):
    pass

  def load(self, rows):
    """Add rows, but guard the object's own rule first."""
    pass

  def fail(self, reason):
    pass

  def __repr__(self):
    pass

  @classmethod
  def from_dict(cls, record):
    """The alternate constructor: build one from a config record."""
    pass
