from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class Connector(ABC):
  """The contract every connector must meet."""

  @abstractmethod
  def name(self):
    """What this connector is called."""

  @abstractmethod
  def fetch(self):
    """The rows it produces."""

  def report(self):
    """Shared logic, written once, built on the methods subclasses must supply."""
    pass


class PostgresConnector(Connector):
  def name(self):
    pass

  def fetch(self):
    pass


class EmptyConnector(Connector):
  def name(self):
    pass

  def fetch(self):
    pass


@runtime_checkable
class Fetchable(Protocol):
  """Structural: anything with a fetch() matches, inheritance or not."""

  def fetch(self): ...


def can_fetch(value):
  """Whether a value satisfies the Fetchable protocol."""
  pass
