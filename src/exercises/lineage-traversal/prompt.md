# Lineage Traversal

A lineage graph is `table -> [tables built from it]`.

```python
{
    "raw_orders": ["stg_orders"],
    "stg_orders": ["fct_sales"],
    "fct_sales":  ["report_daily", "report_monthly"],
}
```

| Function | Returns (sorted, except the path) |
| --- | --- |
| `downstream(graph, table)` | everything that depends on it, however far |
| `upstream(graph, table)` | everything it is built from |
| `path_between(graph, start, end)` | the **shortest** path, or `[]` |
| `impacted_by(graph, table)` | the table **plus** everything downstream |

A table is **not** downstream of itself. A table not in the graph has no
lineage — but it still impacts itself.

```python
downstream(lineage, "fct_sales")    # ['report_daily', 'report_monthly']
path_between(lineage, "raw_orders", "fct_sales")
# ['raw_orders', 'stg_orders', 'fct_sales']
```

## Notes

- **`upstream` is `downstream` on the reversed graph.** Build the reverse once —
  every `a -> b` becomes `b -> a` — and then reuse the walk you already wrote.
  Writing the traversal twice is the mistake here.
- **The `seen` set is not an optimisation, it's what makes this terminate.**
  Lineage graphs have diamonds (two paths reaching the same table) and
  occasionally real cycles. A test walks a deliberately cyclic graph and expects
  an answer rather than a hang.
- **Breadth-first gives the *shortest* path; depth-first gives *a* path.** Both
  are correct traversals, only one answers "how many hops". A test on a diamond
  pins the length at 3 — a depth-first walk could wander and still arrive.
- **Carry the path on the queue, not a parent map.** Queueing `path + [next]` is
  the shortest thing that works and reads directly; reconstructing from parents
  is faster but earns its keep only on large graphs.
- **`impacted_by` is the question people actually ask.** "If I change this
  column, what breaks?" — downstream plus the table itself, which is why the
  union with `{table}` is there and not an oversight.
