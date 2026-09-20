# Chunked Row Stream

Rows arrive one at a time and must never all be in memory at once.

## `read_rows(rows)`

The simplest generator — hand back one row at a time.

## `chunked(rows, size)`

Batch the stream into lists. The **final batch may be short**, and must not be
dropped.

```python
list(chunked(["a", "b", "c"], 2))   # [['a', 'b'], ['c']]
list(chunked([], 2))                # []
```

## `run_ids(prefix)`

An **endless** stream of ids.

```python
take(run_ids("run"), 3)   # ['run-1', 'run-2', 'run-3']
```

## `take(stream, count)`

The first `count` values of any stream — including an endless one.

## `merge_streams(*streams)`

Re-emit every stream's items in turn, **without** a manual inner loop.

```python
list(merge_streams(["a", "b"], ["c"]))   # ['a', 'b', 'c']
```

## Notes

- **Calling a generator function runs none of its body.** A test defines one
  that raises on its first line, calls it, and proves nothing happens until
  `next()`. The body starts when the first value is pulled and freezes again at
  each `yield` — locals, position and all.
- **`run_ids` has `while True` in it and that is fine.** It can only ever
  produce as much as someone asks for. This is the whole argument for
  generators: the stream's length stops being the consumer's problem.
- **`take(stream, 0)` is the test that will catch you.** If you append first and
  check the length afterwards, the count can never match against an endless
  stream and the loop runs forever. Check before you pull.
- **`chunked` needs a final flush.** The loop only yields when a batch fills, so
  whatever is left over when the rows run out has to be yielded after it — but
  only if there's anything there, or an empty input produces a spurious `[]`.
- **`yield from other` re-emits another iterable's items** — the delegation is
  the point, and writing the inner `for` loop by hand is the thing it replaces.
- **A generator is single-use**, exactly like the cursor in the previous
  exercise. Walk it twice and the second walk gets nothing.
