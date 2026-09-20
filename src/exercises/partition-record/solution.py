from dataclasses import asdict, dataclass, field, replace


@dataclass(order=True)
class Partition:
  """A mutable record. The decorator writes __init__, __repr__, __eq__ and <."""

  table: str
  date: str
  rows: int = 0
  # A bare [] here would be ONE list shared by every partition.
  tags: list = field(default_factory=list)

  def __post_init__(self):
    """Runs after __init__ — the place to normalise or validate."""
    self.table = self.table.lower()


@dataclass(frozen=True)
class PartitionKey:
  """Immutable, and therefore hashable — usable as a dict key."""

  table: str
  date: str


def as_record(partition):
  """The dataclass as a plain dict."""
  return asdict(partition)


def with_rows(partition, rows):
  """A copy with a different row count, leaving the original alone."""
  return replace(partition, rows=rows)
