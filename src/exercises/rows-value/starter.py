class Rows:
  """A row count that behaves like a built-in: it prints, compares, adds, sizes."""

  def __init__(self, count):
    self.count = count

  def __repr__(self):
    pass

  def __str__(self):
    pass

  def __eq__(self, other):
    pass

  def __lt__(self, other):
    pass

  def __add__(self, other):
    pass

  def __len__(self):
    pass

  # Defining __eq__ sets __hash__ to None. Put it back, or Rows can never
  # go in a set or be a dict key.
  def __hash__(self):
    pass
