assert ConsoleSink().write(5) == "console: 5", "the console sink"
assert TableSink("orders").write(5) == "orders: 5", "the table sink uses its own name"
assert NullSink().write(5) == "discarded", "the null sink ignores the rows entirely"

assert fan_out([ConsoleSink(), TableSink("orders"), NullSink()], 5) == ["console: 5", "orders: 5", "discarded"], "one call, each object's own version runs"
assert fan_out([], 5) == [], "no sinks, nothing written"
assert fan_out([NullSink(), NullSink()], 1) == ["discarded", "discarded"], "two of the same kind"
assert fan_out([TableSink("a"), TableSink("b")], 9) == ["a: 9", "b: 9"], "same class, different state"


class MetricsSink:
  def write(self, rows):
    return f"metrics<{rows}>"


assert fan_out([ConsoleSink(), MetricsSink()], 3) == ["console: 3", "metrics<3>"], "an unrelated class with the right method just fits — no base class needed"
assert issubclass(MetricsSink, ConsoleSink) is False, "and it inherits from nothing here"

assert len(Batch(["r1", "r2", "r3"])) == 3, "len() calls __len__ on your own class"
assert len(Batch([])) == 0, "an empty batch"

assert total_size(["hi", [1, 2], Batch(["a"])]) == 5, "a string, a list and a Batch all answer the same call"
assert total_size([]) == 0, "nothing to measure"
assert total_size([Batch(["a", "b"]), Batch([])]) == 2, "two batches"
assert total_size(["abc"]) == 3, "len() on a built-in type is the same protocol"
