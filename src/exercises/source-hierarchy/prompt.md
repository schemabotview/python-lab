# Source Hierarchy

Write the general source once; let each kind specialise the parts that differ.

## `Source`

- `__init__(self, name)` stores `name` and sets `reads` to `0`.
- `kind()` → `"source"`, `uri()` → the name.
- `describe()` → `"<kind>: <uri>"`.
- `read()` adds one to `reads` and returns the new count.

## `S3Source(Source)` and `KafkaSource(Source)`

Each takes one extra argument, calls the base's `__init__`, and overrides
`kind()` and `uri()`.

```python
S3Source("orders", "lake").describe()      # "s3: s3://lake/orders"
KafkaSource("events", "clicks").describe() # "kafka: kafka://clicks"
```

Neither rewrites `describe()` or `read()`.

## `mro_names(cls)`

The chain of class names Python walks to find a method.

```python
mro_names(S3Source)   # ['S3Source', 'Source', 'object']
```

## Notes

- **`super().__init__(name)` extends the base rather than replacing it.** Skip
  it and `self.name` and `self.reads` never get set, so every inherited method
  breaks. Call it *first*, then add the subclass's own attributes.
- **`describe()` is the point of the whole exercise.** It is written once, on
  the base, and never overridden — yet it produces the right answer for every
  subclass, because the `self.kind()` inside it finds the subclass's version.
  That is inheritance and polymorphism doing the work together.
- **Lookup walks a fixed chain**, and `__mro__` shows it. `object` is at the end
  of every chain — it is the root class everything inherits from.
- `issubclass(A, B)` asks about the classes; `isinstance(a, B)` asks about an
  object. An `S3Source` instance is an instance of `Source` too, which is what
  "is-a" means in code.
- **Inherit only for a true is-a.** An `S3Source` *is a* `Source`, so this fits.
  If the relationship is really *has-a* — a run *has* a source — hold the object
  as an attribute instead of subclassing it.
