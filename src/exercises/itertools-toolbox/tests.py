import itertools

assert stitch(["a", "b"], ["c"]) == ["a", "b", "c"], "chain stitches iterables into one stream"
assert stitch() == [], "nothing to stitch"
assert stitch([], ["a"], []) == ["a"], "empty batches contribute nothing"
assert stitch(["a"]) == ["a"], "a single batch"

assert page(["a", "b", "c", "d", "e"], 1, 3) == ["b", "c"], "islice takes a half-open range, like a slice"
assert page(["a", "b"], 0, 5) == ["a", "b"], "asking past the end stops cleanly"
assert page([], 0, 3) == [], "slicing an empty stream"

assert page(endless_ids("run"), 0, 3) == ["run-1", "run-2", "run-3"], "islice on an ENDLESS stream — nothing is built until asked"
assert page(endless_ids("job"), 2, 4) == ["job-3", "job-4"], "skipping ahead in an endless stream"

assert rotate(["a", "b"], 5) == ["a", "b", "a", "b", "a"], "cycle repeats forever; islice decides when to stop"
assert rotate(["only"], 3) == ["only", "only", "only"], "one option, repeated"
assert rotate(["a", "b", "c"], 2) == ["a", "b"], "stopping before the first lap is done"

assert group_by_table([("orders", 5), ("events", 3), ("orders", 7)]) == {"orders": [5, 7], "events": [3]}, "rows collected under their table"
assert group_by_table([]) == {}, "nothing to group"
assert group_by_table([("a", 1)]) == {"a": [1]}, "one row"


UNSORTED = [("orders", 5), ("events", 3), ("orders", 7)]
NAIVE = {}
for table, entries in itertools.groupby(UNSORTED, key=lambda row: row[0]):
  NAIVE[table] = [entry[1] for entry in entries]

assert NAIVE == {"orders": [7], "events": [3]}, "unsorted input SILENTLY loses rows — groupby only groups neighbours"

assert running_total([100, 50, 25]) == [100, 150, 175], "a cumulative total after each batch"
assert running_total([]) == [], "nothing to accumulate"
assert running_total([7]) == [7], "one batch is its own running total"

assert pairs(["a", "b", "c"]) == [("a", "b"), ("a", "c"), ("b", "c")], "every unordered pair, each once"
assert pairs(["a"]) == [], "one table makes no pairs"
assert pairs([]) == [], "nor does none"
assert len(pairs(["a", "b", "c", "d"])) == 6, "four tables make six pairs"

SPENT = itertools.chain(["a", "b"])

assert list(SPENT) == ["a", "b"], "the first walk reads it"
assert list(SPENT) == [], "itertools results are one-shot iterators, like generators"
