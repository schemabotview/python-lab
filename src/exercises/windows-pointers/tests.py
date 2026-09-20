RUNS = [15, 22, 19, 30, 8, 25, 19]

assert max_window(RUNS, 3)[0] == 71, "22 + 19 + 30 is the best three in a row"
assert max_window_naive(RUNS, 3)[0] == 71, "the naive version agrees"
assert max_window(RUNS, 1)[0] == 30, "a window of one is just the maximum"
assert max_window(RUNS, 7)[0] == 138, "a window covering everything is the total"
assert max_window(RUNS, 8) == (0, 0), "a window bigger than the data"
assert max_window(RUNS, 0) == (0, 0), "a window of nothing"
assert max_window([], 3) == (0, 0), "no data"
assert max_window([-5, -1, -9], 2)[0] == -6, "negatives work — the best is the least bad"

assert max_window(RUNS, 3)[1] == 7, "the sliding version touches each value once"
assert max_window_naive(RUNS, 3)[1] == 15, "the naive version re-adds every window from scratch"

LONG = list(range(200))

assert max_window(LONG, 50)[0] == max_window_naive(LONG, 50)[0], "same answer on 200 values"
assert max_window(LONG, 50)[1] == 200, "sliding stays linear — one step per value"
assert max_window_naive(LONG, 50)[1] == 7550, "the naive version does the window's work over and over"
assert max_window_naive(LONG, 50)[1] > max_window(LONG, 50)[1] * 35, "thirty-five times the work for the same number"

SORTED = [2, 5, 8, 12, 16, 23]

assert pair_sum_sorted(SORTED, 20) == (2, 3), "8 + 12 — found by walking inwards"
assert (pair_sum_sorted(SORTED, 25), pair_sum_sorted(SORTED, 100)) == ((0, 5), None), "the outermost pair; and None when nothing reaches the target"
assert (pair_sum_sorted(SORTED, 20), pair_sum_sorted(SORTED, 3)) == ((2, 3), None), "a real pair; and None when no pair is that small"
assert (pair_sum_sorted([4, 6], 10), pair_sum_sorted([], 5)) == ((0, 1), None), "the only pair there is; and None for an empty list"
assert (pair_sum_sorted([4, 6], 10), pair_sum_sorted([5], 10)) == ((0, 1), None), "one value cannot be used twice"

assert dedupe_sorted([1, 1, 2, 3, 3, 3]) == [1, 2, 3], "runs collapse"
assert dedupe_sorted([]) == [], "nothing to dedupe"
assert dedupe_sorted([1]) == [1], "a single value"
assert dedupe_sorted([1, 2, 3]) == [1, 2, 3], "nothing repeated"
assert dedupe_sorted([1, 1, 1]) == [1], "all the same"
assert dedupe_sorted([1, 2, 1]) == [1, 2, 1], "only NEIGHBOURS collapse — unsorted input keeps both 1s"

assert longest_under([1, 2, 3, 4], 5) == 2, "1+2+3 is 6, too much; 2+3 is 5, which fits"
assert longest_under([1, 1, 1, 1], 10) == 4, "everything fits"
assert longest_under([9, 9], 1) == 0, "nothing fits on its own"
assert longest_under([], 5) == 0, "no data"
assert longest_under([5], 5) == 1, "exactly the limit fits"
assert longest_under([1, 2, 3], 3) == 2, "1+2 fits, 1+2+3 does not"
