# Recursion & Memoisation

A JSON manifest nests to no fixed depth, so a loop can't walk it. Recursion
can.

## `depth_of(value)`

How deeply it nests. A plain value is `0`; an **empty** container is still `1`.

```python
depth_of(5)                      # 0
depth_of([1, [2]])               # 2
depth_of({"a": [1, {"b": 2}]})   # 3
```

## `flatten(value)` → every leaf of a nested list, left to right

## `count_leaves(value)` → how many non-container values it holds

## `fib_naive(n)` and `fib_memo(n)`

Both return **`(value, calls)`** — the Fibonacci number and how many times the
recursive step ran.

```python
fib_naive(20)   # (6765, 21891)
fib_memo(20)    # (6765, 21)
```

## Notes

- **Every recursion needs a base case that the work shrinks toward.** Here it's
  "this isn't a container" — and forgetting it doesn't loop, it raises
  `RecursionError`.
- **A string is a leaf, not something to descend into.** It's iterable, so a
  naive `isinstance(x, (list, str))` check recurses into `"abc"`, then into
  `"a"`, which is a one-character string, which is iterable… A test flattens
  `["a", ["b"]]` specifically to pin this.
- **The `(value, calls)` pair is the lesson.** The naive Fibonacci makes
  **21,891** calls for `n=20`; the memoised one makes **21** — one per value.
  Step to `n=25` and the naive count multiplies again, because each call spawns
  two more. That's exponential, and memoisation flattens it to linear by
  refusing to compute the same answer twice.
- **This is what `@lru_cache` does**, from the functools exercise — same idea,
  one line. Writing the dict by hand once is how you know what that line buys.
- **Recursion has a hard ceiling.** Python's limit is about a thousand frames.
  A test lowers it to 60 deliberately, proves `RecursionError` fires, and puts
  it back — 200 levels of nesting is otherwise fine here.
- **Do not go looking for the real ceiling in this lab.** Python running in
  WebAssembly has a much smaller stack than Python on your machine, and a deep
  enough recursion overflows *that* stack before Python's own counter trips.
  The result is not a `RecursionError` you can catch — it is the interpreter
  dying, taking the page's runtime with it. Unbounded input depth wants an
  explicit stack, the one from the previous exercise, rather than a bigger
  limit.
