# Instrumented Steps

Timing, logging and retries are the same three problems on every pipeline step.
A decorator puts them in one place.

## `counted(fn)`

Wraps a function so it tallies its own calls on a `.calls` attribute.

```python
load("orders")   # "loaded orders"
load.calls       # 1
```

## `tagged(label)`

A decorator **that takes an argument**, prefixing the result.

```python
summarise("orders")   # "[etl] summary of orders"
```

## `retry(times)`

Re-runs a step that raises, up to `times` attempts. If it never succeeds,
returns `"gave up after <times>: <last error>"`.

```python
@retry(2)
def always_fails():
    raise ValueError("disk full")

always_fails()   # "gave up after 2: disk full"
```

A call that succeeds returns immediately and doesn't use its remaining
attempts.

## Notes

- **`@counted` above `def load` just means `load = counted(load)`.** There is no
  other magic. The wrapper is a closure over `fn` — which is why the previous
  exercise came first.
- **`*args, **kwargs` in the wrapper forwards any call unchanged**, so one
  decorator works on functions of any shape. A test decorates a two-argument
  function with a default and calls it positionally *and* by keyword.
- **`@functools.wraps(fn)` stops the wrapper masquerading as itself.** Without
  it, `load.__name__` is `"wrapper"` and the docstring is gone — which breaks
  every debugger, traceback and `help()` that reader will ever use. Two tests
  pin the name and the docstring.
- **A decorator with an argument needs three layers, not two**: `tagged("etl")`
  is *called*, and what it returns is the decorator. Read `@tagged("etl")` as
  `summarise = tagged("etl")(summarise)` and the extra layer explains itself.
- `wrapper.calls = 0` is set on the wrapper **after** defining it — a function
  is an object, so it can carry attributes like any other.
