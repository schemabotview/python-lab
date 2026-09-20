# Partition Records

A record type that mostly holds data. `@dataclass` writes the tedious parts
from the fields you declare.

## `Partition` — `@dataclass(order=True)`

Four fields, in this order:

| Field | Type | Default |
| --- | --- | --- |
| `table` | `str` | — |
| `date` | `str` | — |
| `rows` | `int` | `0` |
| `tags` | `list` | a **new empty list each time** |

`__post_init__` lowercases the table name after construction.

```python
Partition("ORDERS", "2026-01-04")
# Partition(table='orders', date='2026-01-04', rows=0, tags=[])
```

## `PartitionKey` — `@dataclass(frozen=True)`

Two fields, `table` and `date`. Frozen, so it can be a dict key.

## `as_record(partition)` → a plain `dict`

## `with_rows(partition, rows)`

A **copy** with a new row count. The original is unchanged.

## Notes

- **Declaring the fields is all you write.** The decorator generates `__init__`,
  `__repr__` and `__eq__` from them. Those `x: str` annotations are the type
  hints from Course 2, finally doing real work rather than just documenting.
- **`tags: list = []` is the trap.** A bare mutable default is built **once**,
  when the class is defined, so every partition would share one list — the same
  bug as `def f(errors=[])`. `field(default_factory=list)` runs the factory per
  instance instead. A test appends to one partition's tags and checks the other
  is still empty. (Python actually refuses a bare `[]` here outright, which is
  one of the few places it protects you from this.)
- **`order=True` generates `<`**, comparing fields **in declaration order** —
  so `Partition` sorts by table, then date, then rows. That's also why field
  order is a design decision, not just layout.
- **`frozen=True` makes a record immutable and therefore hashable**, which is
  what lets `PartitionKey` be a dict key — exactly the reason composite keys
  were tuples earlier. Assigning to a frozen field raises
  `FrozenInstanceError`.
- **`replace()` is how you "change" an immutable record**: it builds a new one
  with your change and every other field copied. `asdict()` goes the other way,
  to a plain dict ready for JSON.
