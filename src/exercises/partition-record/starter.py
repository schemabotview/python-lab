from dataclasses import asdict, dataclass, field, replace


@dataclass(order=True)
class Partition:
  """A mutable record. The decorator writes __init__, __repr__, __eq__ and <."""

  # Declare the fields here: table, date, rows (default 0), tags (default []).
  pass

  def __post_init__(self):
    """Runs after __init__ — the place to normalise or validate."""
    pass


@dataclass(frozen=True)
class PartitionKey:
  """Immutable, and therefore hashable — usable as a dict key."""

  pass


def as_record(partition):
  """The dataclass as a plain dict."""
  pass


def with_rows(partition, rows):
  """A copy with a different row count, leaving the original alone."""
  pass
