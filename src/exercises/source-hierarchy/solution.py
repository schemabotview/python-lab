class Source:
  """The general case. Subclasses specialise the two hooks."""

  def __init__(self, name):
    self.name = name
    self.reads = 0

  def kind(self):
    return "source"

  def uri(self):
    return self.name

  def describe(self):
    """Shared logic, written once, that calls whatever the subclass supplied."""
    return f"{self.kind()}: {self.uri()}"

  def read(self):
    self.reads += 1
    return self.reads


class S3Source(Source):
  def __init__(self, name, bucket):
    super().__init__(name)
    self.bucket = bucket

  def kind(self):
    return "s3"

  def uri(self):
    return f"s3://{self.bucket}/{self.name}"


class KafkaSource(Source):
  def __init__(self, name, topic):
    super().__init__(name)
    self.topic = topic

  def kind(self):
    return "kafka"

  def uri(self):
    return f"kafka://{self.topic}"


def mro_names(cls):
  """The lookup chain Python walks to find a method."""
  return [entry.__name__ for entry in cls.__mro__]
