class Budget:
  """A spend budget that guards its own rules behind attribute syntax."""

  def __init__(self, limit):
    self._limit = limit
    self._spent = 0.0

  @property
  def spent(self):
    """Read-only: callers can see it, only spend() can move it."""
    return self._spent

  @property
  def limit(self):
    return self._limit

  @limit.setter
  def limit(self, value):
    """Validates the write before anything bad is stored."""
    if value < 0:
      raise ValueError("limit cannot be negative")
    if value < self._spent:
      raise ValueError("limit cannot be below what is already spent")
    self._limit = value

  @property
  def remaining(self):
    """Computed on every read — never stored, never stale."""
    return self._limit - self._spent

  @property
  def exhausted(self):
    return self._spent >= self._limit

  def spend(self, amount):
    if amount > self.remaining:
      return "denied"
    self._spent += amount
    return "approved"
