# The Pipeline DAG

This is what Airflow and dbt do. A pipeline is a dict of
`task -> [what it needs first]`.

```python
{
    "extract": [],
    "clean_a": ["extract"],
    "clean_b": ["extract"],
    "join":    ["clean_a", "clean_b"],
}
```

| Function | Returns |
| --- | --- |
| `ready_tasks(deps, done)` | tasks that can start now, **sorted** |
| `topo_order(deps)` | one valid run order, or `[]` if cyclic |
| `has_cycle(deps)` | whether anything depends on itself, however indirectly |
| `levels(deps)` | waves of tasks that could run **in parallel** |

Where several tasks are equally ready, take them in **alphabetical order**, so
the answer is reproducible.

```python
topo_order(pipeline)   # ['extract', 'clean_a', 'clean_b', 'join']
levels(pipeline)       # [['extract'], ['clean_a', 'clean_b'], ['join']]
```

## Notes

- **Start from the tasks that need nothing, then remove them and look again.**
  Each removal may unblock others. That's Kahn's algorithm, and it is the whole
  idea — no cleverness required.
- **A cycle is detected by what's left over.** If you run out of ready tasks
  before placing them all, the remainder must depend on each other in a loop.
  That's why `topo_order` returns `[]` rather than raising, and why `has_cycle`
  can be written in terms of it.
- **`levels` is `topo_order` with the parallelism kept.** A topological order
  is a single queue; the waves tell you what could have run **at the same
  time**. The fan-out has four tasks but only **three** waves, and that
  difference is your critical path.
- **A diamond is not a cycle.** `a → b → d` and `a → c → d` looks circular
  drawn badly, but every edge points forward. A test pins it, because "it looks
  like a loop" is a common misreading of a DAG.
- **Sorting the ready set is what makes this testable.** Any topological order
  is *correct*, so without a tie-break rule the output is legitimately
  non-deterministic — and a test could never pin it.
