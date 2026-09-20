# The Pipeline Run Class

One class that holds what a run **has** and what it **does**.

## `__init__(self, table, rows=0)`

Stores `table` and `rows` on the instance, sets `status` to `"pending"`, and
adds one to the shared `runs_started` counter.

## `load(self, rows)`

Adds rows and sets `status` to `"loaded"`, returning `"loaded"`.

**Unless `rows` is negative** — then it changes nothing at all and returns
`"rejected"`.

```python
run = PipelineRun("orders", 10)
run.load(100)    # "loaded"    rows is now 110
run.load(-5)     # "rejected"  rows is still 110
```

## `fail(self, reason)`

Sets and returns `"failed: <reason>"`.

## `__repr__(self)`

```python
repr(PipelineRun("orders", 5))   # "PipelineRun(orders, 5)"
```

## `from_dict(cls, record)`

A `@classmethod` that builds a run from a config record. A record with no
`rows` key uses the default.

```python
PipelineRun.from_dict({"table": "orders", "rows": 42})
PipelineRun.from_dict({"table": "orders"})   # rows is 0
```

## Notes

- **`self` is this particular object.** Store on `self`, read back through
  `self` — that is the whole of how an object remembers anything. Python passes
  it for you, so `run.load(100)` calls `load(run, 100)`.
- **`runs_started` is a class attribute — one copy, shared.** Increment it as
  `PipelineRun.runs_started += 1`, not `self.runs_started += 1`. The second
  reads the shared value and then writes a *new instance attribute* that shadows
  it, so the shared count never moves.
- **A method can guard the object's rules**, not just store data. `load`
  rejecting a negative is the difference between a class and a dict.
- **`__repr__` exists so an object prints as itself.** Without it you get
  `<PipelineRun object at 0x7f...>`, which tells a reader nothing. A test checks
  there is no `0x` in yours.
- **A `@classmethod` takes the class as `cls`, not an instance as `self`**, and
  the usual reason to write one is exactly this: an alternate constructor.
  Return `cls(...)` rather than `PipelineRun(...)`, so a subclass building one
  gets a subclass back.
