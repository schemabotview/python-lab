class Rows:
  """A row count that behaves like a built-in: it prints, compares, adds, sizes."""

  def __init__(self, count):
    self.count = count

  def __repr__(self):
    return f"Rows({self.count})"

  def __str__(self):
    return f"{self.count} rows"

  def __eq__(self, other):
    if not isinstance(other, Rows):
      return NotImplemented
    return self.count == other.count

  def __lt__(self, other):
    return self.count < other.count

  def __add__(self, other):
    return Rows(self.count + other.count)

  def __len__(self):
    return self.count

  # Defining __eq__ sets __hash__ to None. Put it back, or Rows can never
  # go in a set or be a dict key.
  def __hash__(self):
    return hash(self.count)
