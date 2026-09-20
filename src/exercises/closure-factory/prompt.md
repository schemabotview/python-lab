# Function Factories

A nested function remembers the variables of the function that made it — even
after that function has returned.

## `scaler(factor)`

```python
double = scaler(2)
double(10)   # 20
```

## `make_counter(start=0)`

Returns a function that counts up, one per call.

```python
count = make_counter()
count()   # 1
count()   # 2
```

## `threshold(limit)`

Returns a predicate.

```python
threshold(100)(150)   # True
```

## `build_scalers(factors)`

One scaler per factor.

```python
[f(10) for f in build_scalers([1, 2, 3])]   # [10, 20, 30]
```

## `compose(*functions)`

Builds a transform chain **once**; the returned function remembers the steps.

```python
clean = compose(str.strip, str.lower)
clean("  Orders ")   # "orders"
```

## Notes

- **The captured variable outlives the call that created it.** `scaler(2)`
  returns and disappears, yet `double` still knows `factor` is `2`. That's the
  closure: the inner function holds onto the scope it was born in.
- **Each call captures independently.** `double` and `triple` have separate
  `factor`s, and two counters from `make_counter` count separately. A test pins
  both.
- **Reading a captured variable is automatic; reassigning it is not.**
  `current += 1` without `nonlocal` makes `current` a *local* of the inner
  function, so the `+=` reads a name that was never assigned and you get
  `UnboundLocalError`. A test defines exactly that broken version and proves it
  raises. `nonlocal current` says "the one from the enclosing function, please".
- `compose` is the same idea as `apply_all` from the functions exercise, turned
  inside out: the steps are fixed up front and the value comes later, so the
  chain can be built once and used many times.
- **This is the mechanism decorators are built on** — which is the next
  exercise.
