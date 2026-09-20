class Source:
  """The general case. Subclasses specialise the two hooks."""

  def __init__(self, name):
    pass

  def kind(self):
    pass

  def uri(self):
    pass

  def describe(self):
    """Shared logic, written once, that calls whatever the subclass supplied."""
    pass

  def read(self):
    pass


class S3Source(Source):
  def __init__(self, name, bucket):
    pass

  def kind(self):
    pass

  def uri(self):
    pass


class KafkaSource(Source):
  def __init__(self, name, topic):
    pass

  def kind(self):
    pass

  def uri(self):
    pass


def mro_names(cls):
  """The lookup chain Python walks to find a method."""
  pass
