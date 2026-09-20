assert list(read_rows(["a", "b"])) == ["a", "b"], "the generator yields each row"
assert list(read_rows([])) == [], "an empty stream"

import types

assert isinstance(read_rows([]), types.GeneratorType), "a function with yield returns a generator, not a list"


def never_runs():
  raise ValueError("this must not run yet")
  yield


CALLED = never_runs()

assert isinstance(CALLED, types.GeneratorType), "calling a generator function runs NONE of its body"

try:
  next(CALLED)
except ValueError:
  DEFERRED = "ran on first next()"
else:
  DEFERRED = "never ran"

assert DEFERRED == "ran on first next()", "the body starts only when the first value is pulled"

assert list(chunked(["a", "b", "c", "d"], 2)) == [["a", "b"], ["c", "d"]], "two full batches"
assert list(chunked(["a", "b", "c"], 2)) == [["a", "b"], ["c"]], "the final batch is short, and must not be lost"
assert list(chunked([], 2)) == [], "nothing in, nothing out — and no empty final batch"
assert list(chunked(["a"], 5)) == [["a"]], "fewer rows than a batch holds"
assert list(chunked(["a", "b"], 1)) == [["a"], ["b"]], "batches of one"

assert take(run_ids("run"), 3) == ["run-1", "run-2", "run-3"], "three ids off an ENDLESS stream — laziness is what makes this terminate"
assert take(run_ids("job"), 1) == ["job-1"], "just the first"
assert take(run_ids("run"), 0) == [], "none at all, and still no hang"
assert take(["a", "b", "c"], 2) == ["a", "b"], "take works on a plain list too"
assert take(["a"], 5) == ["a"], "asking for more than there is"

assert take(run_ids("a"), 2) == ["a-1", "a-2"], "each call starts a fresh stream"
assert list(merge_streams(["a", "b"], ["c"])) == ["a", "b", "c"], "yield from re-emits each stream in turn"
assert list(merge_streams()) == [], "no streams at all"
assert list(merge_streams([], ["a"], [])) == ["a"], "empty streams contribute nothing"
assert list(merge_streams(read_rows(["a"]), read_rows(["b"]))) == ["a", "b"], "generators merge into a generator"
assert take(merge_streams(["a"], run_ids("run")), 3) == ["a", "run-1", "run-2"], "a finite stream chained ahead of an endless one"

SPENT = read_rows(["a", "b"])

assert list(SPENT) == ["a", "b"], "the first walk gets the rows"
assert list(SPENT) == [], "a generator is single-use, just like a cursor"
