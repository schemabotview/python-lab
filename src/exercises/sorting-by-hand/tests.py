assert insertion_sort([5, 2, 9, 1])[0] == [1, 2, 5, 9], "insertion sort orders the values"
assert merge_sort([5, 2, 9, 1])[0] == [1, 2, 5, 9], "and so does merge sort"
assert insertion_sort([])[0] == [], "an empty list"
assert merge_sort([])[0] == [], "likewise"
assert insertion_sort([7])[0] == [7], "a single value"
assert merge_sort([7])[0] == [7], "likewise"
assert insertion_sort([3, 3, 1])[0] == [1, 3, 3], "duplicates are kept, not collapsed"
assert merge_sort([3, 3, 1])[0] == [1, 3, 3], "likewise"
assert merge_sort([-2, 5, -9])[0] == [-9, -2, 5], "negatives sort too"

ORIGINAL = [3, 1, 2]
insertion_sort(ORIGINAL)
merge_sort(ORIGINAL)

assert ORIGINAL == [3, 1, 2], "work on a copy — the caller's list is untouched"

assert merge([1, 4], [2, 3])[0] == [1, 2, 3, 4], "two sorted halves interleave"
assert merge([], [1, 2])[0] == [1, 2], "one side empty"
assert merge([1, 2], [])[0] == [1, 2], "the other side empty"
assert merge([], [])[0] == [], "both empty"
assert merge([1, 2], [3, 4])[0] == [1, 2, 3, 4], "no interleaving needed"
assert merge([], [1, 2])[1] == 0, "an empty side costs no comparisons at all"

SHUFFLED = [(i * 37) % 50 for i in range(50)]

assert insertion_sort(SHUFFLED)[0] == sorted(SHUFFLED), "fifty values, insertion sort"
assert merge_sort(SHUFFLED)[0] == sorted(SHUFFLED), "fifty values, merge sort"
assert merge_sort(SHUFFLED)[1] < insertion_sort(SHUFFLED)[1], "merge sort compares far less on fifty values"
assert merge_sort(SHUFFLED)[1] < 300, "n log n stays small — under 300 comparisons"
assert insertion_sort(SHUFFLED)[1] > 500, "n squared does not — over 500"

ALREADY = list(range(50))

assert insertion_sort(ALREADY)[1] == 49, "insertion sort's BEST case is linear — one comparison per value"
assert merge_sort(ALREADY)[1] > insertion_sort(ALREADY)[1], "and on sorted input it beats merge sort, which always splits"

BACKWARDS = list(range(50, 0, -1))

assert insertion_sort(BACKWARDS)[0] == sorted(BACKWARDS), "still correct on the worst case"
assert insertion_sort(BACKWARDS)[1] == 1225, "its WORST case is every pair — 50 * 49 / 2"
assert merge_sort(BACKWARDS)[1] < 300, "merge sort does not care how the input was arranged"

BIGGER = [(i * 37) % 100 for i in range(100)]

assert insertion_sort(BIGGER)[1] > insertion_sort(SHUFFLED)[1] * 3, "doubling the input roughly quadruples insertion sort"
assert merge_sort(BIGGER)[1] < merge_sort(SHUFFLED)[1] * 3, "but barely more than doubles merge sort"

assert sorted(SHUFFLED) == merge_sort(SHUFFLED)[0], "and the built-in agrees with both — which is what you should actually use"
