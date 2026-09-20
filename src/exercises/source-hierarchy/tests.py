assert Source("raw").name == "raw", "the base stores the name"
assert Source("raw").reads == 0, "and starts the read counter"
assert Source("raw").kind() == "source", "the base's own kind"
assert Source("raw").uri() == "raw", "the base's uri is just the name"
assert Source("raw").describe() == "source: raw", "describe combines the two"

assert S3Source("orders", "lake").name == "orders", "super().__init__ ran, so the name is set"
assert S3Source("orders", "lake").reads == 0, "and so is everything else the base sets up"
assert S3Source("orders", "lake").bucket == "lake", "the subclass adds its own attribute"
assert S3Source("orders", "lake").uri() == "s3://lake/orders", "the override replaces the base's uri"
assert S3Source("orders", "lake").kind() == "s3", "and its kind"
assert S3Source("orders", "lake").describe() == "s3: s3://lake/orders", "describe is inherited, but calls the OVERRIDDEN methods"

assert KafkaSource("events", "clicks").uri() == "kafka://clicks", "a different specialisation"
assert KafkaSource("events", "clicks").describe() == "kafka: kafka://clicks", "same inherited describe, different result"
assert KafkaSource("events", "clicks").topic == "clicks", "its own attribute"
assert KafkaSource("events", "clicks").name == "events", "and the base's, via super()"

READER = S3Source("orders", "lake")

assert READER.read() == 1, "read is inherited from the base, not rewritten"
assert READER.read() == 2, "and it updates state on the subclass instance"
assert READER.reads == 2, "which lives where the base put it"

assert issubclass(S3Source, Source) is True, "an S3Source is-a Source"
assert issubclass(KafkaSource, Source) is True, "so is a KafkaSource"
assert issubclass(S3Source, KafkaSource) is False, "but they are siblings, not parent and child"
assert isinstance(S3Source("o", "b"), Source) is True, "an instance is also an instance of its base"

assert mro_names(S3Source) == ["S3Source", "Source", "object"], "the chain Python walks, ending at the root every class shares"
assert mro_names(Source) == ["Source", "object"], "the base's own chain"
assert mro_names(KafkaSource)[1] == "Source", "lookup reaches the base second"
