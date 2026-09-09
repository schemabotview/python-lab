# Two Sum

Given a list of integers `numbers` and an integer `target`, write a function
`two_sum(numbers, target)` that returns the **indices** of the two values that
add up to `target`, as a tuple `(i, j)` with `i < j`.

If no such pair exists, return `None`.

## Examples

```python
two_sum([2, 7, 11, 15], 9)   # (0, 1)  because 2 + 7 == 9
two_sum([3, 2, 4], 6)        # (1, 2)  because 2 + 4 == 6
two_sum([1, 2, 3], 100)      # None
```

## Notes

- Exactly one pair will match in the tests that have an answer.
- The same element can't be used twice, so `two_sum([3], 6)` is `None`.
- The obvious solution checks every pair, which takes O(n²) time. There is an
  O(n) approach: walk the list once, and for each value ask whether the value
  you still need has already been seen. A dictionary remembers where.
