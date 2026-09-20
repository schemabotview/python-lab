# Sorting by Hand

Two sorts, both returning **`(sorted_list, comparisons)`**. Neither may touch
the caller's list, and neither may call `sorted()`.

## `insertion_sort(values)`

Walk left to right; slide each value back past everything larger. Count each
comparison between two values.

## `merge(left, right)`

Merge two already-sorted lists into one. Count each comparison.

## `merge_sort(values)`

Split in half, sort each half **with itself**, then `merge`. The comparison
count is both halves plus the merge.

```python
insertion_sort([5, 2, 9, 1])   # ([1, 2, 5, 9], 5)
merge_sort([5, 2, 9, 1])       # ([1, 2, 5, 9], 4)
```

## Notes

- **The counts are the point, and they diverge fast.** On 50 shuffled values
  insertion sort takes over 500 comparisons and merge sort under 300. Double to
  100 values and insertion sort **more than triples** while merge sort barely
  doubles. That is O(n²) against O(n log n), measured.
- **Insertion sort is not simply worse.** On already-sorted input it takes 49
  comparisons for 50 values — linear, and *better* than merge sort, which splits
  regardless. Tests pin its best case (49) and its worst (1,225, every pair).
  "Which is faster" always depends on the data.
- **Merge sort doesn't care about the arrangement.** Sorted, reversed or
  shuffled, the count barely moves. Predictability is a feature.
- **`merge` is where the `<=` matters.** Taking from the left on a tie is what
  makes the sort **stable** — equal values keep their original order. Use `<`
  and you silently lose that, which breaks any sort-by-one-key-then-another.
- **You should never actually write these.** Python's `sorted` is Timsort, which
  detects existing runs and gets insertion sort's best case *and* merge sort's
  worst-case guarantee. The reason to write them once is to know what that is
  saving you.
- `merge_sort` calls itself — and the base case (one value or none is already
  sorted) is what stops it. Recursion gets a proper exercise at #44.
