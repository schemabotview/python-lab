# Top-K with a Heap

Which tables are biggest? You don't need the list sorted — you need the top
few. A heap gives you that without either.

Pairs are `(name, rows)`.

| Function | Returns |
| --- | --- |
| `top_k(pairs, k)` | the k biggest, **biggest first** |
| `bottom_k(pairs, k)` | the k smallest, **smallest first** |
| `streaming_top_k(stream, k)` | the same as `top_k`, holding only k items |
| `high_water(stream, k)` | the most the working set ever held |
| `merge_sorted(*streams)` | already-sorted streams merged into one |

`top_k` and `bottom_k` can use `heapq.nlargest`/`nsmallest`. Build
`streaming_top_k` by hand with `heappush` and `heapreplace`.

```python
top_k(tables, 2)   # [('logs', 9000), ('orders', 1500)]
```

## Notes

- **A heap gives you the extreme cheaply and nothing else.** It is only
  *partially* ordered — `heap[0]` is the smallest, and the rest is unspecified.
  That weaker promise is exactly why it costs less than a full sort, and why
  the result has to be sorted at the end to be reportable.
- **`streaming_top_k` is the one that matters.** Push until you hold k, then
  only replace when something beats the smallest you're keeping. A test streams
  a thousand items with `k=3` and `high_water` proves the heap **never held more
  than three**. Sorting first would need all thousand in memory; this needs
  three, and works on a stream with no end.
- **Store `(rows, name)`, not `(name, rows)`.** A heap compares tuples left to
  right, so the field you're ranking by has to come first — then flip them back
  on the way out.
- **`heapreplace` is one operation, not two.** Pop-then-push does the same
  thing at twice the cost and briefly leaves the heap a size short.
- **`heapq.merge` is lazy**, which is what makes it the right tool for merging
  sorted files too big to load. It is also precisely the `merge` step from the
  previous exercise, generalised to any number of inputs.
