class Budget:
  """A spend budget that guards its own rules behind attribute syntax."""

  def __init__(self, limit):
    self._limit = limit
    self._spent = 0.0

  @property
  def spent(self):
    """Read-only: callers can see it, only spend() can move it."""
    pass

  @property
  def limit(self):
    pass

  @limit.setter
  def limit(self, value):
    """Validates the write before anything bad is stored."""
    pass

  @property
  def remaining(self):
    """Computed on every read — never stored, never stale."""
    pass

  @property
  def exhausted(self):
    pass

  def spend(self, amount):
    pass
