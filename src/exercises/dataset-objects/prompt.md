# Dataset Instances

One blueprint, many objects — and each one keeps its own state.

## `Dataset`

`__init__(self, name)` stores the `name` and gives the dataset an **empty
column list**. `add_column(self, column)` appends and returns the list so far.

```python
orders = Dataset("orders")
events = Dataset("events")
orders.add_column("id")   # ['id']
events.columns            # []   <- untouched
```

`region` is already declared as a class attribute. Leave it alone.

## `same_object(first, second)`

Whether two names point at **one** object.

```python
d = Dataset("orders")
same_object(d, d)                             # True
same_object(Dataset("o"), Dataset("o"))       # False
```

## `same_type(value, kind)`

Whether a value is of the given type.

## `attributes(obj)`

Every **instance** attribute the object is carrying, sorted.

```python
attributes(Dataset("orders"))   # ['columns', 'name']
```

## `tag(obj, key, value)`

Attaches an attribute that was never declared on the class, and returns the
attribute list afterwards.

## Notes

- **`self.columns = []` must be in `__init__`, not the class body.** This is the
  single nastiest beginner bug in Python OOP: a mutable class attribute is
  **one list shared by every instance**, so appending through one dataset makes
  the column appear on all of them. A test proves it — `events.columns` must
  stay empty.
- `region` is safe in the class body precisely because a string can't be
  mutated. The rule isn't "never put anything in the class body", it's
  "never put anything **mutable** there".
- **`is` asks *same object*, `==` asks *equal value*, `isinstance` asks *same
  type*.** Three different questions, and mixing them up is where a whole class
  of bugs lives.
- **`vars(obj)` shows an object's own attributes** — and *only* its own.
  `region` lives on the class, so it won't appear, even though `obj.region`
  reads fine.
- **Attributes are dynamic.** `setattr(obj, key, value)` adds one at runtime to
  that object alone. Assigning `obj.region = ...` does the same thing, which is
  why it **shadows** the class attribute rather than changing it — a test pins
  that too.
