class PipelineRun:
  """One table's run: what it is, how it went, and how many have started."""

  # A class attribute — one copy, shared by every instance.
  runs_started = 0

  def __init__(self, table, rows=0):
    self.table = table
    self.rows = rows
    self.status = "pending"
    PipelineRun.runs_started += 1

  def load(self, rows):
    """Add rows, but guard the object's own rule first."""
    if rows < 0:
      return "rejected"
    self.rows += rows
    self.status = "loaded"
    return "loaded"

  def fail(self, reason):
    self.status = f"failed: {reason}"
    return self.status

  def __repr__(self):
    return f"PipelineRun({self.table}, {self.rows})"

  @classmethod
  def from_dict(cls, record):
    """The alternate constructor: build one from a config record."""
    return cls(record["table"], record.get("rows", 0))
